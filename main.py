from pyo import *
from random import choices
from genetic import generate_genome

# GLOBAL
BITS_PER_NOTE = 3 # liczba bitów do kodowania noty ; 2^3 = 8
BPM = 120
# Genome = List[int]

def note_from_bits(bits): # bits : [0,1,1]
    for index , bit in enumerate(bits): # enumerate od bita : [(0,0),(1,1),(2,1)]
        return sum(bit*pow(2, index)) # suma : wartość*2^index

def genome_to_melody(genome, num_notes, num_bars):
    notes = [genome[i * BITS_PER_NOTE:i * BITS_PER_NOTE + BITS_PER_NOTE] for i in range(num_notes * num_bars)] # notes : slicing genomu w obszarze 3*n:3*n+3
    
    note_lenght = 4 / num_notes # długość każdej noty

    melody = {
        "notes" : [],
        "velocity" : []
    }

    for note in notes:
        index = note_from_bits(note)

        melody["notes"] += [index]
        melody["velocity"] += [127]

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


if __name__ == '__main__':
    s = Server().boot()

    genome = generate_genome(genome_len)
    Melody = genome_to_melody(genome)
    events = convert_melody_to_genome(Melody, BPM)

    for unit in events:
        unit.play()
    s.start()