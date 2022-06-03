import sys
sys.path.append('.')
from wdn_sa_benchmark import EpanetConverter

# (network name, number of pressure sensors, number of flow sensors, number of faults, bool - if add sensor faults)
configurations = [('networks/TLN.inp', 2, 0, 2, False),
                  ('networks/TLN.inp', 7, 0, 7, False),
                  ('networks/TRN.inp', 12, 0, 12, False),
                  ('networks/BAK.inp', 4, 0, 36, False),
                  ('networks/NYT.inp', 7, 0, 20, False),
                  ('networks/BLA.inp', 4, 0, 31, False),
                  ('networks/HAN.inp', 4, 0, 16, False),
                  ('networks/HAN.inp', 4, 0, 32, False),
                  ('networks/GOY.inp', 4, 0, 23, False),
                  ('networks/FOS.inp', 4, 0, 37, False),
                  ('networks/PES.inp', 8, 0, 22, False),
                  ('networks/MOD.inp', 4, 0, 55, False),
                  ('networks/BIN.inp', 7, 0, 26, False),
                  ('networks/EXN.inp', 4, 0, 38, False)]


for conf in configurations:
    epn_conv = EpanetConverter(*conf, seed=0)
    epn_conv.structural_from_epanet()
    epn_conv.save_files('output')
