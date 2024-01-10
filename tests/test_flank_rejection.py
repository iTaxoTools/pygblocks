from typing import NamedTuple

import pytest

from itaxotools.pygblocks.steps import reject_all_flank_blocks
from itaxotools.pygblocks.types import Block, ConservationDegree, PositionVerdict


class BlockTest(NamedTuple):
    before: list[Block]
    after: list[Block]


tests = [
    BlockTest(
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.NonConserved, 2),
            Block(ConservationDegree.Conserved, 3),
            Block(ConservationDegree.HighlyConserved, 4),
        ],
        [
            Block(PositionVerdict.Rejected, 1),
            Block(PositionVerdict.Rejected, 2),
            Block(PositionVerdict.Rejected, 3),
            Block(ConservationDegree.HighlyConserved, 4),
        ],
    ),
    BlockTest(
        [
            Block(ConservationDegree.HighlyConserved, 4),
            Block(ConservationDegree.Conserved, 3),
            Block(ConservationDegree.NonConserved, 2),
            Block(PositionVerdict.Rejected, 1),
        ],
        [
            Block(ConservationDegree.HighlyConserved, 4),
            Block(PositionVerdict.Rejected, 3),
            Block(PositionVerdict.Rejected, 2),
            Block(PositionVerdict.Rejected, 1),
        ],
    ),
    BlockTest(
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.HighlyConserved, 2),
            Block(ConservationDegree.Conserved, 3),
            Block(ConservationDegree.HighlyConserved, 4),
            Block(PositionVerdict.Rejected, 5),
        ],
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.HighlyConserved, 2),
            Block(ConservationDegree.Conserved, 3),
            Block(ConservationDegree.HighlyConserved, 4),
            Block(PositionVerdict.Rejected, 5),
        ],
    ),
    BlockTest(
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.HighlyConserved, 2),
            Block(ConservationDegree.Conserved, 3),
            Block(PositionVerdict.Rejected, 4),
        ],
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.HighlyConserved, 2),
            Block(PositionVerdict.Rejected, 3),
            Block(PositionVerdict.Rejected, 4),
        ],
    ),
    BlockTest(
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.Conserved, 2),
            Block(ConservationDegree.HighlyConserved, 3),
            Block(PositionVerdict.Rejected, 4),
        ],
        [
            Block(PositionVerdict.Rejected, 1),
            Block(PositionVerdict.Rejected, 2),
            Block(ConservationDegree.HighlyConserved, 3),
            Block(PositionVerdict.Rejected, 4),
        ],
    ),
    BlockTest(
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.HighlyConserved, 2),
            Block(ConservationDegree.NonConserved, 3),
            Block(PositionVerdict.Rejected, 4),
        ],
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.HighlyConserved, 2),
            Block(PositionVerdict.Rejected, 3),
            Block(PositionVerdict.Rejected, 4),
        ],
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
            Block(PositionVerdict.Rejected, 2),
            Block(ConservationDegree.HighlyConserved, 3),
            Block(PositionVerdict.Rejected, 4),
        ],
    ),
    BlockTest(
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.HighlyConserved, 2),
            Block(ConservationDegree.NonConserved, 3),
            Block(PositionVerdict.Rejected, 4),
            Block(ConservationDegree.Conserved, 5),
            Block(ConservationDegree.HighlyConserved, 6),
            Block(ConservationDegree.NonConserved, 7),
            Block(ConservationDegree.HighlyConserved, 8),
            Block(PositionVerdict.Rejected, 9),
        ],
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.HighlyConserved, 2),
            Block(PositionVerdict.Rejected, 3),
            Block(PositionVerdict.Rejected, 4),
            Block(PositionVerdict.Rejected, 5),
            Block(ConservationDegree.HighlyConserved, 6),
            Block(ConservationDegree.NonConserved, 7),
            Block(ConservationDegree.HighlyConserved, 8),
            Block(PositionVerdict.Rejected, 9),
        ],
    ),
]


@pytest.mark.parametrize("test", tests)
def test_flank_rejection(test: BlockTest):
    assert reject_all_flank_blocks(test.before) == test.after
