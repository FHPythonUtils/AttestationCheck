from pydantic import Field

from attestationcheck.models.defaultonnone import DefaultOnNoneModel


class Envelope(DefaultOnNoneModel):
	signature: str = ""
	statement: str = ""


class KindVersion(DefaultOnNoneModel):
	kind: str = ""
	version: str = ""


class LogId(DefaultOnNoneModel):
	key_id: str = ""


class InclusionPromise(DefaultOnNoneModel):
	signed_entry_timestamp: str = ""


class Checkpoint(DefaultOnNoneModel):
	envelope: str = ""


class InclusionProof(DefaultOnNoneModel):
	checkpoint: Checkpoint = Checkpoint()
	hashes: list[str] = Field(default_factory=list)
	log_index: str = ""
	root_hash: str = ""
	tree_size: str = ""


class TransparencyEntry(DefaultOnNoneModel):
	canonicalizedBody: str = ""
	inclusionPromise: InclusionPromise = InclusionPromise()
	inclusionProof: InclusionProof = InclusionProof()

	integratedTime: int = 0
	kindVersion: KindVersion = KindVersion()
	logId: LogId = LogId()
	logIndex: str = ""


class VerificationMaterial(DefaultOnNoneModel):
	certificate: str = ""
	transparency_entries: list[TransparencyEntry] = Field(default_factory=list)


class Attestation(DefaultOnNoneModel):
	envelope: Envelope = Envelope()
	verification_material: VerificationMaterial = VerificationMaterial()
	version: int = 0


class Publisher(DefaultOnNoneModel):
	claims: dict = Field(default_factory=dict)
	environment: str = ""
	kind: str = ""
	repository: str = ""
	workflow: str = ""


class AttestationBundle(DefaultOnNoneModel):
	attestations: list[Attestation] = Field(default_factory=list)
	publisher: Publisher = Publisher()


class Provenance(DefaultOnNoneModel):
	attestation_bundles: list[AttestationBundle]
	version: int = 1
