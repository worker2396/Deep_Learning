from random import choices


def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)
