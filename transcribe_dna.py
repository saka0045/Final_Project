#!/usr/bin/env python3

"""
Transcribe the DNA contigs to RNA
"""

dna_contig = open("/Users/m006703/Class/CSCI5481/Final_Project/final_contigs_no_new_lines.fasta", "r")
rna_contig = open("/Users/m006703/Class/CSCI5481/Final_Project/final_contigs_rna.fasta", "w")

for line in dna_contig:
    line = line.rstrip()
    if line.startswith(">"):
        rna_contig.write(line + "\n")
    else:
        # Replace T with U for RNA
        line = line.replace("T", "U")
        rna_contig.write(line + "\n")

dna_contig.close()
rna_contig.close()
