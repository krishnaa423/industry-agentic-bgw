# Stage 4 Report

This report checks the starter-file generation stage for dfpt.in, kernel.inp, and absorption.inp.

## File Checks

### dfpt.in
- status: ok
- missing_markers: none
- preview:
```text
LiF DFPT starter calculation
&INPUTPH
  prefix='LiF',
  outdir='tmp/',
  tr2_ph=1.0d-14,
  ldisp=.true.,
  nq1=8, nq2=8, nq3=8,
  fildyn='LiF.dyn',
  verbosity='high'
/

```

### kernel.inp
- status: ok
- missing_markers: none
- preview:
```text
screening_semiconductor
number_val_bands 3
number_cond_bands 7
use_wfn_hdf5
verbosity 1

```

### absorption.inp
- status: ok
- missing_markers: none
- preview:
```text
number_val_bands_fine 3
number_val_bands_coarse 3
number_cond_bands_fine 7
number_cond_bands_coarse 7
eqp_corrections
polarization 1 0 0
energy_resolution 0.10
gaussian_broadening
use_wfn_hdf5
verbosity 1

```

## Retrieved Context

- [query] Quantum Espresso INPUT_PH tr2_ph ldisp nq1 nq2 nq3 fildyn verbosity
- [qe_input_ph]
ph.x: input description

 Input File Description 

 Program:
 ph.x / PHonon / Quantum ESPRESSO
 (version: 7.5)

TABLE OF CONTENTS

INTRODUCTION

Line-of-input:
 
title_line

&INPUTPH

amass
 | 
outdir
 | 
prefix
 | 
niter_ph
 | 
tr2_ph
 | 
alpha_mix(niter)
 | 
nmix_ph
 | 
verbosity
 | 
reduce_io
 | 
max_seconds
 | 
dftd3_hess
 | 
fildyn
 | 
fildrho
 | 
fildvscf
 | 
epsil
 | 
lrpa
 | 
lnoloc
 | 
trans
 | 
lraman
 | 
lmultipole
 | 
eth_rps
 | 
eth_ns
 | 
dek
 | 
recover
 | 
low_directory_check
 | 
only_init
 | 
qplot
 | 
q2d
 | 
q_in_band_form
 | 
electron_phonon
 | 
el_ph_nsigma
 | 
el_ph_sigma
 | 
ahc_dir
 | 
ahc_nbnd
 | 
ahc_nbndskip
 | 
skip_upper
 | 
lshift_q
 | 
zeu
 | 
zue
 | 
elop
 | 
fpol
 | 
ldisp
 | 
nogg
 | 
asr
 | 
ldiag
 | 
lqdir
 | 
search_sym
 | 
nq1
 | 
nq2
 | 
nq3
 | 
nk1
 | 
nk2
 | 
nk3
 | 
k1
 | 
k2
 | 
k3
 | 
diagonalization
 | 
read_dns_bare
 | 
ldvscf_interpolate
 | 
wpot_dir
 | 
do_long_range
 | 
do_charge_neutral
 | 
start_irr
 | 
last_irr
 | 
nat_todo
 | 
modenum
 | 
start_q
 | 
last_q
 | 
dvscf_star
 | 
drho_star

Line-of-input:
 
 xq(1) xq(2) xq(3)
 

qPointsSpecs

nqs
 | 
xq1
 | 
xq2
 | 
xq3
 | 
nq

Line-of-input:
 
 atom(1) atom(2) ... atom(nat_todo)
- [qe_input_ph]
Line-of-input:
 
 xq(1) xq(2) xq(3)
 

qPointsSpecs

nqs
 | 
xq1
 | 
xq2
 | 
xq3
 | 
nq

Line-of-input:
 
 atom(1) atom(2) ... atom(nat_todo)
 

lmultipole
 | 
 
 ADDITIONAL INFORMATION 

INTRODUCTION

Input data format:
 { } = optional, [ ] = it depends, # = comment

Structure of the input data:

===============================================================================

title_line

&INPUTPH

 ...

/

[ xq(1) xq(2) xq(3) ] 
# if 
ldisp
 != .true. and 
qplot
 != .true.

[ nqs 
# if 
qplot
 == .true. 

 xq(1,i) xq(2,i) xq(3,1) nq(1)
 ...
 xq(1,nqs) xq(2,nqs) xq(3,nqs) nq(nqs) ]

[ atom(1) atom(2) ... atom(nat_todo) ] 
# if 
nat_todo
 was specified

 

 
 Line of input 
 

Syntax:

title_line
Â Â 

Description of items:

title_line

CHARACTER

Title of the job, i.e., a line that is reprinted on output.
 

[
Back to Top
]

 Namelist: 
&
INPUTPH

amass(i), i=1,ntyp

REAL

Default:

 0.0
 

Atomic mass [amu] of each atomic type.
If not specified, masses are read from data file.
 

[
Back to Top
]

outdir

CHARACTER

Default:

value of the 
ESPRESSO_TMPDIR
 environment variable if set;

 current directory ('./') otherwise
- [query] BerkeleyGW kernel keywords number_val_bands number_cond_bands screening_semiconductor use_wfn_hdf5
- [bgw_kernel_keywords]
use_wfn_hdf5
 

 wfn_hdf5_min_band_block [integer]
 

 no_symmetries_coarse_grid
 

 use_symmetries_coarse_grid
 

 write_vcoul
 

 low_comm
 

 low_memory
 

 high_memory
 

 fullbz_replace
 

 fullbz_write
 

 die_outside_sphere
 

 ignore_outside_sphere
 

 read_kpoints
 

 extended_kernel
 

 exciton_Q_shift
 

 energy_loss
 

 dont_check_norms
 

Kernel
 code input keywords (
kernel.inp
)

Required keywords

number_cond_bands [integer]

number_val_bands [integer]

Optional keywords

bare_coulomb_cutoff [float]

cell_box_truncation

cell_slab_truncation

cell_wire_truncation

coulomb_truncation_radius [float]

die_outside_sphere

dont_check_norms

dont_use_hdf5

energy_loss

exciton_Q_shift

extended_kernel

fermi_level [float]

fermi_level_absolute

fermi_level_relative

fullbz_replace

fullbz_write

g_sum_algo

high_memory

ignore_outside_sphere

low_comm

low_memory

mtxel_algo

n_ffts_per_batch [integer]

no_symmetries_coarse_grid

read_kpoints

screened_coulomb_cutoff [float]

screening_graphene

screening_metal

screening_semiconductor

spherical_truncation

use_symmetries_coarse_grid

use_wfn_hdf5

verbosity [integer]

w_sum_algo

wfn_hdf5_min_band_block [integer]
- [bgw_absorption_keywords]
screening_graphene

screening_metal

screening_semiconductor

skip_interpolation

spherical_truncation

spin_singlet

spin_triplet

spinor

spline_scissors

subsample_algo [integer]

subsample_line

unrestricted_transformation

use_dos

use_elpa

use_momentum

use_symmetries_coarse_grid

use_symmetries_fine_grid

use_symmetries_shifted_grid

use_velocity

use_wfn_hdf5

verbosity [integer]

voigt_broadening

wfn_hdf5_min_band_block [integer]

write_eigenvectors

write_vcoul

zero_coupling_block

zero_q0_element

zero_unrestricted_contribution

Keyword documentation

Band occupation

In metallic systems, PARATEC often outputs incorrect occupation
levels in wavefunctions. Use this to override these values.
lowest_occupied_band should be 1 unless you have some very
exotic situation.

lowest_occupied_band

highest_occupied_band

Screening type

How does the screening of the system behaves? (default=
screening_semiconductor
)
BerkeleyGW uses this information to apply a different numerical
procedure to computing the diverging 
q\rightarrow 0
 contribution
to the screened Coulomb potential 
W_{GG'}(q)
.
These models are not used in Hartree-Fock calculations.

screening_semiconductor
- [query] BerkeleyGW absorption keywords number_val_bands_fine number_cond_bands_fine polarization energy_resolution gaussian_broadening
- [bgw_kernel_keywords]
Misc. parameters
 

 number_val_bands [integer]
 

 number_cond_bands [integer]
 

 screened_coulomb_cutoff [float]
 

 bare_coulomb_cutoff [float]
 

 fermi_level [float]
 

 fermi_level_absolute
 

 fermi_level_relative
 

 dont_use_hdf5
 

 verbosity [integer]
 

 use_wfn_hdf5
 

 wfn_hdf5_min_band_block [integer]
 

 no_symmetries_coarse_grid
 

 use_symmetries_coarse_grid
 

 write_vcoul
 

 low_comm
 

 low_memory
 

 high_memory
 

 fullbz_replace
 

 fullbz_write
 

 die_outside_sphere
 

 ignore_outside_sphere
 

 read_kpoints
 

 extended_kernel
 

 exciton_Q_shift
 

 energy_loss
 

 dont_check_norms
 

 Absorption code
 

 Absorption code
 

 Overview
 

 Input keywords (absorption.inp)
 

 Utilities
 

 Utilities
 

 summarize_eigenvectors
 

 PlotXct
 

 PlotXct
 

 Overview
 

 Input keywords (plotxct.inp)
 

 Magnetic/Spin properties
 

 Magnetic/Spin properties
 

 Exciton magnetic moment
 

 Circular polarized absorption
 

 Inteqp code
 

 Inteqp code
 

 Overview
 

 Input keywords (inteqp.inp)
 

 Subsampling
 

 Subsampling
 

 Overview
 

 NNS
 

 CSI
 

 NonlinearOptics
 

 NonlinearOptics
 

 Overview
 

 Input keywords (nonlinearoptics.inp)
- [bgw_absorption_keywords]
dont_use_elpa
 

 exciton_Q_shift
 

 average_w
 

 kernel_scaling [float]
 

 zero_coupling_block
 

 unrestricted_transformation
 

 zero_unrestricted_contribution
 

 zero_q0_element
 

 dump_bse_hamiltonian
 

 read_bse_hamiltonian
 

 dont_check_norms
 

Absorption
 code input keywords (
absorption.inp
)

Required keywords

energy_resolution [float]

number_cond_bands_coarse [integer]

number_cond_bands_fine [integer]

number_val_bands_coarse [integer]

number_val_bands_fine [integer]

Optional keywords

average_w

avgpot [float]

cell_average_cutoff [float]

cell_box_truncation

cell_slab_truncation

cell_wire_truncation

coulomb_truncation_radius [float]

cvfit [array of integers]

degeneracy_check_override

delaunay_interpolation

delta_frequency [float]

diagonalization

diagonalization_primme

dont_check_norms

dont_use_elpa

dont_use_hdf5

dont_use_hdf5_output

dump_bse_hamiltonian

ec0 [float]

ecdel [float]

ecs [float]

energy_resolution_gamma [float]

energy_resolution_sigma [float]

eqp_co_corrections

eqp_corrections

ev0 [float]

evdel [float]

evs [float]

exciton_Q_shift

extended_kernel

fermi_level [float]

fermi_level_absolute

fermi_level_relative

## Assumptions

- The DFPT q-grid is set to 8x8x8 as a conservative carryover from the paper's converged BSE Brillouin-zone grid.
- The DFPT file omits material-specific masses and dielectric-response flags because the retrieved evidence does not pin down those exact settings.
- The kernel file uses the paper's 3 valence and 7 conduction bands directly.
- The absorption file uses the same 3/7 band window on both coarse and fine grids as a starter assumption.
- The absorption polarization is set to 1 0 0 as a placeholder because the paper does not specify polarization direction in input-file terms.
- The absorption energy_resolution value 0.10 is a heuristic, not a paper-derived value.

## Unresolved Items

- The exact DFPT q-grid, irreducible-q setup, and whether epsil should be enabled still need confirmation from a trusted working example.
- The exact absorption polarization and broadening settings should be confirmed against the target spectrum setup.
- The exact kernel/absorption interpolation and exciton-Q settings still need confirmation from a trusted BerkeleyGW example.

## Documentation Basis

- QE INPUT_PH keywords: prefix, tr2_ph, fildyn, ldisp, nq1, nq2, nq3, verbosity.
- BerkeleyGW kernel keywords: number_val_bands, number_cond_bands, screening_semiconductor, use_wfn_hdf5, verbosity.
- BerkeleyGW absorption keywords: number_val_bands_fine/coarse, number_cond_bands_fine/coarse, eqp_corrections, polarization, energy_resolution, gaussian_broadening, use_wfn_hdf5, verbosity.
- Paper-derived values: DFPT threshold 10^-14 Ry^2, kernel bands 3/7, BSE convergence on an 8x8x8 Brillouin-zone grid.

## Overall Notes

Stage 4 uses manuals-store retrieval for keyword grounding and Stage 2 paper values for the quantitative starter choices.
