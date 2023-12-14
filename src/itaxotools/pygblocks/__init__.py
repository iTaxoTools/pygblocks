from collections import Counter
from typing import Iterator


def compute_blocks(sequences: Iterator[str]) -> str:
    transposed = zip(*sequences)
    most_common = [Counter(column).most_common(1)[0] for column in transposed]
    print(most_common)
    raise NotImplementedError


def trim_sequences(mask: str, sequences: Iterator[str]) -> Iterator[str]:
    for sequence in sequences:
        yield trim_sequence(mask, sequence)


def trim_sequence(mask: str, sequence: str) -> str:
    filtered = filter(lambda c_m: c_m[1] != ".", zip(sequence, mask))
    return "".join(c for c, _ in filtered)
