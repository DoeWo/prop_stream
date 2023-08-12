import requests as r
import datetime as dt

from bs4 import BeautifulSoup

class EuriborParser():
    """
    This class parses historic EURIBOR Data from https://www.euribor-rates.eu/euribor-rates-by-year
    or the current 3M EURIBOR from https://www.euribor-rates.eu/en/current-euribor-rates/2/euribor-rate-3-months/
    """
    URL_HIST = 'https://www.euribor-rates.eu/en/euribor-rates-by-year'
    URL_CURR = 'https://www.euribor-rates.eu/en/current-euribor-rates/2/euribor-rate-3-months/'
    YEARS = list(range(1999,dt.datetime.today().year + 1))

    def __init__(self):
        pass
    

    def parse_historic(self):
        pass

    def parse_current(self):
        """
        This function gets the most recent EURIBOR value
        """
        request = r.get(EuriborParser.URL_CURR)
        soup = BeautifulSoup(request.content, 'lxml')
        current_table = soup.find('div', class_="col-12 col-lg-4 mb-3 mb-lg-0")
        first_row = current_table.find('tbody').find('tr')
        date = first_row.find_all('td')[0].text
        percentage = first_row.find_all('td')[1].text.strip()
        result_dict = {date: percentage}
        return result_dict


if __name__ == "__main__":
    test = EuriborParser()
    current = test.parse_current()
    print(current)