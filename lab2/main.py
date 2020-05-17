from datetime import datetime
import matplotlib.pyplot as plt
import  matplotlib.dates
import re
from operator import itemgetter, attrgetter

def keyfunc(el):
    return el[0]

class Graph:
    def __init__(self):
        self.x = []
        self.y = []
        self.sum = 0

    def add_x(self, time):
        # time format example:
        # 2020-02-25 11:21:06.190
        time = time.split(' ')[0]
        time = re.split(r'[:.]', time)
        self.x.append(
            int(time[0]) * 3.6e+9 + # hours to mc
            int(time[1]) * 6e+7   + # mins  to mc
            int(time[2]) * 1e+6   + # sec   to mc
            int(time[3])
        )

    def add_y(self, bytes):
        self.y.append(float(bytes))

    def get_sum(self):
        for y in self.y:
            self.sum += y
        return  self.sum

    def get_divx(self):
        return [x / 1024 for x in self.x]


    def sort(self):
        xy = []
        for x,y in zip(self.x, self.y):
            xy.append((x,y))


        xy.sort(key=lambda x : x[0])
        self.x.clear()
        self.y.clear()

        for c in xy:
            self.x.append(c[0])
            self.y.append(c[1])


gr = Graph()
data = open('in.txt', 'r').readlines()
ip = '192.168.250.3'

pattern = re.compile(r'[\s]+')
for i in range(len(data)):
    data[i] = re.sub(pattern, ' ', data[i])

i = 0
for line in data:
    # line example :
    # 2020-02-25 11:21:06.190 INVALID Ignore TCP 192.168.250.3:80 -> 23.226.231.226:3682 0.0.0.0:0 -> 0.0.0.0:0 572 0

    el = line.split(' ')

    # el example (ip in tne 10th pos)
    # ['2020-02-25', '11:30:01.860', 'INVALID', '', 'Ignore', 'UDP', '', '', '', '', '192.168.250.62:58474', '->', '', '', '', '192.168.250.1:123', '', '', '', '', '', '', '', '', '', '', '', '0.0.0.0:0', '', '', '', '', '->', '', '', '', '', '', '', '', '', '', '0.0.0.0:0', '', '', '', '', '', '', '', '', '', '152', '', '', '', '', '', '', '', '0\n']

    if el[5].find(ip) >= 0:
        gr.add_x(el[1])
        gr.add_y(el[11])
gr.sort()
plt.xlabel('time, mc')
plt.ylabel('traffic, Kbytes')
plt.plot(gr.get_divx(), gr.y)
plt.show()

print('Bill : ' + str(
    (gr.get_sum() / (1024) - 1000) * 0.5
) + '₽')