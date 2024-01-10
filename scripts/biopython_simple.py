from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from itaxotools.pygblocks import compute_mask, trim_sequence

# Create a MultipleSeqAlignment object manually
# Alternatively, read from a file using AlignIO.read
alignment = MultipleSeqAlignment(
    [
        SeqRecord(Seq("------MEYLLQEYLPILVFLGMASA--PDPEKVSAYFNAFD-DVAFWGLMVFLAVLTVGKGALEWA-------"), id="id1"),
        SeqRecord(Seq("---------MTLEYIYIFIFFWGAFF--SDIEKNSAYFQPFE-FFGVWAIFLFLIILTVGKGALEWD-------"), id="id2"),
        SeqRecord(Seq("--------------MTYLVYIVFTIV--PDSEKVSAYFSPLG-LLGGWITIIFLVILTIGSGAITDSF------"), id="id3"),
        SeqRecord(Seq("-----------IFNFLTLFVSILIFL-TD-SEKSSPYFDPLN-P--IHTP----LILTVGQGGLDWAE------"), id="id4"),
        SeqRecord(Seq("---------MMSEFAPISIYLVISLL-STYPEKLSAYFDPSG-LFGFWSMMAFLFILTIGRGASDRE-------"), id="id5"),
        SeqRecord(Seq("-------------MNSFLIYLLIAIT-MD-QEKLSPYFDPQA-QLSFTLAFLILLILTIGEGGLEWAE------"), id="id6"),
    ]
)

print()

print("ORIGINAL SEQUENCES:")
for record in alignment:
    print(record.seq, record.id)
print()

# Compute and print the trimming mask
mask = compute_mask(record.seq for record in alignment)
print("MASK:")
print(mask)
print()

# Apply the mask to all records
for record in alignment:
    record.seq = trim_sequence(record.seq, mask)

print("TRIMMED SEQUENCES:")
for record in alignment:
    print(record.id, record.seq)
print()
