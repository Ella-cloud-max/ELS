# Depth First Algoritm by Ella van Loenen
# 17-01-2024

import sys
from code.classes.amino import Amino
from code.classes.protein import Protein
import copy
import timeit
from typing import Union, Any

class DepthFirst:
    """
    A Depth First algorithm that builds a stack of proteins with a unique assignment of amino acids for each instance.
    """
    def __init__(self, protein: Protein) -> None:
        self.protein = copy.deepcopy(protein)
        self.directions = [1, -1, 2, -2]

        self.states = [copy.deepcopy(self.protein)]

        self.best_solution: Any = None
        self.best_value = float('inf')

    def get_next_state(self) -> Protein:
        """
        Method that gets the next state from the list of states.
        """
        return self.states.pop()

    def build_children(self, protein: Protein, amino: Amino) -> None:
        """
        Creates all possible child-states and adds them to the list of states.
        """
        # Retrieve all valid possible values for the node.
        directions = amino.get_possibilities()
        #print(directions)

        # Add an instance of the graph to the stack, with each unique value assigned to the node.
        for direction in directions:
            new_protein = copy.deepcopy(protein)
            new_protein.aminos[amino.i - 1].direction = direction
            new_protein.aminos[amino.i].change_coordinates()
            self.states.append(new_protein)

    def check_solution(self, new_protein: Protein) -> None:
        """
        Checks and accepts better solutions than the current solution.
        """
        new_value = new_protein.count_score()
        old_value = self.best_value

        # Update if the new protein has a lower score
        if new_value < old_value:
            self.best_solution = new_protein
            self.best_value = new_value
            print(f"New best value: {self.best_value}")

    def run(self, max_seconds: int) -> None:
        """
        Runs the algorithm untill all possible states are visited.
        """
        start = timeit.default_timer()
        while self.states:
            # Stop if the maximum time has been reached
            update = timeit.default_timer()
            if update - start > max_seconds:
                print(f"Took too long, stopped after {max_seconds} seconds.")
                break
            
            new_protein = self.get_next_state()

            # Retrieve the next empty amino.
            amino = new_protein.get_empty_amino()
            
            # If needed add child-states to the state list
            if amino is not None:
                self.build_children(new_protein, amino)
            # Otherwise check the score
            else:
                self.check_solution(new_protein)
                
                # Stop if we find a solution we want
                # if self.best_value == -1:
                    # break

        # Update the input protein with the best result found.
        self.protein = self.best_solution