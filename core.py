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
    print(df)
    return df
