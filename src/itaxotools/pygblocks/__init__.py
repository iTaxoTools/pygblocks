from collections import Counter
from typing import Iterator

from .types import ConservationDegree, Options


def compute_blocks(sequences: Iterator[str], options: Options = None) -> str:
    sequences = list(sequences)
    sequence_count = len(sequences)
    # position_count = len(sequences[0])

    options = options or Options.default()
    options.update_from_sequence_count(sequence_count)

    transposed = zip(*sequences)
    data = [analyze_column(column, options) for column in transposed]

    print("".join(x for x, _ in data))
    raise NotImplementedError


def analyze_column(column: Iterator[str], options: Options) -> tuple[ConservationDegree, bool]:
    counter = Counter(column)
    has_gaps = "-" in counter
    first_common, *others = counter.most_common(2)
    if first_common[0] == "-" and others:
        first_common = others[0]
    conservation_degree = get_conservation_degree(first_common[1], has_gaps, options)
    return (conservation_degree, has_gaps)


def get_conservation_degree(count: int, has_gaps: bool, options: Options) -> ConservationDegree:
    if has_gaps:
        return ConservationDegree.NonConserved
    if count < options.IS:
        return ConservationDegree.NonConserved
    if count < options.FS:
        return ConservationDegree.Conserved
    return ConservationDegree.HighlyConserved


def trim_sequences(mask: str, sequences: Iterator[str]) -> Iterator[str]:
    for sequence in sequences:
        yield trim_sequence(mask, sequence)


def trim_sequence(mask: str, sequence: str) -> str:
    filtered = filter(lambda c_m: c_m[1] != ".", zip(sequence, mask))
    return "".join(c for c, _ in filtered)
