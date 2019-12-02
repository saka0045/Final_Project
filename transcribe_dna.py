#!/usr/bin/env python3

"""
Transcribe the DNA contigs to RNA
"""

import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--inputFile", dest="input_file", required=True,
        help="Input contig fasta file with no new lines"
    )
    parser.add_argument(
        "-o", "--outDir", dest="output_dir", required=True,
        help="output directory for the result files"
    )

    args = parser.parse_args()

    input_file = os.path.abspath(args.input_file)
    out_path = os.path.abspath(args.output_dir)

    # Add / at the end if it is not included in the output path
    if out_path.endswith("/"):
        out_path = out_path
    else:
        out_path = out_path + "/"

    dna_contig = open(input_file, "r")
    rna_contig = open(out_path + "final_contigs_rna.fasta", "w")

    transcribe_dna(dna_contig, rna_contig)

    dna_contig.close()
    rna_contig.close()


def transcribe_dna(dna_contig, rna_contig):
    """
    Transcribe the DNA contigs to RNA to perform alignment with an RNA reference file
    :param dna_contig:
    :param rna_contig:
    :return:
    """
    for line in dna_contig:
        line = line.rstrip()
        if line.startswith(">"):
            rna_contig.write(line + "\n")
        else:
            # Replace T with U for RNA
            line = line.replace("T", "U")
            rna_contig.write(line + "\n")


if __name__ == "__main__":
    main()
