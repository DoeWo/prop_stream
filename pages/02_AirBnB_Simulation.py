import json

import streamlit as str

from streamlit_lottie import st_lottie
from streamlit_extras.buy_me_a_coffee import button

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


lottie_wait = load_lottiefile(r"./lottie_files/waiting.json")

str.header("dieses Modul ist aktuell noch in Entwicklung")
st_lottie(
    lottie_wait,
    height=200,
    width=200
)

str.divider()

str.subheader("Ich würde mich sehr über einen :coffee: freuen")
button(username="doedlingerT", floating=False, width=221)

str.divider()

with str.container() as container2:
    str.header(":mailbox: bleib informiert :smile:")
    str.markdown("bitte schreib mir wenn du auf dem aktuellsten Stand gehalten werden willst. Nach jedem Deployment von neuen Features wirst du dann eine E-Mail erhalten")

    contact_form = """
    <form action="https://formsubmit.co/doedlingerwolfgang@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="https://propstream-izj4nbnvujncmstnkfdxhc.streamlit.app/AirBnB_Simulation">
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