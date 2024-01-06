import pandas as pd
import numpy_financial as npf
import numpy as np
import datetime as dt


from dateutil.relativedelta import relativedelta

class Tilgungsplan():
    """
    This class represents an amortization schedule with a monthly timeframe

    :param kreditbetrag: the amount of the mortgage
    :type kreditbetrag: float
    :param kreditlaufzeitInJahren: the term of the mortgage in years
    :type kreditlaufzeitInJahren: int
    :param zinssatz: the interest rate per annum
    :type zinssatz: float
    :param quartalsgebühen: the fees per quarter yeahr
    :type quartalsgebuehren: float
    """

    TODAY = dt.date.today()
    START = dt.date(year=TODAY.year if TODAY.month!=12 else TODAY.year+1, 
                    month=TODAY.month+1 if TODAY.month!=12 else 1, 
                    day=1)

    def __init__(self, kreditbetrag, kreditlaufzeitInJahren, zinssatz, quartalsgebuehren, vermittlerprovision, pfandrechtseintragung):
        self.kreditlaufzeitInJahren = kreditlaufzeitInJahren
        self.zinssatz = zinssatz/100
        self.quartalsgebuehren = quartalsgebuehren
        self.vermittlerprovision = vermittlerprovision
        self.pfandrechtseintragung = pfandrechtseintragung
        self.kreditbetrag = kreditbetrag + pfandrechtseintragung + vermittlerprovision


    def tilgungsplan_erstellen(self, startdatum=START):
        """
        Calculates the annuity schedule

        :param startdatum: the date of the first annuity of the mortgage
        :param type: dtype
        :return: returns a dataframe object with the annuity information
        :rtype: pd.dataframe
        """
        self.tilgungsplan = pd.DataFrame(
            index=pd.date_range(start=startdatum, end=startdatum+relativedelta(years=self.kreditlaufzeitInJahren), freq="MS")
        )[:360]

        self.tilgungsplan["rate"] = 0.0
        self.tilgungsplan["zinszahlung"] = 0.0
        self.tilgungsplan["gebuehren"] = 0.0
        self.tilgungsplan["restsaldo"] = 0.0

        # build the first annuity schedule which will be the base for the correct annuity
        for x in range(len(self.tilgungsplan.index)):
            if x==0:
                if self.tilgungsplan.index[x].month in (3,6,9,12):
                    self.tilgungsplan["zinszahlung"][x] = round(self.kreditbetrag * (self.zinssatz/4),2)
                    self.tilgungsplan["gebuehren"][x] = self.quartalsgebuehren
                self.tilgungsplan["rate"][x] = round(-npf.pmt(self.zinssatz/12, self.kreditlaufzeitInJahren*12, self.kreditbetrag), 2)
                self.tilgungsplan["restsaldo"][x] = self.kreditbetrag - self.tilgungsplan["rate"][x] + self.tilgungsplan["zinszahlung"][x] + self.tilgungsplan["gebuehren"][x]
            else:
                if self.tilgungsplan.index[x].month in (3,6,9,12):
                    self.tilgungsplan["zinszahlung"][x] = round(self.tilgungsplan["restsaldo"][x-1] * (self.zinssatz/4),2)
                    self.tilgungsplan["gebuehren"][x] = self.quartalsgebuehren
                if self.tilgungsplan["rate"][x-1] > self.tilgungsplan["restsaldo"][x-1]:
                    self.tilgungsplan["rate"][x] = self.tilgungsplan["restsaldo"][x-1]
                    self.tilgungsplan["restsaldo"][x] = self.tilgungsplan["restsaldo"][x-1] - self.tilgungsplan["rate"][x] + self.tilgungsplan["zinszahlung"][x] + self.tilgungsplan["gebuehren"][x]
                else:
                    self.tilgungsplan["rate"][x] = round(-npf.pmt(self.zinssatz/12, (self.kreditlaufzeitInJahren*12)-(x), self.tilgungsplan["restsaldo"][x-1]), 2)
                    self.tilgungsplan["restsaldo"][x] = self.tilgungsplan["restsaldo"][x-1]  - self.tilgungsplan["rate"][x] + self.tilgungsplan["zinszahlung"][x] + self.tilgungsplan["gebuehren"][x]

        mean_annuity = round(self.tilgungsplan.rate.mean(),2)

        for x in range(len(self.tilgungsplan.index)):
            if x==0:
                if self.tilgungsplan.index[x].month in (3,6,9,12):
                    #self.tilgungsplan["zinszahlung"][x] = round(self.kreditbetrag * (self.zinssatz/4),2)
                    self.tilgungsplan["gebuehren"][x] = self.quartalsgebuehren
                self.tilgungsplan["rate"][x] = mean_annuity
                self.tilgungsplan["restsaldo"][x] = self.kreditbetrag - self.tilgungsplan["rate"][x] + self.tilgungsplan["zinszahlung"][x] + self.tilgungsplan["gebuehren"][x]
            else:
                if self.tilgungsplan.index[x].month in (3,6,9,12):
                    #self.tilgungsplan["zinszahlung"][x] = round(self.tilgungsplan["restsaldo"][x-1] * (self.zinssatz/4),2)
                    self.tilgungsplan["gebuehren"][x] = self.quartalsgebuehren
                if self.tilgungsplan["rate"][x-1] > self.tilgungsplan["restsaldo"][x-1]:
                    self.tilgungsplan["rate"][x] = self.tilgungsplan["restsaldo"][x-1]
                    self.tilgungsplan["restsaldo"][x] = self.tilgungsplan["restsaldo"][x-1] - self.tilgungsplan["rate"][x] + self.tilgungsplan["zinszahlung"][x] + self.tilgungsplan["gebuehren"][x]
                else:
                    self.tilgungsplan["rate"][x] = mean_annuity
                    self.tilgungsplan["restsaldo"][x] = self.tilgungsplan["restsaldo"][x-1]  - self.tilgungsplan["rate"][x] + self.tilgungsplan["zinszahlung"][x] + self.tilgungsplan["gebuehren"][x]


        return self.tilgungsplan


class finrech():

    def __init__(self, in_p, inter, period):
        self.in_p = in_p
        self.inter = inter
        self.period = period

    def calc_tot_payments(self):
        total = 0 
        current_payment = self.in_p

        for per in range(1, self.period + 1):
            total += current_payment
            if per % 12 == 0:
                current_payment += current_payment * (self.inter / 100)
        
        return total


if __name__ == "__main__":
    test = Tilgungsplan(100000, 30, 3.5, 50)
    tilgungsplan = test.tilgungsplan_erstellen()
    print(tilgungsplan)
    print(round(tilgungsplan.rate.mean(),2))
    print(tilgungsplan.rate.values)