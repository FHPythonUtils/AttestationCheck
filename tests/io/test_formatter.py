from __future__ import annotations

from pathlib import Path

import pytest

from attestationcheck.io import fmt
from attestationcheck.models.packageinfo import PackageInfo

fmt.INFO = {"program": "attestationcheck", "version": "dev", "license": "MIT LICENSE"}

THISDIR = str(Path(__file__).resolve().parent)


simplePackages = [PackageInfo(name="example")]
complexPackages = [
	PackageInfo(
		name="example0",
		version="1.0.0",
		homePage="https://example.com",
		author="example_author",
		httpErrorCode=0,
		repo="example_repo",
		filename="example_filename",
		digest_256="example_digest",
		is_supported_publisher=True,
		is_attestation_present=True,
		is_attestation_valid=False,
		is_attestation_verified=False,
	),
	PackageInfo(
		name="example1",
		homePage="https://example.com",
		author="example_author",
		httpErrorCode=1,
	),
]


@pytest.mark.parametrize(
	("_fmt", "packages", "expected_output_file", "hide_params"),
	[
		("markdown", simplePackages, "simple.md", None),
		("markdown", complexPackages, "advanced.md", None),
		("markdown", complexPackages, "advanced_ignore_params.md", []),
		("json", simplePackages, "simple.json", None),
		("json", complexPackages, "advanced.json", None),
		(
			"json",
			complexPackages,
			"advanced_ignore_params.json",
			["IS_SUPPORTED_PUBLISHER", "REPO", "ATTESTATION_INFO"],
		),
		(
			"json",
			complexPackages,
			"advanced_ignore_params2.json",
			["is_supported_publisher", "repo", "attestation_info"],
		),
		("csv", simplePackages, "simple.csv", None),
		("csv", complexPackages, "advanced.csv", None),
		("ansi", simplePackages, "simple.ansi", None),
		("ansi", complexPackages, "advanced.ansi", None),
		("ansi", complexPackages, "advanced.ansi", []),
		("simple", simplePackages, "simple.txt", None),
		("simple", complexPackages, "advanced.txt", None),
		("simple", complexPackages, "advanced.txt", ["WRONG_PARAMETER"]),
	],
)
def test_output__fmt(
	_fmt: str,
	packages: list[PackageInfo],
	expected_output_file: str,
	hide_params: list[str] | None,
) -> None:
	actual_output = fmt.fmt(_fmt, packages, hide_parameters=hide_params)
	expected_output = Path(f"{THISDIR}/data/fmt/{expected_output_file}")
	# expected_output.write_text(actual_output, "utf-8")
	assert assert_eq(actual_output, expected_output.read_text("utf-8"))


def assert_eq(actual_input: str, expected_output: str) -> bool:
	actual = actual_input.strip().splitlines()
	expected = expected_output.strip().splitlines()

	if len(expected) != len(actual):
		return False

	return [x.strip() for x in actual] == [x.strip() for x in expected]
