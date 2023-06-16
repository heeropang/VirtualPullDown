#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import openpyxl
import sys
import subprocess
import math

subprocess.call("mkdir fa", shell=True)
subprocess.call("rm fa/*", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def is_greater_or_equal(value, threshold, tolerance=1e-6):
    return value >= threshold - tolerance

def generate_fasta_file(filename, threshold):
    # Load the Excel spreadsheet
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active

    # Iterate through each row in the spreadsheet
    for row in sheet.iter_rows(min_row=2, values_only=True):
        name = row[0]
        sequence = row[5]
        condition = float(row[2]) if row[2] is not None else None

        # Check if the condition matches the threshold with tolerance
        if isinstance(condition, float) and is_greater_or_equal(condition, threshold):
            # Generate the FASTA file content
            fasta_content = f">{name}\n{sequence}\n"

            # Generate the filename for the FASTA file
            fasta_filename = f"fa/{name}.fa"

            # Write the FASTA content to the file
            with open(fasta_filename, "w") as file:
                file.write(fasta_content)

            print(f"Generated {fasta_filename} with probability >= the {threshold} provided.")
        else:
            print(f"Skipping {name} lower than the threshold.")

# Provide the filename of your Excel spreadsheet
excel_filename = "ESMFold_structure_homologs.xlsx"

# Provide the threshold (probability) value as an argument
threshold = float(sys.argv[1]) if len(sys.argv) > 1 else None

# Generate the FASTA files based on the threshold
if threshold is None:
    print("Please provide a threshold (probability) value as an argument.")
else:
    generate_fasta_file(excel_filename, threshold)

