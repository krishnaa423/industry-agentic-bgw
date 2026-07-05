# Stage 2 Report

This report checks the paper-store retrieval and structured extraction stage.

## Workflow Flags

- uses_dft: True
- uses_dfpt: True
- uses_epw: True
- uses_gw: True
- uses_bse: True

## Extracted Fields

### material
- status: found
- value: 'LiF'
- notes: Target material identified directly from the first-principles section.
- evidence:
```text
first-principles calculations of excitonic polarons for LiF
```

### study_goal
- status: found
- value: 'Perform first-principles calculations of excitonic and polaron properties in LiF using Quantum Espresso, EPW, Wannier90, and BerkeleyGW.'
- notes: Main objective of the computational workflow.
- evidence:
```text
The paper details DFT, DFPT, GW/BSE calculations, and electron-phonon coupling in LiF.
```

### dft_code
- status: found
- value: 'Quantum Espresso'
- notes: DFT software employed.
- evidence:
```text
The paper states the use of Quantum Espresso for DFT and DFPT calculations.
```

### xc_functional
- status: found
- value: 'PBE GGA'
- notes: Exchange-correlation functional used.
- evidence:
```text
The paper specifies the use of the PBE generalized-gradient approximation.
```

### pseudopotentials
- status: found
- value: 'Norm-conserving pseudopotentials'
- notes: Type of pseudopotentials used.
- evidence:
```text
The paper mentions the employment of norm-conserving pseudopotentials.
```

### pw_cutoff_ry
- status: found
- value: '100 Ry'
- notes: Plane-wave cutoff parsed directly from the paper.
- evidence:
```text
planewaves kinetic energy cutoff of 100 Ry
```

### scf_conv_thr_ry
- status: found
- value: '10^-12 Ry'
- notes: SCF threshold parsed directly from the paper.
- evidence:
```text
self-consistent calculations is 10 − 12 superscript 10 12 10^{-12} 10 start_POSTSUPERSCRIPT - 12 end_POSTSUPERSCRIPT Ry
```

### dfpt_conv_thr_ry2
- status: found
- value: '1e-14 Ry^2'
- notes: DFPT convergence threshold.
- evidence:
```text
The DFPT convergence threshold is 10^{-14} Ry^2.
```

### epw_code
- status: found
- value: 'EPW'
- notes: Software used for electron-phonon calculations.
- evidence:
```text
EPW is used to compute electron-phonon coupling matrix elements.
```

### wannier_code
- status: found
- value: 'Wannier90'
- notes: Software used for Wannier functions.
- evidence:
```text
Wannier90 is employed for charge density and displacement pattern visualization.
```

### gw_code
- status: found
- value: 'BerkeleyGW'
- notes: GW/BSE computational package.
- evidence:
```text
BerkeleyGW is used for GW/BSE calculations.
```

### dielectric_cutoff_ry
- status: found
- value: '10 Ry'
- notes: Dielectric cutoff parsed directly from the paper.
- evidence:
```text
dielectric matrix to 10 Ry
```

### sigma_valence_bands
- status: found
- value: '5'
- notes: Sigma/GW valence band count parsed from the self-energy setup sentence.
- evidence:
```text
include 5 valence bands and 195 conduction bands. To compute the self-energy
```

### sigma_conduction_bands
- status: found
- value: '195'
- notes: Sigma/GW conduction band count parsed from the self-energy setup sentence.
- evidence:
```text
include 5 valence bands and 195 conduction bands. To compute the self-energy
```

### sigma_self_energy_method
- status: found
- value: 'COHSEX approximation'
- notes: Method for self-energy calculation.
- evidence:
```text
The self-energy is computed using the COHSEX approximation.
```

### quasiparticle_gap_ev
- status: found
- value: '14.7 eV'
- notes: Quasiparticle gap parsed directly from the paper.
- evidence:
```text
band gap of 14.7 eV
```

### kernel_valence_bands
- status: found
- value: '3'
- notes: BSE kernel valence band count parsed directly from the paper.
- evidence:
```text
BSE kernel is constructed using 3 valence bands and 7 conduction bands
```

### kernel_conduction_bands
- status: found
- value: '7'
- notes: BSE kernel conduction band count parsed directly from the paper.
- evidence:
```text
BSE kernel is constructed using 3 valence bands and 7 conduction bands
```

### bse_k_grid
- status: found
- value: '8×8×8'
- notes: k-point grid for BSE calculations.
- evidence:
```text
The excitonic properties are computed on an 8×8×8 Brillouin zone grid.
```

### supercell_hint
- status: missing
- value: 'not specified'
- notes: No explicit supercell size provided.
- evidence:
```text
(none)
```

## Missing Items

- supercell_hint

## Overall Notes

This is a starter workflow summary based on the provided evidence; it does not include a full reproduction package.
