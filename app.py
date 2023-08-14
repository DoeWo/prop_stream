import streamlit as str

from streamlit_toggle import st_toggle_switch
from modules.kreditrechner import Tilgungsplan
from modules.euriborparser import EuriborParser

from streamlit_extras.buy_me_a_coffee import button

with str.container() as container0:
    str.title("Bruttokaufpreis ermitteln")
    kaufpreis = str.number_input("Kaufpreis: ", step=1)
    str.subheader("Kaufnebenkosten:")
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

    col1, col2 = str.columns([0.25, 0.75], gap="small")

    with col1:
        toggle = st_toggle_switch(
            label="Kaufpreis übernehmen",
            key="swicht_1",
            default_value=False,
            label_after=False
        )
    
    with col2:
        projektsumme = str.number_input(label="Projektsumme eingeben: ", step=1, value=int(bruttokaufpreis) if toggle else 0)

    eigenmittel = str.number_input(label="Eigenmittel eingeben", step=1)
    kreditbetrag = projektsumme - eigenmittel
    if kreditbetrag < 0:
        str.write("Der Kreditbetrag muss größer als 0 sein")
    else:
        str.write(f"Der Kreditbetrag ist: {kreditbetrag}")
        kreditlaufzeit = str.number_input(label="Kreditlaufzeit in Jahren eingeben: ", step=1)

        col1, col2 = str.columns([0.7,0.3])
        
        with col1:
            zinssatz = str.number_input(label="Zinssatz eingeben: ", step=0.01, help="so ungefähr 1 - 2 Aufschlag auf EURIBOR")

        with col2:
            euribor = EuriborParser()
            euribor_df = euribor.parse_current()
            str.markdown(" ")
            str.markdown(f"""3M-EURIBOR {euribor_df.index[-1].date()}:  
                         {(euribor_df.iloc[-1].values[0]):.2f}%""", help="immer der 3M EURIBOR vom Vortag")

        quartalsgebühren = str.number_input(label="Quartalsgebühren eingeben: ", step=1, value=50)

        str.subheader("Finanzierungsnebenkosten:")
        vermittlerprovision = str.number_input("Vermittlerprovision eingeben:", step=1)
        pfandrechtseintragung = str.number_input("Pfrandrechtsgebühr eingeben:", help="ist immer 1,2% von der eingetragenen Summe, normalerweise vom Kreditbetrag", step=0.01,
                                                 value=kreditbetrag*0.012)
        
        tp = Tilgungsplan(
            kreditbetrag=projektsumme, 
            kreditlaufzeitInJahren=kreditlaufzeit, 
            zinssatz=zinssatz, 
            quartalsgebuehren=quartalsgebühren,
            vermittlerprovision=vermittlerprovision,
            pfandrechtseintragung=pfandrechtseintragung).tilgungsplan_erstellen()
        rate = round(tp.rate.mean(),2)

        str.write(f"Die Kreditrate ist: {rate}")
        str.write(f"Der zurückgezahlte Gesamtbetrag ist: {(rate * kreditlaufzeit * 12):.2f}")

str.divider()

with str.container() as container2:
    str.header("Bankkenzahl DSTI")
    str.markdown("""Teil der Bonitätsprüfung einer Bank ist die Kennzahl **DSTI**.  
                 Die **DSTI** oder Debt Service to Income, ist eine Verhältniszahl und sollte sich im Bereich zwischen 0.4 und 0.5 aufhalten.  
                 Sie errechnet sich aus: Kreditrate pro Monat / Nettoeinkommen pro Monat.  
                 Wörtlich: Die Kreditrate sollte nicht mehr als 40% - 50% deines Einkommen ausmachen (je weniger desto besser)""")
    dsti = str.slider(
        label="Wie hoch soll die DSTI sein?",
        min_value=0.01, 
        max_value=1.00,
        value=0.40,
        step=0.01
    )
    str.markdown(f"""Um einen Kredit mit der oben berechneten Rate bedienen zu können und eine **DSTI von {dsti}** zu erfüllen müsstest du  
                 **{(rate/dsti):.2f}**  
                 netto pro Monat verdienen""")

    str.markdown("""**ACHTUNG** - natürlich fließen in eine Bonitätsprüfung einer Bank viel mehr Faktoren ein wie zum Beispiel:  
                 - eine positive Haushaltsrechnung  
                 - Besicherung (LTV)  
                 - Kontoverhalten  
                 - soft Facts (Dienstverhältins, ...)""")
                   
    str.markdown("""Details zu den Kennzahlen findet man bei der  
                 - **[Nationalbank](https://www.oenb.at/finanzmarkt/makroprudenzielle-aufsicht/massnahmen_und_methoden/begrenzung_systemischer_risiken_aus_der_immobilienfinanzierung.html)**  
                 - **[FMA](https://www.fma.gv.at/fma-erlaesst-verordnung-fuer-nachhaltige-vergabestandards-bei-der-finanzierung-von-wohnimmobilien-kim-vo/)**""")

str.divider()

str.subheader("Ich würde mich sehr über einen :coffee: freuen")
button(username="doedlingerT", floating=False, width=221)

str.divider()

with str.container() as container3:
    str.header(":mailbox: kontaktiere mich!")
    str.markdown("bitte schreib mir wenn du auf dem aktuellsten Stand gehalten werden willst. Nach jedem Deployment von neuen Features wirst du dann eine E-Mail erhalten")
    str.markdown('''kommende Features:    
                 **- Tilgungsplan inkl. Kreditdashboard (Export als .xlsx)**  
                 **- Zinssimulation auf Basis 3M EURIBOR (Monte Carlo)**  
                 **- Rentabilitätsrechner AirBnB**''')

    contact_form = """
    <form action="https://formsubmit.co/doedlingerwolfgang@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="https://propstream-izj4nbnvujncmstnkfdxhc.streamlit.app/">
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