from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass(frozen=True)
class SourceSpec:
    name: str
    kind: str
    url: str


class PaperField(BaseModel):
    value: str | None = None
    status: str = Field(description="one of found, inferred, missing")
    evidence: str = ""
    notes: str = ""


class Stage2Plan(BaseModel):
    material: PaperField
    study_goal: PaperField
    uses_dft: bool
    uses_dfpt: bool
    uses_epw: bool
    uses_gw: bool
    uses_bse: bool
    dft_code: PaperField
    xc_functional: PaperField
    pseudopotentials: PaperField
    pw_cutoff_ry: PaperField
    scf_conv_thr_ry: PaperField
    dfpt_conv_thr_ry2: PaperField
    epw_code: PaperField
    wannier_code: PaperField
    gw_code: PaperField
    dielectric_cutoff_ry: PaperField
    sigma_valence_bands: PaperField
    sigma_conduction_bands: PaperField
    sigma_self_energy_method: PaperField
    quasiparticle_gap_ev: PaperField
    kernel_valence_bands: PaperField
    kernel_conduction_bands: PaperField
    bse_k_grid: PaperField
    supercell_hint: PaperField
    missing_items: list[str]
    overall_notes: str


class Stage3Artifacts(BaseModel):
    scf_in: str
    epsilon_inp: str
    sigma_inp: str
    assumptions: list[str]
    unresolved_items: list[str]
    doc_basis: list[str]
    retrieved_context: list[str]
    overall_notes: str


class Stage4Artifacts(BaseModel):
    dfpt_in: str
    kernel_inp: str
    absorption_inp: str
    assumptions: list[str]
    unresolved_items: list[str]
    doc_basis: list[str]
    retrieved_context: list[str]
    overall_notes: str


class Stage5Artifacts(BaseModel):
    epw_in: str
    assumptions: list[str]
    unresolved_items: list[str]
    doc_basis: list[str]
    retrieved_context: list[str]
    overall_notes: str

