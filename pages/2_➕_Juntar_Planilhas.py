from core import join_multiple_excel_files
import pandas as pd
import streamlit as st
import io
import pip

pip.main(["install", "openpyxl"])

st.set_page_config(page_title="Juntar Planilhas", page_icon="➕", layout="wide")
st.title("Juntar Planilhas ➕")
st.subheader("Junte Planilhas geradas, com base na coluna 'MATRICULA'")
st.info(
    "Atenção: faça upload das planilhas .xlsx inalteradas"
)
st.info(
    "Ambas as planilhas devem possuir alguma coluna com 'MATRICULA' em seu nome"
)

if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0
buffer = io.BytesIO()

files = st.file_uploader(
    accept_multiple_files=True,
    label="Adicione os arquivos .xlsx",
    type=["xlsx"],
    key=st.session_state["file_uploader_key"],
)

if files:
    st.session_state["uploaded_files"] = files
    
    # Check if there's at least 1 file
    if len(files) >= 2:
        result_df = join_multiple_excel_files(files)  # Use the new function
        
        # Save the result_df directly to the buffer
        result_df.to_excel(buffer, engine='openpyxl')
        buffer.seek(0)  # Reset the buffer position to the beginning for reading
        
        download = st.download_button(
            label="Fazer Download da Planilha",
            data=buffer.getvalue(),
            file_name=f"planilhas_juntas.xlsx",
            mime="application/vnd.ms-excel",
        )
        if download:
            st.cache_data.clear()
            st.session_state["uploaded_files"] = False
            files = 0
    else:
        st.warning("Por favor, faça upload de pelo duas planilha.")
