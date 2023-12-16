from collections import Counter
from itertools import groupby
from typing import Iterator

from .types import Block, ConservationDegree, GapCharacters, Options, PositionVerdict


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

    blocks = reject_all_flank_blocks(blocks)

    blocks = reject_short_blocks(blocks, options.BL1)

    gaps = (has_gaps for _, has_gaps in positions)
    blocks = reject_gaps_within_blocks(blocks, gaps)

    blocks = reject_short_blocks(blocks, options.BL2)

    print("".join(c for c, _ in positions))
    raise NotImplementedError


def analyze_column(column: Iterator[str], options: Options) -> tuple[ConservationDegree, bool]:
    counter = Counter(column)
    has_gaps = GapCharacters.Gap in counter
    first_common, *others = counter.most_common(2)
    if first_common[0] == GapCharacters.Gap and others:
        first_common = others[0]
    conservation_degree = _get_conservation_degree(first_common[1], has_gaps, options)
    return (conservation_degree, has_gaps)


def _get_conservation_degree(count: int, has_gaps: bool, options: Options) -> ConservationDegree:
    if has_gaps:
        return ConservationDegree.NonConserved
    if count < options.IS:
        return ConservationDegree.NonConserved
    if count < options.FS:
        return ConservationDegree.Conserved
    return ConservationDegree.HighlyConserved


def reject_nonconserved_blocks(blocks: list[Block], options: Options) -> list[Block]:
    return [_reject_nonconserved_block(block, options.CP) for block in blocks]


def _reject_nonconserved_block(block: Block, threshold: int) -> Block:
    if block.letter == ConservationDegree.NonConserved:
        if block.length > threshold:
            return Block(PositionVerdict.Rejected, block.length)
    return block


def reject_all_flank_blocks(blocks: list[Block]) -> list[Block]:
    blocks = list(_reject_left_flank_blocks(blocks))
    blocks = list(_reject_left_flank_blocks(blocks[::-1]))
    return blocks[::-1]


def _reject_left_flank_blocks(blocks: list[Block]) -> Iterator[Block]:
    memory = None
    for block in blocks:
        if block.letter != ConservationDegree.HighlyConserved and memory == PositionVerdict.Rejected:
            memory = PositionVerdict.Rejected
            yield Block(PositionVerdict.Rejected, block.length)
        else:
            memory = block.letter
            yield block


def reject_short_blocks(blocks: list[Block], threshold: int) -> list[Block]:
    return list(_reject_short_blocks(blocks, threshold))


def _reject_short_blocks(blocks: list[Block], threshold: int) -> Iterator[Block]:
    memory: list[Block] = []
    for block in blocks:
        if block.letter == PositionVerdict.Rejected:
            yield from _reject_short_memorized_block(memory, threshold)
            memory = []
            yield block
        else:
            memory.append(block)
    yield from _reject_short_memorized_block(memory, threshold)


def _reject_short_memorized_block(memory: list[Block], threshold: int) -> Iterator[Block]:
    length = sum(b.length for b in memory)
    if 0 < length < threshold:
        yield Block(PositionVerdict.Rejected, length)
        memory = []
    else:
        yield from memory


def reject_gaps_within_blocks(blocks: list[Block], gaps: Iterator[bool]) -> list[Block]:
    return list(_reject_gaps_within_blocks(blocks, iter(gaps)))


def _reject_gaps_within_blocks(blocks: list[Block], gaps: Iterator[bool]) -> Iterator[Block]:
    for block in blocks:
        if block.letter == ConservationDegree.NonConserved:
            if any((next(gaps) for _ in range(block.length))):
                yield Block(PositionVerdict.Rejected, block.length)
            else:
                yield block
        else:
            for _ in range(block.length):
                next(gaps)
            yield block


def trim_sequences(mask: str, sequences: Iterator[str]) -> Iterator[str]:
    for sequence in sequences:
        yield trim_sequence(mask, sequence)


def trim_sequence(mask: str, sequence: str) -> str:
    filtered = filter(lambda c_m: c_m[1] != ".", zip(sequence, mask))
    return "".join(c for c, _ in filtered)
