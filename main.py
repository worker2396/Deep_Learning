from pyo import *
from random import choices
from genetic import generate_genome

# GLOBAL
BITS_PER_NOTE = 3  # liczba bitów do kodowania noty ; 2^3 = 8
genome_len = 3*8
BPM = 120


def note_from_bits(bits):  # bits : [0,1,1]
    return int(sum([bit*pow(2, index) for index, bit in enumerate(bits)]))


def genome_to_melody(genome, num_notes: float, num_bars):
    notes = [genome[i * BITS_PER_NOTE:i * BITS_PER_NOTE + BITS_PER_NOTE] for i in range(num_notes * num_bars)]  # notes : slicing genomu w obszarze 3*n:3*n+3
    
    note_length = 4 / float(num_notes)  # długość każdej noty

    melody = {
        "notes":  [],
        "velocity": []
    }

    for note in notes:
        index = note_from_bits(note)
        melody["notes"].append([index])
        melody["velocity"].append(127)

    return melody


def convert_melody_to_genome(melody):
    events = list()
    for step in melody["notes"]:
        events.append(Events(
            midinote=EventSeq(step, occurrences=1),
            midivel=EventSeq(melody["velocity"], occurrences=1),
            #beat=EventSeq(melody["beat"], occurrences=1),
            attack=0.001,
            decay=0.05,
            sustain=0.5,
            release=0.005,
            bpm=BPM
        ))
    return events


if __name__ == '__main__':
    s = Server().boot()

    genome = generate_genome(genome_len)
    Melody = genome_to_melody(genome, 4, 4)
    Events = convert_melody_to_genome(Melody)

    for unit in Events:
        unit.play()
    s.start()
