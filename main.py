from pyo import *
from genetic import generate_genome

# GLOBAL
BITS_PER_NOTE = 3
BPM = 120  # placeholder
genome_len = 4  # placeholder


def genome_to_melody(genome):
    return None


def convert_melody_to_genome(melody, bpm):
    events = list()
    for step in melody["notes"]:
        events.append(Events(
            midinote=EventSeq(step, occurrences=1),
            midivel=EventSeq(melody["velocity"], occurrences=1),
            beat=EventSeq(melody["beat"], occurrences=1),
            attack=0.001,
            decay=0.05,
            sustain=0.5,
            release=0.005,
            bpm=bpm
        ))
    return events


if __name__ == '__main__':
    s = Server().boot()

    genome = generate_genome(genome_len)
    Melody = genome_to_melody(genome)
    events = convert_melody_to_genome(Melody, BPM)

    for unit in events:
        unit.play()
    s.start()
