# This is a file that makes it look like stuff is happening

import random
import time

class matbg:
    """
    Generate the matrix background
    """
    def __init__(self, width=80, columns=10, rate=20):
        self.width = width
        self.columns = columns
        self.rate = rate
        self.insertedWords = None
        self.charset = ("a",
                        "b",
                        "c",
                        "d",
                        "e",
                        "f",
                        "g",
                        "h",
                        "i",
                        "j",
                        "k",
                        "l",
                        "m",
                        "n",
                        "o",
                        "p",
                        "q",
                        "r",
                        "s",
                        "t",
                        "u",
                        "v",
                        "w",
                        "x",
                        "y",
                        "z",
                        )

    def genDummyStreams(self):
        """
        Generate some random length streams with random data
        """
        nstrings = 100
        self.streamlist = [self.genDummyString() for i in range(nstrings)]

    def genDummyString(self):
        maxlen = 20
        minlen = 5
        dumstr = ""
        for i in range(random.randint(minlen, maxlen)):
            dumstr += self.charset[random.randint(0, len(self.charset)-1)]
        return dumstr

    def genRandColumns(self):
        cols = []
        for i in range(self.columns):
            pick = None
            while pick is None:
                pick = random.randint(0, self.width-1)
                if pick in cols:
                    pick = None
                else:
                    cols.append(pick)
        return cols

    def pickRandStreams(self):
        # pick a subset from the generated list of streams
        streams = [self.streamlist[random.randint(0, len(self.streamlist)-1)] for i in range(self.columns)]
        return streams

    def insert(self, inputstr):
        # Shoehorn in some user-specified text
        wordlist = inputstr.split(" ")
        if len(wordlist) > self.columns:
            self.columns = len(wordlist)
        self.insertedWords = wordlist

    def run(self):
        # Reference blank line
        line = " " * self.width
        itercount = 0
        itertarget = 10
        while True:
            itercount += 1
            insertprint = False
            # pick what columns to use
            cols = self.genRandColumns()
            cols.sort()
            streams = self.pickRandStreams()
            if self.insertedWords is not None:
                if itercount == itertarget:
                    insertprint = True
                    itercount = 0
                    itertarget = random.randint(10, 20)
                    insertstartcol = random.randint(0, len(cols) - len(self.insertedWords))
                    streams[insertstartcol:insertstartcol+len(self.insertedWords)] = self.insertedWords
            streamlens = [len(stream) for stream in streams]
            maxstreamlen = max(streamlens)
            leadspaces = [int((maxstreamlen - streamlen)/2) for streamlen in streamlens]
            # Loop for this block of streams
            #a = "."*80
            #print(a)
            for i in range(maxstreamlen):
                newline = line
                # Loop across each column
                for j in range(len(cols)):
                    if i <= leadspaces[j]:
                        if insertprint:
                            newline = newline[:cols[j]] + 'v' + newline[cols[j]:-1]
                    elif i < streamlens[j] + leadspaces[j]:
                        newline = newline[:cols[j]] + streams[j][i - leadspaces[j]] + newline[cols[j]:-1]
                    else:
                        if insertprint:
                            newline = newline[:cols[j]] + '^' + newline[cols[j]:-1]
                print(newline)
                time.sleep(float(1/self.rate))


if __name__ == "__main__":
    bg = matbg(rate=30)
    bg.genDummyStreams()
    bg.insert("Merry Christmas ya filthy animal")
    bg.run()