from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import subprocess

params = 'data.csv 933156729 2 2 20 in.txt 192.168.250.3'
params = params.split()

cmd = ['python', 'biller.py']
cmd.extend(params)
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
data = proc.communicate()[0]

print(data)

telephone = float(data.decode('ascii').split()[0])
internet = float(data.decode('ascii').split()[1])



INPUT=[
    '1',
    '2',
    '123123123', #INN
    '999999999', #kpp
    'Nikolai Rectangle', #recipient
    '1',
    '1.05',
    '20',
    'Nikolai Rectangle',  # recipient
    'Rostelecom',
    'Telephony',
    str('{:03.2f}'.format(telephone * 1.2)),
    'Internet',
    str('{:03.2f}'.format(internet * 1.2)),
    '2',
    str('{:03.2f}'.format((internet + telephone) * 1.2)),
    str('{:03.2f}'.format((internet + telephone) * 0.2)),
    str('{:03.2f}'.format((internet + telephone) * 1.2)),

]
CORDS=[
    (336,63),
    (336, 86),
    (58, 86),
    (198, 86),
    (84,121),
    (165-1,153),
    (191-1,153),
    (251,153),
    (102,198),
    (102,232),
    (66,295),
    (448,295),
    (66,320),
    (448,320),
    (44,320),
    (444,345),
    (444,358-1),
    (444,371-2)

]

packet = io.BytesIO()

# read your existing PDF
existing_pdf = PdfFileReader(open("original.pdf", "rb"))

sizex = int(existing_pdf.getPage(0).mediaBox[2])
sizey = int(existing_pdf.getPage(0).mediaBox[3])

can = canvas.Canvas(packet, pagesize=letter)
can.setFont('Times-Roman', 11)
for i in range(len(CORDS)):
    can.drawString(CORDS[i][0], sizey - CORDS[i][1], INPUT[i])
can.save()

packet.seek(0)
new_pdf = PdfFileReader(packet)

output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)

outputStream = open("final_bill.pdf", "wb")
output.write(outputStream)
outputStream.close()


#595.32
#841.92