#!/usr/bin/env bash

##################################################
#Global Variables
##################################################

INPUT_DIR=""
OUT_DIR=""
CONTIGS_FILE=""
REFERENCE_FILE=""
PYTHON="/usr/bin/env python3"
CMD=""

##################################################
#FUNCTIONS
##################################################

function usage(){
cat << EOF
Aligns the contig file to the reference RNA contig file using burst
Requires all of the scripts, files and burst to be in the input directory
OPTIONS:
    -h  [optional] help, show this message
    -i  [required] input directory
    -c  [required] input DNA contigs files to align
    -r  [required] reference RNA contig file to align to
    -o  [required] output directory for result files
EOF
}

##################################################
#BEGIN PROCESSING
##################################################

while getopts "hi:c:r:o:" OPTION
do
    case $OPTION in
		h) usage ; exit ;;
		i) INPUT_DIR=${OPTARG} ;;
		c) CONTIGS_FILE=${OPTARG} ;;
		r) REFERENCE_FILE=${OPTARG} ;;
		o) OUT_DIR=${OPTARG} ;;
    esac
done

INPUT_DIR=${INPUT_DIR%/}
OUT_DIR=${OUT_DIR%/}
BURST=${INPUT_DIR}/burst

# Remove the new lines from the input contig fasta and the reference fasta
echo "Running remove_new_lines.py"
CMD="${PYTHON} ${INPUT_DIR}/remove_new_lines.py -i ${CONTIGS_FILE} -r ${REFERENCE_FILE} -o ${OUT_DIR}"
echo "Running command: ${CMD}"
${CMD}
echo "Done running remove_new_lines.py"

# Transcribe the DNA contig file to RNA
echo "Running transcribe_dna.py"
CMD="${PYTHON} ${INPUT_DIR}/transcribe_dna.py -i ${OUT_DIR}/final_contigs_no_new_lines.fasta -o ${OUT_DIR}"
echo "Running command: ${CMD}"
${CMD}
echo "Done running transcribe_dna.py"

# Run burst
echo "Running burst"
CMD="${BURST} -r ${OUT_DIR}/SILVA_132_SSURef_tax_silva_trunc_no_new_lines.fasta -q ${OUT_DIR}/final_contigs_rna.fasta \
-o ${OUT_DIR}/results.txt"
echo "Running command: ${CMD}"
${CMD}
echo "Done running burst"

# Report the results
echo "Running report_results.py"
CMD="${PYTHON} ${INPUT_DIR}/report_results.py -i ${OUT_DIR}/final_contigs_rna.fasta -r ${OUT_DIR}/results.txt \
-o ${OUT_DIR}"
echo "Running command: ${CMD}"
${CMD}
echo "Done running report_results.py"

echo "Script is done running. All results are saved in ${OUT_DIR}"