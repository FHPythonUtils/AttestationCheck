from pydantic import ValidationError
from pypi_attestations._impl import (
	AttestationBundle,
	Distribution,
	GitHubPublisher,
	GitLabPublisher,
	GooglePublisher,
	Publisher,
)
from rfc3986 import exceptions, uri_reference, validators
from sigstore.errors import Error

from attestationcheck.models.packageinfo import PackageInfo


def _check_repository_identity(
	expected_repository_url: str, publisher: GitHubPublisher | GitLabPublisher
) -> tuple[bool, str]:
	"""Check that a repository url matches the given publisher's identity."""
	validator = (
		validators.Validator()
		.allow_schemes("https")
		.allow_hosts("github.com", "gitlab.com")
		.require_presence_of("scheme", "host")
	)
	try:
		expected_uri = uri_reference(expected_repository_url)
		validator.validate(expected_uri)
	except exceptions.RFC3986Exception as e:
		return False, (f"Unsupported/invalid URL: {e}")

	actual_host = "github.com" if isinstance(publisher, GitHubPublisher) else "gitlab.com"
	expected_host = expected_uri.host
	if actual_host != expected_host:
		return False, (
			f"Verification failed: provenance was signed by a {actual_host} repository, but "
			f"expected a {expected_host} repository"
		)

	actual_repository = publisher.repository
	# '/owner/repo' -> 'owner/repo'
	expected_repository = expected_uri.path.lstrip("/")
	if actual_repository != expected_repository:
		return False, (
			f'Verification failed: provenance was signed by repository "{actual_repository}", '
			f'expected "{expected_repository}"'
		)
	return True, "Success"


def validate_attestation(
	attestation_bundles: list[AttestationBundle], package: PackageInfo
) -> bool:

	for attestation_bundle in attestation_bundles:
		publisher: Publisher = attestation_bundle.publisher

		if isinstance(publisher, GooglePublisher):
			return False

		return _check_repository_identity(
			expected_repository_url=package.repo or "", publisher=publisher
		)[0]

	return False


def verify_attestation(attestation_bundles: list[AttestationBundle], package: PackageInfo) -> bool:

	filename = package.filename or ""
	digest_256 = package.digest_256 or ""

	try:
		dist = Distribution(name=filename, digest=digest_256)
	except ValidationError:
		return False

	dist = Distribution(name=filename, digest=digest_256)

	try:
		for attestation_bundle in attestation_bundles:
			publisher: Publisher = attestation_bundle.publisher

			policy = publisher._as_policy()  # noqa: SLF001
			for attestation in attestation_bundle.attestations:
				attestation.verify(policy, dist)
	except (ValueError, Error):
		return False
	else:
		return True
