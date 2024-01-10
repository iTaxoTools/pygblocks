from typing import Iterator, NamedTuple

import pytest

from itaxotools.pygblocks.steps import analyze_column
from itaxotools.pygblocks.types import ConservationDegree, Options


class ColumnTest(NamedTuple):
    letters: Iterator[str]
    conservation_degree: ConservationDegree
    has_gaps: bool
    IS: int
    FS: int
    GT: int
    GC: str

    @property
    def letter_chain(self) -> Iterator[str]:
        return (letter for letter in self.letters)


tests = [
    ColumnTest("AAA-", ConservationDegree.NonConserved, True, 2, 3, 0, "-"),
    ColumnTest("ACGT", ConservationDegree.NonConserved, False, 2, 3, 0, "-"),
    ColumnTest("AACC", ConservationDegree.Conserved, False, 2, 3, 0, "-"),
    ColumnTest("AAAC", ConservationDegree.HighlyConserved, False, 2, 3, 0, "-"),
    ColumnTest("AAAA", ConservationDegree.HighlyConserved, False, 2, 3, 0, "-"),
    ColumnTest("AAC-", ConservationDegree.Conserved, False, 2, 3, 0, "?"),
    ColumnTest("AAC?", ConservationDegree.NonConserved, True, 2, 3, 0, "?"),
    ColumnTest("AACN", ConservationDegree.NonConserved, True, 2, 3, 0, "N"),
    ColumnTest("----", ConservationDegree.NonConserved, True, 2, 3, 0, "-"),
    ColumnTest("----", ConservationDegree.NonConserved, True, 2, 3, 2, "-"),
    ColumnTest("----", ConservationDegree.NonConserved, False, 2, 3, 4, "-"),
    ColumnTest("N?--", ConservationDegree.NonConserved, True, 2, 3, 0, "N?-"),
    ColumnTest("N?--", ConservationDegree.NonConserved, False, 2, 3, 4, "N?-"),
    ColumnTest("N?-A", ConservationDegree.Conserved, False, 1, 2, 4, "N?-"),
    ColumnTest("N?-A", ConservationDegree.HighlyConserved, False, 1, 1, 4, "N?-"),
    ColumnTest("ACG-", ConservationDegree.NonConserved, False, 2, 3, 1, "-"),
    ColumnTest("AAG-", ConservationDegree.Conserved, False, 2, 3, 1, "-"),
]


@pytest.mark.parametrize("test", tests)
def test_column_analysis(test: ColumnTest):
    options = Options(IS=test.IS, FS=test.FS, CP=0, BL1=0, BL2=0, GT=test.GT, GC=test.GC)
    target = (test.conservation_degree, test.has_gaps)
    assert analyze_column(test.letter_chain, options) == target
