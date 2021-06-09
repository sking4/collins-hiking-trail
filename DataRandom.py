class DataRandom(object):
    def __init__(self, mylist):
        super(DataRandom, self).__init__()
        self.mylist = mylist

    def output_randnum_metrics(self):
        # Range
        randnum_min = min(self.mylist)
        randnum_max = max(self.mylist)
        print("\nRandom numbers generated from", randnum_min, "to", randnum_max)

        # Sort randomly generated numbers
        while True:
            sorted_list_print = input("Print sorted list of randomly generated numbers? Yes or no: ")
            if sorted_list_print.lower() == "yes":
                list_formatted = ["{:e}".format(elem) for elem in self.mylist]
                print("The randomly generated numbers sorted from smallest to largest are:\t",
                      *sorted(list_formatted), sep='\n\t')
                break
            elif sorted_list_print.lower() == "no":
                break
            else:
                print("Response not recognized, try again.")
