# Create an ImageJ2 gateway with the newest available version of ImageJ2.
import imagej  # installed via 'pip install pyimagej'
import scyjava
scyjava.config.add_option('-Xmx6g')
ij = imagej.init()
"""
    raise JVMNotFoundException("No JVM shared library file ({0}) "
jpype._jvmfinder.JVMNotFoundException: No JVM shared library file (jvm.dll) found. Try setting up the JAVA_HOME environment variable properly.
"""
    # https://py.imagej.net/en/latest/Initialization.html#configuring-the-jvm

# Load an image.
image_url = 'https://imagej.net/images/clown.png'
jimage = ij.io().open(image_url)

# Convert the image from ImageJ2 to xarray, a package that adds
# labeled datasets to numpy (http://xarray.pydata.org/en/stable/).
image = ij.py.from_java(jimage)

# Display the image (backed by matplotlib).
ij.py.show(image, cmap='gray')