# USE: python3 visualisation.py example_output.csv

import csv
import sys

def get_output(file):
    output = []
    with open(file) as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            if line[0] == "H" or line[0] == "P":
                output.append(line)
    return output

def empty_square(size):
    square = []
    size += 2 #nu gedaan omdat er anders problemen zijn met add_stars index out of reach
    for x in range(0, size):
        square.append(list(" " * size))
    return square

def add_proteins(vis, output):
    mid = len(output) * 2
    vis[mid][mid] = output[0][0]
    now_line = mid
    now_col = mid
    for index, line in enumerate(output):
        direction = int(line[1])
        if direction == 1:
            vis[now_line][now_col + 1] = "-" 
            vis[now_line][now_col + 2] = output[index+1][0]
            now_col += 2
        elif direction == -1:
            vis[now_line][now_col - 1] = "-"   
            vis[now_line][now_col - 2] = output[index+1][0]  
            now_col -= 2
        elif direction == 2:
            vis[now_line - 1][now_col] = "|"
            vis[now_line - 2][now_col] = output[index+1][0]
            now_line -= 2
        elif direction == -2:
            vis[now_line + 1][now_col] = "|"
            vis[now_line + 2][now_col] = output[index+1][0]
            now_line += 2
    return vis 

def delete_empty(square):
    empty = list(" " * len(square))
    nice_square = square.copy()
    for line in square:
        if line == empty:
            nice_square.remove(line)
    return nice_square


def print_nice(square):
    square = delete_empty(square)
    for line in square:
        for item in line:
            print(item, end=" ")
        print()

def print_folded_protein(output):
    vis = empty_square(len(output) * 2 * 2)
    square = add_proteins(vis, output)
    square = add_stars(square)
    print_nice(square)

def add_stars(square):
    for index_line, line in enumerate(square):
        for index_item, item in enumerate(line):
            if item == "H":
                if line[index_item + 2] == "H" and line[index_item + 1] != "-":
                    line[index_item + 1] = "*"
                elif square[index_line - 2][index_item] == "H" and square[index_line - 1][index_item] != "|":
                    square[index_line - 1][index_item] = "*"
    return square
    
if __name__ == "__main__":
    filename = sys.argv[1]
    filepath = "output/" + filename
    output = get_output(filepath)
    print_folded_protein(output)
    