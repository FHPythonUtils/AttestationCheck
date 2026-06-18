"""
The formatter is responsible for outputting the list of PackageInfo[s].

The available output formats are defined as follows

- ansi: Plain text output with ANSI color codes for terminal display.
	used for simple, color-coded output on the command line.
- plain: A basic, no-frills plain text format, used when a clean and simple
	textual representation is needed without any additional markup or styling.
- markdown: A lightweight markup language with plain-text formatting syntax. Ideal
	for creating formatted documents that can be easily converted into HTML for web display.
- html: A format suitable for rendering in web browsers. (can be styled with CSS
	for more complex presentation.)
- json: A structured data format. This format representing the list of PackageInfo[s]
	as a JSON object
- csv: A simple, comma-separated values format. widely used in spreadsheets and
	databases for easy import/export of data.

Note that these support the get_filtered_dict method, which allows users
to hide some of the output via the `--hide-output-parameters` cli flag. In addition
these support the show_only_failing method, which allows users
to show only packages that are not Verified with out license via the
`--show-only-failing` cli flag

"""

from __future__ import annotations

import csv
import json
import re
from collections import OrderedDict
from datetime import datetime
from enum import StrEnum, auto
from importlib.metadata import PackageNotFoundError, version
from io import StringIO
from pathlib import Path
from typing import Any

import markdown as markdownlib
from rich.console import Console
from rich.table import Table

from attestationcheck.models.packageinfo import AttestationInfo, PackageInfo

THISDIR = Path(__file__).resolve().parent

try:
	VERSION = version("attestationcheck")
except PackageNotFoundError:
	VERSION = "dev"
INFO = {"program": "attestationcheck", "version": VERSION, "license": "MIT LICENSE"}


def stripAnsi(string: str) -> str:
	"""
	Strip ansi codes from a given string.

	Args:
	----
		string (str): string to strip codes from

	Returns:
	-------
		str: plaintext, utf-8 string (safe for writing to files)

	"""
	return re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])").sub("", string)


def ansi(
	packages: list[dict[str, Any]],
) -> str:
	"""
	Format to ansi.

	:param License myLice: project license
	:param list[dict[str, Any]] packages: list of PackageInfo, representes as a dict to format.
	:return str: string to send to specified output in ansi format
	"""
	string = StringIO()

	console = Console(file=string, color_system="truecolor", safe_box=False)

	table = Table(title="\nInfo")
	table.add_column("Item", style="cyan")
	table.add_column("Value", style="magenta")
	_ = [table.add_row(k, v) for k, v in INFO.items()]

	console.print(table)

	if len(packages) == 0:
		return f"{string.getvalue()}\nNo packages"

	errors = [x for x in packages if x.get("httpErrorCode", 0) > 0]
	if len(errors) > 0:
		table = Table(title="\nList Of Errors")
		table.add_column("Package", style="magenta")
		table.add_column("Error Code", style="magenta")
		_ = [table.add_row(x.get("name", "?"), str(x.get("httpErrorCode", -1))) for x in errors]
		console.print(table)

	table = Table(title="\nList Of Packages")
	if name_bool := "name" in packages[0]:
		table.add_column("Package", header_style="magenta")
	if attestation_info := "attestation_info" in packages[0]:
		table.add_column("Attestation Info", header_style="magenta")
	if last_updated := "last_updated" in packages[0]:
		table.add_column("Last Updated", header_style="magenta")

	attestation_info_lookup = {
		AttestationInfo.NONE: "[red]Unsupported[/]",
		AttestationInfo.SUPPORTED: "[yellow]Supported[/]",
		AttestationInfo.PRESENT: "[cyan]Present[/]",
		AttestationInfo.VALID: "[green]Valid[/]",
		AttestationInfo.VERIFIED: "[green]Verified[/]",
	}
	_ = [
		table.add_row(
			*(
				([x.get("name")] if name_bool else [])
				+ (
					[attestation_info_lookup[x.get("attestation_info", AttestationInfo.NONE)]]
					if attestation_info
					else []
				)
				+ ([str(x.get("last_updated"))] if last_updated else [])
			)
		)
		for x in packages
	]
	console.print(table)
	return string.getvalue()


def plainText(
	packages: list[dict[str, Any]],
) -> str:
	"""
	Format to plain text.

	:param License myLice: project license
	:param list[dict[str, Any]] packages: list of PackageInfo, representes as a dict to format.
	:return str: string to send to specified output in plain text format

	"""
	return stripAnsi(ansi(packages))


def markdown(
	packages: list[dict[str, Any]],
) -> str:
	"""
	Format to markdown.

	:param License myLice: project license
	:param list[dict[str, Any]] packages: list of PackageInfo, representes as a dict to format.
	:return str: string to send to specified output in markdown format
	"""
	info = "\n".join(f"- {k}: {v}" for k, v in INFO.items())
	strBuf = [f"## Info\n\n{info}\n\n"]

	if len(packages) == 0:
		return f"{strBuf[0]}\nNo packages"

	strBuf.append("## Packages\n\nFind a list of packages below\n")
	packages = sorted(packages, key=lambda i: i.get("name", "?"))

	# Summary Table
	strBuf.append("|Package|Attestation Info|\n|:--|:--|")
	strBuf.extend([f"|{pkg.get('name')}||{pkg.get('attestation_info')}" for pkg in packages])

	# Details
	params_use_in_markdown = {
		"author": "Author",
		"warning": "Warning",
		"is_attestation_verified": "Attestation Verified",
		"is_attestation_valid": "Attestation Valid",
		"is_attestation_present": "Attestation Present",
		"is_supported_publisher": "Attestation Supported",
		"size": "Size",
	}
	for pkg in packages:
		pkg_ordered_dict = OrderedDict(
			(param, pkg[param]) for param in params_use_in_markdown if param in pkg
		)
		strBuf.extend(
			[
				f"\n### {pkg.get('namever')}\n",
				*(f"- {params_use_in_markdown[k]}: {v}" for k, v in pkg_ordered_dict.items()),
			]
		)
	return "\n".join(strBuf) + "\n"


def html(
	packages: list[dict[str, Any]],
) -> str:
	"""
	Format to html.

	:param License myLice: project license
	:param list[dict[str, Any]] packages: list of PackageInfo, representes as a dict to format.
	:return str: string to send to specified output in html format
	"""
	html = markdownlib.markdown(
		markdown(packages=packages),
		extensions=["tables"],
	)
	return (THISDIR / "html.template").read_text("utf-8").replace("{html}", html)


def raw(packages: list[dict[str, Any]]) -> str:
	"""
	Format to json.

	:param list[dict[str, Any]] packages: list of PackageInfo, represents as a dict to format.
	:return str: string to send to specified output in json format
	"""
	return json.dumps(
		{
			"info": INFO,
			"packages": packages,
		},
		indent="\t",
		default=lambda obj: obj.isoformat() if isinstance(obj, datetime) else obj,
	)


def rawCsv(
	packages: list[dict[str, Any]],
) -> str:
	"""
	Format to csv.

	:param list[dict[str, Any]] packages: list of PackageInfo, representes as a dict to format.
	:return str: string to send to specified output in csv format
	"""
	if len(packages) == 0:
		return ""

	string = StringIO()
	fieldnames = list(dict.fromkeys(key for package in packages for key in package.keys()))
	writer = csv.DictWriter(string, fieldnames=fieldnames, lineterminator="\n")
	writer.writeheader()
	writer.writerows(packages)
	return string.getvalue()


def fmt(
	format_: FMT,
	packages: list[PackageInfo],
	hide_parameters: set[str] | None = None,
	*,
	show_only_failing: bool = False,
) -> str:
	"""
	Format to a given format by `format_`.

	:param list[PackageInfo] packages: list of packages to format.
	:param set[str] hide_parameters: set of parameters to ignore in the output.
	:param bool show_only_failing: output only failing packages, defaults to False.
	:return str: string to send to specified output in ansi format
	"""
	hide_parameters = hide_parameters or set()
	if show_only_failing:
		packages = [x for x in packages if not x.is_attestation_verified]

	pkgs: list[dict[str, Any]] = [x.get_filtered_dict(hide_parameters) for x in packages]

	return formatMap.get(format_, plainText)(pkgs)


class FMT(StrEnum):
	json = auto()
	markdown = auto()
	html = auto()
	csv = auto()
	ansi = auto()
	simple = auto()


formatMap = {
	FMT.json: raw,
	FMT.markdown: markdown,
	FMT.html: html,
	FMT.csv: rawCsv,
	FMT.ansi: ansi,
	FMT.simple: plainText,
}
