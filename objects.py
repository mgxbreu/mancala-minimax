class Stone():

    def __init__(self):
        pass

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "O"

class Cluster():

    def __init__(self, pos, stones=None):
        if stones is None: stones = list()
        self.stones = stones
        self.pos = pos

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"POS({self.pos}) - {self.stones}"
    
    def is_store(self):
        return False
    
class Store(Cluster):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_store(self):
        return True

class Table():

    def __init__(self):
        self.clusters = self.__construct_clusters(n_stones=10)

    def __construct_clusters(self, n_clusters_pp=6, n_players=2, n_stones=4):
        clusters = []
        for j in range(n_players):
            clusters += [Store((n_clusters_pp + 1)*j)]
            clusters += [Cluster(1 + i + (n_clusters_pp + 1)*j, [Stone() for _ in range(n_stones)]) for i in range(n_clusters_pp)]
        return clusters
    
    def stream_cluster(self, cluster_id, valid_store_id):

        cluster = self.clusters[cluster_id]
        n_clusters = len(self.clusters)

        if len(cluster.stones) == 0: return

        print("CLUSTER:", cluster)

        idx = -1
        offset = 0
        limit = len(cluster.stones)
        while idx > -limit - 1 + offset:
            next_cluster = self.clusters[(cluster_id + idx)%n_clusters]
            if next_cluster.is_store() and next_cluster.pos != valid_store_id:
                offset -= 1
            else:
                next_cluster.stones.append(cluster.stones.pop())
                print(f"Appending stones to: {next_cluster}, idx: {idx}")
            idx -= 1

        #for idx in range(-1, -len(cluster.stones) - 1, -1):
            #next_cluster = self.clusters[(cluster_id + idx)%n_clusters]
            #next_cluster.stones.append(cluster.stones.pop())
            #print(f"Appending stones to: {next_cluster}, idx: {idx}")

        return next_cluster
    
    def show(self):
        for cluster in self.clusters:
            print(cluster)

class Player():

    def __init__(self, table: Table, store_id: int, cluster_ids: int):
        self.store_id = store_id
        self.cluster_ids = cluster_ids
        self.table = table

    def stream(self, cluster_id: int):
        if cluster_id not in self.cluster_ids: return
        return self.table.stream_cluster(cluster_id, self.store_id)

