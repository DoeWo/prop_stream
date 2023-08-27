from deta import Deta
import datetime as dt

from streamlit import secrets

class Euribor_DB():

    def __init__(self, deta_key=None, deta_base=None):
        self.deta_connection = Deta(deta_key)
        self.deta_base = self.deta_connection.Base(deta_base)

    
    def add_euribor(self, date=None, euribor=None):
        return self.deta_base.put({"key":date, "euribor":euribor})
    
    def add_hist_euribor(self, date, euribor):
        return self.deta_base.put({"key": date, "index": "3M_EURIBOR", "value": euribor})
    
    def get_euribor(self, date:str):
        return self.deta_base.fetch(query={"key": date}).items[-1]["euribor"], self.deta_base.fetch(query={"key": date}).items[-1]["key"]



if __name__ == "__main__":
    test = Euribor_DB(deta_key=secrets["data_key"], deta_base="db_euribor")
    test.add_euribor(date="2023-08-18", euribor=3.816)
    euribor, date = test.get_euribor(date="2023-08-18")
    print(euribor, date)