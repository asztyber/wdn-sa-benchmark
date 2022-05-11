from network_converter import EpanetConverter

configurations = [('TLN', 7, 0, 7, False),
                  ('TRN', 12, 0, 12, False),
                  ('BAK', 4, 0, 36, False),
                  ('NYT', 7, 0, 20, False),
                  ('BLA', 4, 0, 31, False),
                  ('HAN', 4, 0, 32, False),
                  ('GOY', 4, 0, 23, False),
                  ('FOS', 4, 0, 37, False),
                  ('PES', 8, 0, 22, False),
                  ('MOD', 4, 0, 55, False),
                  ('BIN', 7, 0, 26, False),
                  ('EXN', 4, 0, 38, False)]


for conf in configurations:
    epn_conv = EpanetConverter.create_random_model(*conf)
    epn_conv.save_files('examples/structural_models', conf[0])
