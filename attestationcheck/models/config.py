from __future__ import annotations

from dataclasses import field

from depgather.models.defaultonnone import DefaultOnNoneModel


class LC_Config(DefaultOnNoneModel):
	"""LC_Config type."""

	file: str | None
	format: str | None
	pypi_api: str | None
	show_only_failing: bool
	zero: bool

	requirements_paths: set[str] = field(default_factory=set)
	groups: set[str] = field(default_factory=set)
	extras: set[str] = field(default_factory=set)
	skip_dependencies: set[str] = field(default_factory=set)
	hide_output_parameters: set[str] = field(default_factory=set)
