from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pytest

from itaxotools.pygblocks import compute_blocks, trim_sequences
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

        print("MASK:".ljust(50, "-"))
        for sequence in mask_sequences:
            print(sequence)

        mask = compute_blocks(sequence.seq for sequence in input_sequences)
        assert mask == next(mask_sequences).seq

        results = trim_sequences(mask, (sequence.seq for sequence in output_sequences))
        assert list(results) == list(output_sequences)

        assert False


@pytest.mark.parametrize(
    "test",
    [
        FileTest("nad3.pir"),
    ],
)
def test_files(test: FileTest) -> None:
    test.validate()
