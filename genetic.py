from random import choices
from typing import List


Genome = List[int]


def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)
