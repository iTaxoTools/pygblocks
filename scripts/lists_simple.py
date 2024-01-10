from itaxotools.pygblocks import compute_mask, trim_sequences

sequences = [
    "--TTTNTTACTTTTTTT-ATT",
    "--TTTNTTACGTTTTTG-ATT",
    "--TTTNTTAGTTTTTTC-ATT",
]

print()

print("ORIGINAL SEQUENCES:")
for seq in sequences:
    print(seq)
print()

mask = compute_mask(sequences)
print("MASK:")
print(mask)
print()

trimmed_sequences = trim_sequences(sequences, mask)

print("TRIMMED SEQUENCES:")
for seq in trimmed_sequences:
    print(seq)
print()
