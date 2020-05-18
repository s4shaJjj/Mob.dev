import re
import sys


class Telephone:

    def __init__(self, filename, num, k_call, k_sms, free_call):
        self.filename = filename
        self.num = num
        self.k_call = float(k_call)
        self.k_sms = float(k_sms)
        self.free_call = float(free_call)
        pass

    def Calculate(self):
        bill_sms = 0
        bill_call = 0

        file = open(self.filename)
        lines = file.readlines()
        for line in lines:
            data = line.split(',')
            if self.num == data[1]:
                bill_call += float(data[3]) * self.k_call
                bill_sms += float(data[4]) * self.k_sms
        bill_call -= float(self.free_call) * self.k_call
        if bill_call < 0:
            bill_call = 0
        return bill_call + bill_sms

class Internet:
    def __init__(self, filename, ip):
        self.filename = filename
        self.ip = ip

    def Calculate(self):
        bill = []
        data = open(self.filename, 'r').readlines()

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

            if el[5].find(self.ip) >= 0:
                #gr.add_x(el[1])
                #gr.add_y(el[11])
                bill.append(float(el[11]))
        sum = 0
        for each in bill:
            sum += each
        return (sum / (1024) - 1000) * 0.5

tel_param=[]
int_param=[]

for i in range(1,5 + 1):
    tel_param.append(sys.argv[i])
for i in range(6,6+2):
    int_param.append(sys.argv[i])

tel = Telephone(tel_param[0],tel_param[1],tel_param[2],tel_param[3],tel_param[4]).Calculate()
inter = Internet(int_param[0],int_param[1]).Calculate()

print(tel, inter)

