#! /usr/bin/env python3

import argparse
import decimal
import re

def parseMove(line):
    s = line.split(" ")
    move = {}
    for x in s[1:]:
        move[x[0]] = decimal.Decimal(x[1:])
    return move


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True)
parser.add_argument('-o', '--output', required=True)
parser.add_argument('-z', '--zThreshold', required=False, type=float, default=100)
args = parser.parse_args()

# Open file and read all lines
with open(args.input) as f:
    lines = f.readlines()

# Scan through lines looking for Z-movements that rise
# Must go above some threshold
for i in range(len(lines)):
    if (lines[i][0:3] == "G01"):
        move1 = parseMove(lines[i])
        # Check that line is followed by a X and/or Y movement and no Z movement, then
        # followed by a lowering of Z
        if "Z" in move1 and "F" in move1 and len(move1) == 2:
            if (lines[i+2][0:3] == "G01"):
                move3 = parseMove(lines[i+2])
                if "Z" in move3 and "F" in move3 and len(move3) == 2 and (lines[i+1][0:3] == "G01"):
                    move2 = parseMove(lines[i+1])
                    if not "Z" in move2 and move1["Z"] > args.zThreshold:
                        # Change the three lines to be G00 instead of G01 and remove feed rate
                        lines[i] = "G00 Z" + str(move1["Z"]) + "\n"
                        lines[i+1] = "G00"
                        lines[i+1] = lines[i+1] + ((" X" + str(move2["X"])) if ("X" in move2) else "")
                        lines[i+1] = lines[i+1] + ((" Y" + str(move2["Y"])) if ("Y" in move2) else "")
                        lines[i+1] = lines[i+1] + ((" B" + str(move2["B"])) if ("B" in move2) else "")
                        lines[i+1] = lines[i+1] + "\n"
                        lines[i+2] = "G00 Z" + str(move3["Z"]) + "\n"

with open(args.output, "w") as f:
    f.writelines(lines)
