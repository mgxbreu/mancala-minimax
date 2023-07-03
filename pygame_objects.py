import pygame

class UIObject(pygame.sprite.Sprite):

    def __init__(self, img_path, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y
        self.img_path = img_path
        self.__load_image(self.img_path)

    def __load_image(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = (self.x, self.y)

class Button(UIObject):
    
        def __init__(self, img_path, x=0, y=0):
            super().__init__(img_path, x=x, y=y)
    
        def is_clicked(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)

class Stone(UIObject):

    def __init__(self, x, y):
        path = "images/stone.png"
        super().__init__(path, x=x, y=y)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "O"

class Cluster(UIObject):

    def __init__(self, pos, stones=None, path="images/cluster.png", x=0, y=0):
        super().__init__(path, x=x, y=y)
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
        super().__init__(path="images/store.png", *args, **kwargs)

    def is_store(self):
        return True

class Table():

    def __init__(self, pivot_pos):
        self.x, self.y = pivot_pos
        self.clusters = self.__construct_clusters(n_stones=10)

    def __construct_clusters(self, n_clusters_pp=6, n_players=2, n_stones=4):
        clusters = []
        store_padding = 350
        cluster_padding = 250
        for j in range(n_players):
            clusters += [Store((n_clusters_pp + 1)*j, x=self.x - store_padding + store_padding*2 * j, y=self.y)]
            clusters += [Cluster(1 + i + (n_clusters_pp + 1)*j, [Stone() for _ in range(n_stones)], x=self.x - cluster_padding + cluster_padding*(2/(n_clusters_pp-1)) * i, y=self.y - 100 + 100*2 * j ) for i in range(n_clusters_pp)]
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

