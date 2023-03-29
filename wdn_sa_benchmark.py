import wntr
import matplotlib.pyplot as plt
import os
import json
import numpy as np

from typing import Optional, Union, List
from pathlib import Path


class EpanetConverter():
    """ Conversion from the Epanet water distribution network structure (.inp file) to structural analysis model
        dedicated for fault diagnosis algorithms testing and evaluation.

        The conversion method was adapted from:
        (possibilty to add sensor faults was added)
        Sarrate, R., Nejjari, F., & Rosich, A. (2012). Sensor placement for fault diagnosis performance maximization in
        Distribution Networks. 2012 20th Mediterranean Conference on Control and Automation,
        MED 2012 - Conference Proceedings, 110–115. https://doi.org/10.1109/MED.2012.6265623


    Parameters
    ----------
    input_file_name : str
        Path to the input (.inp) file with water network structure.
    pressure_sensors : Optional[Union[List, int]], default=None
        * If pressure_sensors is a list, then pressure sensors are placed in all the network nodes in the list.
        * If pressure_sensors is an int, then the given number of pressure sensors is placed in random network nodes.
        * If None, then there are no pressure sesnors.
    flow_sensors : Optional[Union[List, int]], default=None
        * If flow_sensors is a list, then flow sensors are placed in all the network pipes in the list.
        * If flow_sensors is an int, then the given number of flow sensors is placed in random network pipes.
        * If None, then there are no pressure sesnors.
    leaks : Optional[Union[List, int]], default=None
        * If leaks is a list, then leaks are possible in all the network nodes in the list.
        * If leaks is an int, then the given number of possible leaks is placed in random network nodes.
        * If None, the leaks are possible in all the network nodes.
    sensor_faults : bool, default=False
        * If True, then sensors faults are added to the model. Faults are added for all existing sensors
        (both pressure and flow)
    pumps: Optional[List], default = None,
        * List of the pipes containing pumps
    tanks: Optional[List], default = None,
        * List of the nodes containing tanks
    pressure_prefix : str, default='p'
        Prefix for pressure variables names in the model. The prefix is followed by a node id.
    flow_prefix : str, default='q'
        Prefix for flow variables names in the model. The prefix is followed by a pipe id.
    leak_prefix : default='f'
        Prefix for leak variables names in the model. The prefix is followed by a fault number.
    demand_prefix : default='d'
        Prefix for demand variables names in the model. The prefix is followed by a node id.
    seed : int, default=None
        Random generatior seed for random model generation.

    Attributes
    ----------
    wn : wntr.network.WaterNetworkModel
        water network
    G : NetworkX graph
        graph of a water network
    eq_cnt : int
        The highest equation id (equations are numbered from 0)
    f_cnt : int
        The highest fault id (faults are numbered from 0)
    eq_name_map : dict
        map of equations names
    f_name_map : dict
        map of faults names
    faults : list
        list of faults
    sensors : list
        list of sensors
    model : dict
        the structural model

    """

    def __init__(
        self,
        input_file_name: str,
        pressure_sensors: Optional[Union[List, int]] = None,
        flow_sensors: Optional[Union[List, int]] = None,
        leaks: Optional[Union[List, int]] = None,
        demands: Optional[Union[List, int]] = None,
        sensor_faults: bool = False,
        pressure_prefix: str = 'p',
        flow_prefix: str = 'q',
        leak_prefix: str = 'f',
        demand_prefix: str = 'd',
        pumps: Optional[List] = None,
        tanks: Optional[List] = None,
        seed: int = None,
    ):
        self.input_file_name = input_file_name
        self.wn = wntr.network.WaterNetworkModel(input_file_name)
        self.G = self.wn.get_graph(self.wn)
        self.G = self.G.to_undirected()

        if seed is not None:
            np.random.seed(seed)

        self.pressure_sensors = self._parse_pressure_sensors(pressure_sensors)
        self.flow_sensors = self._parse_flow_sensors(flow_sensors)
        self.demands = self._parse_demands(demands)
        self.leaks = self._parse_leaks(leaks)
        self.pumps = pumps
        self.tanks = tanks

        self.pressure_prefix = pressure_prefix
        self.flow_prefix = flow_prefix
        self.leak_prefix = leak_prefix
        self.demand_prefix = demand_prefix
        self.sensor_faults = sensor_faults

        self.eq_cnt = -1
        self.f_cnt = -1
        self.eq_name_map = dict()
        self.f_name_map = dict()
        self.faults = []
        self.sensors = [flow_prefix + s for s in self.flow_sensors] + \
            [pressure_prefix + s for s in self.pressure_sensors] + \
            [demand_prefix + s for s in self.demands]
        self.model = dict()

    def _flow_balance_eqs(self):
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
            if node in self.demands:
                d_name = self.demand_prefix + node_name
                ds = [d_name]
            else:
                ds = []
            qis = [self.flow_prefix + name for e in list(set(self.G.edges(node)))
                   for name in self.G.get_edge_data(*e).keys()]
            qis = sorted(qis)
            if self.tanks is not None and node in self.tanks:
                qis.append(node_name)
            flow_balance_eq[eq] = qis + fs + ds

        return flow_balance_eq

    def _pipe_eqs(self):
        pipe_eq = dict()
        for p1, p2, q in self.G.edges:
            q_name, p1_name, p2_name = self.flow_prefix + q, self.pressure_prefix + p1, self.pressure_prefix + p2
            eq_name = 'e' + q_name
            self.eq_cnt += 1
            eq = 'e' + str(self.eq_cnt)
            self.eq_name_map[eq] = eq_name
            if self.pumps is None or q not in self.pumps:
                pipe_eq[eq] = sorted([q_name, p1_name, p2_name])
            else:
                pipe_eq[eq] = [q_name]

        return pipe_eq

    def _sensor_eqs(self):
        sensor_eq = dict()
        for s in self.sensors:
            eq_name = 'em' + s
            self.eq_cnt += 1
            eq = 'e' + str(self.eq_cnt)
            self.eq_name_map[eq] = eq_name
            sensor_eq[eq] = [s, 'm' + s]
            if self.sensor_faults:
                f_name = 'fm' + s
                self.f_cnt += 1
                f = 'f' + str(self.f_cnt)
                sensor_eq[eq].append(f)
                self.f_name_map[f] = f_name
                self.faults.append(f)
        return sensor_eq

    def structural_from_epanet(self):
        """ Structural model calculation
        """
        unknown = [self.pressure_prefix + n for n in self.wn.node_name_list]
        unknown += [self.flow_prefix + link for link in self.wn.link_name_list]
        known = ['m' + s for s in self.sensors]

        model = dict()
        flow_balance_eq = self._flow_balance_eqs()
        model.update(flow_balance_eq)

        pipe_eq = self._pipe_eqs()
        model.update(pipe_eq)

        sensor_eq = self._sensor_eqs()
        model.update(sensor_eq)

        sa_model = {'model': model, 'unknown': unknown, 'known': known, 'faults': self.faults}
        self.model = sa_model

    def save_files(self, output_dir='.', network_name=None):
        """Saves generated model and name maps in .json files.
        The naming conversionis as follows:
        [network_name]_[number of pressure sensors]_[number of flow sensors]_[number of faults]

        Parameters
        ----------
        output_dir : str, default='.'
            Output directory
        network_name : str, default=None
            Prefix of the file names.
            If None, then the name of the input network is used.
        """
        if network_name is None:
            network_name = Path(self.input_file_name).stem

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        output_name = network_name + '_' + str(len(self.pressure_sensors)) + '_' + str(len(self.flow_sensors))
        output_name = output_name + '_' + str(len(self.leaks))
        file_name = output_name + '.json'
        with open(os.path.join(output_dir, file_name), 'w') as f:
            json.dump(self.model, f)

        # name maps
        eq_name_map_file_name = output_name + '_eq_name_map.json'
        with open(os.path.join(output_dir, eq_name_map_file_name), 'w') as f:
            json.dump(self.eq_name_map, f)

        f_name_map_file_name = output_name + '_f_name_map.json'
        with open(os.path.join(output_dir, f_name_map_file_name), 'w') as f:
            json.dump(self.f_name_map, f)

    ########################
    #   Init args processing
    def _parse_pressure_sensors(self, pressure_sensors: Optional[Union[List[str], int]]) -> List[str]:
        if pressure_sensors is None:
            return []
        elif isinstance(pressure_sensors, list):
            return sorted(pressure_sensors)
        else:
            return np.random.choice(self.wn.node_name_list, pressure_sensors, replace=False)

    def _parse_flow_sensors(self, flow_sensors: Optional[Union[List[str], int]]) -> List[str]:
        if flow_sensors is None:
            return []
        elif isinstance(flow_sensors, list):
            return sorted(flow_sensors)
        else:
            return np.random.choice(self.wn.link_name_list, flow_sensors, replace=False)

    def _parse_leaks(self, leaks: Optional[Union[List[str], int]]) -> List[str]:
        if leaks is None:
            return self.wn.node_name_list
        elif isinstance(leaks, list):
            return sorted(leaks)
        else:
            return np.random.choice(self.wn.node_name_list, leaks, replace=False)
        
    def _parse_demands(self, demands: Optional[Union[List[str], int]]) -> List[str]:
        if demands is None:
            return []
        elif isinstance(demands, list):
            return sorted(demands)
        else:
            return np.random.choice(self.wn.node_name_list, demands, replace=False)


def network_preview(input_file_name, node_labels=True, link_labels=True, node_size=150):
    """Prints basic network information and plots network structure.

    Parameters
    ----------
    input_file_name : str
        Path to the input (.inp) file with water network structure.
    node_labels : bool, default=True
        If True, then nodes are labeled with their ids.
    link_labels : bool, default=True
        If True, then nodes are labeled with their ids.
    node_size : int, default=150
        Node size
    """
    wn = wntr.network.WaterNetworkModel(input_file_name)
    print('numer of nodes: ', len(wn.node_name_list))
    print('number of pipes: ', len(wn.link_name_list))
    print('node name list: ', wn.node_name_list)
    print('pipe name list: ', wn.pipe_name_list)

    wntr.graphics.network.plot_network(wn, node_attribute=wn.node_name_list, node_labels=node_labels,
                                       link_labels=link_labels, node_size=node_size, node_cmap=['lightgray'])
    plt.show()
