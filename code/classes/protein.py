from .amino import Amino
import csv
from typing import Any, Union


class Protein():
    def __init__(self, input_file: str) -> None:
        self.i_list: list[int] = []
        self.aminos = self.make_aminos(input_file)
        self.score = 0
        self.coordinates_set: set[tuple[int]] = set()
        
        for i in self.i_list:
            coordinates = self.aminos[i].coordinates
            self.coordinates_set.add(coordinates)
            if self.aminos[i].direction != 0:
                self.aminos[i].next = self.aminos[i + 1]
        

    def make_aminos(self, input_file: str) -> dict[int, Any]:
        """ Add aminos to a protein """
        if input_file[:6] == "output":
            return self.import_structure(input_file)
        aminos = {}
        structure = [*str(*open(input_file))]
        
        aminos[0] = Amino(0, structure[0], 0, (0, 0), None)
        self.i_list.append(0)
        for i in range(1, len(structure)):
            aminos[i] = Amino(i, structure[i], 0, (0, 0), aminos[i-1])
            self.i_list.append(i)
        return aminos

    def import_structure(self, file_directory: str) -> dict:
        """
        Imports the amino acids from a file that contains a known solution

        pre: string which is the directory to the file
        post: outputs a dictionary containing the amino-acids
        """

        file = open(file_directory, "r")
        aminos: dict = {}
        reader = csv.reader(file)
        next(reader)    # skip header
        soort, direction = next(reader) # first line
        direction = int(direction)
        amino_id = 0
        coordinates = (0, 0)
        aminos[amino_id] = Amino(amino_id, soort, direction, coordinates, None)
        self.i_list.append(amino_id)
        for soort, direction in reader:
            if soort == "score":
                break
            direction = int(direction)
            amino_id += 1
            previous_direction = aminos[amino_id - 1].direction
            if previous_direction == 0:
                coordinates = (coordinates[0] + 1, coordinates[1] + 1)
            elif abs(previous_direction) == 1:
                coordinates = (coordinates[0] + previous_direction, coordinates[1])
            else:
                if previous_direction > 0:
                    coordinates = (coordinates[0], coordinates[1] + 1)
                else:
                    coordinates = (coordinates[0], coordinates[1] - 1)
            self.i_list.append(amino_id)
            aminos[amino_id] = Amino(amino_id, soort, direction, coordinates,
                                  aminos[amino_id - 1])
        file.close()
        return aminos
    
    def get_empty_amino(self) -> Any:
        """ Get the first amino that does not have coordinates yet""" 
        for amino in self.aminos.values():
            if amino.coordinates == (0, 0) and amino.i != 0:
                return amino

        return None

    def check_viability(self) -> bool:
        """ Check that no aminos have the same coordinates """
        check_amino = self.aminos[self.i_list[-1]]
        while check_amino != None:
            check_previous = check_amino.previous_amino
            while check_previous != None:
                if check_amino.coordinates == check_previous.coordinates:
                    return False
                check_previous = check_previous.previous_amino
            check_amino = check_amino.previous_amino
        return True

    def count_score(self) -> Union[bool, int]:
        """ Count and update the score of the protein """
        if not self.check_viability():
            return False
        
        self.score = 0
        count_amino = self.aminos[self.i_list[-1]]
        while count_amino != None:
            if count_amino.soort == "H":
                check_previous = count_amino.previous_amino
                while check_previous != None:
                    if (abs(check_previous.coordinates[0] - count_amino.coordinates[0]) + abs(check_previous.coordinates[1] - count_amino.coordinates[1])) == 1 and check_previous.soort == "H" and abs(check_previous.i - count_amino.i) != 1:
                        self.score -= 1
                    check_previous = check_previous.previous_amino
            count_amino = count_amino.previous_amino
        return self.score

    def print_output(self, output_file_name: str) -> None:
        """ Print the output of a protein to a file"""
        output_file = open(f"output/{output_file_name}", "w")
        output_file.write("amino,fold\n")
        for amino in self.aminos.values():
            output_file.write(f"{amino.soort},{amino.direction}\n")
        output_file.write(f"score,{self.count_score()}")
        output_file.close()

    def change_coordinates(self, old_coordinates, new_coordinates) -> None:
        self.coordinates_set.pop(old_coordinates)
        self.coordinates_set.add(new_coordinates)
