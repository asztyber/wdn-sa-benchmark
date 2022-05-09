import wntr


class EpanetConverter():
    """
    conversion from Epanet water distribution network structure to structural model
    .inp file is imported with wntr package
    method according to:
    Sarrate, R., Nejjari, F., & Rosich, A. (2012). Sensor placement for fault diagnosis performance maximization in
    Distribution Networks. 2012 20th Mediterranean Conference on Control and Automation,
    MED 2012 - Conference Proceedings, 110–115. https://doi.org/10.1109/MED.2012.6265623
    """

    def __init__(self, input_file_name, pressure_sensors, flow_sensors, leaks=None, add_prefix=True):
        """
        Parameters:
        add_prefix (boolean): if true prefix 'P' (pipe) is added to flow variables
        and 'J' (junction) to pressure variables, needed to assure unique identifiers in the structural model
        """

        self.wn = wntr.network.WaterNetworkModel(input_file_name)
        self.G = self.wn.get_graph(self.wn)
        self.G = self.G.to_undirected()
        self.eq_cnt = -1
        self.f_cnt = -1
        self.eq_name_map = dict()
        self.f_name_map = dict()
        self.add_prefix = add_prefix

        if leaks is None:
            self.leaks = self.wn.node_name_list
        else:
            self.leaks = leaks

        if self.add_prefix:
            self.sensors = ['P' + s for s in flow_sensors] + ['J' + s for s in pressure_sensors]
            self.leaks = ['J' + leak for leak in self.leaks]
        else:
            self.sensors = flow_sensors + pressure_sensors

        try:
            self.sensors.sort(key=lambda x: (x[:1], int(x[1:])))
        except ValueError:
            print('Unexpected node name convention, sorting failed, node names are expected to be integers\
                    or integers proceeded by a single letter')

    def flow_balance_eqs(self):
        faults = []
        flow_balance_eq = dict()
        for node in self.G.nodes:
            node_name = node
            if self.add_prefix:
                node_name = 'J' + node_name
            eq_name = 'e' + node_name
            self.eq_cnt += 1
            eq = 'e' + str(self.eq_cnt)
            self.eq_name_map[eq] = eq_name
            if node_name in self.leaks:
                f_name = 'f' + node_name
                self.f_cnt += 1
                f = 'f' + str(self.f_cnt)
                self.f_name_map[f] = f_name
                faults.append(f)
                fs = [f]
            else:
                fs = []
            qis = ['P' + name if self.add_prefix else name for e in list(set(self.G.edges(node)))
                   for name in self.G.get_edge_data(*e).keys()]
            flow_balance_eq[eq] = qis + fs

        return flow_balance_eq, faults

    def pipe_eqs(self):
        pipe_eq = dict()
        for p1, p2, q in self.G.edges:
            q_name, p1_name, p2_name = q, p1, p2
            if self.add_prefix:
                q_name, p1_name, p2_name = 'P' + q, 'J' + p1, 'J' + p2
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
        return sensor_eq

    def structural_from_epanet(self):
        if self.add_prefix:
            unknown = ['J' + n for n in self.wn.node_name_list] + ['P' + link for link in self.wn.link_name_list]
        else:
            unknown = self.wn.node_name_list + self.wn.link_name_list
        known = ['m' + s for s in self.sensors]

        model = dict()
        flow_balance_eq, faults = self.flow_balance_eqs()
        model.update(flow_balance_eq)

        pipe_eq = self.pipe_eqs()
        model.update(pipe_eq)

        sensor_eq = self.sensor_eqs()
        model.update(sensor_eq)

        sa_model = {'model': model, 'unknown': unknown, 'known': known, 'faults': faults}
        return sa_model
