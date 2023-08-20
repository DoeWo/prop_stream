import requests as r
import datetime as dt
import pytz
import pandas as pd#

from bs4 import BeautifulSoup
from pathlib import Path

if __name__ == "__main__":
    from deta_base import Euribor_DB
else:
    from modules.deta_base import Euribor_DB

from streamlit import secrets

class EuriborParser():
    """
    This class parses historic EURIBOR Data from https://www.euribor-rates.eu/euribor-rates-by-year
    or the current 3M EURIBOR from https://www.euribor-rates.eu/en/current-euribor-rates/2/euribor-rate-3-months/
    """
    URL_HIST = 'https://www.euribor-rates.eu/en/euribor-rates-by-year'
    URL_CURR = 'https://www.euribor-rates.eu/en/current-euribor-rates/2/euribor-rate-3-months/'
    YEARS = list(range(1999,dt.datetime.today().year + 1))
    HEUTE = dt.datetime.today()
    TZ = pytz.timezone('Europe/Berlin')

    def __init__(self, current_euribor=None, deta_base=None):
        # I have to free the memory here, because somehow I run into troubles when running the script multiple times in a row
        self.current_euribor = pd.DataFrame(columns=["3M_EURIBOR"], index=pd.DatetimeIndex([]))
        self.deta_base = Euribor_DB(deta_key=secrets["data_key"], deta_base="db_euribor")
    

    def parse_historic(self):
        pass
    
    def parse_current(self):
        """
        This function gets the most recent EURIBOR value
        """

        if EuriborParser.HEUTE.weekday() in (1,2,3,4):
            check_tag = EuriborParser.HEUTE - dt.timedelta(days=1)
        elif EuriborParser.HEUTE.weekday() in (5,6):
            check_tag = EuriborParser.HEUTE - dt.timedelta(days=EuriborParser.HEUTE.weekday()%4)
        elif EuriborParser.HEUTE.weekday() == 0:
            check_tag = EuriborParser.HEUTE - dt.timedelta(days=3)


        try:
            query1_tag = check_tag.strftime("%Y-%m-%d")
            self.current_euribor, self.euribor_date = self.deta_base.get_euribor(date=query1_tag)
            print("read from database before exception")

        except (IndexError):
            if dt.datetime.now(EuriborParser.TZ).time() < dt.datetime.strptime("14:15", "%H:%M").time():
                query2_tag = (check_tag - dt.timedelta(days=1)).strftime("%Y-%m-%d")
                self.current_euribor, self.euribor_date = self.deta_base.get_euribor(date=query2_tag)
                print("read from csv after exception")
            else:   
                request = r.get(EuriborParser.URL_CURR)
                soup = BeautifulSoup(request.content, 'lxml')
                current_table = soup.find('div', class_="col-12 col-lg-4 mb-3 mb-lg-0")
                first_row = current_table.find('tbody').find('tr')
                date = first_row.find_all('td')[0].text
                percentage = first_row.find_all('td')[1].text.strip().rstrip(" %")
                date = dt.datetime.strptime(date, "%m/%d/%Y")

                self.current_euribor = percentage
                self.euribor_date = date.strftime("%Y-%m-%d")

                self.deta_base.add_euribor(date=self.euribor_date,
                                           euribor=self.current_euribor)

                print("read from Homepage - written to DB")

        return self.current_euribor, self.euribor_date


if __name__ == "__main__":
    test = EuriborParser()
    euribor, date = test.parse_current()
    print(euribor, date)