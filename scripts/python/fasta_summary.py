from pathlib import Path

fasta_file = Path("practice/multiple_sequences.fasta")

sequences = {}
current_id = None

for line in fasta_file.read_text().splitlines():
    line = line.strip()

    if not line:
        continue

    if line.startswith(">"):
        current_id = line[1:]
        sequences[current_id] = ""
    else:
        sequences[current_id] += line.upper()

print("Total sequences:", len(sequences))

for sequence_id, sequence in sequences.items():
    print("Sequence ID:", sequence_id)
    print("Length:", len(sequence))
