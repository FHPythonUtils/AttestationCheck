[![GitHub top language](https://img.shields.io/github/languages/top/FHPythonUtils/AttestationCheck.svg?style=for-the-badge&cacheSeconds=28800)](../../)
[![Issues](https://img.shields.io/github/issues/FHPythonUtils/AttestationCheck.svg?style=for-the-badge&cacheSeconds=28800)](../../issues)
[![License](https://img.shields.io/github/license/FHPythonUtils/AttestationCheck.svg?style=for-the-badge&cacheSeconds=28800)](/LICENSE.md)
[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/AttestationCheck.svg?style=for-the-badge&cacheSeconds=28800)](../../commits/master)
[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/AttestationCheck.svg?style=for-the-badge&cacheSeconds=28800)](../../commits/master)
[![PyPI Downloads](https://img.shields.io/pypi/dm/attestationcheck.svg?style=for-the-badge&cacheSeconds=28800)](https://pypistats.org/packages/attestationcheck)
[![PyPI Total Downloads](https://img.shields.io/badge/dynamic/json?style=for-the-badge&label=total%20downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi%2Epepy%2Etech%2Fapi%2Fv2%2Fprojects%2Fattestationcheck)](https://pepy.tech/project/attestationcheck)
[![PyPI Version](https://img.shields.io/pypi/v/attestationcheck.svg?style=for-the-badge&cacheSeconds=28800)](https://pypi.org/project/attestationcheck)

<!-- omit in toc -->
# AttestationCheck

<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">

Output the attestation status used by dependencies. e.g. Verified, Valid, Supported by package host etc.

<!-- omit in toc -->
## Table of Contents

- [Examples from the command-line](#examples-from-the-command-line)
  - [Using pyproject.toml (default if not piping input)](#using-pyprojecttoml-default-if-not-piping-input)
  - [Use csv format](#use-csv-format)
  - [Groups](#groups)
- [Help](#help)
- [Configuration Example](#configuration-example)
  - [Example 1: pyproject.toml](#example-1-pyprojecttoml)
  - [Example 2: attestationcheck.json](#example-2-attestationcheckjson)
- [Documentation](#documentation)
- [Install With PIP](#install-with-pip)
- [Language information](#language-information)
- [Working with the repo](#working-with-the-repo)
- [Community Files](#community-files)
  - [Licence](#licence)
  - [Changelog](#changelog)
  - [Code of Conduct](#code-of-conduct)
  - [Contributing](#contributing)
  - [Security](#security)
  - [Support](#support)

## Examples from the command-line

See below for the output if you run `attestationcheck` in this directory. More examples are available
[here](documentation/user/examples.md)

### Using pyproject.toml (default if not piping input)

```txt
>> uv run attestationcheck 
                              
             Info             
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Item    ┃ Value            ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ program │ attestationcheck │
│ version │ 0.1.1            │
│ license │ MIT LICENSE      │
└─────────┴──────────────────┘
                                                                              
                               List Of Packages                               
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Package              ┃ Attestation Info ┃ Last Updated                     ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ annotated-types      │ Supported        │ 2024-05-20 21:33:25.928805+00:00 │
│ attrs                │ Verified         │ 2026-03-19 14:22:25.026315+00:00 │
│ cattrs               │ Valid            │ 2026-02-18 22:15:19.406296+00:00 │
│ certifi              │ Valid            │ 2026-05-20 11:46:50.073147+00:00 │
│ cffi                 │ Supported        │ 2025-09-08 23:24:04.541971+00:00 │
.....
│ tuf                  │ Verified         │ 2026-05-18 08:28:57.408643+00:00 │
│ typing-extensions    │ Verified         │ 2025-08-25 13:49:26.313895+00:00 │
│ typing-inspection    │ Verified         │ 2025-10-01 02:14:41.687923+00:00 │
│ url-normalize        │ Supported        │ 2026-04-25 00:31:59.514290+00:00 │
│ urllib3              │ Verified         │ 2026-05-07 16:13:18.596909+00:00 │
└──────────────────────┴──────────────────┴──────────────────────────────────┘

```

### Use csv format

```csv
>>> uv run attestationcheck -f csv
name,version,namever,homePage,author,repo,filename,digest_256,is_supported_publisher,is_attestation_present,is_attestation_valid,is_attestation_verified,last_updated,httpErrorCode,attestation_info
annotated-types,0.7.0,annotated-types-0.7.0,,Adrian Garcia Badaracco,https://github.com/annotated-types/annotated-types,annotated_types-0.7.0-py3-none-any.whl,1f02e8b43a8fbbc3f3e0d4f0f4bfc8131bcb4eebe8849b8e5c773f3a1c582a53,True,False,False,False,2024-05-20 21:33:25.928805+00:00,0,Supported
attrs,26.1.0,attrs-26.1.0,,Hynek Schlawack,https://tidelift.com/subscription/pkg/pypi-attrs?utm_source=pypi-attrs&utm_medium=pypi,attrs-26.1.0-py3-none-any.whl,c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309,True,True,False,True,2026-03-19 14:22:25.026315+00:00,0,Verified
cattrs,26.1.0,cattrs-26.1.0,,Tin Tvrtkovic,https://github.com/python-attrs/cattrs,cattrs-26.1.0-py3-none-any.whl,d1e0804c42639494d469d08d4f26d6b9de9b8ab26b446db7b5f8c2e97f7c3096,True,True,True,True,2026-02-18 22:15:19.406296+00:00,0,Verified
certifi,2026.5.20,certifi-2026.5.20,https://github.com/certifi/python-certifi,Kenneth Reitz,https://github.com/certifi/python-certifi,certifi-2026.5.20-py3-none-any.whl,3c52e209ba0a4ad7aebe60436a4ab349c39e1e602e8c134221e546902ad25897,True,True,True,True,2026-05-20 11:46:50.073147+00:00,0,Verified
cffi,2.0.0,cffi-2.0.0,,"Armin Rigo, Maciej Fijalkowski",https://github.com/python-cffi/cffi,cffi-2.0.0-cp39-cp39-win_amd64.whl,b882b3df248017dba09d6b16defe9b5c407fe32fc7c65a9c69798e6175601be9,True,False,False,False,2025-09-08 23:24:04.541971+00:00,0,Supported
...
tuf,7.0.0,tuf-7.0.0,,theupdateframework@googlegroups.com,https://github.com/theupdateframework/python-tuf,tuf-7.0.0-py3-none-any.whl,572bdbdc9ff4a82278a0d4773e6100863b9b33023f27575e84ca65b486dd0d79,True,True,True,True,2026-05-18 08:28:57.408643+00:00,0,Verified
typing-extensions,4.15.0,typing-extensions-4.15.0,,"""Guido van Rossum, Jukka Lehtosalo, Łukasz Langa, Michael Lee""",https://github.com/python/typing_extensions,typing_extensions-4.15.0-py3-none-any.whl,f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548,True,True,True,True,2025-08-25 13:49:26.313895+00:00,0,Verified
typing-inspection,0.4.2,typing-inspection-0.4.2,,Victorien Plot,https://github.com/pydantic/typing-inspection,typing_inspection-0.4.2-py3-none-any.whl,4ed1cacbdc298c220f1bd249ed5287caa16f34d44ef4e9c3d0cbad5b521545e7,True,True,True,True,2025-10-01 02:14:41.687923+00:00,0,Verified
url-normalize,3.0.0,url-normalize-3.0.0,,Nikolay Panov,https://github.com/niksite/url-normalize,url_normalize-3.0.0-py3-none-any.whl,95234bd359f86831c1fd87c248877f2a6887db2f3b5087120083f2fffcba4889,True,False,False,False,2026-04-25 00:31:59.514290+00:00,0,Supported
urllib3,2.7.0,urllib3-2.7.0,,Andrey Petrov,https://github.com/urllib3/urllib3/issues,urllib3-2.7.0-py3-none-any.whl,9fb4c81ebbb1ce9531cce37674bbc6f1360472bc18ca9a553ede278ef7276897,True,True,False,True,2026-05-07 16:13:18.596909+00:00,0,Verified

```

### Groups

```txt
uv run attestationcheck  --show-only-failing -g dev

...
                                                           
                             List Of Packages                              
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Package           ┃ Attestation Info ┃ Last Updated                     ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ annotated-types   │ Supported        │ 2024-05-20 21:33:25.928805+00:00 │
│ basedpyright      │ Supported        │ 2026-06-14 09:05:30.177236+00:00 │
│ cffi              │ Supported        │ 2025-09-08 23:24:04.541971+00:00 │
│ configurator      │ Supported        │ 2023-09-13 07:03:15.373819+00:00 │
│ email-validator   │ Supported        │ 2025-08-26 13:09:06.831581+00:00 │
│ markdown          │ Supported        │ 2026-02-09 14:57:26.942957+00:00 │
│ markdown-it-py    │ Supported        │ 2026-05-07 12:08:28.360612+00:00 │
│ mdurl             │ Supported        │ 2022-08-14 12:40:10.846281+00:00 │
│ pyasn1            │ Supported        │ 2026-03-17 01:06:53.382518+00:00 │
│ pycparser         │ Supported        │ 2026-01-21 14:26:51.890565+00:00 │
│ pydantic-core     │ Supported        │ 2026-05-22 13:19:00.229323+00:00 │
│ pygments          │ Supported        │ 2026-03-29 13:29:33.898791+00:00 │
│ pyopenssl         │ Valid            │ 2026-06-12 20:28:07.458876+00:00 │
│ rfc3986           │ Unsupported      │ 2022-01-10 00:52:30.832978+00:00 │
│ rfc8785           │ Supported        │ 2024-09-27 16:33:31.206853+00:00 │
│ rich              │ Supported        │ 2026-04-12 08:24:00.750018+00:00 │
│ ruff              │ Supported        │ 2026-06-11 17:54:47.663633+00:00 │
│ tomli             │ Supported        │ 2026-03-25 20:22:03.828102+00:00 │
│ typing-extensions │ Valid            │ 2025-08-25 13:49:26.313895+00:00 │
│ url-normalize     │ Supported        │ 2026-04-25 00:31:59.514290+00:00 │
└───────────────────┴──────────────────┴──────────────────────────────────┘

```

## Help

```txt
usage: attestationcheck [-h] [--format FORMAT] [--requirements-paths REQUIREMENTS_PATHS [REQUIREMENTS_PATHS ...]]
                        [--groups GROUPS [GROUPS ...]] [--extras EXTRAS [EXTRAS ...]] [--file FILE]
                        [--skip-dependencies SKIP_DEPENDENCIES [SKIP_DEPENDENCIES ...]]
                        [--hide-output-parameters HIDE_OUTPUT_PARAMETERS [HIDE_OUTPUT_PARAMETERS ...]] [--show-only-failing]
                        [--pypi-api PYPI_API] [--zero]

Output the attestation status used by dependencies. e.g. Verified, Valid, Supported by package host etc.

options:
  -h, --help            show this help message and exit
  --format, -f FORMAT   Output format. one of: html, simple, csv, ansi, markdown, json. default=simple
  --requirements-paths, -r REQUIREMENTS_PATHS [REQUIREMENTS_PATHS ...]
                        Filenames to read from (omit for stdin if piping, else pyproject.toml)
  --groups, -g GROUPS [GROUPS ...]
                        Select groups from supported files
  --extras, -e EXTRAS [EXTRAS ...]
                        Select extras from supported files
  --file, -o FILE       Filename to write output to (omit this for stdout)
  --skip-dependencies SKIP_DEPENDENCIES [SKIP_DEPENDENCIES ...]
                        set of packages/dependencies to skip
  --hide-output-parameters HIDE_OUTPUT_PARAMETERS [HIDE_OUTPUT_PARAMETERS ...]
                        set of parameters to hide from the produced output
  --show-only-failing   Only output a set of failing packages from this lib
  --pypi-api PYPI_API   Specify a custom pypi api endpoint, for example if using a custom pypi server, note this must implement the 'pypi' and
                        'integrity' endpoints
  --zero, -0            Return non zero exit code if a package with an unverified attestation is found, ideal for CI/CD
```

<!-- More information on using `attestationcheck` from the command line is available [here](documentation/user/README.md) -->

You can also import this into your own project and use any of the functions
in the DOCS

## Configuration Example

Configuration files are parsed in the following order: `pyproject.toml`, 
 `attestationcheck.toml`, `attestationcheck.json`, `~/attestationcheck.toml`, `~/attestationcheck.json`,

- ⚠ All config files are parsed, however configuration defined in previous files takes precedent

### Example 1: pyproject.toml

```toml

[tool.attestationcheck]
format = "simple"             # Output format (e.g., "json", "csv", etc.)
requirements_paths = []       # List of filenames to read from
groups = []                   # List of selected groups
extras = []                   # List of selected extras
file = ""                     # Output file (leave empty for stdout)
skip_dependencies = []        # Dependencies to skip (compatibility = True)
hide_output_parameters = []   # Parameters to hide from output
show_only_failing = false     # Show only incompatible/failing packages
pypi_api = "https://pypi.org" # Custom PyPI API endpoint
zero = false                  # Return non-zero exit code 

```

### Example 2: attestationcheck.json

```json
{
  "tool": {
    "attestationcheck": {
      "format": "simple",
      "requirements_paths": [],
      "groups": [],
      "extras": [],
      "file": "",
      "skip_dependencies": [],
      "hide_output_parameters": [],
      "show_only_failing": false,
      "pypi_api": "https://pypi.org",
      "zero": false
    }
  }
}
```

## Documentation

A high-level overview of how the documentation is organized organized will help you know
where to look for certain things:

<!--
- [Tutorials](/documentation/tutorials) take you by the hand through a series of steps to get
  started using the software. Start here if you’re new.
-->
- The [Technical Reference](/documentation/reference) documents APIs and other aspects of the
  machinery. This documentation describes how to use the classes and functions at a lower level
  and assume that you have a good high-level understanding of the software.
<!--
- The [Help](/documentation/help) guide provides a starting point and outlines common issues that you
  may have.
-->

## Install With PIP

```python
pip install attestationcheck
```

Head to <https://pypi.org/project/attestationcheck/> for more info

## Language information

Using python 3.12, to 3.14

## Working with the repo

Clone, the repo with

```bash
git clone https://github.com/FHPythonUtils/AttestationCheck
```

Format

```sh
uv run ruff format
```

Linting

```sh
uv run ruff check
uv run python3 -m basedpyright -p .
```

Testing

```sh
uv run python3 -m pytest
```

Alternatively use `tox` to run tests over a range of python versions

```sh
uvx tox
```

Documentation

```sh
uvx --python 3.10  handsdown --output-path ./documentation/reference
```

## Community Files

### Licence

MIT License
Copyright (c) FredHappyface
(See the [LICENSE](/LICENSE.md) for more information.)

### Changelog

See the [Changelog](/CHANGELOG.md) for more information.

### Code of Conduct

Online communities include people from many backgrounds. The *Project*
contributors are committed to providing a friendly, safe and welcoming
environment for all. Please see the
[Code of Conduct](https://github.com/FHPythonUtils/.github/blob/master/CODE_OF_CONDUCT.md)
 for more information.

### Contributing

Contributions are welcome, please see the
[Contributing Guidelines](https://github.com/FHPythonUtils/.github/blob/master/CONTRIBUTING.md)
for more information.

### Security

Thank you for improving the security of the project, please see the
[Security Policy](https://github.com/FHPythonUtils/.github/blob/master/SECURITY.md)
for more information.

### Support

Thank you for using this project, I hope it is of use to you. Please be aware that
those involved with the project often do so for fun along with other commitments
(such as work, family, etc). Please see the
[Support Policy](https://github.com/FHPythonUtils/.github/blob/master/SUPPORT.md)
for more information.
