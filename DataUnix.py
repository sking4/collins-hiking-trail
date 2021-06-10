import datetime


class DataUnix(object): # putting object uses object inheritance?
    import datetime #FIXME Where does this import go?

    def __init__(self, mylist):

        super(DataUnix, self).__init__()
        self.mylist = mylist

    def duration(self):
        return max(self.mylist) - min(self.mylist)

    def start_time(self):
        return datetime.datetime.fromtimestamp(min(self.mylist))

    def end_time(self):
        return datetime.datetime.fromtimestamp(max(self.mylist))

    def output_unix_metrics(self):
        print("\nNumber of data points: ", len(self.mylist))
        print("Duration: ", self.duration(), "seconds")
        print("Data collected from", self.start_time(), "to", self.end_time())
