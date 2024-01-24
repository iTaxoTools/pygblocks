# PyGblocks

[![PyPI - Version](https://img.shields.io/pypi/v/itaxotools-pygblocks)](
    https://pypi.org/project/itaxotools-pygblocks)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/itaxotools-pygblocks)](
    https://pypi.org/project/itaxotools-pygblocks)
[![GitHub - Tests](https://img.shields.io/github/actions/workflow/status/iTaxoTools/pygblocks/test.yml?label=tests)](
    https://github.com/iTaxoTools/pygblocks/actions/workflows/test.yml)

Pure Python implementation for the algorithm behind Gblocks.

## Differences

- Can define which characters are considered as gaps
- Any character that is not defined as a gap is considered for conservation
- Can define how many gaps are allowed per position (number or percentage)
- Positions that only contain gaps are not pre-emptively removed
- Conservation threshold may be set below 50%
- No support for similarity matrices

## Installation

PyGblocks is available on PyPI. You can install it through `pip`:

```
pip install itaxotools-pygblocks
```

## Usage

First create a mask from your sequences, then apply that mask to each sequence:

```
from itaxotools.pygblocks import compute_mask, trim_sequences

sequences = [
    "--TTTNNTACTTTTTTT-ATT",
    "--TTTNTTACGTTTTTG-ATT",
    "--TTTNTTAGTTTTTTC-ATT",
]

mask = compute_mask(sequences)
trimmed_sequences = trim_sequences(sequences, mask)
```

You may customize the trimming parameters and enable logging
when creating the mask:

```
from itaxotools.pygblocks import Options, compute_mask

options = Options(
    IS=2,    # Minimum Number Of Sequences For A Conserved Position
    FS=3,    # Minimum Number Of Sequences For A Flank Position
    CP=2,    # Maximum Number Of Contiguous Nonconserved Positions
    BL1=3,   # Minimum Length Of A Block, 1st iteration
    BL2=3,   # Minimum Length Of A Block, 2nd iteration
    GT=2,    # Maximum Number of Allowed Gaps For Any Position
    GC="-",  # Definition of Gap Characters
)

mask = compute_mask(sequences, options, log=True)
```

You may optionally set IS, FS and GT as a percentage of the number of sequences
by setting IS, FS and GT values to zero, then modifying the percentage
defaults if desired:

```
options = Options(
    IS=0, FS=0, CP=2, BL1=3, BL2=3, GT=0, GC="-",

    IS_percent = 0.50
    FS_percent = 0.85
    GT_percent = 0.00
)

mask = compute_mask(sequences, options, log=True)
```

You may find the above examples, plus some examples on how to use PyGblocks
with BioPython alignments, in the [scripts](scripts) folder.

# Citations

Castresana J. Selection of conserved blocks from multiple alignments for their use in phylogenetic analysis.
Mol Biol Evol. 2000 Apr;17(4):540-52. doi: 10.1093/oxfordjournals.molbev.a026334. PMID: 10742046.
