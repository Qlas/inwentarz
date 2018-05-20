from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer, TableStyle
from reportlab.pdfbase.ttfonts import TTFont, pdfmetrics
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import  stringWidth
from reportlab.platypus import PageBreak
from datetime import datetime
def zy(tab):
	class Test(object):
		""""""

		# ----------------------------------------------------------------------
		def __init__(self):
			"""Constructor"""
			pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
			pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
			#pdfmetrics.registerFont(TTFont('Dejavu-Italic', 'DejaVuSerif-Italic.ttf'))
			self.width, self.height = letter
			self.styles = getSampleStyleSheet()


		# ----------------------------------------------------------------------
		def run(self):
			"""
            Run the report
            """
			now = datetime.now()
			z = now.strftime("%Y-%m-%d")
			self.doc = SimpleDocTemplate("Inwentaryzacja " + z +".pdf")
			self.story = [Spacer(1, 0)]
			self.createLineItems()
			self.doc.build(self.story, onFirstPage=self.createDocument)
			print ("finished!")

		# ----------------------------------------------------------------------
		def createDocument(self, canvas, doc):
			"""
            Create the document
            """
			self.c = canvas
			width, height = A4
			# dodanie czcionek
			pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
			pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
			#pdfmetrics.registerFont(TTFont('Dejavu-Italic', 'DejaVuSerif-Italic.ttf'))

			# umieszczanie grafiki
			minus = 40

			# prosty tekst
			self.c.setFont("Arial", 10)
			z = "Inwentaryzacja otwarta dnia .................."
			text_width = stringWidth(z, "Arial", 10)
			self.c.drawString((width - text_width) / 2, (height - minus), z)
			minus += 60
			z = 0
			for i in range(len(tab)-1):
				z = float(z) + float(tab[i][5])
			z = round(z,2)
			q = ["Arkusz spisu z natury towarów handlowych (materiałów) sporządzony na dzień ................",
				 "Adres i nazwa jednostki inwentaryzowanej ..............................................................",
				 "Imię i nazwisko osoby odpowiedzialnej materialnie .........................",
				 "Skład komisji inwentaryzacyjnej (zespołu spisującego, imiona nazwiska, stanowiska służbowe) ...........................",
				 "Inne osoby obecne przy spisie (imiona nazwiska, stanowiska służbowe) .............................",
				 "Spis rozpoczęto dnia .................. o godzinie ..................",
				 "Ilość pozycji inwentaryzacji: " + str(len(tab)-1),
				 "Wartość inwentaryzacji: " + str(z) +" zł"]
			for q in q:
				self.c.drawString(50, (height - minus), q)
				if q == "Spis rozpoczęto dnia .................. o godzinie ..................":
					minus += 100
				else:
					minus += 30

			self.c.showPage()
		# ----------------------------------------------------------------------

		def createLineItems(self):
			"""
            Create the line items
            """
			text_data = ["Lp.", "Nazwa", "JM",
						 "Ilość", "Cena zł", "Wartość zł",
						 "Uwagi"]
			d = []
			font_size = 10
			centered = ParagraphStyle(name="centered", alignment=TA_CENTER, fontName = "Arial")
			for text in text_data:
				ptext = "<font size=%s><b>%s</b></font>" % (font_size, text)
				p = Paragraph(ptext, centered)
				d.append(p)

			data = [d]

			line_num = 1

			formatted_line_data = []
			for x in range(len(tab)-1):
				line_data = tab[x]

				for item in line_data:
					ptext = "<font size=%s>%s</font>" % (font_size - 1, item)
					p = Paragraph(ptext, centered)
					formatted_line_data.append(p)
				data.append(formatted_line_data)
				formatted_line_data = []
				line_num += 1

			table = Table(data, colWidths=[30, 200,50,50])
			table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)]))

			q = ["Spis zakończono dn. .................... o godzinie ...................",
				 "Spis zakończono na pozycji .......................",
				 "Podpis osoby sporządzaj spis ...........................",
				 "Podpis właściciela zakładu (wspólników) ..........................."]
			centered = ParagraphStyle(name="centered",  fontName="Arial", leading = 24)
			z = Paragraph(q[0], centered)
			z1 = Paragraph(q[1], centered)
			z2 = Paragraph(q[2], centered)
			z3 = Paragraph(q[3], centered)
			self.story.append(table)
			self.story.append(PageBreak())
			self.story.append(z)
			self.story.append(z1)
			self.story.append(z2)
			self.story.append(z3)

	# ----------------------------------------------------------------------
	t = Test()
	t.run()



















