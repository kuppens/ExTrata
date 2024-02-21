import streamlit as st

st.set_page_config(page_title="ExTrato", page_icon="🍅", layout="wide")


co1, co2 = st.columns(2)

with co1:
    st.write("# ExTrato")
    st.write("### Ferramentas do Extrator")

    st.write('Navegue pelas Ferramentas pelo menu à esquerda!')

with co2:
    st.write("![Era para ter um GIF aqui...](https://media.tenor.com/F2PjYZeqkt8AAAAi/tomato.gif)")

