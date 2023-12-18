from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pytest

from itaxotools.pygblocks import Options, compute_mask, trim_sequences
from itaxotools.taxi2.sequences import SequenceHandler, Sequences

TEST_DATA_DIR = Path(__file__).parent / Path(__file__).stem


class FileTest(NamedTuple):
    input_filename: str
    output_filename: str
    mask_filename: str
    options_dict: dict[str, int | float]
    is_pir: bool = True

    @property
    def input_path(self) -> Path:
        return TEST_DATA_DIR / self.input_filename

    @property
    def output_path(self) -> Path:
        return TEST_DATA_DIR / self.output_filename

    @property
    def mask_path(self) -> Path:
        return TEST_DATA_DIR / self.mask_filename

    @property
    def options(self) -> Options:
        return Options(**self.options_dict)

    def validate(self) -> None:
        input_sequences = Sequences.fromPath(self.input_path, SequenceHandler.Fasta)
        output_sequences = Sequences.fromPath(self.output_path, SequenceHandler.Fasta)
        mask_sequences = Sequences.fromPath(self.mask_path, SequenceHandler.Fasta)

        if self.is_pir:
            # Files are in PIR format but we read as Fasta, so we need to remove
            # the ending codon (*) at the end of each sequence
            global_input = list(seq.seq[:-1] for seq in input_sequences)
            target_output = list(seq.seq[:-1] for seq in output_sequences)
            target_mask = next(iter(mask_sequences)).seq
            if target_mask.endswith("*"):
                target_mask = target_mask[:-1] + "."
        else:
            global_input = list(seq.seq for seq in input_sequences)
            target_output = list(seq.seq for seq in output_sequences)
            target_mask = next(iter(mask_sequences)).seq

        print("-" * 58)
        print("INPUT:")
        print("-" * 58)
        for sequence in global_input:
            print(sequence)

        # print("-" * 58)
        # print("TARGET OUTPUT:")
        # print("-" * 58)
        # for sequence in target_output:
        #     print(sequence)

        print("-" * 58)
        print()

        input = (sequence.seq for sequence in input_sequences)
        generated_mask = compute_mask(input, self.options, log=True)

        print("CREATED MASK:")
        print(generated_mask)

        print("TARGET MASK:")
        print(target_mask)

        assert generated_mask == target_mask

        generated_output = list(trim_sequences(global_input, generated_mask))

        for generated, target in zip(generated_output, target_output):
            print(generated)
            print(target)
            print("")

        assert generated_output == target_output


tests = [
    FileTest(
        "nad3.pir",
        "nad3.pir-gb",
        "nad3.pir-gbMask",
        dict(IS=0, FS=0, CP=8, BL1=0, BL2=10, IS_percent=0.50, FS_percent=0.85),
    ),
    FileTest(
        "nad5.pir",
        "nad5.pir-gb",
        "nad5.pir-gbMask",
        dict(IS=0, FS=0, CP=8, BL1=0, BL2=10, IS_percent=0.50, FS_percent=0.85),
    ),
    FileTest(
        "cox2.pir",
        "cox2.pir-gb",
        "cox2.pir-gbMask",
        dict(IS=0, FS=0, CP=8, BL1=0, BL2=10, IS_percent=0.50, FS_percent=0.85),
    ),
    FileTest(
        "cytb.pir",
        "cytb.pir-gb",
        "cytb.pir-gbMask",
        dict(IS=0, FS=0, CP=8, BL1=0, BL2=10, IS_percent=0.50, FS_percent=0.85),
    ),
    FileTest(
        "nad3.pir",
        "nad3.pir-gbv",
        "nad3.pir-gbvMask",
        dict(IS=0, FS=0, CP=1, BL1=0, BL2=3, IS_percent=0.50, FS_percent=0.85),
    ),
    FileTest(
        "nad5.pir",
        "nad5.pir-gbv",
        "nad5.pir-gbvMask",
        dict(IS=9, FS=9, CP=4, BL1=0, BL2=2, IS_percent=0, FS_percent=0),
    ),
    FileTest(
        "cox2.pir",
        "cox2.pir-gbv",
        "cox2.pir-gbvMask",
        dict(IS=9, FS=12, CP=0, BL1=0, BL2=2, IS_percent=0, FS_percent=0),
    ),
    FileTest(
        "cytb.pir",
        "cytb.pir-gbv",
        "cytb.pir-gbvMask",
        dict(IS=0, FS=0, CP=5, BL1=0, BL2=6, IS_percent=0.50, FS_percent=0.85),
    ),
    FileTest(
        "mafft.fas",
        "mafft.fas-gb",
        "mafft.fas-gbMask",
        dict(IS=0, FS=0, CP=8, BL1=0, BL2=10, IS_percent=0.50, FS_percent=0.85),
        is_pir=False,
    ),
]


@pytest.mark.parametrize("test", tests)
def test_files(test: FileTest) -> None:
    test.validate()
