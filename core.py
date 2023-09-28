import pandas as pd
import shutil
import gzip


def extract_ref_info(ref_file_path):
    with open(ref_file_path, "r") as f:
        lines = f.readlines()

    last_numbers = [int(line.split()[-1]) for line in lines]
    txt_delimiters = [0]
    for num in last_numbers:
        txt_delimiters.append(txt_delimiters[-1] + num)

    txt_delimiters_with_last = txt_delimiters + [
        txt_delimiters[-1] + (txt_delimiters[-1] - txt_delimiters[-2])
    ]
    column_names = [line[3:].split()[0] for line in lines]

    return txt_delimiters_with_last, column_names

def extract_only_delimiters(ref_file):
    with open(ref_file, "r") as f:
        lines = f.readlines()

    last_numbers = [int(line.split()[-1]) for line in lines]
    txt_delimiters = [0]
    for num in last_numbers:
        txt_delimiters.append(txt_delimiters[-1] + num)

    txt_delimiters_str = [str(x) for x in txt_delimiters]
    txt_delimiters_joined = ",".join(txt_delimiters_str)
    
    return txt_delimiters_joined

def unzip(files, ref_file_index, txt_file_index):
    ref_gz_path = files[ref_file_index]
    ref_path = "data.REF"
    txt_gz_path = files[txt_file_index]
    txt_path = "reference.TXT"

    with gzip.open(ref_gz_path, "rb") as f_in:
        with open(ref_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    with gzip.open(txt_gz_path, "rb") as f_in:
        with open(txt_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    return ref_path, txt_path


def processa(ref, txt):
    txt_delimiters, column_names = extract_ref_info(ref)
    txt_delimiters = txt_delimiters[:-1]

    widths_with_last = [
        txt_delimiters[i + 1] - txt_delimiters[i]
        for i in range(len(txt_delimiters) - 1)
    ]
    df = pd.read_fwf(txt, widths=widths_with_last, names=column_names)
    return df

def join_multiple_excel_files(files):
    # Initialize the result DataFrame with the first file
    result_df = pd.read_excel(files[0], engine='openpyxl')
    index_col = next(col for col in result_df.columns if 'MATRICULA' in col)
    result_df.set_index(index_col, inplace=True)

    # Iteratively join each subsequent file
    for file in files[1:]:
        df_to_join = pd.read_excel(file, engine='openpyxl')
        index_col_join = next(col for col in df_to_join.columns if 'MATRICULA' in col)
        df_to_join.set_index(index_col_join, inplace=True)
        result_df = result_df.join(df_to_join, how='outer', rsuffix=f'_from_{file.name}')
    
    return result_df
