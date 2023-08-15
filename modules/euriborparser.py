import requests as r
import datetime as dt
import pandas as pd

from bs4 import BeautifulSoup
from pathlib import Path

class EuriborParser():
    """
    This class parses historic EURIBOR Data from https://www.euribor-rates.eu/euribor-rates-by-year
    or the current 3M EURIBOR from https://www.euribor-rates.eu/en/current-euribor-rates/2/euribor-rate-3-months/
    """
    URL_HIST = 'https://www.euribor-rates.eu/en/euribor-rates-by-year'
    URL_CURR = 'https://www.euribor-rates.eu/en/current-euribor-rates/2/euribor-rate-3-months/'
    YEARS = list(range(1999,dt.datetime.today().year + 1))
    HEUTE = dt.datetime.today()

    def __init__(self, current_euribor=None):
        # I have to free the memory here, because somehow I run into troubles when running the script multiple times in a row
        self.current_euribor = None
        self.current_euribor = pd.DataFrame(columns=["3M_EURIBOR"], index=pd.DatetimeIndex([]))
        pass
    

    def parse_historic(self):
        pass

    def parse_current(self):
        """
        This function gets the most recent EURIBOR value
        """
        try:
            if EuriborParser.HEUTE.weekday() in (1,2,3,4):
                check_tag = EuriborParser.HEUTE - dt.timedelta(days=1)
            elif EuriborParser.HEUTE.weekday() in (5,6):
                check_tag = EuriborParser.HEUTE - dt.timedelta(days=EuriborParser.HEUTE.weekday()%4)
            elif EuriborParser.HEUTE.weekday() == 0:
                check_tag = EuriborParser.HEUTE - dt.timedelta(days=3)

            self.current_euribor = pd.read_csv(r"./data/current_euribor.csv", index_col=0, names=["3M_EURIBOR"])
            self.current_euribor.index = pd.to_datetime(self.current_euribor.index)
            self.current_euribor.loc[dt.datetime.strftime(check_tag, "%Y-%m-%d")]
            print("read from csv bevore exception")

        except (KeyError, FileNotFoundError):
            if dt.datetime.now().time() < dt.datetime.strptime("16:00", "%H:%M").time():
                self.current_euribor = pd.read_csv(r"./data/current_euribor.csv", index_col=0, names=["3M_EURIBOR"])
                self.current_euribor.index = pd.to_datetime(self.current_euribor.index)
                print("read from csv after exception")
            else:   
                request = r.get(EuriborParser.URL_CURR)
                soup = BeautifulSoup(request.content, 'lxml')
                current_table = soup.find('div', class_="col-12 col-lg-4 mb-3 mb-lg-0")
                first_row = current_table.find('tbody').find('tr')
                date = first_row.find_all('td')[0].text
                percentage = first_row.find_all('td')[1].text.strip().rstrip(" %")
                date = dt.datetime.strptime(date, "%m/%d/%Y")
                self.current_euribor.loc[date] = percentage
                self.current_euribor.to_csv(r"./data/current_euribor.csv", mode="a", header=False, index=True)
                self.current_euribor = pd.read_csv(r"./data/current_euribor.csv", index_col=0, names=["3M_EURIBOR"])
                print("read from Homepage")

        return self.current_euribor.tail(1)


if __name__ == "__main__":
    test = EuriborParser()
    current = test.parse_current()
    print(current)