"""
Daniel Walther
creation date (dd.mm.yyyy): 18.09.2023
purpose of this file: calculate final cropping coordinates of a given specimen-individual cropping table by considering all possible edge cases (boundary conditions). Take excel table and write to excel table (at least for now/starters).

(re)sources:
https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html#importing-and-exporting-data
https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-excel
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html#pandas.DataFrame.to_excel
https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html#selection-by-position
"""


import pandas as pd
import fileHandling as fH


file = "dataset05-cropping-table-babb02.1,babb03-no_tail.xlsx"
# file = "dataset05-cropping-table-babb02.1,babb03-whole_organism.xlsx"
filename, extension = fH.exclude_extension_from_filename(filename_with_extension=file, delim=".")
file_out = filename + "-filled" + "." + extension
# print(file)
# print(file_out)

table = pd.read_excel(file)  # requires installed package: openpyxl
column_names = table.columns
# print(column_names)


def case2_0(table: pd.DataFrame, n: str, i: int):

    print(f"    case 2.0, i:{i}")

    # do this case (create some intermediate variables)
    row = table.iloc[i]
    n0_temp = (row[n+"0_ind"] + row[n+"1_ind"]) / 2 - dn_norm / 2
    n1_temp = (row[n+"0_ind"] + row[n+"1_ind"]) / 2 + dn_norm / 2

    # if case 2.1:
    if n0_temp < 0:
        print(f"     case 2.1")
        # do this case (adapt variables)
        n0_undershoot = abs(n0_temp)
        table.loc[i, n+"0_check"] = int(n0_temp + n0_undershoot)
        table.loc[i, n+"1_check"] = int(n1_temp + n0_undershoot)

    # else if case 2.2:
    elif n1_temp >= row[n+"_size"]:
        print(f"     case 2.2")
        # do this case (adapt variables)
        n1_overshoot = n1_temp - (row[n+"_size"] - 1)
        table.loc[i, n+"0_check"] = int(n0_temp - n1_overshoot)
        table.loc[i, n+"1_check"] = int(n1_temp - n1_overshoot)

    # finish case 2.0 if neither case 2.1 nor 2.2 were true
    else:
        print(f"     case 2.3")
        table.loc[i, n+"0_check"] = int(n0_temp)
        table.loc[i, n+"1_check"] = int(n1_temp)

    return table


def case3_1(table: pd.DataFrame, n: str, i: int):

    # TBD verify the rounding done here works for every set of individual cropping coordinates (use maths).

    n_interest = table.loc[i, n+"_interest"]
    n0_ind = table.loc[i, n+"0_ind"]
    n1_ind = table.loc[i, n+"1_ind"]
    dn_ind = table.loc[i, "d"+n+"_ind"]
    dn_norm = table.loc[i, "d"+n+"_norm"]
    dn_diff = dn_ind - dn_norm  # should always be positive, because, inside this function, there are only specimens with dn_ind > dn_norm.

    n_skew = (n_interest - n0_ind) / dn_ind
    n0_check = n0_ind + n_skew * dn_diff
    n1_check = n1_ind - (1 - n_skew) * dn_diff
    table.loc[i, n+"0_check"] = int(n0_check)  # solved the rounding problem
    table.loc[i, n+"1_check"] = int(n1_check)  # solved the rounding problem

    return table


# iterate over dimensions
dimensions = ("x", "y", "z")
for n in dimensions:
    print(f" dimension {n}")

    # calculate the individual span of every image
    table["d"+n+"_ind"] = table[n+"1_ind"] - table[n+"0_ind"]

    n_images = table.ID.count()  # number of rows (observations, specimens, images) ...in that column

    # if case 1.0 (applies to whole dataset):
    dn_max = max(table["d" + n + "_ind"])
    n_size_min = min(table[n+"_size"])
    if dn_max < n_size_min:
        print(f"  case 1.0")

        # setting dn_norm value
        dn_norm = dn_max
        table["d"+n+"_norm"] = dn_norm

        # do for every image:
        for i in range(n_images):

            # do case 2.0:
            table = case2_0(table, n, i)

    # else case 1.1 (applies to whole dataset)
    else:
        print(f"  case 1.1")

        # setting dn_norm value
        dn_norm = n_size_min - 1
        table["d"+n+"_norm"] = dn_norm

        # do for every image:
        for i in range(n_images):

            # if case 3.0:
            if table.loc[i, "d"+n+"_ind"] <= dn_norm:
                print(f"   case 3.0, i:{i}")
                # do case 2.0 (see above)
                table = case2_0(table, n, i)

            # else case 3.1:
            else:
                print(f"   case 3.1, i:{i}")
                # do this case (previously divided into three cases 4.i, presently generalised into one case optimised to more precise data (coordinates of interest) about each individual image)
                table = case3_1(table, n, i)

table.to_excel(file_out, index=False)
