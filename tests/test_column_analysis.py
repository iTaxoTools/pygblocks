from typing import Iterator, NamedTuple

import pytest

from itaxotools.pygblocks import (
    ConservationDegree,
    Options,
    analyze_column,
)


class ColumnTest(NamedTuple):
    letters: Iterator[str]
    conservation_degree: ConservationDegree
    has_gaps: bool
    IS: int
    FS: int

    @property
    def letter_chain(self) -> Iterator[str]:
        return (letter for letter in self.letters)


@pytest.mark.parametrize(
    "test",
    [
        ColumnTest("AAA-", ConservationDegree.NonConserved, True, 2, 3),
        ColumnTest("ACGT", ConservationDegree.NonConserved, False, 2, 3),
        ColumnTest("AACC", ConservationDegree.Conserved, False, 2, 3),
        ColumnTest("AAAC", ConservationDegree.HighlyConserved, False, 2, 3),
        ColumnTest("AAAA", ConservationDegree.HighlyConserved, False, 2, 3),
    ],
)
def test_column_analysis(test: ColumnTest):
    options = Options(IS=test.IS, FS=test.FS, CP=0, BL1=0, BL2=0)
    target = (test.conservation_degree, test.has_gaps)
    assert analyze_column(test.letter_chain, options) == target
