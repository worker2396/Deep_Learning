from pyo import *
from random import choices
from genetic import generate_genome

# GLOBAL
BITS_PER_NOTE = 3


def genome_to_melody():
    pass


def play_melody_from_genome(melody, bpm):
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
    for unit in events:
        unit.play()
    s.start()


if __name__ == '__main__':
    pass
