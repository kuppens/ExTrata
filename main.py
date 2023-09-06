import streamlit as st
from core import unzip, processa
from xlsxwriter import Workbook
import pandas as pd
import time
import io

st.set_page_config(page_title="ExTrata", page_icon="🪄", layout="wide")
st.title("ExTrata")
st.subheader("Faça upload dos arquivos do Extrator, e baixe uma planilha formatada")
st.write(
    "Atenção: faça upload dos arquivos REF e TXT, ambos no formato .gz original (zipados)"
)

# Initialize Variables
has_ref, has_txt = False, False
if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0
buffer = io.BytesIO()

files = st.file_uploader(
    accept_multiple_files=True,
    label="Adicione os arquivos .gz",
    type=["gz"],
    key=st.session_state["file_uploader_key"],
)

if files:
    st.session_state["uploaded_files"] = files
    output_num = files[0].name.split(".")[0]

for i, f in enumerate(files):
    if "REF" in f.name:
        has_ref = True
        ref_file_index = i
    elif "TXT" in f.name:
        has_txt = True
        txt_file_index = i

type_val = has_ref == True and has_txt == True

if len(files) == 2 and type_val == False:
    st.write(
        "Faça o Upload apenas dos arquivos originais do Extrator (formato REF.GZ e TXT.GZ)"
    )
    time.sleep(5)
    st.session_state["file_uploader_key"] += 1
    st.experimental_rerun()

elif len(files) == 2 and (type_val):
    st.write("Iniciando Processamento 🔨")
    ref, txt = unzip(
        files=files, ref_file_index=ref_file_index, txt_file_index=txt_file_index
    )
    df = processa(ref, txt)
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        # Write each dataframe to a different worksheet.
        df.to_excel(writer, sheet_name="Sheet1", index=False)
        writer.close()
        st.write("Concluído! 🪄")
        download = st.download_button(
            label="Fazer Download da Planilha",
            data=buffer,
            file_name=f"{output_num}_tratado.xlsx",
            mime="application/vnd.ms-excel",
        )
