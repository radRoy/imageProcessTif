"""
daniel walther
creation: 28.09.2023 (dd.mm.yyyy)

purpose: function that converts one tif image (np.ndarray) from uint16 to uint8.
core operations:
    npNdarrayUint8 = npNdarrayUint16 // 2**8
"""


import numpy as np

def convertTifUint16ToTifUint8(tif: np.ndarray):

    # if the given tif truly has bit depth of 16 (uint16), then the given np.ndarray will have dtype np.uint16 which excludes too large values by definition (I verified this by testing it here in this file - array.astype(np.uint16)).
    assert tif.max() < 2**16, "convertTifUint16ToTifUint8(tif): Expected np.array of dtype np.uint16, but at least one value is beyond this bit range/depth (max. value is 2^16 - 1, whereas the biggest value encountered was > 2^16 - 1)."

    assert tif.dtype == np.uint16, "convertTifUint16ToTifUint8(tif): Expected input tif (np.array) of dtype np.uint16 (even though values are valid, the encoding is wrong). You can try to check your input directory to solve this problem."

    tif_out = tif // 2**8
    return tif_out.astype(np.uint8)


if __name__ == "__main__":
    # print(f"{__file__}")

    tif16 = [[[0,32767,65535,65536],
              [0,32767,65535,65536]],
             [[0,32767,65535,65536],
              [0,32767,65535,65536]],
             [[0,32767,65535,65536],
              [0,32767,65535,65536]]]
    print(f"\ntif16 list:\n{tif16}")
    # tif16 = np.array(tif16)
    tif16 = np.array(tif16).astype(np.uint16)

    # tif16_multichannel = np.concatenate(([tif16], [tif16]))
    # print(tif16.shape)
    # print(tif16_multichannel.shape)

    tif8 = convertTifUint16ToTifUint8(tif16)
    print(f"\ninput array tif16:\nshape: {tif16.shape}\ndtype: {tif16.dtype}\n{tif16}")
    print(f"\noutput array tif8:\nshape: {tif8.shape}\ndtype: {tif8.dtype}\n{tif8}")
