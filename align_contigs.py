#!/usr/bin/env python3


def main():
    contigs_fasta = open("/Users/m006703/Class/CSCI5481/Final_Project/final_contigs.fasta", "r")
    contigs_fasta_no_new_lines = open("/Users/m006703/Class/CSCI5481/Final_Project/final_contigs_no_new_lines.fasta",
                                      "w")
    """
    ref_fasta = open("/Users/m006703/Class/CSCI5481/Final_Project/SILVA_132_SSURef_tax_silva_trunc.fasta", "r")
    ref_fasta_no_new_lines = open(
        "/Users/m006703/Class/CSCI5481/Final_Project/SILVA_132_SSURef_tax_silva_trunc_no_new_lines.fasta", "w")
    """
    # Remove the new line character "\n" from the original fasta files
    remove_new_lines_in_fasta(contigs_fasta, contigs_fasta_no_new_lines)
    # remove_new_lines_in_fasta(ref_fasta, ref_fasta_no_new_lines)

    contigs_fasta.close()
    contigs_fasta_no_new_lines.close()
    # ref_fasta.close()
    # ref_fasta_no_new_lines.close()


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
