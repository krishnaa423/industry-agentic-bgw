# Stage 5 Report

This report checks the starter-file generation stage for epw.in.

## File Check

### epw.in
- status: ok
- missing_markers: none
- preview:
```text
&inputepw
  prefix      = 'LiF'
  outdir      = 'tmp/'
  dvscf_dir   = 'tmp/'
  elph        = .true.
  epbwrite    = .true.
  epwwrite    = .true.
  wannierize  = .true.
  kmaps       = .true.
  nk1         = 8
  nk2         = 8
  nk3         = 8
  nq1         = 8
  nq2         = 8
  nq3         = 8
  nkf1        = 8
  nkf2        = 8
  nkf3        = 8
  nqf1        = 8
  nqf2        = 8
  nqf3        = 8
  nbndsub     = 10
  nbndskip    = 0
  proj(1)     = 'random'
  num_iter    = 500
  degaussw    = 0.01
  fsthick     = 0.40
  efermi_read = .false.
/

```

## Retrieved Context

- [query] EPW inputs prefix outdir dvscf_dir elph epbwrite epwwrite wannierize kmaps
- [epw_inputs]
EPW
 
 | Inputs for EPW
 
 

|||

Quick search

Project

About

Releases

Documentation

Inputs for EPW

Inputs for ZG

Theory

Tutorials

Schools

Acknowledgements

Papers using EPW

Contact

Source code

Download and Install

Code coverage

Accuracy

GitLab

Test Farm

Developers

Benchmarks

Developers

Developers meetings

Steering committee meetings

Website maintenance

Inputs for EPW
¶

List of inputs of EPW v6.0
¶

Structure of the input data
¶

title line

&inputepw
…

/
…

&inputepw
¶

A
 
a2f
, 
a2f_iso
, 
adapt_ethrdg_plrn
, 
ahc_nbnd
, 
ahc_nbndskip
, 
ahc_win_max
, 
ahc_win_min
, 
amass
, 
asr_typ
, 
assume_metal
, 
a_gap0

B
 
band_plot
, 
bands_skipped
, 
bfieldx, bfieldy, bfieldz
, 
bnd_cum
, 
broyden_beta
, 
broyden_ndim

C
 
cal_psir_plrn
, 
carrier
, 
calc_nelec_wann
, 
conv_thr_iaxis
, 
conv_thr_plrn
, 
conv_thr_racon
, 
conv_thr_raxis
, 
cumulant

D
 
degaussq
, 
degaussw
, 
delta_approx
, 
delta_qsmear
, 
delta_smear
, 
dvscf_dir
, 
do_CHBB
, 
do_tdbe
, 
dt_tdbe
, 
dph_tdbe
- [epw_inputs]
Back to Top

<
Page contents

>
Page contents:

Inputs for EPW

List of inputs of EPW v6.0

Structure of the input data

&inputepw

a2f

a2f_iso

ahc_nbnd

ahc_nbndskip

ahc_win_max

ahc_win_min

amass(:)

asr_typ

assume_metal

a_gap0

band_plot

bands_skipped

bfieldx,
 
bfieldy,
 
bfieldz

bnd_cum

broyden_beta

broyden_ndim

carrier

calc_nelec_wann

conv_thr_iaxis

conv_thr_racon

conv_thr_raxis

cumulant

degaussq

degaussw

delta_approx

delta_qsmear

delta_smear

dvscf_dir

do_CHBB

efermi_read

eig_read

elecselfen

elecselfen_type

eliashberg

elph

emax_coulomb

emin_coulomb

ep_coupling

epbwrite,
 
epbread

epexst

ephwrite

epmatkqread

eps_acoustic

epsiHEG

eps_cut_ir

epw_memdist

epwread

epwwrite

etf_mem

exciton

explrn

fbw

fermi_diff

fermi_energy

fermi_plot

fila2f

fildvscf

filirobj

filkf

filnscf_coul

filqf

filukk

filukq

fixsym

fsthick

gap_edge

gb_scattering

gb_only

gb_size

griddens

gridsamp

icoulomb

imag_read

int_mob

iterative_bte

iverbosity

ii_g

ii_scattering

ii_only

ii_lscreen

ii_partion

ii_charge

ii_n

ii_eda

kerread

kerwrite

kmaps

lacon

laniso

lifc

limag

lindabs

liso

lpade

lphase

lpolar

lreal

ltrans_crta
- [query] EPW inputs nk1 nk2 nk3 nq1 nq2 nq3 nkf1 nkf2 nkf3 nqf1 nqf2 nqf3
- [epw_inputs]
Back to Top

<
Page contents

>
Page contents:

Inputs for EPW

List of inputs of EPW v6.0

Structure of the input data

&inputepw

a2f

a2f_iso

ahc_nbnd

ahc_nbndskip

ahc_win_max

ahc_win_min

amass(:)

asr_typ

assume_metal

a_gap0

band_plot

bands_skipped

bfieldx,
 
bfieldy,
 
bfieldz

bnd_cum

broyden_beta

broyden_ndim

carrier

calc_nelec_wann

conv_thr_iaxis

conv_thr_racon

conv_thr_raxis

cumulant

degaussq

degaussw

delta_approx

delta_qsmear

delta_smear

dvscf_dir

do_CHBB

efermi_read

eig_read

elecselfen

elecselfen_type

eliashberg

elph

emax_coulomb

emin_coulomb

ep_coupling

epbwrite,
 
epbread

epexst

ephwrite

epmatkqread

eps_acoustic

epsiHEG

eps_cut_ir

epw_memdist

epwread

epwwrite

etf_mem

exciton

explrn

fbw

fermi_diff

fermi_energy

fermi_plot

fila2f

fildvscf

filirobj

filkf

filnscf_coul

filqf

filukk

filukq

fixsym

fsthick

gap_edge

gb_scattering

gb_only

gb_size

griddens

gridsamp

icoulomb

imag_read

int_mob

iterative_bte

iverbosity

ii_g

ii_scattering

ii_only

ii_lscreen

ii_partion

ii_charge

ii_n

ii_eda

kerread

kerwrite

kmaps

lacon

laniso

lifc

limag

lindabs

liso

lpade

lphase

lpolar

lreal

ltrans_crta
- [epw_inputs]
EPW
 
 | Inputs for EPW
 
 

|||

Quick search

Project

About

Releases

Documentation

Inputs for EPW

Inputs for ZG

Theory

Tutorials

Schools

Acknowledgements

Papers using EPW

Contact

Source code

Download and Install

Code coverage

Accuracy

GitLab

Test Farm

Developers

Benchmarks

Developers

Developers meetings

Steering committee meetings

Website maintenance

Inputs for EPW
¶

List of inputs of EPW v6.0
¶

Structure of the input data
¶

title line

&inputepw
…

/
…

&inputepw
¶

A
 
a2f
, 
a2f_iso
, 
adapt_ethrdg_plrn
, 
ahc_nbnd
, 
ahc_nbndskip
, 
ahc_win_max
, 
ahc_win_min
, 
amass
, 
asr_typ
, 
assume_metal
, 
a_gap0

B
 
band_plot
, 
bands_skipped
, 
bfieldx, bfieldy, bfieldz
, 
bnd_cum
, 
broyden_beta
, 
broyden_ndim

C
 
cal_psir_plrn
, 
carrier
, 
calc_nelec_wann
, 
conv_thr_iaxis
, 
conv_thr_plrn
, 
conv_thr_racon
, 
conv_thr_raxis
, 
cumulant

D
 
degaussq
, 
degaussw
, 
delta_approx
, 
delta_qsmear
, 
delta_smear
, 
dvscf_dir
, 
do_CHBB
, 
do_tdbe
, 
dt_tdbe
, 
dph_tdbe
- [query] EPW inputs nbndsub nbndskip proj num_iter degaussw fsthick efermi_read
- [epw_inputs]
Back to Top

<
Page contents

>
Page contents:

Inputs for EPW

List of inputs of EPW v6.0

Structure of the input data

&inputepw

a2f

a2f_iso

ahc_nbnd

ahc_nbndskip

ahc_win_max

ahc_win_min

amass(:)

asr_typ

assume_metal

a_gap0

band_plot

bands_skipped

bfieldx,
 
bfieldy,
 
bfieldz

bnd_cum

broyden_beta

broyden_ndim

carrier

calc_nelec_wann

conv_thr_iaxis

conv_thr_racon

conv_thr_raxis

cumulant

degaussq

degaussw

delta_approx

delta_qsmear

delta_smear

dvscf_dir

do_CHBB

efermi_read

eig_read

elecselfen

elecselfen_type

eliashberg

elph

emax_coulomb

emin_coulomb

ep_coupling

epbwrite,
 
epbread

epexst

ephwrite

epmatkqread

eps_acoustic

epsiHEG

eps_cut_ir

epw_memdist

epwread

epwwrite

etf_mem

exciton

explrn

fbw

fermi_diff

fermi_energy

fermi_plot

fila2f

fildvscf

filirobj

filkf

filnscf_coul

filqf

filukk

filukq

fixsym

fsthick

gap_edge

gb_scattering

gb_only

gb_size

griddens

gridsamp

icoulomb

imag_read

int_mob

iterative_bte

iverbosity

ii_g

ii_scattering

ii_only

ii_lscreen

ii_partion

ii_charge

ii_n

ii_eda

kerread

kerwrite

kmaps

lacon

laniso

lifc

limag

lindabs

liso

lpade

lphase

lpolar

lreal

ltrans_crta
- [epw_inputs]
EPW
 
 | Inputs for EPW
 
 

|||

Quick search

Project

About

Releases

Documentation

Inputs for EPW

Inputs for ZG

Theory

Tutorials

Schools

Acknowledgements

Papers using EPW

Contact

Source code

Download and Install

Code coverage

Accuracy

GitLab

Test Farm

Developers

Benchmarks

Developers

Developers meetings

Steering committee meetings

Website maintenance

Inputs for EPW
¶

List of inputs of EPW v6.0
¶

Structure of the input data
¶

title line

&inputepw
…

/
…

&inputepw
¶

A
 
a2f
, 
a2f_iso
, 
adapt_ethrdg_plrn
, 
ahc_nbnd
, 
ahc_nbndskip
, 
ahc_win_max
, 
ahc_win_min
, 
amass
, 
asr_typ
, 
assume_metal
, 
a_gap0

B
 
band_plot
, 
bands_skipped
, 
bfieldx, bfieldy, bfieldz
, 
bnd_cum
, 
broyden_beta
, 
broyden_ndim

C
 
cal_psir_plrn
, 
carrier
, 
calc_nelec_wann
, 
conv_thr_iaxis
, 
conv_thr_plrn
, 
conv_thr_racon
, 
conv_thr_raxis
, 
cumulant

D
 
degaussq
, 
degaussw
, 
delta_approx
, 
delta_qsmear
, 
delta_smear
, 
dvscf_dir
, 
do_CHBB
, 
do_tdbe
, 
dt_tdbe
, 
dph_tdbe

## Assumptions

- The EPW coarse and fine meshes are all set to 8x8x8 as a conservative carryover from the paper's reported 8x8x8 BSE convergence context.
- The EPW file enables elph, epbwrite, epwwrite, and wannierize because the paper explicitly uses EPW and Wannier90, but does not provide a ready-to-run EPW input block.
- The nbndsub value is set to 10 as a starter Wannier subspace placeholder based on the paper's 3 valence + 7 conduction BSE window.
- The proj(1) = 'random' setting is taken from the EPW input reference as the simplest starter projection choice.
- The degaussw and fsthick values are heuristic starter values, not paper-derived values.

## Unresolved Items

- The actual EPW Wannier subspace, projections, and frozen-window choices still need to be chosen from a trusted LiF workflow or convergence study.
- The exact EPW coarse and fine meshes should be confirmed against the phonon and interpolation setup used for the excitonic-polaron workflow.
- The exact dvscf_dir layout and whether additional EPW read/write flags are needed depends on how the QE and PH outputs are organized in the real workflow.

## Documentation Basis

- EPW input keywords: prefix, outdir, dvscf_dir, elph, epbwrite, epwwrite, wannierize, kmaps, nk1/nk2/nk3, nq1/nq2/nq3, nkf1/nkf2/nkf3, nqf1/nqf2/nqf3, nbndsub, nbndskip, proj(:), num_iter, degaussw, fsthick, efermi_read.
- Paper-derived values: EPW and Wannier90 are used, and the broader workflow reports an 8x8x8 converged BSE k-grid that is reused here as a conservative mesh hint.

## Overall Notes

Stage 5 uses manuals-store retrieval to ground EPW keyword choices, but this remains the most assumption-heavy starter file in the pipeline.
