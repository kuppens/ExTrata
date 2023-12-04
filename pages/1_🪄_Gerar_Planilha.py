import streamlit as st
from core import unzip, processa
import pandas as pd
import time
import io

st.set_page_config(page_title="Gerar Planilha", page_icon="🪄", layout="wide")
st.title("Gerar Planilha 🪄")
st.subheader("Faça upload dos arquivos do Extrator, e baixe uma planilha formatada")
st.info(
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
        "Faça Upload apenas dos arquivos originais do Extrator (formato REF.GZ e TXT.GZ)"
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
        df.to_excel(writer, sheet_name="PRINCIPAL", index=False)

        workbook  = writer.book
        worksheet = writer.sheets['PRINCIPAL']
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})

        for col_num, value in enumerate(df.columns.values):
            if value.startswith('DA-'):
                # Apply the format to the column. Excel columns start from 0
                worksheet.set_column(col_num, col_num, None, date_format)

        writer.close()
        
        st.write("Concluído! 🪄")
        download = st.download_button(
            label="Fazer Download da Planilha",
            data=buffer,
            file_name=f"{output_num}_tratado.xlsx",
            mime="application/vnd.ms-excel",
        )
        if download:
            st.cache_data.clear()
            st.session_state["uploaded_files"] = False
            files = 0
