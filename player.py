
# 
class Player():

    def __init__(self, store_id: int, cluster_ids: int):
        self.store_id = store_id
        self.cluster_ids = cluster_ids
        # self.table = table

    def stream(self, cluster_id: int):
        print(self.cluster_ids)
        # if cluster_id not in self.cluster_ids: return
        # return self.table.stream_cluster(cluster_id, self.store_id)