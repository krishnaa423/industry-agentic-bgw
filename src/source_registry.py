from models import SourceSpec


SOURCE_SPECS = [
    SourceSpec(
        name="bgw_epsilon_keywords",
        kind="manual",
        url="http://manual.berkeleygw.org/4.0/epsilon-keywords/",
    ),
    SourceSpec(
        name="bgw_sigma_keywords",
        kind="manual",
        url="http://manual.berkeleygw.org/4.0/sigma-keywords/",
    ),
    SourceSpec(
        name="bgw_kernel_keywords",
        kind="manual",
        url="http://manual.berkeleygw.org/4.0/kernel-keywords/",
    ),
    SourceSpec(
        name="bgw_absorption_keywords",
        kind="manual",
        url="http://manual.berkeleygw.org/4.0/absorption-keywords/",
    ),
    SourceSpec(
        name="qe_input_pw",
        kind="manual",
        url="https://www.quantum-espresso.org/Doc/INPUT_PW.html",
    ),
    SourceSpec(
        name="qe_input_ph",
        kind="manual",
        url="https://www.quantum-espresso.org/Doc/INPUT_PH.html",
    ),
    SourceSpec(
        name="epw_inputs",
        kind="manual",
        url="https://docs.epw-code.org/Inputs/Inputs.html",
    ),
    SourceSpec(
        name="paper_lif_excitonic_polarons_arxiv_abs",
        kind="paper",
        url="https://arxiv.org/abs/2401.09369",
    ),
    SourceSpec(
        name="paper_lif_excitonic_polarons_arxiv_html",
        kind="paper",
        url="https://arxiv.org/html/2401.09369v1",
    ),
]

