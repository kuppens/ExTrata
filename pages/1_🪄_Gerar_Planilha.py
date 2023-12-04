import streamlit as st
import pyautogui
from core import unzip, processa
import pandas as pd
import time
import io

st.set_page_config(page_title="Gerar Planilha", page_icon="🪄", layout="wide")

# Creating a dictionary of placeholders
placeholders = {
    "title": st.empty(),
    "instruction": st.empty(),
    "alert": st.empty(),
    "alert2": st.empty(),
    "file_uploader": st.empty()
}

# Using the placeholders
placeholders["title"].title("Gerar Planilha 🪄")
placeholders["instruction"].write("Faça upload dos arquivos do Extrator, e baixe uma planilha formatada")
placeholders["alert"].info("Atenção: faça upload dos arquivos REF e TXT, ambos no formato .gz original (zipados)")

# Initialize Variables
buffer = io.BytesIO()
has_ref, has_txt = False, False
if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0

files = placeholders["file_uploader"].file_uploader(
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

if files and len(files) != 2:
    placeholders["alert2"].warning("Faça Upload dos DOIS arquivos originais do Extrator (formato REF.GZ e TXT.GZ)")
    time.sleep(5)
    st.session_state["file_uploader_key"] += 1
    st.experimental_rerun()

elif len(files) == 2 and (type_val):
    col1, col2, col3 = st.columns(3)
    with col1:
        pass
    with col2:
        ref, txt = unzip(
            files=files, ref_file_index=ref_file_index, txt_file_index=txt_file_index
        )
        df = processa(ref, txt)
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="PRINCIPAL", index=False)
            writer.close()
            # Emptying previous placeholders
            for placeholder in placeholders.values():
                placeholder.empty()
            st.title("Feshow!")
            download = st.download_button(
                label="Fazer Download da Planilha",
                data=buffer,
                file_name=f"{output_num}_tratado.xlsx",
                mime="application/vnd.ms-excel",
            )
            st.balloons()
            if download:
                st.cache_data.clear()
                st.session_state["uploaded_files"] = False
                files = 0

            another = st.button(label="Gerar Outra Planilha")

            if another:
                pyautogui.hotkey("ctrl","F5")
                
    with col3:
        pass
