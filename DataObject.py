class DataObject(object):
    def __init__(self, mylist):
        super(DataObject, self).__init__()
        print("Invoking the __init__ method of the data object class")
        self.mylist = mylist
