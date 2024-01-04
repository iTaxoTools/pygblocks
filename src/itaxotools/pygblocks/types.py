from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import NamedTuple


@dataclass
class Options:
    # No support for similarity matrix

    IS: int  # Minimum Number Of Sequences For A Conserved Position
    FS: int  # Minimum Number Of Sequences For A Flank Position
    CP: int  # Maximum Number Of Contiguous Nonconserved Positions
    BL1: int  # Minimum Length Of A Block, 1st iteration
    BL2: int  # Minimum Length Of A Block, 2nd iteration

    GT: int = 0  # Maximum Number of Allowed Gaps For Any Position
    GC: str = "-"  # Definition of Gap Characters

    IS_percent: float = 0.50
    FS_percent: float = 0.85
    GT_percent: float = 0.00

    @classmethod
    def default(cls) -> Options:
        return cls(
            IS=0,
            FS=0,
            CP=8,
            BL1=10,
            BL2=10,
        )

    def update_from_sequence_count(self, count: int):
        self.IS = self.IS or round(count * self.IS_percent) + 1
        self.FS = self.FS or round(count * self.FS_percent)
        self.GT = self.GT or round(count * self.GT_percent)

    def as_dict(self):
        return asdict(self)


class ConservationDegree(StrEnum):
    NonConserved = "?"
    Conserved = "$"
    HighlyConserved = "@"


class PositionVerdict(StrEnum):
    Accepted = "#"
    Rejected = "."


class GapCharacters(StrEnum):
    Gap = "-"
    Any = "."


class Block(NamedTuple):
    letter: str
    length: int
