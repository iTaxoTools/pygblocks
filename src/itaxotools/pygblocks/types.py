from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import NamedTuple


class ReprEnum(Enum):
    """
    Only changes the repr(), leaving str() and format() to the mixed-in type.
    """


class StrEnum(str, ReprEnum):
    """
    Enum where members are also (and must be) strings
    """

    def __new__(cls, *values):
        "values must already be of type `str`"
        if len(values) > 3:
            raise TypeError("too many arguments for str(): %r" % (values,))
        if len(values) == 1:
            # it must be a string
            if not isinstance(values[0], str):
                raise TypeError("%r is not a string" % (values[0],))
        if len(values) >= 2:
            # check that encoding argument is a string
            if not isinstance(values[1], str):
                raise TypeError("encoding must be a string, not %r" % (values[1],))
        if len(values) == 3:
            # check that errors argument is a string
            if not isinstance(values[2], str):
                raise TypeError("errors must be a string, not %r" % (values[2]))
        value = str(*values)
        member = str.__new__(cls, value)
        member._value_ = value
        return member

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Return the lower-cased version of the member name.
        """
        return name.lower()


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
