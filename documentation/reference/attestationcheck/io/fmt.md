# Fmt

[Attestationcheck Index](../../README.md#attestationcheck-index) / [Attestationcheck](../index.md#attestationcheck) / [Io](./index.md#io) / Fmt

> Auto-generated documentation for [attestationcheck.io.fmt](../../../../attestationcheck/io/fmt.py) module.

- [Fmt](#fmt)
  - [ansi](#ansi)
  - [fmt](#fmt)
  - [html](#html)
  - [markdown](#markdown)
  - [plainText](#plaintext)
  - [raw](#raw)
  - [rawCsv](#rawcsv)
  - [stripAnsi](#stripansi)

## ansi

[Show source in fmt.py:69](../../../../attestationcheck/io/fmt.py#L69)

Format to ansi.

#### Arguments

- `myLice` *License* - project license
:param list[dict[str, Any]] packages: list of PackageInfo, representes as a dict to format.

#### Returns

Type: *str*
string to send to specified output in ansi format

#### Signature

```python
def ansi(packages: list[dict[str, Any]]) -> str: ...
```



## fmt

[Show source in fmt.py:241](../../../../attestationcheck/io/fmt.py#L241)

Format to a given format by `format_`.

:param list[PackageInfo] packages: list of packages to format.
:param set[str] hide_parameters: set of parameters to ignore in the output.

#### Arguments

- `show_only_failing` *bool* - output only failing packages, defaults to False.

#### Returns

Type: *str*
string to send to specified output in ansi format

#### Signature

```python
def fmt(
    format_: str,
    packages: list[PackageInfo],
    hide_parameters: set[str] | None = None,
    show_only_failing: bool = False,
) -> str: ...
```

#### See also

- [PackageInfo](../models/packageinfo.md#packageinfo)



## html

[Show source in fmt.py:189](../../../../attestationcheck/io/fmt.py#L189)

Format to html.

#### Arguments

- `myLice` *License* - project license
:param list[dict[str, Any]] packages: list of PackageInfo, representes as a dict to format.

#### Returns

Type: *str*
string to send to specified output in html format

#### Signature

```python
def html(packages: list[dict[str, Any]]) -> str: ...
```



## markdown

[Show source in fmt.py:144](../../../../attestationcheck/io/fmt.py#L144)

Format to markdown.

#### Arguments

- `myLice` *License* - project license
:param list[dict[str, Any]] packages: list of PackageInfo, representes as a dict to format.

#### Returns

Type: *str*
string to send to specified output in markdown format

#### Signature

```python
def markdown(packages: list[dict[str, Any]]) -> str: ...
```



## plainText

[Show source in fmt.py:130](../../../../attestationcheck/io/fmt.py#L130)

Format to plain text.

#### Arguments

- `myLice` *License* - project license
:param list[dict[str, Any]] packages: list of PackageInfo, representes as a dict to format.

#### Returns

Type: *str*
string to send to specified output in plain text format

#### Signature

```python
def plainText(packages: list[dict[str, Any]]) -> str: ...
```



## raw

[Show source in fmt.py:206](../../../../attestationcheck/io/fmt.py#L206)

Format to json.

:param list[dict[str, Any]] packages: list of PackageInfo, representes as a dict to format.

#### Returns

Type: *str*
string to send to specified output in json format

#### Signature

```python
def raw(packages: list[dict[str, Any]]) -> str: ...
```



## rawCsv

[Show source in fmt.py:222](../../../../attestationcheck/io/fmt.py#L222)

Format to csv.

:param list[dict[str, Any]] packages: list of PackageInfo, representes as a dict to format.

#### Returns

Type: *str*
string to send to specified output in csv format

#### Signature

```python
def rawCsv(packages: list[dict[str, Any]]) -> str: ...
```



## stripAnsi

[Show source in fmt.py:53](../../../../attestationcheck/io/fmt.py#L53)

Strip ansi codes from a given string.

#### Arguments

----
 - `string` *str* - string to strip codes from

#### Returns

-------
 - `str` - plaintext, utf-8 string (safe for writing to files)

#### Signature

```python
def stripAnsi(string: str) -> str: ...
```