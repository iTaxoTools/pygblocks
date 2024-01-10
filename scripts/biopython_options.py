from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from itaxotools.pygblocks import Options, compute_mask, trim_sequence

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

options = Options(
    IS=2,  # Minimum Number Of Sequences For A Conserved Position
    FS=3,  # Minimum Number Of Sequences For A Flank Position
    CP=2,  # Maximum Number Of Contiguous Nonconserved Positions
    BL1=3,  # Minimum Length Of A Block, 1st iteration
    BL2=3,  # Minimum Length Of A Block, 2nd iteration
    GT=3,  # Maximum Number of Allowed Gaps For Any Position
    GC="-",  # Definition of Gap Characters
)

print()

print("ORIGINAL SEQUENCES:")
for record in alignment:
    print(record.seq, record.id)
print()

# Compute and print the trimming mask
sequences = (record.seq for record in alignment)
mask = compute_mask(sequences, options, log=True)
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
