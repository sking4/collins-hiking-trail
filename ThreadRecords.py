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
        if self.__entries:
            return self.__entries[0]
        #return [entry[0] for entry in self.__entries if self.__entries]

    def randomNumbers(self):
        if self.__entries:
            return self.__entries[1]
        #return [entry[1] for entry in self.__entries if self.__entries]
