import numpy as np
import fileHandling as fH
import list_resolutions as lR


def minial_x(resolutions_zyx):
    a_resolutions = np.array(resolutions_zyx)
    pass


if __name__ == "__main__":

    file_paths = fH.get_file_path_list()
    resolutions = lR.list_resolutions_h5(file_paths)
    for res in resolutions:
        print(res)

    exit(0)
