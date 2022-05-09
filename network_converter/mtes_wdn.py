from EpanetConverter import EpanetConverter
import faultdiagnosistoolbox as fdt
import json
import wntr
import os

'''
benchmarks downloaded from:
https://emps.exeter.ac.uk/engineering/research/cws/resources/benchmarks/design-resiliance-pareto-fronts/data-files/

Wang, Q., Guidolin, M., Savic, D. and Kapelan, Z. 2014, Two-Objective Design of Benchmark Problems of a Water
Distribution System via MOEAs: Towards the Best-Known Approximation of the True Pareto Front.
J. of Water Resources Planning and Management, doi:10.1061/(ASCE)WR.1943-5452.0000460

The benchmarks were prepared for other optimization problem - here used for fault diagnosis
'''
in_path = 'Data_and_Models/examples/wdn/networks/'
out_path = 'Data_and_Models/examples/wdn/mtes_results/'

benchmarks = ['TLN.inp', 'TRN_v1.inp', 'NYT_v1.inp', 'GOY_v1.inp', 'BLA.inp', 'HAN.inp', 'FOS_v1.inp', 'BAK_1.inp',
              'PES.inp', 'MOD.inp', 'BIN.inp', 'EXN.inp']


def calculate_mtes(input_file_name, psensor_div=1, f_div=1, mso=False):
    variant = input_file_name[:-4] + '_' + str(psensor_div) + '_' + str(f_div)
    print()
    print('---------------------------', variant, '------------------------------------')
    print()
    wn = wntr.network.WaterNetworkModel(os.path.join(in_path, input_file_name))
    print('numer of nodes: ', len(wn.node_name_list))
    print('number of pipes: ', len(wn.link_name_list))
    print('node name list from wn: ', wn.node_name_list)
    print('pipe name list from wn: ', wn.pipe_name_list)
    pressure_sensors = wn.node_name_list[::psensor_div]
    flow_sensors = []
    leaks = list(set(wn.node_name_list[::f_div] + pressure_sensors))
    epn_cnv = EpanetConverter(os.path.join(in_path, input_file_name), pressure_sensors, flow_sensors, leaks)
    data = epn_cnv.structural_from_epanet()
    with open(out_path + variant + '_sm_data.json', 'w') as f:
        json.dump(data, f)

    sm = data['model']
    print('sm: ', sm)
    relsX = [sm[e] for e in sorted(sm.keys(), key=lambda x: int(x[1:]))]
    model_def = {
        'type': 'VarStruc',
        'x': data['unknown'],
        'z': data['known'],
        'f': data['faults'],
        'rels': relsX
        }

    print('unknown: ', model_def['x'])
    print('known: ', model_def['z'])
    print('faults: ', model_def['f'])

    model = fdt.DiagnosisModel(model_def, name=input_file_name[:-4])
    model.Lint()

    mtes = model.MTES()
    print("number of TES: ", len(mtes))

    isol = model.IsolabilityAnalysisArrs(mtes)
    print('unambiguity groups: ', isol.sum(axis=1))
    with open(out_path + variant + '_unambiguity_groups.json', 'w') as f:
        json.dump([str(el) for el in list(isol.sum(axis=1))], f)

    if mso:
        msos = model.MSO()
        print("number of MSO: ", len(msos))
        msos = [[int(x) for x in list(m)] for m in msos]
        with open(out_path + variant + '_msos.json', 'w') as f:
            json.dump(msos, f)

    mtes = [[int(x) for x in list(m)] for m in mtes]
    with open(out_path + variant + '_mtes.json', 'w') as f:
        json.dump(mtes, f)
    with open(out_path + variant + '_f_name_map.json', 'w') as f:
        json.dump(epn_cnv.f_name_map, f)
    with open(out_path + variant + '_eq_name_map.json', 'w') as f:
        json.dump(epn_cnv.eq_name_map, f)

    result_stats = {
        'junctions': len(wn.node_name_list),
        'pipes': len(wn.link_name_list),
        'psensors': len(pressure_sensors),
        'faults': len(leaks),
        'mtes': len(mtes)
    }
    if mso:
        result_stats['msos'] = len(msos)
    with open(out_path + variant + '_result_stats.json', 'w') as f:
        json.dump(result_stats, f)


if __name__ == '__main__':
    # for name in benchmarks[:3] + benchmarks[4:9]:
    #    for psensor_div in range(3, 8):
    #        calculate_mtes(name, psensor_div, mso=True)

    # for psensor_div in range(5, 10):
    #     calculate_mtes('GOY_v1.inp', psensor_div, mso=True)

    # for psensor_div in [6, 8, 10]:
    #     calculate_mtes('BLA_v1.inp', psensor_div, mso=True)

    # for psensor_div in [6, 8, 10]:
    #    calculate_mtes('HAN.inp', psensor_div, mso=True)

    # for psensor_div in [6, 8, 10]:
    #     calculate_mtes('BAK_v1.inp', psensor_div)
    # for psensor_div in [6, 8, 10]:
    #    calculate_mtes('FOS_v1.inp', psensor_div)

    # calculate_mtes('PES_v1.inp', 10, 4)
    # calculate_mtes('PES_v1.inp', 13, 1)

    # calculate_mtes('MOD.inp', 70, 5)
    # calculate_mtes('BIN.inp', 70, 20)
    # calculate_mtes('EXN_v1.inp', 500, 50)

    calculate_mtes('NYT_v1.inp', 5, 1, mso=True)
