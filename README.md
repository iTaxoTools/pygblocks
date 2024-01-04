# PyGblocks

Python implementation for Gblocks.

# Differences

- Can define which characters are considered as gaps
- Any character that is not defined as gap is considered for conservation
- Can define how many gaps are allowed per position (number or percentage)
- Positions that only contain gaps are not pre-emptively removed
- Conservation threshold may be set below 50%
- No support for similarity matrices

# Citations

Castresana J. Selection of conserved blocks from multiple alignments for their use in phylogenetic analysis.
Mol Biol Evol. 2000 Apr;17(4):540-52. doi: 10.1093/oxfordjournals.molbev.a026334. PMID: 10742046.
