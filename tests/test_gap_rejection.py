from typing import Iterator, NamedTuple

import pytest

from itaxotools.pygblocks import (
    Block,
    ConservationDegree,
    GapCharacters,
    PositionVerdict,
    reject_gaps_within_blocks,
)


class BlockTest(NamedTuple):
    before: list[Block]
    after: list[Block]
    gaps: str

    @property
    def gap_chain(self) -> Iterator[bool]:
        for letter in self.gaps:
            yield (letter == GapCharacters.Gap)


tests = [
    BlockTest(
        [Block(PositionVerdict.Rejected, 1)],
        [Block(PositionVerdict.Rejected, 1)],
        "-",
    ),
    BlockTest(
        [Block(PositionVerdict.Rejected, 1)],
        [Block(PositionVerdict.Rejected, 1)],
        "+",
    ),
    BlockTest(
        [Block(ConservationDegree.HighlyConserved, 1)],
        [Block(ConservationDegree.HighlyConserved, 1)],
        "+",
    ),
    BlockTest(
        [Block(ConservationDegree.Conserved, 1)],
        [Block(ConservationDegree.Conserved, 1)],
        "+",
    ),
    BlockTest(
        [Block(ConservationDegree.NonConserved, 1)],
        [Block(ConservationDegree.NonConserved, 1)],
        "+",
    ),
    BlockTest(
        [Block(ConservationDegree.NonConserved, 1)],
        [Block(PositionVerdict.Rejected, 1)],
        "-",
    ),
    BlockTest(
        [Block(ConservationDegree.NonConserved, 3)],
        [Block(PositionVerdict.Rejected, 3)],
        "+-+",
    ),
    BlockTest(
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.NonConserved, 2),
            Block(ConservationDegree.Conserved, 3),
            Block(ConservationDegree.NonConserved, 4),
            Block(ConservationDegree.HighlyConserved, 5),
        ],
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.NonConserved, 2),
            Block(ConservationDegree.Conserved, 3),
            Block(PositionVerdict.Rejected, 4),
            Block(ConservationDegree.HighlyConserved, 5),
        ],
        "-+++++++-++++++",
    ),
]


@pytest.mark.parametrize("test", tests)
def test_gap_rejection(test: BlockTest):
    assert reject_gaps_within_blocks(test.before, test.gap_chain) == test.after
