class ThreadRecords(object):
    def __init__(self, threadID=None, entries=None):
        self.__threadID = int(threadID)
        self.__entries = entries

    def getThreadID(self):
        return self.__threadID

    def appendEntry(self, timestamp, randomNumber):
        if not self.__entries:
            self.__entries = []
        self.__entries.append((timestamp, randomNumber))
        # print(self.__entries)

    def timestamps(self):
        return [entry[0] for entry in self.__entries if self.__entries]

    def randomNumbers(self):
        return [entry[1] for entry in self.__entries if self.__entries]
