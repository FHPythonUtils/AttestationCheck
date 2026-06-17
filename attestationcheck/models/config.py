from __future__ import annotations

from dataclasses import field
from typing import Any, Literal

from depgather.models.defaultonnone import DefaultOnNoneModel
from pydantic import field_validator

from attestationcheck.io.fmt import FMT


class LC_Config(DefaultOnNoneModel):
	"""LC_Config type."""

	file: str = ""
	license: str = ""
	format: FMT = FMT.simple
	pypi_api: str = ""
	show_only_failing: bool = False
	zero: bool = False

	requirements_paths: set[str] = field(default_factory=set)
	groups: set[str] = field(default_factory=set)
	extras: set[str] = field(default_factory=set)
	skip_dependencies: set[str] = field(default_factory=set)
	hide_output_parameters: set[str] = field(default_factory=set)

	@field_validator("format", mode="before")
	@classmethod
	def normalize_format(cls, value: Any) -> Any | Literal[FMT.simple]:
		if value not in FMT:
			return FMT.simple
		return value
