import streamlit as st

st.set_page_config(page_title="ExTrato", page_icon="🍅", layout="wide")


co1, co2 = st.columns(2)

with co1:
    st.write("# ExTrato🍅")
    st.write("### Ferramentas do Extrator")
    st.write('Navegue pelas Ferramentas pelo menu à esquerda!')

with co2:
    st.image("https://media.tenor.com/gO5PVeNebZIAAAAi/%D1%82%D0%BE%D0%BC%D0%B0%D1%82-%D0%B4%D0%B0.gif", width=300)


