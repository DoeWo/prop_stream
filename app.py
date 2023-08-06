import streamlit as str
import streamlit_extras as stre
import numpy as np
import pandas as pd
import numpy_financial as npf

from streamlit_toggle import st_toggle_switch
from dateutil.relativedelta import relativedelta

with str.container() as container0:
    str.title("Bruttokaufpreis ermitteln")
    kaufpreis = str.number_input("Kaufpreis: ", step=1)
    grundbuchseintragung = str.number_input("Grundbuchseintragung in %:", step=0.01, value=1.1)
    grunderwerbssteuer = str.number_input("Grunderwerbssteuer in %:", step=0.01, value=3.5)
    maklerprovision = str.number_input("Maklerprovision in %:", step=0.01, value=3.6)
    kaufvertrag = str.number_input("Kaufvertragskosten: ", step=1)
    
    bruttokaufpreis = round(
        kaufpreis
        + (kaufpreis * (grundbuchseintragung/100))
        + (kaufpreis * (grunderwerbssteuer/100))
        + (kaufpreis * (maklerprovision/100))
        + kaufvertrag,
        2
    )

    str.write(f"der Bruttokaufpreis ist: {bruttokaufpreis}")



with str.container() as container1:
    str.title("Kreditrechner")
    toggle = st_toggle_switch(
        label="Kaufpreis übernehmen",
        key="swicht_1",
        default_value=False,
        label_after=False
    )
    
    projektsumme = str.number_input(label="Projektsumme eingeben: ", step=1, value=int(bruttokaufpreis) if toggle else 0)
    eigenmittel = str.number_input(label="Eigenmittel eingeben", step=1)
    kreditbetrag = projektsumme - eigenmittel
    if kreditbetrag < 0:
        str.write("Der Kreditbetrag muss größer als 0 sein")
    else:
        str.write(f"Der Kreditbetrag ist: {kreditbetrag}")
        kreditlaufzeit = str.number_input(label="Kreditlaufzeit in Jahren eingeben: ", step=1)
        zinssatz = str.number_input(label="Zinssatz eingeben: ", step=0.01)/100

        rate = round(-npf.pmt(zinssatz/12, kreditlaufzeit*12, kreditbetrag),2)

        str.write("Die Kreditrate ist:", rate)


with str.container() as container2:
    str.header(":mailbox: kontaktiere mich!")

    contact_form = """
    <form action="https://formsubmit.co/doedlingerwolfgang@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Dein Name" required>
        <input type="email" name="email" placeholder="Deine E-Mail" required>
        <textarea name="message" placeholder="Deine Nachricht hier"></textarea>
        <button type="submit">Send</button>
    </form>
    """

    str.markdown(contact_form, unsafe_allow_html=True)
    def local_css(file_name):
        with open(file_name) as f:
            str.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    local_css(r"./style/style.css")