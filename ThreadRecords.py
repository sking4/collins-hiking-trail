class ThreadRecords(object):
    def __init__(self, threadID=None, entries=None):
        self.__threadID = threadID
        self.__entries = entries

    def getThreadID(self):
        return self.__threadID

    def appendEntry(self, timestamp, randomNumber):
        if not self.__entries:
            self.__entries = []
        self.__entries.append([timestamp, randomNumber])

    def timestamps(self):
        # error_entry_fix = [float(issue1),float(issue2)]
        self.__entries.pop(0) # FIXME what is going on with the first 2 entries???
        self.__entries.pop(0)
        # return self.__entries
        # self.__entries.insert(0, error_entry_fix)
        return [entry[0] for entry in self.__entries if self.__entries]

    def randomNumbers(self):
        return [entry[1] for entry in self.__entries if self.__entries]
