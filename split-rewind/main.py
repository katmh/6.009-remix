import io
import wave
import struct  # C structs represented as Python bytes objects

# helper functions for converting back and forth between WAV files and
# our internal dictionary representation for sounds
# code copied from lab scaffold
def load_wav(filename):
    """
    Given the filename of a WAV file, load the data from that file
    and return a Python dictionary representing that sound
    """
    f = wave.open(filename, "r")  # returns Wave_read object
    chan, bd, sr, count, _, _ = f.getparams()
    # returns a namedtuple() (nchannels, sampwidth, framerate, nframes, comptype, compname)

    assert bd == 2, "only 16-bit WAV files are supported"
    # aka 2 bytes; audio resolution of a CD; 24-bit has more headroom for peaks

    left = []
    right = []
    # loop over frames
    for _ in range(count):
        frame = f.readframes(1)  # returns at most n frames, as bytes object
        if chan == 2:  # stereo
            # unpack(format, buffer), returns tuple
            left.append(struct.unpack("<h", frame[:2])[0])
            right.append(struct.unpack("<h", frame[2:])[0])
        else:
            datum = struct.unpack("<h", frame)[0]
            left.append(datum)
            right.append(datum)

    # each measurement takes 2 bytes: values from -2^15 = -32768 to 32767
    # good explanation: https://stackoverflow.com/questions/13039846/what-do-the-bytes-in-a-wav-file-represent
    left = [i / (2 ** 15) for i in left]
    right = [i / (2 ** 15) for i in right]

    return {"rate": sr, "left": left, "right": right}


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, "w")
    outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))

    out = []
    # zip() joins tuples; ((tuple 1 item 1, tuple 2 item 1), ...)
    for l, r in zip(sound["left"], sound["right"]):
        # TODO: clarify; take smaller of 1 or l/r, but if too small use -1; then scale
        l = int(max(-1, min(1, l)) * (2 ** 15 - 1))
        r = int(max(-1, min(1, r)) * (2 ** 15 - 1))
        out.append(l)
        out.append(r)

    # b"" bytes-like object / binary string
    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


def remove_vocals(sound):
    """
    Given a sound dictionary, return a new sound whose left and right channels
    are both replaced with the difference of the original sound's L & R values.
    """
    new_sound = {"rate": sound["rate"], "left": None, "right": None}
    n = len(sound["left"])
    new_sound["left"] = [sound["left"][i] - sound["right"][i] for i in range(n)]
    new_sound["right"] = new_sound["left"]
    return new_sound


# phase inversion: use instrumental & original, invert one so it cancels out the instrumentals, and you're left with the vocals
# good tutorial: https://www.youtube.com/watch?v=770LBIOWvgk
# good diagram: we *want* a phase cancellation https://music.stackexchange.com/questions/66737/what-is-the-purpose-of-phase-invert
# if, like me, you didn't understand your physics classes, here's a cool interactive guide to waves: https://pudding.cool/2018/02/waveforms/


def invert(sound):
    """
    Given a sound, return a new sound that is the inverted version.
    Generally doesn't affect how it sounds
    """
    return {
        "rate": sound["rate"],
        "left": [-s for s in sound["left"]],
        "right": [-s for s in sound["right"]],
    }


# this doesn't really work, likely because of how my instrumentals are derived
def isolate_vocals(sound):
    """
    Use the vocals-removed/instrumental and inverted versions of a sound
    to cancel out the instrumentals, isolating the vocals
    """
    new_sound = {"rate": sound["rate"], "left": None, "right": None}
    n = len(sound["left"])
    instrumental = remove_vocals(sound)
    inverted = invert(sound)
    new_sound["left"] = [
        inverted["left"][i] + instrumental["left"][i] for i in range(n)
    ]
    new_sound["right"] = [
        inverted["right"][i] + instrumental["right"][i] for i in range(n)
    ]
    return new_sound


# splitting by silence: visualize audio waveform
# maybe https://walczak.org/2019/02/automatic-splitting-audio-files-silence-python/


def backwards(sound):
    """
    Given a sound, return a new sound with the samples reversed
    """
    return {
        "rate": sound["rate"],
        "left": sound["left"].reverse(),
        "right": sound["right"].reverse(),
    }


# stitch the clips together

# when interpreter runs a module, the __name__ variable gets set as __main__ if the module
# being run is the main program. if the code is importing the module from another module,
# then __name__ is set to that (imported) module's name.
if __name__ == "__main__":
    pass

    """
    norgaard = load_wav("sounds/norgaard.wav")
    norgaard_v = isolate_vocals(norgaard)
    norgaard_i = remove_vocals(norgaard)
    write_wav(norgaard_v, "norgaard_v.wav")
    write_wav(norgaard_i, "norgaard_i.wav")
    """
