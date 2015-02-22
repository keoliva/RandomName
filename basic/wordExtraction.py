import re
from datetime import datetime

def ExamString (text, examsList, ExamKeys):
	flag = False
	for key in ExamKeys:   # go through the list of the keys
		if key in text:      # if the key is found in that string
			examsList = examsList + [text[text.find(key):]]
			flag = True
	return (flag, examsList)

def AssignmentString(text, assList, AssKeys):
	flag = False
	for key in AssKeys:   # go through the list of the keys
		if key in text:      # if the key is found in that string
			assList = assList + [text[text.find(key): ]]
			flag = True
	return (flag, assList)



def textReplacement(text):
	text = text.replace("january ", " 1/")
	text = text.replace("jan ", " 1/")

	text = text.replace("february ", " 2/")
	text = text.replace("feb ", " 2/")	

	text = text.replace("march ", " 3/")
	text = text.replace("mar ", " 3/")

	text = text.replace("april ", " 4/")
	text = text.replace("apr ", " 4/")

	text = text.replace("may ", " 5/")

	text = text.replace("june ", " 6/")
	text = text.replace("jun ", " 6/")

	text = text.replace("july ", " 7/")

	text = text.replace("august ", " 8/")
	text = text.replace("aug ", " 8/")

	text = text.replace("september ", " 9/")
	text = text.replace("sept ", " 9/")
	text = text.replace("sep ", " 9/")

	text = text.replace("october ", " 10/")
	text = text.replace("oct ", " 10/")

	text = text.replace("november ", " 11/")
	text = text.replace("nov ", " 11/")

	text = text.replace("decemeber ", " 12/")
	text = text.replace("dec ", " 12/")
	return text

def getDate(text):
	
	text = textReplacement(text)

	

	match = re.search(r'\d*/\d*', text)
	year = datetime.now().year

	try:
		date = datetime.strptime(str(year) + "/" + match.group(), '%Y/%m/%d').date()
		date = date.strftime("%m/%d/%Y")
		return (True, date)
	except:
		a = 0

	return (False, None)



def checkCalendarSection(line, calendarKeys):
	for i in calendarKeys:
		if (i in line):
			return True
	return False




def main(allText):

# MAIN CODE
#with open ("newsyllabus.txt") as FILE:

	#l = list(FILE)
	
	l = allText.split("\n")
	# the list to holds the exams and the assignemnts
	examsList = []
	assList = []

	# the lists for the keywords of exams and the assignments
	ExamKeys = ["exam ", "test ", "midterm ", "mid term ", "mid-term ", "quiz "]
	AssKeys = ["homework ", "assignment ", "assignments ", " problem set ", " problemset ", "lab ", "paper "]
	CalendarKeys = ["calendar\n", "schedule\n", "outline\n", "calendar:\n"]

	calendarSection = False; # a flag that we are in the calendarSection
	dateFound = False  # a flag when the date is found to handle the multi-line cases

	prevDate = None  # initializing the date to None till we encounter a date

	for line in l:

		# pre-processing for the line
		line = line.lower()
		line = line.replace("\t", " ")

		# If we reached to the calendar section set the flag to true
		if (checkCalendarSection(line, CalendarKeys)):
			calendarSection = True

		line = line.replace("\n", "")

		# If we are in the calendar section start getting the information
		if (calendarSection):
			
			(dateFlag, date) = getDate(line)

			if (dateFlag == True):
				dateFound = True
				prevDate = date

				#line = ' '.join(line2[1:])

			# examsFlag to check if there was an exams keyword
			(examsFlag, examsListTemp) = ExamString (line, [], ExamKeys)
			(assFlag, assListTemp) = AssignmentString(line, [], AssKeys)

			if (examsFlag == True and prevDate != None):
				examsList = examsList + [(str(prevDate), examsListTemp[0])]
			elif (assFlag == True and prevDate != None):
				assList = assList + [(str(prevDate), assListTemp[0])]

	
	return (assList, examsList)

