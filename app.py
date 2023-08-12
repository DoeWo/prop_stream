import streamlit as str
import streamlit_extras as stre

from streamlit_toggle import st_toggle_switch
from modules.kreditrechner import Tilgungsplan

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

str.divider()

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
        zinssatz = str.number_input(label="Zinssatz eingeben: ", step=0.01)
        quartalsgebühren = str.number_input(label="Quartalsgebühren eingeben: ", step=1, value=50)

        tp = Tilgungsplan(kreditbetrag=projektsumme, kreditlaufzeitInJahren=kreditlaufzeit, zinssatz=zinssatz, quartalsgebuehren=quartalsgebühren).tilgungsplan_erstellen()
        rate = round(tp.rate.mean(),2)

        str.write(f"Die Kreditrate ist: {rate}")
        str.write(f"Der zurückgezahlte Gesamtbetrag ist: {(rate * kreditlaufzeit * 12):.2f}")

str.divider()

with str.container() as container2:
    str.header(":mailbox: kontaktiere mich!")
    str.markdown("bitte schreib mir wenn du auf dem aktuellsten Stand gehalten werden willst. Nach jedem Deployment von neuen Features wirst du dann eine E-Mail erhalten")
    str.markdown('''kommende Features:  
                 **- Bankkennzahlen (DSTI, LTV)**  
                 **- Tilgungsplan (Export als .xlsx)**  
                 **- Zinssimulation (Monte Carlo)**  
                 **- Rentabilitätsrechner AirBnB**''')

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