import pygame
import random
from utils import lerp

class UIObject(pygame.sprite.Sprite):

    def __init__(self, img_path, x=0, y=0,  x_scale=1, y_scale=1, alpha=False):
        super().__init__()
        self.x = x
        self.y = y
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.img_path = img_path
        self.load_image(self.img_path, alpha)
        self.held=False
        self.selectable = True

    # def __load_image(self, path):
    #     self.image = pygame.image.load(path).convert_alpha()
    #     self.rect = self.image.get_rect()
    def load_image(self, path, alpha):
        if alpha: self.base_image = pygame.image.load(path).convert_alpha()
        else: self.base_image = pygame.image.load(path).convert()
        self.__refresh_sprite()


    def update(self):
        self.rect.center = (self.x, self.y)

    def update(self):
        if self.held and self.selectable: self.on_hold()
        if self.held and not pygame.mouse.get_pressed()[0]:
            self.held = False
            self.on_realease()
        if self.is_colliding(pygame.mouse.get_pos()):
            self.on_hover()
            self.held = pygame.mouse.get_pressed()[0]
        self.__refresh_sprite()
        self.rect.center = (self.x, self.y)

    def on_click(self):
        pass

    def on_hover(self):
        pass

    def on_hold(self):
        pass

    def on_realease(self):
        pass

    def is_colliding(self, pos):
        return self.rect.collidepoint(pos)
    
    def __refresh_sprite(self):
        self.image = pygame.transform.scale(self.base_image, (self.base_image.get_width()*self.x_scale, self.base_image.get_height()*self.y_scale))
        self.rect = self.image.get_rect()

class Button(UIObject):
    
        def __init__(self, img_path, x=0, y=0,*args, **kwargs):
            super().__init__(img_path, x=x, y=y,*args, **kwargs)
    
        def is_clicked(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)

class Stone(UIObject):

    def __init__(self, path = "images/sphere.png",x=0, y=0):
        super().__init__(path, x=x, y=y, x_scale=0.008, y_scale=0.008, alpha=True)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "O"

class Cluster(Button):

    def __init__(self, pos, stones_quantity=None, path="images/cluster.png", x=0, y=0):
        super().__init__(path, x=x, y=y, x_scale=1, y_scale=1)
        if stones_quantity is None: stones_quantity = 0
        self.stones = self._construct_stones(stones_quantity)
        self.pos = pos
        self._construct_stones(stones_quantity)
        self.basex = x
        self.basey = y
        self.is_played=False

    def _construct_stones(self, stones_quantity):
        stones = []
        for i in range(stones_quantity):
            stones.append(Stone())

        stone_padding = 5
        # for i, stone in enumerate(stones):
        #     stone.x = self.x + (i - 1.5) * (stone.rect.width + stone_padding)
        #     stone.y = self.y
        # create them randomly within the cluster space
        for i, stone in enumerate(stones):
            stone.x = self.x + (i - 1.5) * (stone.rect.width + stone_padding) + (stone.rect.width + stone_padding) * (0.5 - random.random())
            stone.y = self.y + (stone.rect.height + stone_padding) * (0.5 - random.random())
        return stones

        

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"POS({self.pos}) - {self.stones}"
    
    def get_id(self):
        return self.pos
    
    def is_store(self):
        return False
    
    def get_size(self):
        return self.rect.width * self.x_scale
    
    def update_base(self):
        self.basex = self.x
        self.basey = self.y


    def update(self):
        # print("sd")
        self.x_scale = lerp(self.x_scale, 0.15, 0.1)
        self.y_scale = lerp(self.y_scale, 0.15, 0.1)

        super().update()

    def on_hover(self):
        self.on_click()
        self.x_scale = lerp(self.x_scale, 0.20, 0.1)
        self.y_scale = lerp(self.y_scale, 0.20, 0.1)

    def on_hold(self):
        self.is_played=True
        # pos = pygame.mouse.get_pos()
        # self.x = pos[0]
        # self.y = pos[1]

    def on_realease(self):
        self.x = self.basex
        self.y = self.basey

    def on_click(self):
        self.is_clicked = True

    def update_stones_position(self):
        stone_padding = 5
        # for i, stone in enumerate(self.stones):
        #     stone.x = self.x + (i - 1.5) * (stone.rect.width + stone_padding)
        #     stone.y = self.y
        # create them randomly within the cluster space
        for i, stone in enumerate(self.stones):
            stone.x = self.x + (i - 1.5) * (stone.rect.width + stone_padding) + (stone.rect.width + stone_padding) * (0.02 - random.random())
            stone.y = self.y + (stone.rect.height + stone_padding) * (0.2 - random.random())

    
class Store(Cluster):

    def __init__(self, *args, **kwargs):
        super().__init__(path="images/store.png", *args, **kwargs)

    def is_store(self):
        return True

class Table():

    def __init__(self, pivot_pos):
        self.x, self.y = pivot_pos
        self.player_quantity = 2
        self.clusters = self.__construct_clusters()

    def __construct_clusters(self, n_clusters_pp=6, n_stones=4):
        clusters = []
        store_padding = 350
        cluster_padding = 250
        for j in range(self.player_quantity):
            clusters += [Store((n_clusters_pp + 1)*j, x=self.x - store_padding + store_padding*2 * j, y=self.y)]
            clusters += [Cluster(1 + i + (n_clusters_pp + 1)*j, n_stones, x=self.x - cluster_padding + cluster_padding*(2/(n_clusters_pp-1)) * i, y=self.y - 100 + 100*2 * j ) for i in range(n_clusters_pp)]
        print("sd", clusters)
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

    def update_table(self):
        for cluster in self.clusters:
            cluster.update_stones_position()

class Player():

    def __init__(self, table: Table, store_id: int, cluster_ids: int):
        self.store_id = store_id
        self.cluster_ids = cluster_ids
        self.table = table

    def stream(self, cluster_id: int):
        if cluster_id not in self.cluster_ids: return
        return self.table.stream_cluster(cluster_id, self.store_id)

class Mancala:
    def __init__(self, table):
        self.table = table
        p1 = Player(self.table, 0, [i for i in range(1, 7)])
        p2 = Player(self.table, 7, [i for i in range(8, 14)])
        self.players = [p1, p2]
        self.turn = 0

    def get_current_player(self) -> Player:
        return self.players[self.turn]

    def main(self):

        while True:

            print(f"\nTURNO {self.turn}")

            self.table.show()
            curr_player = self.get_current_player()

            while True:
                cluster_id = int(input("Cluster to stream: "))
                last_cluster = curr_player.stream(cluster_id)
                if last_cluster is not None: break
                print("Cluster invalido !!!!!!")
            
            # Regla de doble turnos
            print(last_cluster)
            print(curr_player.store_id)
            if last_cluster.pos == curr_player.store_id:
                print("Felicidades, otro turno!!!")
                continue
            
            self.turn += 1
            if self.turn >= len(self.players): self.turn = 0

