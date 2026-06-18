"""Get information for installed and online packages."""

from __future__ import annotations

import datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import requests
from depgather.models.pypijson import Info, ProjectResponse
from depgather.parse import gather
from packaging.utils import canonicalize_name
from pypi_attestations._impl import AttestationBundle, Provenance

from attestationcheck.models.packageinfo import PackageInfo, PackageLike
from attestationcheck.session import session
from attestationcheck.verify_attestation import validate_attestation, verify_attestation

RAW_JOINS = " AND "
PUBLISHER_HOSTS = (
	"github.com",
	"gitlab.com",
)
HTTP_OK = 200
UNPINNED_DEPENDENCY_WARNING = (
	"Warning: no version specifier present, result may not represent the version "
	"installed in a real environment"
)


class PackageInfoManager:
	"""Manages retrieval of local and remote package information."""

	def __init__(self, base_pypi_url: str = "https://pypi.org") -> None:
		"""
		Manage retrieval of local and remote package information.

		:param str pypi_api: url of pypi server. Typically the public instance, defaults
		to "https://pypi.org"
		"""
		self.base_pypi_url = base_pypi_url
		self.reqs: set[PackageLike] = set()

	def resolve_requirements(
		self,
		requirements_paths: set[str],
		groups: set[str],
		extras: set[str],
		skip_dependencies: set[str],
	) -> None:
		for requirements_path in requirements_paths:
			self.reqs.update(
				gather(
					skipDependencies=skip_dependencies,
					groups=groups,
					extras=extras,
					requirementsPath=Path(requirements_path),
					base_index_url=self.base_pypi_url,
				)
			)

	def getPackages(self) -> set[PackageInfo]:
		"""
		Retrieve package information from local installation or PyPI.

		:param set[str] reqs: Set of dependency names to retrieve information for.
		:return set[PackageInfo]: A set of package information objects.
		"""
		with ThreadPoolExecutor() as executor:
			return set(executor.map(self._get_package_info, self.reqs))

	def _get_package_info(self, package: PackageLike) -> PackageInfo:
		"""
		Retrieve package information, preferring local info.

		:param PackageLike package: package info to unpack
		:return PackageInfo: Information about the package.
		"""
		versions: set[str | None] = {None}
		warning: str | None = None

		specifier = getattr(package, "specifier", None)
		if specifier is not None:
			parsed_versions = {item.version for item in specifier}

			if parsed_versions:
				versions = parsed_versions
			else:
				warning = UNPINNED_DEPENDENCY_WARNING

		package.name = canonicalize_name(package.name)

		base_pkg_info: PackageInfo = PackageInfo(
			name=package.name, version=versions.pop(), httpErrorCode=1
		)

		rpi = RemotePackageInfo(pypi_api=self.base_pypi_url, package=base_pkg_info)
		all_urls = list(rpi.info.project_urls.values()) or [None]
		repo = (
			rpi.info.project_urls.get("Source")
			or rpi.info.project_urls.get("Repository")
			or all_urls[-1]
		)
		fn, sha256 = rpi.get_fileinfo()
		attestation_bundle = rpi.get_attestation_bundle()

		# check attestation valid

		pkg_info = PackageInfo(
			name=package.name,
			version=rpi.get_version(),
			homePage=rpi.get_homePage(),
			author=rpi.get_author(),
			repo=str(repo) if repo else None,
			warning=warning,
			filename=fn,
			digest_256=sha256,
			is_supported_publisher=rpi.is_supported_publisher(),
			is_attestation_present=isinstance(attestation_bundle, list),
			httpErrorCode=rpi.http_code if rpi.http_code != HTTP_OK else 0,
			last_updated=rpi.get_lastUpdated(),
		)

		if isinstance(attestation_bundle, list):
			pkg_info.is_attestation_valid = validate_attestation(attestation_bundle, pkg_info)
			pkg_info.is_attestation_verified = verify_attestation(attestation_bundle, pkg_info)

		return pkg_info


class RemotePackageInfo:
	"""Handles retrieval of package info from PyPI."""

	def __init__(self, pypi_api: str, package: PackageInfo) -> None:
		self.pypi_api_pypi: str = pypi_api + "/pypi"
		self.pypi_api_integrity: str = pypi_api + "/integrity"
		self.package: PackageInfo = package

		# Attempt to get versioned info first
		rc, raw_resp = self.make_req(
			url=f"{self.pypi_api_pypi}{self.package.name}/{self.package.version}/json"
		)
		# Otherwise just get the latest
		if rc != HTTP_OK:
			rc, raw_resp = self.make_req(url=f"{self.pypi_api_pypi}/{self.package.name}/json")

		self.http_code: int = rc
		self.resp: ProjectResponse = ProjectResponse.model_validate(raw_resp)
		self.info: Info = self.resp.info

	def make_req(
		self, url: str, headers: dict[str, str] | None = None
	) -> tuple[int, dict[str, Any]]:
		headers = headers or {}
		try:
			r = session.get(url, headers=headers, timeout=60)

			return r.status_code, r.json()
		except requests.exceptions.JSONDecodeError:
			return -1, {}
		except requests.exceptions.RequestException:
			return -2, {}

	def get_name(self) -> str:
		return self.info.name

	def get_version(self) -> str:
		return self.info.version

	def get_homePage(self) -> str:
		return self.info.home_page

	def get_author(self) -> str:
		author_email = self.info.author_email or ""
		return self.info.author or author_email.split("<")[0].strip()

	def is_supported_publisher(self) -> bool:
		urls = self.info.project_urls.values()
		return any((url.host or "").startswith(PUBLISHER_HOSTS) for url in urls)

	def get_fileinfo(self) -> tuple[str, str] | tuple[None, None]:
		wheel_files = [x for x in self.resp.urls if x.filename.endswith(".whl")]
		if len(wheel_files) > 0:
			f = wheel_files[-1]
			return f.filename, f.digests.sha256
		return None, None

	def get_attestation_bundle(self) -> list[AttestationBundle] | int:

		fn, _digest = self.get_fileinfo()

		if fn is not None:
			url = (
				f"{self.pypi_api_integrity}/{self.package.name}/"
				f"{self.get_version()}/{fn}/provenance"
			)
			rc, attestation_bundle = self.make_req(
				url,
			)
			if rc == HTTP_OK:
				return Provenance.model_validate(attestation_bundle).attestation_bundles
			return rc
		return -3

	def get_lastUpdated(self) -> datetime.datetime:
		files = self.resp.urls
		if len(files) > 0:
			f = files[-1]
			return f.upload_time_iso_8601
		return datetime.datetime(1970, 1, 1, tzinfo=datetime.UTC)
