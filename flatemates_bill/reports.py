import webbrowser

from filestack import Client
from fpdf import FPDF
import os

class PDFReport:
    """
    Creates the PDF file that contains data about the flatemates such as their name, Due amount and the period of bill.
    """

    def __init__(self, filename):
        self.filename = filename

    def generate(self, flatemate1, flatemate2, bill):
        flatemate1_pay = str(round(flatemate1.pays(bill, flatemate2), 2))
        flatemate2_pay = str(round(flatemate2.pays(bill, flatemate1), 2))

        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        # Add icon
        pdf.image("files/house.png", w=30, h=30)

        # Insert Title
        pdf.set_font(family='Times', size=24, style='B')
        pdf.cell(w=0, h=80, txt="Flatemates Bill", border=0, align="C", ln=1)

        # Insert period label and value
        pdf.set_font(family='Times', size=14, style='B')
        pdf.cell(w=100, h=40, txt="Period: ", border=0)
        pdf.cell(w=150, h=40, txt=bill.period, border=0, ln=1)

        # Insert name and amount of first flatmate
        pdf.set_font(family='Times', size=12, style='B')
        pdf.cell(w=100, h=25, txt=flatemate1.name, border=0)
        pdf.cell(w=150, h=25, txt=flatemate1_pay, border=0, ln=1)

        # Insert name and amount of second flatmate
        pdf.cell(w=100, h=25, txt=flatemate2.name, border=0)
        pdf.cell(w=150, h=25, txt=flatemate2_pay, border=0, ln=1)
        os.chdir("bills")
        pdf.output(self.filename)
        webbrowser.open(self.filename)

class Filesharer:

    def __init__(self, filepath, api_key="AvOf7xCeMTIa5bhOT4kp6z"):
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url