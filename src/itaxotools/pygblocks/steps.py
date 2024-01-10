from collections import Counter
from itertools import groupby
from typing import Iterator

from .types import Block, ConservationDegree, GapCharacters, Options, PositionVerdict


def compute_mask(sequences: Iterator[str], options: Options = None, log=False) -> str:
    sequences = list(sequences)
    sequence_count = len(sequences)

    options = options or Options.default()
    options.update_from_sequence_count(sequence_count)

    _log_options(log, options)

    transposed = zip(*sequences)
    positions = [analyze_column(column, options) for column in transposed]
    gaps = [has_gaps for _, has_gaps in positions]
    groups = groupby(letter for letter, _ in positions)
    blocks = [Block(letter, sum(1 for _ in group)) for letter, group in groups]

    _log_gaps(log, gaps)

    _log_blocks(log, "starting blocks", blocks)

    blocks = reject_nonconserved_blocks(blocks, options)
    _log_blocks(log, "reject non-conserved", blocks)

    blocks = reject_all_flank_blocks(blocks)
    _log_blocks(log, "reject flanks", blocks)

    blocks = reject_short_blocks(blocks, options.BL1)
    _log_blocks(log, "reject short 1", blocks)

    blocks = reject_gaps_within_blocks(blocks, gaps)
    _log_blocks(log, "reject gaps", blocks)

    blocks = reject_short_blocks(blocks, options.BL2)
    _log_blocks(log, "reject short 2", blocks)

    return create_mask_from_blocks(blocks)


def _log_options(log: bool, options: Options) -> None:
    if not log:
        return
    print("OPTIONS:")
    for option, value in options.as_dict().items():
        print("-", option + ":", value)
    print()


def _log_gaps(log: bool, gaps: list[bool]) -> None:
    if not log:
        return
    print("DETECTED GAPS:")
    mask = "".join(GapCharacters.Gap if gap else GapCharacters.Any for gap in gaps)
    print(mask)
    print()


def _log_blocks(log: bool, title: str, blocks: list[Block]) -> None:
    if not log:
        return
    title = title.upper() + ":"
    mask = "".join(block.letter * block.length for block in blocks)
    print(title)
    print(mask)
    print()


def analyze_column(column: Iterator[str], options: Options) -> tuple[ConservationDegree, bool]:
    counter = Counter(column)
    counter, has_gaps = _check_for_gaps(counter, options)
    most_common = counter.most_common(1)
    if not most_common:
        return ConservationDegree.NonConserved, has_gaps
    conservation_degree = _get_conservation_degree(most_common[0][1], has_gaps, options)
    return conservation_degree, has_gaps


def _check_for_gaps(counter: Counter, options: Options) -> tuple[Counter, bool]:
    gaps = sum(counter[gap] for gap in options.GC)
    has_gaps = bool(gaps > options.GT)
    for gap in options.GC:
        del counter[gap]
    return counter, has_gaps


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


def reject_gaps_within_blocks(blocks: list[Block], gaps: list[bool]) -> list[Block]:
    return list(_reject_gaps_within_blocks(blocks, iter(gaps)))


def _reject_gaps_within_blocks(blocks: list[Block], gaps: Iterator[bool]) -> Iterator[Block]:
    for block in blocks:
        if block.letter == ConservationDegree.NonConserved:
            if any([next(gaps) for _ in range(block.length)]):
                yield Block(PositionVerdict.Rejected, block.length)
            else:
                yield block
        else:
            for _ in range(block.length):
                next(gaps)
            yield block


def create_mask_from_blocks(blocks: list[Block]) -> str:
    return "".join(_create_mask_from_blocks(blocks))


def _create_mask_from_blocks(blocks: list[Block]) -> Iterator[str]:
    for block in blocks:
        letter = PositionVerdict.Accepted
        if block.letter == PositionVerdict.Rejected:
            letter = PositionVerdict.Rejected
        for _ in range(block.length):
            yield letter


def trim_sequences(sequences: Iterator[str], mask: str) -> Iterator[str]:
    for sequence in sequences:
        yield trim_sequence(sequence, mask)


def trim_sequence(sequence: str, mask: str) -> str:
    filtered = filter(lambda c_m: c_m[1] != ".", zip(sequence, mask))
    return "".join(c for c, _ in filtered)
