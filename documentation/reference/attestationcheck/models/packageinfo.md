# PackageInfo

[Attestationcheck Index](../../README.md#attestationcheck-index) / [Attestationcheck](../index.md#attestationcheck) / [Models](./index.md#models) / PackageInfo

> Auto-generated documentation for [attestationcheck.models.packageinfo](../../../../attestationcheck/models/packageinfo.py) module.

- [PackageInfo](#packageinfo)
  - [AttestationInfo](#attestationinfo)
  - [PackageInfo](#packageinfo-1)
    - [PackageInfo().__post_init__](#packageinfo()__post_init__)
    - [PackageInfo().attestation_info](#packageinfo()attestation_info)
    - [PackageInfo().get_filtered_dict](#packageinfo()get_filtered_dict)
  - [PackageLike](#packagelike)
  - [iter_fields_and_properties](#iter_fields_and_properties)

## AttestationInfo

[Show source in packageinfo.py:11](../../../../attestationcheck/models/packageinfo.py#L11)

#### Signature

```python
class AttestationInfo(StrEnum): ...
```



## PackageInfo

[Show source in packageinfo.py:35](../../../../attestationcheck/models/packageinfo.py#L35)

PackageInfo type.

#### Signature

```python
class PackageInfo: ...
```

### PackageInfo().__post_init__

[Show source in packageinfo.py:54](../../../../attestationcheck/models/packageinfo.py#L54)

Set the namever once the object is initialised.

#### Signature

```python
def __post_init__(self) -> None: ...
```

### PackageInfo().attestation_info

[Show source in packageinfo.py:58](../../../../attestationcheck/models/packageinfo.py#L58)

#### Signature

```python
@property
def attestation_info(self) -> str: ...
```

### PackageInfo().get_filtered_dict

[Show source in packageinfo.py:70](../../../../attestationcheck/models/packageinfo.py#L70)

Return a filtered dictionary of the object.

:param set[str] hide_output_parameters: set of parameters to ignore

#### Returns

Type: *dict*
filtered dictionary

#### Signature

```python
def get_filtered_dict(self, hide_output_parameters: set[str]) -> dict[str, Any]: ...
```



## PackageLike

[Show source in packageinfo.py:19](../../../../attestationcheck/models/packageinfo.py#L19)

#### Signature

```python
class PackageLike(Protocol): ...
```



## iter_fields_and_properties

[Show source in packageinfo.py:23](../../../../attestationcheck/models/packageinfo.py#L23)

#### Signature

```python
def iter_fields_and_properties(obj: Any) -> Generator[tuple[str, Any], Any, None]: ...
```