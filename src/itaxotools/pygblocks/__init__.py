from collections import Counter
from itertools import groupby
from typing import Iterator

from .types import Block, ConservationDegree, Options, PositionVerdict


def compute_blocks(sequences: Iterator[str], options: Options = None) -> str:
    sequences = list(sequences)
    sequence_count = len(sequences)
    # position_count = len(sequences[0])

    options = options or Options.default()
    options.update_from_sequence_count(sequence_count)

    transposed = zip(*sequences)
    positions = [analyze_column(column, options) for column in transposed]

    groups = groupby(letter for letter, _ in positions)
    blocks = [Block(letter, sum(1 for _ in group)) for letter, group in groups]

    blocks = reject_nonconserved_blocks(blocks, options)

    # print("OONE")
    # for block in blocks:
    #     print(block)

    # blocks = reject_all_flank_blocks(blocks)

    # print("TTWO")
    # for block in blocks:
    #     print(block)

    print("".join(c for c, _ in positions))
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


def reject_nonconserved_blocks(blocks: list[Block], options: Options) -> list[Block]:
    return [reject_nonconserved_block(block, options.CP) for block in blocks]


def reject_nonconserved_block(block: Block, threshold: int) -> Block:
    if block.letter == ConservationDegree.NonConserved:
        if block.length > threshold:
            return Block(PositionVerdict.Rejected, block.length)
    return block


def reject_all_flank_blocks(blocks: list[Block]) -> list[Block]:
    blocks = list(reject_left_flank_blocks(blocks))
    blocks = list(reject_left_flank_blocks(blocks[::-1]))
    return blocks[::-1]


def reject_left_flank_blocks(blocks: list[Block]) -> Iterator[Block]:
    memory = None
    for block in blocks:
        if block.letter != ConservationDegree.HighlyConserved and memory == PositionVerdict.Rejected:
            memory = PositionVerdict.Rejected
            yield Block(PositionVerdict.Rejected, block.length)
        else:
            memory = block.letter
            yield block


def trim_sequences(mask: str, sequences: Iterator[str]) -> Iterator[str]:
    for sequence in sequences:
        yield trim_sequence(mask, sequence)


def trim_sequence(mask: str, sequence: str) -> str:
    filtered = filter(lambda c_m: c_m[1] != ".", zip(sequence, mask))
    return "".join(c for c, _ in filtered)
