from fpdf import FPDF
import sys, json, random
import unicodedata

# Convert list object to string
def listToString(list):
	return ','.join(map(str, list))

# Open resume db
f = open('./routes/pdf/db.json', encoding="utf8")
db = json.load(f)
f.close()

# Extract raw json data from post request
info = json.loads(sys.argv[1])
studentName = listToString(info["studentName"])
email = listToString(info["email"])
education = listToString(info["education"])

# Mapping of json headers to resume headers
convert = {
	"education": "Education",
	"experience": "Work Experience",
	"programmingLanguage" : "Programming Languages",
	"techSkill" : "Technical Skills",
	"softSkill" : "Soft Skills",
	"project" : "Projects",
	"volunteering" : "Volunteering"
}

class PDF(FPDF):	
	# Name and email
	def header(self):
		self.set_font('Arial', 'B', 15)
		
		#-------------------Name--------------------
		self.cell(80)
		self.cell(30, 10, studentName, 'B', 0, 'C')
		self.ln(10)
		#------------------Email--------------------
		self.set_font('Arial', '', 14)
		self.cell(80)
		self.cell(30, 10, email, 0, 0, 'C')
		# Line Break
		self.ln(10)
		
    # Page footer
	def footer(self):
		self.set_y(-15)
		self.set_font('Arial', '', 8)
		self.cell(0, 10, str(self.page_no()), 0, 0, 'C')

def setColor(pdf):
	pdf.set_draw_color(200, 200, 200)
	pdf.set_fill_color(200, 200, 200)

def setSectionHeader(pdf, header):
	setColor(pdf)
	pdf.set_font('Arial', 'B', 12)
	pdf.cell(0, 5, header, 1, 1, 'L', True)

def checkSection(section):
	for key in convert:
		if section == convert[key]:
			return key

def getDbSize(key):
	return len(db[key])

def unicode_normalise(s):
	normalised = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
	return normalised.decode()

def populateSection(pdf, section):
	pdf.set_font('Arial', '', 12)
	if section == "Education":
		pdf.cell(30, 8, education, 0, 1, 'L')
	else:
		target = checkSection(section)
		answer = listToString(info[target])
		answers = answer.split(",")
		if len(answers) < 2:
			answerPool = getDbSize(section)
			# Special section
			if section == "Technical Skills":
				answerPool -= 1
			selectedIndex = random.randint(0, answerPool-1)
			index = str(selectedIndex)
			replacedText = db[section][index].replace('$dynamic', answer)
			completedText = "- " + unicode_normalise(replacedText)
			pdf.multi_cell(0, 8, completedText, 0, 1, 'L')
		else:
			numberOfEntries = len(answers)
			answerPool = getDbSize(section)
			# Special section
			if section == "Technical Skills":
				answerPool -= 1
			usedPool = []
			for i in range(numberOfEntries):
				selectedIndex = random.randint(0, answerPool-1)
				while selectedIndex in usedPool:
					selectedIndex = random.randint(0, answerPool-1)
				index = str(selectedIndex)
				replacedText = db[section][index].replace('$dynamic', answers[i])
				completedText = "- " + unicode_normalise(replacedText)
				pdf.multi_cell(0, 8, completedText, 0, 1, 'L')
				usedPool.append(index)
			

if __name__ == "__main__":
	pdf = PDF()
	pdf.alias_nb_pages()
	pdf.add_page()
	pdf.set_font('Arial', '', 12)
	for key, value in info.items():
		if key == "studentName" or key == "email":
			continue
		setSectionHeader(pdf, convert[key])
		populateSection(pdf, convert[key])
	pdf.output('myresume.pdf', 'F')