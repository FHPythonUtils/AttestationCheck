# Packageinforesolver

[Attestationcheck Index](../README.md#attestationcheck-index) / [Attestationcheck](./index.md#attestationcheck) / Packageinforesolver

> Auto-generated documentation for [attestationcheck.packageinforesolver](../../../attestationcheck/packageinforesolver.py) module.

- [Packageinforesolver](#packageinforesolver)
  - [PackageInfoManager](#packageinfomanager)
    - [PackageInfoManager()._get_package_info](#packageinfomanager()_get_package_info)
    - [PackageInfoManager().getPackages](#packageinfomanager()getpackages)
    - [PackageInfoManager().resolve_requirements](#packageinfomanager()resolve_requirements)
  - [RemotePackageInfo](#remotepackageinfo)
    - [RemotePackageInfo().get_attestation_bundle](#remotepackageinfo()get_attestation_bundle)
    - [RemotePackageInfo().get_author](#remotepackageinfo()get_author)
    - [RemotePackageInfo().get_fileinfo](#remotepackageinfo()get_fileinfo)
    - [RemotePackageInfo().get_homePage](#remotepackageinfo()get_homepage)
    - [RemotePackageInfo().get_name](#remotepackageinfo()get_name)
    - [RemotePackageInfo().get_version](#remotepackageinfo()get_version)
    - [RemotePackageInfo().is_supported_publisher](#remotepackageinfo()is_supported_publisher)
    - [RemotePackageInfo().make_req](#remotepackageinfo()make_req)

## PackageInfoManager

[Show source in packageinforesolver.py:27](../../../attestationcheck/packageinforesolver.py#L27)

Manages retrieval of local and remote package information.

#### Signature

```python
class PackageInfoManager:
    def __init__(self, base_pypi_url: str = "https://pypi.org") -> None: ...
```

### PackageInfoManager()._get_package_info

[Show source in packageinforesolver.py:68](../../../attestationcheck/packageinforesolver.py#L68)

Retrieve package information, preferring local info.

#### Arguments

- `package` *PackageLike* - package info to unpack

#### Returns

Type: *PackageInfo*
Information about the package.

#### Signature

```python
def _get_package_info(self, package: PackageLike) -> PackageInfo: ...
```

#### See also

- [PackageInfo](models/packageinfo.md#packageinfo)
- [PackageLike](models/packageinfo.md#packagelike)

### PackageInfoManager().getPackages

[Show source in packageinforesolver.py:58](../../../attestationcheck/packageinforesolver.py#L58)

Retrieve package information from local installation or PyPI.

:param set[str] reqs: Set of dependency names to retrieve information for.

#### Returns

Type: *set[PackageInfo]*
A set of package information objects.

#### Signature

```python
def getPackages(self) -> set[PackageInfo]: ...
```

#### See also

- [PackageInfo](models/packageinfo.md#packageinfo)

### PackageInfoManager().resolve_requirements

[Show source in packageinforesolver.py:40](../../../attestationcheck/packageinforesolver.py#L40)

#### Signature

```python
def resolve_requirements(
    self,
    requirements_paths: set[str],
    groups: set[str],
    extras: set[str],
    skip_dependencies: set[str],
) -> None: ...
```



## RemotePackageInfo

[Show source in packageinforesolver.py:120](../../../attestationcheck/packageinforesolver.py#L120)

Handles retrieval of package info from PyPI.

#### Signature

```python
class RemotePackageInfo:
    def __init__(self, pypi_api: str, package: PackageInfo) -> None: ...
```

#### See also

- [PackageInfo](models/packageinfo.md#packageinfo)

### RemotePackageInfo().get_attestation_bundle

[Show source in packageinforesolver.py:178](../../../attestationcheck/packageinforesolver.py#L178)

#### Signature

```python
def get_attestation_bundle(self) -> list[AttestationBundle] | int: ...
```

### RemotePackageInfo().get_author

[Show source in packageinforesolver.py:162](../../../attestationcheck/packageinforesolver.py#L162)

#### Signature

```python
def get_author(self) -> str | None: ...
```

### RemotePackageInfo().get_fileinfo

[Show source in packageinforesolver.py:170](../../../attestationcheck/packageinforesolver.py#L170)

#### Signature

```python
def get_fileinfo(self) -> tuple[str, str] | tuple[None, None]: ...
```

### RemotePackageInfo().get_homePage

[Show source in packageinforesolver.py:159](../../../attestationcheck/packageinforesolver.py#L159)

#### Signature

```python
def get_homePage(self) -> str | None: ...
```

### RemotePackageInfo().get_name

[Show source in packageinforesolver.py:153](../../../attestationcheck/packageinforesolver.py#L153)

#### Signature

```python
def get_name(self) -> str | None: ...
```

### RemotePackageInfo().get_version

[Show source in packageinforesolver.py:156](../../../attestationcheck/packageinforesolver.py#L156)

#### Signature

```python
def get_version(self) -> str | None: ...
```

### RemotePackageInfo().is_supported_publisher

[Show source in packageinforesolver.py:166](../../../attestationcheck/packageinforesolver.py#L166)

#### Signature

```python
def is_supported_publisher(self) -> bool: ...
```

### RemotePackageInfo().make_req

[Show source in packageinforesolver.py:140](../../../attestationcheck/packageinforesolver.py#L140)

#### Signature

```python
def make_req(
    self, url: str, headers: dict[str, str] | None = None
) -> tuple[int, dict[str, Any]]: ...
```