from pathlib import Path

fasta_file = Path("practice/example.fasta")

lines = fasta_file.read_text().splitlines()

header = lines[0]
sequence = "".join(lines[1:]).upper()

valid_bases = set("ATGC")
invalid_bases = set(sequence) - valid_bases

print("FASTA file:", fasta_file)
print("Sequence ID:", header[1:])
print("Sequence:", sequence)
print("Sequence length:", len(sequence))

if invalid_bases:
    print("Invalid characters:", sorted(invalid_bases))
else:
    print("DNA validation: PASS")
