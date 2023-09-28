import streamlit as st
from time import sleep
import gzip
import shutil
from core import extract_only_delimiters

st.set_page_config(page_title="Delimitadores", page_icon="✂️", layout="wide")

st.markdown("# Gerar Delimitadores ✂️")
st.write("Gera delimitadores para inserção no Excel")
st.info('Atenção, faça o upload apenas do arquivo REF em formato .gz (zipado)')

# Inicializa
ref_path = 'data.REF'
if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0

file = st.file_uploader(
    accept_multiple_files=False,
    label="Adicione o arquivo REF em .gz",
    type=["gz"],
    key=st.session_state["file_uploader_key"],
)
if file:
    st.session_state["uploaded_files"] = file

    if "REF.gz" not in file.name:
        st.error(
            "Faça Upload apenas do arquivo REF original do Extrator (formato REF.gz zipado)"
        )
        sleep(6)
        st.session_state["file_uploader_key"] += 1
        st.experimental_rerun()
    else:
        st.write("Iniciando Processamento 🔨")
        with gzip.open(file, "rb") as f_in:
            with open(ref_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        delimiters = extract_only_delimiters(ref_path)
        st.success('Sucesso! Os delimitadores se encontram abaixo:')
        st.info(delimiters)