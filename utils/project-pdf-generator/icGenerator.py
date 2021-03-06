# This generates pdf for projects under each IC.
# Place the csv file in the same directory with the name `ic_list.csv` and later run the script.
# Format of ic_list.csv Course Code,Course Name,IC Name,Email ID
# Format of allotement_list.csv ID NO , STUDENT NAME, FACULTY NAME, PROJECT CODE,EMAIL, ELE TYPE, PROJECT TITLE

import csv
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
#from WebKit.Page import Page
from time import strftime
from cStringIO import StringIO
import datetime
styles = getSampleStyleSheet()
 
# csv file name
filename = "ic_list.csv"
 
# initializing the titles and rows list
fields = []
rowsIC = []
 
# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
     
    # extracting field names through first row
    fields = csvreader.next()
 
    # extracting each data row one by one
    for row in csvreader:
        rowsIC.append(row)
 
    # get total number of rows
    print("Total no. of rows: %d"%(csvreader.line_num))
 
# printing the field names
print('Field names are:' + ', '.join(field for field in fields))
 
#  printing first 5 rows
print('\nFirst 5 rows are:\n')
for row in rowsIC[:6]:
    # parsing each column of a row
    for col in row:
        print("%10s , "%col),
    print('\n')

instructors = [] #  -- IC --
courselist = [] 
instructoremails = []
data = []  
for row in rowsIC :
    if row[2] in instructors:
        courselist[instructors.index(row[2])].append(row[0])
    else:
        instructors.append(row[2])
        courselist.append([row[0]])
        instructoremails.append(row[3])

#for row in courselist :
    #print row

with open('instructor_new.csv', 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
     
    # extracting field names through first row
    fields = csvreader.next()
    rows = []
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
    
i = 0


for row in courselist:
    data.append([])
    for col in row:
        for row1 in rows:
            if col.strip() == row1[3].strip():
                data[i].append(row1)
    i = i+1


# data contains list of lists . data[i] corresponds to ith instructor in instructors. 
# data[i][j] corresponds to jth project under ith instructor.

#making pdf starts 
i = 0

#print data[1]

#deleting unncecessary column
for row in data:
    for col in row:
        del col[5]
        del col[4]

for instructor in instructors :  
    instructoremail = instructoremails[instructors.index(instructor)]
    print instructoremail
    print instructor
    heading1 = "SECOND SEMESTER 2018-2019"
    name = "Dear "+ instructor+ ","
    heading2 = "LIST OF ALLOTED PROJECT STUDENTS"
    para = "The following is the allotted list of students under your project course during Second Semester 2018-19. There is a possibility that some of the allotted project students may not register for the same. The final list of registered students will be downloaded from the registration module of ERP. In case of any discrepancy, please contact the office of AUGSD (Extn: 822) or email at augsd@hyderabad.bits-pilani.ac.in."
    datetoday = datetime.datetime.today().strftime('%d-%m-%Y')
    elements = []
    footer1 = "(Prof. A. Vasan)<br/> Associate Dean <br/>"

    # title = '<para align = "centre"><font size = 18><strong>%s</strong></font></para>' % title
    ptext = '<font size=12>%s</font>' % name
    head1text = '<para align = "centre">"<font size = 18><strong>%s</strong></font></para>' % heading1
    head2text = '<para align = "centre"><font size = 18><strong>%s</strong></font></para>' % heading2
    paratext = '<para leading=22><font size=12>%s</font></para>' % para
    date = '<para align="right"><font>%s</font></para>' % datetoday
    footer = '<para align = "left"><font size = "12">%s</font></para>' % footer1
    j = 0
    im = Image("head.png", width=4*inch, height=0.75*inch)
    im.hAlign = "LEFT"
    elements.append(im)
    while j < 5 :
        elements.append(Spacer(1, 12))
        j = j+1



    elements.append(Paragraph(head1text, styles["Normal"])) 
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12)) 

    elements.append(Paragraph(head2text, styles["Normal"])) 
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12)) 

    elements.append(Paragraph(date, styles["Normal"])) 
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(ptext, styles["Normal"])) 
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph(paratext, styles["Normal"])) 

    elements.append(Spacer(1, 12)) 
    elements.append(Spacer(1, 12)) 

    doc = SimpleDocTemplate(("./IC-PDF/"+ instructoremail + ".pdf"), pagesize=letter)
    
    GRID_STYLE = TableStyle(
              [('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('ALIGN', (1,1), (-1,-1), 'LEFT')]
              )

                  
    # container for the 'Flowable' objects
    # if data[i] != []:
    if(data[i]==[]):
         print instructor
    # 	print courselist[instructors.index(instructor)]
    data[i].insert(0,['S. No','ID No.','Student Name','Name of the guide','Course Code','Title'])
    for j in range(1,len(data[i])):
        data[i][j].insert(0,str(j))
    number_of_students = len(data[i])-1

    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    data2 = [[Paragraph(cell, s) for cell in row] for row in data[i]]
    t=Table(data2,colWidths=[None,None,None,1*inch,1*inch,2.5*inch])
    t.setStyle(GRID_STYLE)
    i = i+1
    elements.append(t)

    elements.append(Spacer(1, 12)) 
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Number of students alloted to your course: "+str(number_of_students), styles["Normal"]))
    elements.append(Spacer(1, 12)) 
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(footer, styles["Normal"])) 
    doc.build(elements)
