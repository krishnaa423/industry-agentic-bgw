# agentic_bgw

`agentic_bgw` is a staged, literature-grounded starter-input generator for a first-principles workflow built around:

- Quantum ESPRESSO for `scf.in` and `dfpt.in`
- EPW for `epw.in`
- BerkeleyGW for `epsilon.inp`, `sigma.inp`, `kernel.inp`, and `absorption.inp`

The current target study is the LiF excitonic-polaron workflow from Dai et al. (2024). The goal is not to claim a reproduction-ready workflow. The goal is to show a clean, inspectable pipeline that combines retrieval with structured extraction and deterministic file rendering.

**What This Repo Does**
It downloads a small curated corpus of manuals and one paper, builds local vector stores, extracts paper facts into a structured plan, and then writes starter input files with explicit assumptions and unresolved items.

The generated starter files are:

- [scf.in](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage3_outputs/scf.in:1)
- [epsilon.inp](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage3_outputs/epsilon.inp:1)
- [sigma.inp](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage3_outputs/sigma.inp:1)
- [dfpt.in](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage4_outputs/dfpt.in:1)
- [kernel.inp](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage4_outputs/kernel.inp:1)
- [absorption.inp](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage4_outputs/absorption.inp:1)
- [epw.in](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage5_outputs/epw.in:1)

**Architecture**
The refactor keeps the code in plain files under `src/`, not as a package.

Main pieces:

- `src/main.py`: command router for the stage commands
- `src/stage1.py`: source fetch + vector-store build + corpus report
- `src/stage2.py`: paper retrieval + structured extraction into a `Stage2Plan`
- `src/stage3.py`: deterministic generation of `scf.in`, `epsilon.inp`, `sigma.inp`
- `src/stage4.py`: deterministic generation of `dfpt.in`, `kernel.inp`, `absorption.inp`
- `src/stage5.py`: deterministic generation of `epw.in`
- `src/retrieval_store.py`: local Chroma store build/load/retrieve helpers
- `src/models.py`: shared Pydantic and dataclass models

The code is organized so the interesting decisions are visible in function names and model names rather than buried in comments.

**RAG Design**
This repo now uses two persistent local Chroma vector stores:

- manuals store: [docs/vector_store/manuals](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/vector_store)
- papers store: [docs/vector_store/papers](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/vector_store)

Why two stores:

- the manuals store is for syntax, keyword names, and executable-specific expectations
- the papers store is for study-specific facts like cutoffs, band windows, software used, and workflow hints
- splitting them reduces cross-talk between “what does this keyword mean?” and “what did this LiF paper actually do?”

Current Stage 1 build created:

- `337` manual chunks
- `419` paper chunks

Those counts are reported in [docs/stage1_report.md](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage1_report.md:1).

**What Went Into Each Store**
Manuals store documents:

- BerkeleyGW `epsilon` keywords
- BerkeleyGW `sigma` keywords
- BerkeleyGW `kernel` keywords
- BerkeleyGW `absorption` keywords
- Quantum ESPRESSO `INPUT_PW`
- Quantum ESPRESSO `INPUT_PH`
- EPW `Inputs`

Paper store documents:

- arXiv abstract page for the LiF excitonic-polaron paper
- arXiv HTML full text for the LiF excitonic-polaron paper

Source snapshots live under [docs/sources](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/sources).

**How Retrieval Is Used**
Stage 1:

- fetch source pages with `requests`
- clean HTML with `BeautifulSoup`
- split text with `RecursiveCharacterTextSplitter`
- embed chunks with `OpenAIEmbeddings`
- persist the chunks to Chroma

Stage 2:

- query the paper store for a few focused evidence requests
- pass the retrieved paper chunks to `gpt-4.1-nano`
- ask for structured output into `Stage2Plan`
- apply deterministic regex overrides for the numeric fields that matter most

Stages 3 to 5:

- query the manuals store for the relevant keyword context
- keep file writing deterministic
- use the Stage 2 plan for numerical values from the paper
- render starter templates instead of letting the model free-write input files

That last choice is deliberate. Retrieval and model extraction are useful for evidence gathering, but the actual file emission is more trustworthy when the output is a template with explicit assumptions.

**Tools Used**
- `requests`
- `BeautifulSoup`
- `RecursiveCharacterTextSplitter`
- `OpenAIEmbeddings`
- `Chroma`
- `ChatOpenAI` with `gpt-4.1-nano`
- Pydantic structured output models
- deterministic template renderers
- regex overrides for critical paper values

**Stage Flow**
Stage 1:

- fetch docs and paper
- build vector stores
- write [stage1_manifest.json](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage1_manifest.json:1)
- write [stage1_report.md](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage1_report.md:1)

Stage 2:

- retrieve paper evidence
- extract structured workflow facts
- write [stage2_plan.json](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage2_plan.json:1)
- write [stage2_report.md](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage2_report.md:1)

Stage 3:

- generate `scf.in`, `epsilon.inp`, `sigma.inp`
- write [stage3_payload.json](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage3_payload.json:1)
- write [stage3_report.md](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage3_report.md:1)

Stage 4:

- generate `dfpt.in`, `kernel.inp`, `absorption.inp`
- write [stage4_payload.json](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage4_payload.json:1)
- write [stage4_report.md](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage4_report.md:1)

Stage 5:

- generate `epw.in`
- write [stage5_payload.json](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage5_payload.json:1)
- write [stage5_report.md](/Users/krishnaa/Documents/programming/python/industry/cs/agentic_bgw/docs/stage5_report.md:1)

**How To Run**
From the repo root:

```bash
python src/main.py stage1-fetch
python src/main.py stage1-check
python src/main.py stage2-extract
python src/main.py stage2-check
python src/main.py stage3-generate
python src/main.py stage3-check
python src/main.py stage4-generate
python src/main.py stage4-check
python src/main.py stage5-generate
python src/main.py stage5-check
```

Or run the whole smoke test:

```bash
python tests/run_pipeline_check.py
```

That test rebuilds the sources, vector stores, reports, and generated starter inputs, then checks for expected markers in the final files.

**Generated File Snippets**
`scf.in`

```text
&SYSTEM
  ibrav=0,
  nat=2,
  ntyp=2,
  ecutwfc=100.0,
  occupations='fixed'
/
...
K_POINTS automatic
  8 8 8 0 0 0
```

`epsilon.inp`

```text
epsilon_cutoff 10.0
number_bands 200
frequency_dependence 0
screening_semiconductor
use_wfn_hdf5
```

`dfpt.in`

```text
&INPUTPH
  prefix='LiF',
  outdir='tmp/',
  tr2_ph=1.0d-14,
  ldisp=.true.,
  nq1=8, nq2=8, nq3=8,
/
```

`epw.in`

```text
&inputepw
  prefix      = 'LiF'
  outdir      = 'tmp/'
  dvscf_dir   = 'tmp/'
  elph        = .true.
  wannierize  = .true.
  nk1         = 8
  nq1         = 8
  proj(1)     = 'random'
/
```

**Current Limitations**
- `scf.in` still contains placeholders for pseudopotential filenames, cell vectors, and atomic positions
- the exact BerkeleyGW mapping for the paper’s COHSEX choice still needs confirmation from a trusted working example
- `epw.in` is the most assumption-heavy file because Wannier subspace, projection choice, and interpolation details are not fully specified by the paper alone
- this repo currently generates starter inputs, not guaranteed reproduction-ready inputs

That tradeoff is intentional. The project is meant to be understandable, inspectable, and showcaseable rather than over-automated and brittle.
