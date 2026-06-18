from __future__ import annotations

from pathlib import Path

import pytest
from packaging.requirements import Requirement

from attestationcheck.models.packageinfo import PackageInfo
from attestationcheck.packageinforesolver import (
	PackageInfoManager,
	RemotePackageInfo,
)

THISDIR = str(Path(__file__).resolve().parent)


@pytest.fixture
def package_info_manager() -> PackageInfoManager:
	"""Fixture to provide a PackageInfoManager instance."""
	return PackageInfoManager("https://pypi.org/")


@pytest.fixture
def remote_package_info() -> RemotePackageInfo:
	return RemotePackageInfo("https://pypi.org/", requests_package)


def aux_packageinfo(package_name: str) -> PackageInfo:
	return PackageInfo(name=package_name)


requests_package = aux_packageinfo("requests")


def test_getPackageInfoPypi(remote_package_info: RemotePackageInfo) -> None:
	pkg = remote_package_info

	assert pkg.get_name() == "requests"
	assert pkg.get_author() == "Kenneth Reitz"


def test_getPackageInfoPypiExtended(remote_package_info: RemotePackageInfo) -> None:
	pkg = remote_package_info

	assert pkg.get_name() == "requests"
	assert pkg.get_author() == "Kenneth Reitz"
	assert pkg.is_supported_publisher()
	assert isinstance(pkg.get_attestation_bundle(), list)


def test_sample(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {aux_packageinfo("sample")}
	packages = package_info_manager.getPackages()
	package: PackageInfo = packages.pop()
	assert package.name == "sample"
	assert package.author == ""
	assert not package.is_supported_publisher
	assert not package.is_attestation_present
	assert not package.is_attestation_valid
	assert package.httpErrorCode == 0


def test_requests(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {aux_packageinfo("requests")}
	packages = package_info_manager.getPackages()
	package: PackageInfo = packages.pop()
	assert package.name == "requests"
	assert package.author == "Kenneth Reitz"
	assert package.is_supported_publisher
	assert package.is_attestation_present
	assert package.is_attestation_valid
	assert package.is_attestation_verified
	assert package.httpErrorCode == 0


def test_depgather(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {aux_packageinfo("depgather")}
	packages = package_info_manager.getPackages()
	package: PackageInfo = packages.pop()
	assert package.repo == "https://github.com/FHPythonUtils/DepGather"
	assert package.is_supported_publisher
	assert package.is_attestation_present
	assert package.is_attestation_valid
	assert package.is_attestation_verified
	assert package.httpErrorCode == 0


def test_getPackagesNotFound(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {aux_packageinfo("this_package_does_not_exist")}

	packages = package_info_manager.getPackages()
	package = packages.pop()

	assert package.name == "this-package-does-not-exist"
	assert package.httpErrorCode == 404


def test_unpinned_requirement_reports_warning(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {Requirement("sample")}

	packages = package_info_manager.getPackages()
	package: PackageInfo = packages.pop()

	assert package.name == "sample"
	assert package.httpErrorCode == 0
	assert package.warning == (
		"Warning: no version specifier present, result may not represent the version "
		"installed in a real environment"
	)
