class Bill:
    """
    Object contains data about the bill, such as total amount and period of bill
    """

    def __init__(self, amount, period):
        self.amount = amount
        self.period = period


class Flatemate:
    """
    Creates a flatemate person who live in tha flat and pays a share of the bill.
    """

    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    def pays(self, bill, flatemate2):
        weight = self.days_in_house / (self.days_in_house + flatemate2.days_in_house)
        to_pay = bill.amount * weight
        return to_pay
