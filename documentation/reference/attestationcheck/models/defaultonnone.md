# Defaultonnone

[Attestationcheck Index](../../README.md#attestationcheck-index) / [Attestationcheck](../index.md#attestationcheck) / [Models](./index.md#models) / Defaultonnone

> Auto-generated documentation for [attestationcheck.models.defaultonnone](../../../../attestationcheck/models/defaultonnone.py) module.

- [Defaultonnone](#defaultonnone)
  - [DefaultOnNoneModel](#defaultonnonemodel)
    - [DefaultOnNoneModel.default_on_none](#defaultonnonemodeldefault_on_none)

## DefaultOnNoneModel

[Show source in defaultonnone.py:6](../../../../attestationcheck/models/defaultonnone.py#L6)

#### Signature

```python
class DefaultOnNoneModel(BaseModel): ...
```

### DefaultOnNoneModel.default_on_none

[Show source in defaultonnone.py:7](../../../../attestationcheck/models/defaultonnone.py#L7)

#### Signature

```python
@model_validator(mode="before")
@classmethod
def default_on_none(cls, values: Any) -> Any | dict[Any, Any]: ...
```