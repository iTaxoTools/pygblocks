from itertools import groupby
from typing import NamedTuple

import pytest

from itaxotools.pygblocks.steps import reject_gaps_within_blocks
from itaxotools.pygblocks.types import Block, ConservationDegree, GapCharacters, PositionVerdict


class BlockTest(NamedTuple):
    before: list[Block]
    after: list[Block]
    gaps: list[bool]


def gaps_from_mask(mask: str) -> list[bool]:
    return [bool(letter == GapCharacters.Gap) for letter in mask]


def blocks_from_mask(mask: str) -> list[Block]:
    return [Block(k, sum(1 for _ in g)) for k, g in groupby(mask)]


tests = [
    BlockTest(
        [Block(PositionVerdict.Rejected, 1)],
        [Block(PositionVerdict.Rejected, 1)],
        [True],
    ),
    BlockTest(
        [Block(PositionVerdict.Rejected, 1)],
        [Block(PositionVerdict.Rejected, 1)],
        [False],
    ),
    BlockTest(
        [Block(ConservationDegree.HighlyConserved, 1)],
        [Block(ConservationDegree.HighlyConserved, 1)],
        [False],
    ),
    BlockTest(
        [Block(ConservationDegree.Conserved, 1)],
        [Block(ConservationDegree.Conserved, 1)],
        [False],
    ),
    BlockTest(
        [Block(ConservationDegree.NonConserved, 1)],
        [Block(ConservationDegree.NonConserved, 1)],
        [False],
    ),
    BlockTest(
        [Block(ConservationDegree.NonConserved, 1)],
        [Block(PositionVerdict.Rejected, 1)],
        [True],
    ),
    BlockTest(
        [Block(ConservationDegree.NonConserved, 3)],
        [Block(PositionVerdict.Rejected, 3)],
        [False, True, False],
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
        gaps_from_mask("-+++++++-++++++"),
    ),
    BlockTest(
        blocks_from_mask("@$???????$??@@??$@"),
        blocks_from_mask("@$.......$??@@??$@"),
        gaps_from_mask("..-------........."),
    ),
    BlockTest(
        blocks_from_mask("@$@@$?$$?$$??$$?$$??@"),
        blocks_from_mask("@$@@$.$$?$$??$$?$$??@"),
        gaps_from_mask(".....-..............."),
    ),
    BlockTest(
        blocks_from_mask("............@?$@@@@"),
        blocks_from_mask("............@?$@@@@"),
        gaps_from_mask(".....----.........."),
    ),
]


@pytest.mark.parametrize("test", tests)
def test_gap_rejection(test: BlockTest):
    print("BEFORE")
    for block in test.before:
        print(block)
    generated_blocks = reject_gaps_within_blocks(test.before, test.gaps)
    print("GENERATED")
    for block in generated_blocks:
        print(block)
    print("TARGET")
    for block in test.after:
        print(block)
    assert generated_blocks == test.after
