import wntr
import matplotlib.pyplot as plt
import os
import json
import numpy as np


class EpanetConverter():
    """  Conversion from Epanet water distribution network structure to structural model
        .inp file is imported with wntr package
        conversion method according to:
        Sarrate, R., Nejjari, F., & Rosich, A. (2012). Sensor placement for fault diagnosis performance maximization in
        Distribution Networks. 2012 20th Mediterranean Conference on Control and Automation,
        MED 2012 - Conference Proceedings, 110–115. https://doi.org/10.1109/MED.2012.6265623

    Parameters
    ----------
    input_file_name : type
        Description of parameter `input_file_name`.
    pressure_sensors : type
        Description of parameter `pressure_sensors`.
    flow_sensors : type
        Description of parameter `flow_sensors`.
    leaks : type
        Description of parameter `leaks`.

    """

    def __init__(self, input_file_name, pressure_sensors, flow_sensors, leaks=None,
                 pressure_prefix='p', flow_prefix='q', leak_prefix='f', sensor_faults=False):

        self.wn = wntr.network.WaterNetworkModel(input_file_name)
        self.G = self.wn.get_graph(self.wn)
        self.G = self.G.to_undirected()
        self.eq_cnt = -1
        self.f_cnt = -1
        self.eq_name_map = dict()
        self.f_name_map = dict()
        self.faults = []
        self.pressure_prefix = pressure_prefix
        self.flow_prefix = flow_prefix
        self.leak_prefix = leak_prefix
        self.sensor_faults = sensor_faults

        if leaks is None:
            self.leaks = self.wn.node_name_list
        else:
            self.leaks = leaks

        flow_sensors.sort()
        pressure_sensors.sort()
        self.pressure_sensors = pressure_sensors
        self.flow_sensors = flow_sensors
        self.sensors = [flow_prefix + s for s in flow_sensors] + [pressure_prefix + s for s in pressure_sensors]

        self.model = dict()

    def flow_balance_eqs(self):
        flow_balance_eq = dict()
        for node in self.G.nodes:
            node_name = self.pressure_prefix + node
            eq_name = 'e' + node_name
            self.eq_cnt += 1
            eq = 'e' + str(self.eq_cnt)
            self.eq_name_map[eq] = eq_name
            if node in self.leaks:
                f_name = self.leak_prefix + node_name
                self.f_cnt += 1
                f = 'f' + str(self.f_cnt)
                self.f_name_map[f] = f_name
                self.faults.append(f)
                fs = [f]
            else:
                fs = []
            qis = [self.flow_prefix + name for e in list(set(self.G.edges(node)))
                   for name in self.G.get_edge_data(*e).keys()]
            flow_balance_eq[eq] = qis + fs

        return flow_balance_eq

    def pipe_eqs(self):
        pipe_eq = dict()
        for p1, p2, q in self.G.edges:
            q_name, p1_name, p2_name = self.flow_prefix + q, self.pressure_prefix + p1, self.pressure_prefix + p2
            eq_name = 'e' + q_name
            self.eq_cnt += 1
            eq = 'e' + str(self.eq_cnt)
            self.eq_name_map[eq] = eq_name
            pipe_eq[eq] = [q_name, p1_name, p2_name]

        return pipe_eq

    def sensor_eqs(self):
        sensor_eq = dict()
        for s in self.sensors:
            eq_name = 'em' + s
            self.eq_cnt += 1
            eq = 'e' + str(self.eq_cnt)
            self.eq_name_map[eq] = eq_name
            sensor_eq[eq] = [s, 'm' + s]
            if self.sensor_faults:
                f_name = 'fm' + s
                sensor_eq[eq].append(f_name)
                self.f_cnt += 1
                f = 'f' + str(self.f_cnt)
                self.f_name_map[f] = f_name
                self.faults.append(f)
        return sensor_eq

    def structural_from_epanet(self):
        unknown = [self.pressure_prefix + n for n in self.wn.node_name_list]
        unknown += [self.flow_prefix + link for link in self.wn.link_name_list]
        known = ['m' + s for s in self.sensors]

        model = dict()
        flow_balance_eq = self.flow_balance_eqs()
        model.update(flow_balance_eq)

        pipe_eq = self.pipe_eqs()
        model.update(pipe_eq)

        sensor_eq = self.sensor_eqs()
        model.update(sensor_eq)

        sa_model = {'model': model, 'unknown': unknown, 'known': known, 'faults': self.faults}
        self.model = sa_model

    def save_files(self, output_folder, network_name):
        output_name = network_name + '_' + str(len(self.pressure_sensors)) + '_' + str(len(self.flow_sensors))
        output_name = output_name + '_' + str(len(self.leaks))
        file_name = output_name + '.json'
        with open(os.path.join(output_folder, file_name), 'w') as f:
            json.dump(self.model, f)

        # name maps
        eq_name_map_file_name = output_name + '_eq_name_map.json'
        with open(os.path.join(output_folder, eq_name_map_file_name), 'w') as f:
            json.dump(self.eq_name_map, f)

        f_name_map_file_name = output_name + '_f_name_map.json'
        with open(os.path.join(output_folder, f_name_map_file_name), 'w') as f:
            json.dump(self.f_name_map, f)


def network_preview(input_file_name):
    wn = wntr.network.WaterNetworkModel(input_file_name)
    print('numer of nodes: ', len(wn.node_name_list))
    print('number of pipes: ', len(wn.link_name_list))
    print('node name list: ', wn.node_name_list)
    print('pipe name list: ', wn.pipe_name_list)

    wntr.graphics.network.plot_network(wn, node_attribute=wn.node_name_list, node_labels=True, link_labels=True,
                                       node_cmap=['lightgray'], node_size=150)
    plt.show()


def create_random_model(network_name, n_pressure_sensors, n_flow_sensors, n_leaks, sensor_faults=True,
                        input_folder='examples/networks'):
    input_file_name = network_name + '.inp'
    input_file_path = os.path.join(input_folder, input_file_name)

    wn = wntr.network.WaterNetworkModel(input_file_path)
    pressure_sensors = np.random.choice(wn.node_name_list, n_pressure_sensors, replace=False)
    flow_sensors = np.random.choice(wn.link_name_list, n_flow_sensors, replace=False)
    leaks = np.random.choice(wn.node_name_list, n_leaks, replace=False)

    epn_conv = EpanetConverter(input_file_path, pressure_sensors, flow_sensors, leaks)
    epn_conv.structural_from_epanet()
    return epn_conv
