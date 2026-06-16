from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass, field, fields
from enum import StrEnum
from typing import Any, Protocol

UNKNOWN = "unknown"


class AttestationInfo(StrEnum):
	VERIFIED = "Verified"
	VALID = "Valid"
	PRESENT = "Present"
	SUPPORTED = "Supported"
	NONE = "Unsupported"


class PackageLike(Protocol):
	name: str


def iter_fields_and_properties(obj: Any) -> Generator[tuple[str, Any], Any, None]:
	# dataclass fields
	for f in fields(obj):
		yield f.name, getattr(obj, f.name)

	# properties
	for name, attr in vars(type(obj)).items():
		if isinstance(attr, property):
			yield name, getattr(obj, name)


@dataclass(unsafe_hash=True, order=True)
class PackageInfo:
	"""PackageInfo type."""

	name: str
	version: str | None = None
	namever: str = field(init=False)
	homePage: str | None = None
	author: str | None = None
	repo: str | None = None
	filename: str | None = None
	digest_256: str | None = None

	is_supported_publisher: bool = False
	is_attestation_present: bool = False
	is_attestation_valid: bool = False
	is_attestation_verified: bool = False

	httpErrorCode: int = 0

	def __post_init__(self) -> None:
		"""Set the namever once the object is initialised."""
		self.namever = f"{self.name}-{self.version or UNKNOWN}"

	@property
	def attestation_info(self) -> str:
		if self.is_attestation_verified:
			return AttestationInfo.VERIFIED
		if self.is_attestation_valid:
			return AttestationInfo.VALID
		if self.is_attestation_present:
			return AttestationInfo.PRESENT
		if self.is_supported_publisher:
			return AttestationInfo.SUPPORTED
		return AttestationInfo.NONE

	def get_filtered_dict(self, hide_output_parameters: set[str]) -> dict[str, Any]:
		"""
		Return a filtered dictionary of the object.

		:param set[str] hide_output_parameters: set of parameters to ignore
		:return dict: filtered dictionary
		"""
		hide_output_parameters_upper = {x.upper() for x in hide_output_parameters}
		return {
			k: (v if v is not None else UNKNOWN)
			for k, v in iter_fields_and_properties(self)
			if k.upper() not in hide_output_parameters_upper
		}
