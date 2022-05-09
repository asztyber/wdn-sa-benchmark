from network_converter import EpanetConverter

input_file_name = 'examples/networks/TLN.inp'

EpanetConverter.network_preview(input_file_name)

epn_conv = EpanetConverter.EpanetConverter(input_file_name, ['1', '2', '3'], ['4', '5', '6'])

model = epn_conv.structural_from_epanet()

print(model)
print()
print(epn_conv.eq_name_map)
print()
print(epn_conv.f_name_map)
