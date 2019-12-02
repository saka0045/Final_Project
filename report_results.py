#!/usr/bin/env python3

"""
Report the species with matched ribosomal sequences and the contigs that didn't match any sequence
"""

import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--inputFile", dest="input_file", required=True,
        help="Input RNA contig fasta file"
    )
    parser.add_argument(
        "-r", "--resultFile", dest="result_file", required=True,
        help="Output result file from burst"
    )
    parser.add_argument(
        "-o", "--outDir", dest="output_dir", required=True,
        help="output directory for the result files"
    )

    args = parser.parse_args()

    input_file = os.path.abspath(args.input_file)
    result_file = os.path.abspath(args.result_file)
    out_path = os.path.abspath(args.output_dir)

    # Add / at the end if it is not included in the output path
    if out_path.endswith("/"):
        out_path = out_path
    else:
        out_path = out_path + "/"

    # Open files and make result files
    burst_result_file = open(result_file, "r")
    unique_specimen_file = open(out_path + "identified_unique_speimens.txt", "w")
    contig_file = open(input_file, "r")
    unidentified_contig_file = open(out_path + "unidentified_contigs_rna.fasta", "w")
    identified_contig_file = open(out_path + "identified_contigs_rna.fasta", "w")

    # Go through the result file and identify the contigs and unique specimens that the contigs matched to
    matched_contigs_list = identiry_unique_specimens(burst_result_file, unique_specimen_file)

    # Separate out the contigs by identified and unidentified contigs
    # See if contigs were matched with the ref sequence, if not write it to the unidentified contigs file
    make_identified_and_unidentified_contig_list(contig_file, identified_contig_file, matched_contigs_list,
                                                 unidentified_contig_file)

    burst_result_file.close()
    unique_specimen_file.close()
    contig_file.close()
    unidentified_contig_file.close()
    identified_contig_file.close()


def make_identified_and_unidentified_contig_list(contig_file, identified_contig_file, matched_contigs_list,
                                                 unidentified_contig_file):
    """
    Separate out the contigs with those that matched a reference sequence and those that didn't match any reference
    :param contig_file:
    :param identified_contig_file:
    :param matched_contigs_list:
    :param unidentified_contig_file:
    :return:
    """
    contig_list = []
    sequence_list = []
    # Go through the contigs list and obtain the identifier and sequence
    for line in contig_file:
        line = line.rstrip()
        if line.startswith(">"):
            contig = line[1:]
            contig_list.append(contig)
        else:
            sequence_list.append(line)
    for contig in contig_list:
        index_in_list = contig_list.index(contig)
        if contig in matched_contigs_list:
            identified_contig_file.write(">" + contig + "\n" + sequence_list[index_in_list] + "\n")
        else:
            unidentified_contig_file.write(">" + contig + "\n" + sequence_list[index_in_list] + "\n")


def identiry_unique_specimens(burst_result_file, unique_specimen_file):
    """
    Parse the burst result file and identify the unique specimen the contigs matched to the reference with the count
    of how many times the specimens was matched
    :param burst_result_file:
    :param unique_specimen_file:
    :return:
    """
    matched_contigs_list = []
    matched_specimen_dict = {}
    for line in burst_result_file:
        line = line.rstrip()
        line_item = line.split("\t")
        matched_contig = line_item[0]
        matched_contigs_list.append(matched_contig)
        specimen = line_item[1]
        if specimen not in matched_specimen_dict.keys():
            matched_specimen_dict[specimen] = 1
        else:
            matched_specimen_dict[specimen] += 1
    # Make a file of unique specimens
    for specimen, count in matched_specimen_dict.items():
        unique_specimen_file.write(specimen + "\t" + str(count) + "\n")
    return matched_contigs_list


if __name__ == "__main__":
    main()
