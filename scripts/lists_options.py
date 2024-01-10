from itaxotools.pygblocks import Options, compute_mask, trim_sequences

sequences = [
    "--TTTNNTACTTTTTTT-ATT",
    "--TTTNTTACGTTTTTG-ATT",
    "--TTTNTTAGTTTTTTC-ATT",
]

print()

print("ORIGINAL SEQUENCES:")
for seq in sequences:
    print(seq)
print()

options = Options(
    IS=2,  # Minimum Number Of Sequences For A Conserved Position
    FS=2,  # Minimum Number Of Sequences For A Flank Position
    CP=2,  # Maximum Number Of Contiguous Nonconserved Positions
    BL1=3,  # Minimum Length Of A Block, 1st iteration
    BL2=3,  # Minimum Length Of A Block, 2nd iteration
    GT=2,  # Maximum Number of Allowed Gaps For Any Position
    GC="N-",  # Definition of Gap Characters
)

mask = compute_mask(sequences, options, log=True)
print("MASK:")
print(mask)
print()

trimmed_sequences = trim_sequences(sequences, mask)

print("TRIMMED SEQUENCES:")
for seq in trimmed_sequences:
    print(seq)
print()
