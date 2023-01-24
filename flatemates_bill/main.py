from flat import Bill, Flatemate
from reports import PDFReport, Filesharer

amount = float(input("Enter the bill amount: "))
period = input("Enter the period to generate bill (e.g. April 2020): ")
name1 = input("What is your name?: ")
days_in_house1 = int(input(f"Enter the days {name1} stayed in house during bill period: "))
name2 = input("What is name of other flatemate?: ")
days_in_house2 = int(input(f"Enter the days {name2} stayed in house during bill period: "))

the_bill = Bill(amount, period)
flatemate1 = Flatemate(name1, days_in_house1)
flatemate2 = Flatemate(name2, days_in_house2)

pdf_report = PDFReport(filename=f"{the_bill.period}.pdf")
pdf_report.generate(flatemate1, flatemate2, bill=the_bill)

file_share = Filesharer(filepath=pdf_report.filename)
print(file_share.share())
