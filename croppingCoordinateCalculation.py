"""
Daniel Walther
creation date (dd.mm.yyyy): 18.09.2023
purpose of this file: calculate final cropping coordinates of a given specimen-individual cropping table by considering all possible edge cases (boundary conditions). Take excel table and write to excel table (at least for now/starters).

(re)sources:
https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html#importing-and-exporting-data
https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-excel
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html#pandas.DataFrame.to_excel
"""


import pandas as pd
import fileHandling as fH


if __name__ == "__main__":

    file = "dataset05-cropping-table-babb02.1,babb03-no_tail.xlsx"
    filename, extension = fH.exclude_extension_from_filename(filename_with_extension=file, delim=".")
    file_out = filename + "-suffix" + "." + extension
    # print(file)
    # print(file_out)

    table = pd.read_excel(file)  # requires installed package: openpyxl
    print(table.columns)
    # table.to_excel(file_out)g
