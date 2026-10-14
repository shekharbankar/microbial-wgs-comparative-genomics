from collections import Counter
import csv

fasta_file = "data/raw/ecoli/ncbi_dataset/data/GCF_000005845.2/GCF_000005845.2_ASM584v2_genomic.fna"

counts = Counter()

with open(fasta_file, "r") as file:
    for line in file:
        if not line.startswith(">"):
            counts.update(line.strip().upper())

total = sum(counts.values())
gc_count = counts["G"] + counts["C"]
gc_percent = (gc_count / total) * 100

print("Genome length:", total)
print("A:", counts["A"])
print("T:", counts["T"])
print("G:", counts["G"])
print("C:", counts["C"])
print("GC percentage:", round(gc_percent, 2), "%")

with open("results/base_composition.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Metric", "Value"])
    writer.writerow(["Genome length (bp)", total])
    writer.writerow(["A count", counts["A"]])
    writer.writerow(["T count", counts["T"]])
    writer.writerow(["G count", counts["G"]])
    writer.writerow(["C count", counts["C"]])
    writer.writerow(["GC percentage", round(gc_percent, 2)])

print("Results saved to results/base_composition.csv")
