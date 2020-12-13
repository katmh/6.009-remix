# split rewind

Extends Lab 0: Audio Processing

Write a script that splits an audio file (i.e. an acapella song into individual words, ideally), reverses them, then stitches them back together

## Overview of original lab

**Purpose:** Warmup/make sure we can program in Python, run tests, etc. Introduce us to the idea that we can read in file formats (and show that multimedia files aren't that scary to work with). Do some simple manipulations with impressive mileage!

- Backwards
- Mixing two audio clips on top of each other: `p` times the samples in first sound and `1-p` times samples in the second
- Echo: with parameters `num_echos`, `delay`, `scale`
- Pan side to side: if sound is `N` samples long:
  - Scale the first sample in the right channel by 0, the second by `1/(N-1)`, the third by `2/(N-1)`... and the last by 1
  - Left: First sample 1, second `1-1/(N-1)`, third `1-2/(N-1)`... last by 0
- Removing vocals from music by using `left-right` as both left and right (because instruments are often off-center)

More on echo:

```
s = {
    'rate': 8,
    'left': [1, 2, 3, 4, 5],
    'right': [5, 4, 3, 2, 1],
}
s2 = echo(s, 2, 0.4, 0.2)
s2['left']
# would be [1, 2, 3, 4.2, 5.4, 0.6, 0.84, 1.08, 0.12, 0.16, 0.2]
```

## Tasks

- [x] Read/write audio files to/from friendly format
- [x] Attempt to isolate vocals (learned about phase cancellation!)
- [x] Implement splits
- [ ] Implement splits without a library
- [ ] Write unit (e.g. file I/O, "correct" split locations, correct reversals) and integration (e.g. entire file split-reversed correctly) tests
- [ ] Level up code style
- [ ] Write-up