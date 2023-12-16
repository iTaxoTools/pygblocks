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

        # Files are in PIR format but we read as Fasta, so we need to remove
        # the ending codon (*) at the end of each sequence
        global_input = list(seq.seq[:-1] for seq in input_sequences)
        target_output = list(seq.seq[:-1] for seq in output_sequences)
        target_mask = next(iter(mask_sequences)).seq
        if target_mask.endswith("*"):
            target_mask = target_mask[:-1] + "."

        print("INPUT:".ljust(50, "-"))
        for sequence in global_input:
            print(sequence)

        print("OUTPUT:".ljust(50, "-"))
        for sequence in target_output:
            print(sequence)

        print("TARGET MASK:".ljust(50, "-"))
        print(target_mask)

        generated_mask = compute_mask(sequence.seq for sequence in input_sequences)
        print("CREATED MASK:".ljust(50, "-"))
        print(generated_mask)

        assert generated_mask == target_mask

        generated_output = list(trim_sequences(generated_mask, global_input))

        for generated, target in zip(generated_output, target_output):
            print(generated)
            print(target)
            print("")

        assert generated_output == target_output


tests = [
    FileTest("nad3.pir"),
]


@pytest.mark.parametrize("test", tests)
def test_files(test: FileTest) -> None:
    test.validate()
