import sys
import json
sys.path.append('.')
from wdn_sa_benchmark import EpanetConverter

input_file_name = 'networks/L-TOWN_simplified.inp'

pressure_sensors = ['n1', 'n4', 'n31', 'n54', 'n105', 'n114', 'n163', 'n188', 'n215', 'n229', 'n288', 'n296', 'n332',
                    'n342', 'n410', 'n415', 'n429', 'n458', 'n469', 'n495', 'n506', 'n516', 'n519', 'n549', 'n613',
                    'n636', 'n644', 'n679', 'n722', 'n726', 'n740', 'n752', 'n769', 'T1']
flow_sensors = ['PUMP_1', 'p227', 'p235']
demands = ['n1', 'n2', 'n3', 'n4', 'n6', 'n7', 'n8', 'n9', 'n10', 'n11', 'n13', 'n16', 'n17', 'n18', 'n19', 'n20',
           'n21', 'n22', 'n23', 'n24', 'n25', 'n26', 'n27', 'n28', 'n29', 'n30', 'n31', 'n32', 'n33', 'n34', 'n35',
           'n36', 'n39', 'n40', 'n41', 'n42', 'n43', 'n44', 'n45', 'n343', 'n344', 'n345', 'n346', 'n347', 'n349',
           'n350', 'n351', 'n352', 'n353', 'n354', 'n355', 'n356', 'n357', 'n358', 'n360', 'n361', 'n362', 'n364',
           'n365', 'n366', 'n367', 'n368', 'n369', 'n370', 'n371', 'n372', 'n373', 'n374', 'n375', 'n376', 'n377',
           'n378', 'n379', 'n381', 'n382', 'n383', 'n384', 'n385', 'n386', 'n387', 'n388', 'n389']

with open("networks/full_skel_node_name_map.json", "r") as file:
    full_skel_node_name_map = json.load(file)

pressure_sensors = [full_skel_node_name_map[n] for n in pressure_sensors]
demands = [full_skel_node_name_map[n] for n in demands]
demands = sorted(set(demands))

epn_conv = EpanetConverter(input_file_name, pressure_sensors=pressure_sensors, flow_sensors=flow_sensors,
                           leaks=20, sensor_faults=False, pumps=['PUMP_1'], tanks=['T1'], demands=demands,
                           pressure_prefix='', flow_prefix='')
epn_conv.structural_from_epanet()

print(epn_conv.model)
print()
print(epn_conv.eq_name_map)
print()
print(epn_conv.f_name_map)

epn_conv.save_files('output', 'L-TOWN_simplified')
