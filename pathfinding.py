import heapq
import math

class Graph():
    def __init__(self, nodes, edges):
        self.nodes = nodes # dictionary mapping id to (x, y)
        self.edges = edges # adjacency list

    def l2(self, id1, id2):
        dx = self.nodes[id1][0] - self.nodes[id2][0]
        dy = self.nodes[id1][1] - self.nodes[id2][1]
        return math.sqrt(dx * dx + dy * dy)

    def pathfind(self, source_id, dest_id):
        """
        Returns list of node ids on shortest path from source_id to dest_id
        including endpoints.
        """
        pq = [(0, source_id, source_id)] # (dist, parent, node)
        heapq.heapify(pq)
        par = {_id: None for _id in self.nodes.keys()}
        while len(pq) > 0 and par[dest_id] is None:
            dist, parent, node = heapq.heappop(pq)
            if par[node] is None:
                par[node] = parent
                for neigh in self.edges[node]:
                    heapq.heappush(pq, (dist + self.l2(node, neigh), node, neigh))
        path = []
        cur_node = dest_id
        while par[cur_node] != cur_node:
            path.append(cur_node)
            cur_node = par[cur_node]
        path.append(source_id)
        path.reverse()
        return path

if __name__ == "__main__":
    g = Graph(
        {
            0: (0, 0),
            1: (2, 2),
            2: (1, 2),
            3: (0, 2)
        },
        {
            0: [1, 3],
            1: [2],
            2: [],
            3: [2]
        }
    )
    assert(g.pathfind(0, 2) == [0, 3, 2])
    print("test passed")



