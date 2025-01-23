import csv
import numpy

class Reader:
    def __init__(self):
        with open('config/data.csv', 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            init_data = [row for row in reader]
        message_count = int(init_data[0][0])
        channel_id = init_data[0][1]

        messages = numpy.zeros((message_count,2), dtype=object)
        data_array = numpy.zeros((message_count,2,20), dtype=object)

        index = int(1)
        for x in range(message_count):
            messages[x,0] = init_data[index][0]
            ahead = int(init_data[index][1])
            messages[x,1] = ahead
            
            index = index + 1
            next_index = index + ahead
            y = int(0)
            while index < next_index:
                data_array[x,0,y] = init_data[index][0]
                data_array[x,1,y] = init_data[index][1]
                y = y + 1
                index = index + 1
        self.channel = channel_id
        self.mcount = message_count
        self.messages = messages
        self.data = data_array

def read():
    return Reader()