"""Output the attestation status used by dependencies. e.g. Verified, Valid, Supported by package host etc."""

from __future__ import annotations

import argparse
from dataclasses import fields
from enum import Enum
from pathlib import Path
from sys import exit as sysexit
from sys import stdout

from configurator import Config
from configurator.node import ConfigNode

from attestationcheck import packageinforesolver  # ,checker
from attestationcheck.io import fmt
from attestationcheck.models.config import LC_Config
from attestationcheck.models.packageinfo import PackageInfo

stdout.reconfigure(encoding="utf-8")  # type: ignore[general-type-issues]


class ExitCode(Enum):
	SUCCESS = 0
	UNVERIFIED_PACKAGE = 1
	NO_PACKAGES = 3


def cli() -> None:  # pragma: no cover
	"""Cli entry point."""
	parser = argparse.ArgumentParser(description=__doc__, argument_default=argparse.SUPPRESS)

	parser.add_argument(
		"--format",
		"-f",
		help=f"Output format. one of: {', '.join(set(fmt.formatMap))}. default=simple",
	)
	parser.add_argument(
		"--requirements-paths",
		"-r",
		help="Filenames to read from (default=pyproject.toml)",
		nargs="+",
	)
	parser.add_argument(
		"--groups",
		"-g",
		help="Select groups from supported files",
		nargs="+",
	)
	parser.add_argument(
		"--extras",
		"-e",
		help="Select extras from supported files",
		nargs="+",
	)
	parser.add_argument(
		"--file",
		"-o",
		help="Filename to write output to (omit this for stdout)",
	)
	parser.add_argument(
		"--skip-dependencies",
		help="set of packages/dependencies to skip",
		nargs="+",
	)
	parser.add_argument(
		"--hide-output-parameters",
		help="set of parameters to hide from the produced output",
		nargs="+",
	)
	parser.add_argument(
		"--show-only-failing",
		help="Only output a set of failing packages from this lib",
		action="store_true",
	)
	parser.add_argument(
		"--pypi-api",
		help="Specify a custom pypi api endpoint, for example if using a custom pypi server, "
		"note this must implement the 'pypi' and 'integrity' endpoints",
	)
	parser.add_argument(
		"--zero",
		"-0",
		help="Return non zero exit code if a package with an unverified attestation is found, ideal"
		" for CI/CD",
		action="store_true",
	)
	args = vars(parser.parse_args())

	if not args.get("requirements_paths"):
		args["requirements_paths"] = ["pyproject.toml"]

	config: ConfigNode = Config()

	# (Parses in the following order:
	config_files = [
		"~/attestationcheck.json",
		"~/attestationcheck.toml",
		"attestationcheck.json",
		"attestationcheck.toml",
		"pyproject.toml",
	]

	for file in config_files:
		config += Config.from_path(file, optional=True)

	scopedData: ConfigNode = config.get("tool", {}).get("attestationcheck", ConfigNode())
	attestationcheckConf: LC_Config = LC_Config.model_validate({**scopedData.data, **args})

	ec = main(attestationcheckConf)

	sysexit(ec.value)


def main(attestationcheckConf: LC_Config) -> ExitCode:
	"""Test entry point."""
	exitCode = ExitCode.SUCCESS

	# File
	requirements_paths = attestationcheckConf.requirements_paths
	output_file = (
		stdout
		if attestationcheckConf.file == ""
		else Path(attestationcheckConf.file).open("w", encoding="utf-8")
	)

	package_info_manager = packageinforesolver.PackageInfoManager(
		attestationcheckConf.pypi_api or "https://pypi.org"
	)

	package_info_manager.resolve_requirements(
		requirements_paths=requirements_paths,
		groups=attestationcheckConf.groups,
		extras=attestationcheckConf.extras,
		skip_dependencies=attestationcheckConf.skip_dependencies,
	)

	all_packages: set[PackageInfo] = package_info_manager.getPackages()

	incompatible = any(not x.is_attestation_verified for x in all_packages)

	# Format the results
	hide_output_parameters = attestationcheckConf.hide_output_parameters

	available_params = [param.name.upper() for param in fields(PackageInfo)]
	if not all(hop in available_params for hop in hide_output_parameters):
		msg = (
			f"Invalid parameter(s) in `hide_output_parameters`. "
			f"Valid parameters are: {', '.join(available_params)}"
		)
		raise ValueError(msg)

	print(
		fmt.fmt(
			attestationcheckConf.format,
			sorted(all_packages),
			hide_output_parameters,
			show_only_failing=attestationcheckConf.show_only_failing,
		),
		file=output_file,
	)

	# Exit code of 1 if args.zero
	if attestationcheckConf.zero:
		if len(all_packages) == 0:
			exitCode = ExitCode.NO_PACKAGES
		if incompatible:
			exitCode = ExitCode.UNVERIFIED_PACKAGE

	# Cleanup + exit
	if attestationcheckConf.file not in [None, ""]:
		output_file.close()
	return exitCode
