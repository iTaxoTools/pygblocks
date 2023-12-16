from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pytest

from itaxotools.pygblocks import compute_mask, trim_sequences
from itaxotools.taxi2.sequences import SequenceHandler, Sequences

TEST_DATA_DIR = Path(__file__).parent / Path(__file__).stem


class FileTest(NamedTuple):
    file_prefix: str

    @property
    def input_path(self) -> Path:
        return TEST_DATA_DIR / self.file_prefix

    @property
    def output_path(self) -> Path:
        return TEST_DATA_DIR / (self.file_prefix + "-gb")

    @property
    def mask_path(self) -> Path:
        return TEST_DATA_DIR / (self.file_prefix + "-gbMask")

    def validate(self) -> None:
        input_sequences = Sequences.fromPath(self.input_path, SequenceHandler.Fasta)
        output_sequences = Sequences.fromPath(self.output_path, SequenceHandler.Fasta)
        mask_sequences = Sequences.fromPath(self.mask_path, SequenceHandler.Fasta)

        print("INPUT:".ljust(50, "-"))
        for sequence in input_sequences:
            print(sequence)

        print("OUTPUT:".ljust(50, "-"))
        for sequence in output_sequences:
            print(sequence)

        print("TARGET MASK:".ljust(50, "-"))
        for sequence in mask_sequences:
            print(sequence.seq)

        mask = compute_mask(sequence.seq for sequence in input_sequences)

        print("CREATED MASK:".ljust(50, "-"))
        print(mask)

        assert mask == next(iter(mask_sequences)).seq

        results = trim_sequences(mask, (sequence.seq for sequence in output_sequences))
        assert list(results) == list(output_sequences)

        assert False


tests = [
    FileTest("nad3.pir"),
]


@pytest.mark.parametrize("test", tests)
def test_files(test: FileTest) -> None:
    test.validate()
