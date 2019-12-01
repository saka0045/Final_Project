#!/usr/bin/env python3

import argparse
import os
import gzip


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--inputFile", dest="input_file", required=True,
        help="Input contig fasta file"
    )
    parser.add_argument(
        "-r", "--refFile", dest="ref_file", required=True,
        help="reference fasta file to align the contigs to"
    )
    parser.add_argument(
        "-o", "--outDir", dest="output_dir", required=True,
        help="output directory for the result files"
    )

    args = parser.parse_args()

    input_file = os.path.abspath(args.input_file)
    ref_file = os.path.abspath(args.ref_file)
    out_path = os.path.abspath(args.output_dir)

    # Add / at the end if it is not included in the output path
    if out_path.endswith("/"):
        out_path = out_path
    else:
        out_path = out_path + "/"

    # Open files and create output files
    contigs_fasta = open(input_file, "r")
    ref_fasta = gzip.open(ref_file, "rt")
    contigs_fasta_no_new_lines = open(out_path + "final_contigs_no_new_lines.fasta", "w")
    ref_fasta_no_new_lines = open(out_path + "SILVA_132_SSURef_tax_silva_trunc_no_new_lines.fasta", "w")

    # Remove the new line character "\n" from the original fasta files
    remove_new_lines_in_fasta(contigs_fasta, contigs_fasta_no_new_lines)
    remove_new_lines_in_fasta(ref_fasta, ref_fasta_no_new_lines)

    contigs_fasta.close()
    contigs_fasta_no_new_lines.close()
    ref_fasta.close()
    ref_fasta_no_new_lines.close()


def remove_new_lines_in_fasta(original_fasta, fasta_no_new_lines):
    """
    Takes in fasta files with new lines in the fasta sequence and removes the new line characer "\n"
    :param original_fasta:
    :param fasta_no_new_lines:
    :return:
    """
    sequence = ""
    for line in original_fasta:
        line = line.rstrip()
        if line.startswith(">"):
            if sequence != "":
                fasta_no_new_lines.write(sequence + "\n")
                sequence = ""
            fasta_no_new_lines.write(line + "\n")
        # If the line is not a header, add it to the sequence until you hit the next header
        else:
            sequence += line
    # Write the last sequence to the file
    fasta_no_new_lines.write(sequence + "\n")


if __name__ == "__main__":
    main()
