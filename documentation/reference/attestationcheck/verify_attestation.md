# Verify Attestation

[Attestationcheck Index](../README.md#attestationcheck-index) / [Attestationcheck](./index.md#attestationcheck) / Verify Attestation

> Auto-generated documentation for [attestationcheck.verify_attestation](../../../attestationcheck/verify_attestation.py) module.

- [Verify Attestation](#verify-attestation)
  - [_check_repository_identity](#_check_repository_identity)
  - [validate_attestation](#validate_attestation)
  - [verify_attestation](#verify_attestation)

## _check_repository_identity

[Show source in verify_attestation.py:16](../../../attestationcheck/verify_attestation.py#L16)

Check that a repository url matches the given publisher's identity.

#### Signature

```python
def _check_repository_identity(
    expected_repository_url: str, publisher: GitHubPublisher | GitLabPublisher
) -> tuple[bool, str]: ...
```



## validate_attestation

[Show source in verify_attestation.py:51](../../../attestationcheck/verify_attestation.py#L51)

#### Signature

```python
def validate_attestation(
    attestation_bundles: list[AttestationBundle], package: PackageInfo
) -> bool: ...
```

#### See also

- [PackageInfo](models/packageinfo.md#packageinfo)



## verify_attestation

[Show source in verify_attestation.py:68](../../../attestationcheck/verify_attestation.py#L68)

#### Signature

```python
def verify_attestation(
    attestation_bundles: list[AttestationBundle], package: PackageInfo
) -> bool: ...
```

#### See also

- [PackageInfo](models/packageinfo.md#packageinfo)