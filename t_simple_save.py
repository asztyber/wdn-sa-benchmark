from network_converter import EpanetConverter
import json
import os

input_file_name = 'examples/networks/TLN.inp'
output_folder = 'examples/structural_models'
output_name = 'TLN_simple'

EpanetConverter.network_preview(input_file_name)
epn_conv = EpanetConverter.EpanetConverter(input_file_name, ['1', '2', '3'], ['6'], ['1', '4', '6'], sensor_faults=True)
epn_conv.structural_from_epanet()

print(epn_conv.model)
print()
print(epn_conv.eq_name_map)
print()
print(epn_conv.f_name_map)

epn_conv.save_files(output_folder, output_name)
