import streamlit as st


st.set_page_config(page_title="Manuais e Arquivos", page_icon="🧠", layout="wide")

## Declare
url_macro = "https://cogep.notion.site/Utiliza-o-de-Macro-bb3fef3e3df448f1b04dc3f97b1f05f4"
url_dw_regional = "https://cogep.notion.site/Servidores-por-Regional-e-V-nculo-541acd6fc5094f428f9dc6bcc6ce692f"
url_pasta_macros = "https://drive.google.com/drive/folders/1oqE-1eeT9a5gnOcJYPFScWg4DACRtxbs?usp=drive_link"

st.markdown("# Manuais e Arquivos🧠")
st.write("Aproveite, jovem padawan...")

st.markdown(
    f'<a href="{url_pasta_macros}" style="display: inline-block; padding: 12px 20px; background-color: transparent; border: 1px solid pink; color: black; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px;" onmouseover="this.style.backgroundColor=\'pink\'; this.style.color=\'white\';" onmouseout="this.style.backgroundColor=\'transparent\'; this.style.color=\'black\';">Pasta com Macros 📁</a>',
    unsafe_allow_html=True
)

st.markdown(
    f'<a href="{url_macro}" style="display: inline-block; padding: 12px 20px; background-color: transparent; border: 1px solid pink; color: black; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px;" onmouseover="this.style.backgroundColor=\'pink\'; this.style.color=\'white\';" onmouseout="this.style.backgroundColor=\'transparent\'; this.style.color=\'black\';">Guia Utilização de Macro 🎰</a>',
    unsafe_allow_html=True
)

st.markdown(
    f'<a href="{url_dw_regional}" style="display: inline-block; padding: 12px 20px; background-color: transparent; border: 1px solid pink; color: black; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px;" onmouseover="this.style.backgroundColor=\'pink\'; this.style.color=\'white\';" onmouseout="this.style.backgroundColor=\'transparent\'; this.style.color=\'black\';">Guia Extração DW Regional 🧲</a>',
    unsafe_allow_html=True
)


