#
# Script for processing PSSM generated by psi-blast. Script parse matrix from
# PSSM file passed as program argument and print with columns ordered as in 
# ICML2014 dataset. That is ACDEFGHIKLMNPQRSTVWXY.
# When an option -s is passed matrix will be scaled using sigmoid function.
#
# Takes one argument, a path to a PSSM file generated by psi-blast.
#
# Usage: python process_pssm.py pssm_file [-s]
#

from __future__ import print_function
import sys
import math


column_order = 'ACDEFGHIKLMNPQRSTVWXY'


def sigmoid(x):
    return 1.0 / (1 + math.exp(-x))


def scale_matrix(matrix):
    # aply sigmoid on every value in matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = sigmoid(matrix[i][j])
            
    return matrix


def transform_row(row):
    # from ARNDCQEGHILKMFPSTWYV
    # to   ACDEFGHIKLMNPQRSTVWXY
    new_row = [0]*21
    for c, v in zip('ARNDCQEGHILKMFPSTWYV', row):
        new_row[column_order.index(c)] = v
    return new_row


def parse_pssm(pssm_file):
    with open(pssm_file, 'r') as fin:
        _ = fin.readline()
        _ = fin.readline()
        _ = fin.readline()

        pssm = []
        line = fin.readline()
        while len(line) > 1:
            # psssm row
            row = line.split()
            row = map(float,row[2:22])
            row = transform_row(row)
            pssm.append(row)
            
            line = fin.readline()

    return pssm

def main():
    try:
        pssm_file = sys.argv[1]
    except IndexError:
        print('No missing parameter.\n')
        print('Usage: python process_pssm.py pssm_file\n')
        return

    try:
        scale_par = sys.argv[2]
    except IndexError:
        scale_par = '-'

    scale = False
    if scale_par == '-s':
        scale = True

    pssm = parse_pssm(pssm_file)
    if scale:
        pssm = scale_matrix(pssm)

    row_f = '{} '*21
    print(row_f.format(*column_order))

    for row in pssm:
        print(row_f.format(*row))


if __name__ == "__main__":
    main()

