from pyo import *
from random import choices
from genetic import generate_genome
from midiutil import MIDIFile
from datetime import datetime

# GLOBAL
BITS_PER_NOTE = 3 # liczba bitów do kodowania noty ; 2^3 = 8
NUM_NOTES = 4
NUM_BARS = 3
BPM = 120
genome_len = BITS_PER_NOTE*NUM_NOTES*NUM_BARS
KEY = 'C'
SCALE = 'major'
ROOT = 4
NUM_STEPS = 1
# Genome = List[int]

def note_from_bits(bits): # bits : [0,1,1] # enumerate od bita : [(0,0),(1,1),(2,1)]
    return sum([bit*pow(2, index) for index, bit in enumerate(bits)]) # suma : wartość*2^index

def genome_to_melody(genome, num_notes, num_bars):
    notes = [genome[i * BITS_PER_NOTE:i * BITS_PER_NOTE + BITS_PER_NOTE] for i in range(num_notes * num_bars)] # notes : slicing genomu w obszarze 3*n:3*n+3
    
    note_lenght = 4 / num_notes # długość każdej noty

    scl = EventScale(root=KEY, scale=SCALE, first=ROOT)

    melody = {
        "notes" : [],
        "velocity" : []
    }

    for note in notes:
        index = note_from_bits(note)

        melody["notes"].append(int(index)) 
        melody["velocity"] += [127]

    steps = []

    for step in range(NUM_STEPS):
        current_step = []
        for note in melody["notes"]:
            step_index = int((note+step*2) % len(scl.data))
            current_data = scl.data[step_index]
            steps.append(current_data) 
        #steps.append(list([(scl.data[int((note+step*2) % len(scl.data))] for note in melody["notes"])])) #krwmć
                    
    melody["notes"] = [steps]

    return melody

#jedna operacja - krzyżowanie, mutacja
#zip = pdf + kod | opisać problemy

def convert_melody_to_genome(melody, bpm):
    events = list()
    for step in melody["notes"]:
        events.append(Events(
            midinote=EventSeq(step, occurrences=1),
            midivel=EventSeq(melody["velocity"], occurrences=1),
            # beat=EventSeq(melody["beat"], occurrences=1),
            attack=0.001,
            decay=0.05,
            sustain=0.5,
            release=0.005,
            bpm=BPM
        ))
    return events


def save_genome_to_midi(filename, Genome, NUM_BARS, NUM_NOTES, NUM_STEPS, key, scale, root, bpm):
    melody = genome_to_melody(genome, NUM_BARS, NUM_NOTES, NUM_STEPS, key, scale, root)

    if len(melody["notes"][0]) != len(melody["velocity"]):
        raise ValueError

    mf = MIDIFile(1)

    track = 0
    channel = 0

    time = 0.0
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, bpm)

    for i, vel in enumerate(melody["velocity"]):
        if vel > 0:
            for step in melody["notes"]:
                mf.addNote(track, channel, step[i], time, melody["beat"][i], vel)

        time += melody["beat"][i]

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        mf.writeFile(f)


population_size = 3

def main(): 

    folder = str(int(datetime.now().timestamp()))

    population = [generate_genome(num_bars * num_notes * BITS_PER_NOTE) for _ in range(population_size)]

    population_id = 0

    s = Server().boot()

    genome = generate_genome(genome_len)
    Melody = genome_to_melody(genome, 4 , 4)
    events = convert_melody_to_genome(Melody, BPM)

    for unit in events:
        unit.play()
    s.start()
    time.sleep(20)

    print("saving population midi …")
    for i, genome in enumerate(population):
        save_genome_to_midi(f"{folder}/{population_id}/{scale}-{key}-{i}.mid", genome, num_bars, num_notes, num_steps, pauses, key, scale, root, bpm)
    print("done")

    running = input("continue? [Y/n]") != "n"
    # population = next_generation
    # population_id += 1


    if __name__ == '__main__':
        main()