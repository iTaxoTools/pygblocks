from typing import NamedTuple

import pytest

from itaxotools.pygblocks.steps import create_mask_from_blocks
from itaxotools.pygblocks.types import Block, ConservationDegree, PositionVerdict


class MaskTest(NamedTuple):
    blocks: list[Block]
    mask: str


tests = [
    MaskTest(
        [Block(PositionVerdict.Rejected, 1)],
        ".",
    ),
    MaskTest(
        [Block(PositionVerdict.Rejected, 3)],
        "...",
    ),
    MaskTest(
        [Block(ConservationDegree.NonConserved, 1)],
        "#",
    ),
    MaskTest(
        [Block(ConservationDegree.NonConserved, 3)],
        "###",
    ),
    MaskTest(
        [Block(ConservationDegree.Conserved, 1)],
        "#",
    ),
    MaskTest(
        [Block(ConservationDegree.Conserved, 3)],
        "###",
    ),
    MaskTest(
        [Block(ConservationDegree.HighlyConserved, 1)],
        "#",
    ),
    MaskTest(
        [Block(ConservationDegree.HighlyConserved, 3)],
        "###",
    ),
    MaskTest(
        [
            Block(PositionVerdict.Rejected, 1),
            Block(ConservationDegree.NonConserved, 2),
            Block(PositionVerdict.Rejected, 3),
            Block(ConservationDegree.Conserved, 4),
            Block(ConservationDegree.HighlyConserved, 5),
        ],
        "." + "#" * 2 + "." * 3 + "#" * 4 + "#" * 5,
    ),
]


@pytest.mark.parametrize("test", tests)
def test_mask_Creation(test: MaskTest):
    assert create_mask_from_blocks(test.blocks) == test.mask
