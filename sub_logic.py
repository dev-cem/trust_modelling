import os
import json


def cumulative_fusion(opinion1, opinion2):
    b = (opinion1.b * opinion2.u + opinion2.b * opinion1.u) / (opinion1.u + opinion2.u - opinion1.u * opinion2.u)
    d = (opinion1.d * opinion2.u + opinion2.d * opinion1.u) / (opinion1.u + opinion2.u - opinion1.u * opinion2.u)
    u = (opinion1.u * opinion2.u) / (opinion1.u + opinion2.u - opinion1.u * opinion2.u)
    a = opinion1.a
    return SubLog(True, {'a': a, 'b': b, 'd': d, 'u': u})


class Graph:
    def __init__(self, my_node_id):
        self.id = my_node_id
        self.directNodes = {}
        self.indirectNodes = {}
        self.filename = (my_node_id + '_data.json')

        if not os.path.isfile(self.filename):
            value = {"data": {"node_id": my_node_id, "opinion": {}, "opinion_of": {}}}
            with open(self.filename, "w") as f:
                json.dump(value, f, indent=4)
            f.close()

    def add_direct_nodes(self, node_id, opinion):
        with open(self.filename, 'r') as f:
            data = json.load(f)

        if node_id in data['data']['opinion']:
            data["data"]["opinion"][node_id] = cumulative_fusion(opinion, SubLog(True, data["data"]["opinion"][
                node_id])).opinion_print_bdu()
        else:
            data["data"]["opinion"][node_id] = opinion.opinion_print_bdu()

        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def add_indirect_nodes(self, opinion_of, opinion_on, opinion):
        with open(self.filename, 'r') as f:
            data = json.load(f)

        key = opinion_of + " - " + opinion_on

        data["data"]["opinion_of"][key] = opinion.opinion_print_bdu()

        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def get_my_opinion(self, node_id):
        with open(self.filename) as f:
            data = json.load(f)

        for node in data['data']['opinion']:
            if node == node_id:
                a = data['data']['opinion'][node]['a']
                b = data['data']['opinion'][node]['b']
                d = data['data']['opinion'][node]['d']
                u = data['data']['opinion'][node]['u']
                return SubLog(True, {'a': a, 'b': b, 'd': d, 'u': u})

        return SubLog(True, {'a': 0.5, 'b': 0, 'd': 0, 'u': 1})

    def get_opinion_of(self, node_id, on_node):
        with open(self.filename) as f:
            data = json.load(f)

        key = str(node_id) + " - " + str(on_node)

        for node in data['data']['opinion_of']:
            if node == key:
                a = data['data']['opinion_of'][node]['a']
                b = data['data']['opinion_of'][node]['b']
                d = data['data']['opinion_of'][node]['d']
                u = data['data']['opinion_of'][node]['u']
                return SubLog(True, {'a': a, 'b': b, 'd': d, 'u': u})

        return 0

    def compute_trust(self, node_id):
        my_nodes = self.get_my_nodes()

        opinions = []
        for i in my_nodes:
            op = self.get_opinion_of(i, node_id)
            if op == 0:
                pass
            else:
                my_op = self.get_my_opinion(i)
                op = op.transitivity(my_op)
                opinions.append(op)

        if len(opinions) > 1:
            f = opinions[0]
            for o in range(len(opinions) - 1):
                f = cumulative_fusion(f, opinions[o + 1])
        elif len(opinions) == 1:
            f = opinions[0]
            f = cumulative_fusion(f, self.get_my_opinion(node_id))
        else:
            f = self.get_my_opinion(node_id)
        return f.trust()

    def print_graph(self):
        with open(self.filename) as f:
            data = json.load(f)

        print("Stored opinions on node : " + self.id)
        for value in data['data']['opinion']:
            print('My opinion on ' + str(value) + ' - - - - > ' + str(data['data']['opinion'][value]))

        for value in data['data']['opinion_of']:
            print('Opinion of ' + value[:8] + ' on ' + value[-8:] + ' - - - - > ' + str(
                data['data']['opinion_of'][value]))

    def get_my_nodes(self):
        with open(self.filename) as f:
            data = json.load(f)

        ids = []
        for node in data['data']['opinion']:
            ids.append(node)

        return ids


class SubLog:
    def __init__(self, is_opinion, data):
        if is_opinion:
            self.a = data['a']
            self.b = data['b']
            self.d = data['d']
            self.u = data['u']
            self.r = (2 * self.b) / self.u
            self.s = (2 * self.d) / self.u
        else:
            self.r = data['r']
            self.s = data['s']
            self.a = data['a']
            self.b = self.r / (self.r + self.s + 2)
            self.d = self.s / (self.r + self.s + 2)
            self.u = 2 / (self.r + self.s + 2)

    def trust(self):
        return round(self.b + self.a * self.u, 6)

    def transitivity(self, opinion1):
        b = self.b * opinion1.b
        d = self.b * opinion1.d
        u = self.d + self.u + self.b * opinion1.u
        a = self.a
        return SubLog(True, {'a': a, 'b': b, 'd': d, 'u': u})

    def opinion_print_sr(self):
        a = self.a
        r = self.r
        s = self.s
        return {'good': round(r), 'bad': round(s), 'a': a}

    def opinion_print_bdu(self):
        a = self.a
        b = self.b
        d = self.d
        u = self.u
        return {'a': a, 'b': b, 'd': d, 'u': u}
