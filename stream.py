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
            # stored as a list of indices from 0 to width of console (default 80)
            cols = self.genRandColumns()
            cols.sort()
            streams = self.pickRandStreams()
            if self.insertedWords is not None:
                if itercount == itertarget:
                    #print("X"*80)
                    insertprint = True
                    itercount = 0
                    itertarget = random.randint(10, 20)
                    # Index of the cols list used as the starting point for the inserted words
                    insertstartcol = random.randint(0, len(cols) - len(self.insertedWords))
                    insertendcol = insertstartcol+len(self.insertedWords)-1
                    streams[insertstartcol:insertendcol] = self.insertedWords
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
                    if i < leadspaces[j]:
                        if insertprint and (insertstartcol <= j <= insertendcol):
                            newline = newline[:cols[j]] + '.' + newline[cols[j]:-1]
                    elif i < streamlens[j] + leadspaces[j]:
                        newline = newline[:cols[j]] + streams[j][i - leadspaces[j]] + newline[cols[j]:-1]
                    else:
                        if insertprint and (insertstartcol <= j <= insertendcol):
                            newline = newline[:cols[j]] + '.' + newline[cols[j]:-1]
                print(newline)
                # This wait between each new line sets the rate
                time.sleep(float(1/self.rate))
            # At completion of a block, if the message was inserted, do some stuff
            if insertprint:
                statusline = line
                startpoint = cols[insertstartcol]
                endpoint = cols[insertendcol]
                midpoint = int((startpoint + endpoint) / 2)
                statusline = statusline[:startpoint-1] + "{" + "-"*(endpoint - startpoint + 1) + "}" + statusline[endpoint:-2]
                msgfound = "MESSAGE FOUND"
                print(statusline)
                if midpoint + len(msgfound) + 2 > self.width:
                    msgfound += " ^"
                    msgline = " "*(midpoint - len(msgfound)) + msgfound
                else:
                    msgfound = "^ " + msgfound
                    msgline = " "*(midpoint) + msgfound
                print(msgline)
                for t in range(4):
                    print("")
                    time.sleep(1)


if __name__ == "__main__":
    bg = matbg(rate=100)
    bg.genDummyStreams()
    bg.insert("Merry Christmas ya filthy animal")
    bg.run()