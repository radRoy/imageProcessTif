# https://pyyaml.org/wiki/PyYAMLDocumentation

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open('H:/cloud/configs/pytorch-3dunet 1.6.0/DW-3DUnet_lightsheet_boundary/train_config_testing.yml', "r") as yaml_in:
    data = load(stream=yaml_in, Loader=Loader)
    print(f"{data=}")  # an orderly, nested dictionary
    output = dump(data=data, Dumper=Dumper)
    print(f"{output=}")
    print(output)
