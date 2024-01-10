from typing import NamedTuple

import pytest

from itaxotools.pygblocks.steps import reject_short_blocks
from itaxotools.pygblocks.types import Block, ConservationDegree, PositionVerdict


class BlockTest(NamedTuple):
    before: list[Block]
    after: list[Block]
    BL: int


tests = [
    BlockTest(
        [Block(PositionVerdict.Rejected, 1)],
        [Block(PositionVerdict.Rejected, 1)],
        2,
    ),
    BlockTest(
        [Block(PositionVerdict.Rejected, 2)],
        [Block(PositionVerdict.Rejected, 2)],
        2,
    ),
    BlockTest(
        [Block(PositionVerdict.Rejected, 3)],
        [Block(PositionVerdict.Rejected, 3)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.NonConserved, 1)],
        [Block(PositionVerdict.Rejected, 1)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.NonConserved, 2)],
        [Block(ConservationDegree.NonConserved, 2)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.NonConserved, 3)],
        [Block(ConservationDegree.NonConserved, 3)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.Conserved, 1)],
        [Block(PositionVerdict.Rejected, 1)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.Conserved, 2)],
        [Block(ConservationDegree.Conserved, 2)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.Conserved, 3)],
        [Block(ConservationDegree.Conserved, 3)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.HighlyConserved, 1)],
        [Block(PositionVerdict.Rejected, 1)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.HighlyConserved, 2)],
        [Block(ConservationDegree.HighlyConserved, 2)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.HighlyConserved, 3)],
        [Block(ConservationDegree.HighlyConserved, 3)],
        2,
    ),
    BlockTest(
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.NonConserved, 2),
            Block(ConservationDegree.HighlyConserved, 3),
            Block(PositionVerdict.Rejected, 4),
        ],
        [
            Block(PositionVerdict.Rejected, 1),
            Block(PositionVerdict.Rejected, 5),
            Block(PositionVerdict.Rejected, 4),
        ],
        10,
    ),
    BlockTest(
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.NonConserved, 2),
            Block(ConservationDegree.HighlyConserved, 3),
            Block(PositionVerdict.Rejected, 4),
        ],
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.NonConserved, 2),
            Block(ConservationDegree.HighlyConserved, 3),
            Block(PositionVerdict.Rejected, 4),
        ],
        5,
    ),
    BlockTest(
        [
            Block(ConservationDegree.HighlyConserved, 1),
            Block(ConservationDegree.HighlyConserved, 2),
            Block(PositionVerdict.Rejected, 3),
            Block(ConservationDegree.HighlyConserved, 4),
            Block(ConservationDegree.HighlyConserved, 5),
            Block(PositionVerdict.Rejected, 6),
        ],
        [
            Block(PositionVerdict.Rejected, 3),
            Block(PositionVerdict.Rejected, 3),
            Block(ConservationDegree.HighlyConserved, 4),
            Block(ConservationDegree.HighlyConserved, 5),
            Block(PositionVerdict.Rejected, 6),
        ],
        5,
    ),
]


@pytest.mark.parametrize("test", tests)
def test_length_rejection(test: BlockTest):
    assert reject_short_blocks(test.before, test.BL) == test.after
