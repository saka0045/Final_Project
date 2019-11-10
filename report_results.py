#!/usr/bin/env python3

"""
Report the species with matched ribosomal sequences and the contigs that didn't match any sequence
"""


def main():
    result_file = open("/Users/m006703/Class/CSCI5481/Final_Project/results.txt", "r")
    unique_specimen_file = open("/Users/m006703/Class/CSCI5481/Final_Project/identified_unique_speimens.txt",
                                "w")

    # Go through the result file and identify the contigs and unique specimens that the contigs matched to
    matched_contigs_list = []
    matched_specimen_dict = {}
    for line in result_file:
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

    # See which contigs didn't match any reference
    contig_file = open("/Users/m006703/Class/CSCI5481/Final_Project/final_contigs_rna.fasta", "r")
    unidentified_contig_file = open("/Users/m006703/Class/CSCI5481/Final_Project/unidentified_contigs_rna.fasta", "w")

    contig_list = []
    sequence_list = []
    for line in contig_file:
        line = line.rstrip()
        if line.startswith(">"):
            contig = line[1:]
            contig_list.append(contig)
        else:
            sequence_list.append(line)

    # See if contigs were matched with the ref sequence, if not write it to the unidentified contigs file
    for contig in contig_list:
        if contig in matched_contigs_list:
            continue
        else:
            index_in_list = contig_list.index(contig)
            unidentified_contig_file.write(">" + contig + "\n" + sequence_list[index_in_list] + "\n")

    result_file.close()
    unique_specimen_file.close()
    contig_file.close()
    unidentified_contig_file.close()


if __name__ == "__main__":
    main()
