from pyo import *
import time
# from random import choices
# from genetic import generate_genome


def convert_melody_to_genome(melody):
    events = list()
    for step in melody:
        events.append(Events(
            midinote=EventSeq(step, occurrences=1),
            midivel=EventSeq(melody["velocity"], occurrences=1),
            # beat=EventSeq(melody["beat"], occurrences=1),
            # attack=0.001,
            # decay=0.05,
            # sustain=0.5,
            # release=0.005,
            # bpm=BPM
        ))
    return events


if __name__ == '__main__':
    melody = [[41, 36, 36, 32, 48, 48, 34, 38, 32, 32, 32, 32, 32, 32]]
    velocity = [127]*len(melody[0])
    beat = [1]*len(melody[0])
    s = Server().boot()
    events = list()

    for step in melody:
        events.append(Events(
            midinote=EventSeq(step, occurrences=1),
            midivel=EventSeq(velocity, occurrences=1),
            beat=EventSeq(beat, occurrences=1),
            attack=0.001,
            decay=0.05,
            sustain=0.5,
            release=0.005,
            bpm=128
        ))

    for unit in events:
        unit.play()

    s.start()
    time.sleep(10)
