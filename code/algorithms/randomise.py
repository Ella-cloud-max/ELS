import random

def random_assignment_amino(protein, amino):
    if amino.i == protein.i_list[-1]:
        amino.direction = 0
        amino.change_coordinates()
        return
    amino.change_direction(random.choice([-2, -1, 1, 2]))
    amino.change_coordinates()

def random_assignment_protein(protein):
    for amino in protein.aminos.values():
        random_assignment_amino(protein, amino)

def random_redirect_amino(protein, change_amino):
    """
    Redirects change_amino to another direction and resets all later aminos.
    """
    original_direction = change_amino.direction
    while change_amino.direction == original_direction:
        change_amino.change_direction(random.choice([-2, -1, 1, 2]))
    for amino in protein.aminos.values():
        if amino.i > change_amino.i:
            amino.change_coordinates()

def random_redirect_aminos(protein, change_amino):
    """
    Redirects change_amino to another direction and updates the coordinates
    of later aminos accordingly.
    """
    change_amino.change_direction(random.choice([-2, -1, 1, 2]))
    for amino in protein.aminos.values():
        if amino.i > change_amino.i:
            amino.change_coordinates()
            