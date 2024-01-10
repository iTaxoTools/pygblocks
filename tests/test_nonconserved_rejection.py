from typing import NamedTuple

import pytest

from itaxotools.pygblocks.steps import reject_nonconserved_blocks
from itaxotools.pygblocks.types import Block, ConservationDegree, Options, PositionVerdict


class BlockTest(NamedTuple):
    before: list[Block]
    after: list[Block]
    CP: int


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
        [Block(ConservationDegree.NonConserved, 1)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.NonConserved, 2)],
        [Block(ConservationDegree.NonConserved, 2)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.NonConserved, 3)],
        [Block(PositionVerdict.Rejected, 3)],
        2,
    ),
    BlockTest(
        [Block(ConservationDegree.Conserved, 1)],
        [Block(ConservationDegree.Conserved, 1)],
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
        [Block(ConservationDegree.HighlyConserved, 1)],
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
            Block(ConservationDegree.HighlyConserved, 1),
            Block(ConservationDegree.NonConserved, 3),
            Block(ConservationDegree.Conserved, 3),
            Block(ConservationDegree.NonConserved, 1),
        ],
        [
            Block(ConservationDegree.HighlyConserved, 1),
            Block(PositionVerdict.Rejected, 3),
            Block(ConservationDegree.Conserved, 3),
            Block(ConservationDegree.NonConserved, 1),
        ],
        2,
    ),
]


@pytest.mark.parametrize("test", tests)
def test_nonconserved_rejection(test: BlockTest):
    options = Options(IS=0, FS=0, CP=test.CP, BL1=0, BL2=0)
    assert reject_nonconserved_blocks(test.before, options) == test.after
