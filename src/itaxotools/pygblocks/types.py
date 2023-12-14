from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


@dataclass
class Options:
    # No support for similarity matrix or gap positions
    IS: int  # Minimum Number Of Sequences For A Conserved Position
    FS: int  # Minimum Number Of Sequences For A Flank Position
    CP: int  # Maximum Number Of Contiguous Nonconserved Positions
    BL1: int  # Minimum Length Of A Block, 1st iteration
    BL2: int  # Minimum Length Of A Block, 2nd iteration

    IS_percent: float = 0.50
    FS_percent: float = 0.85

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


class ConservationDegree(StrEnum):
    NonConserved = "?"
    Conserved = "$"
    HighlyConserved = "@"
