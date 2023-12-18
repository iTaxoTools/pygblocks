from itaxotools.pygblocks import trim_sequence, trim_sequences


def test_trim_basic():
    assert trim_sequence("ACGT", ".#.#") == "CT"


def test_trim_end_codon():
    assert trim_sequence("ACG*", ".#.*") == "C*"


def test_multiple():
    result = trim_sequences(
        [
            "ACGT",
            "TGCA",
        ],
        ".#.#",
    )
    assert list(result) == [
        "CT",
        "GA",
    ]
