from objects import *

class Game:

    def __init__(self):
        self.table = Table()
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



game = Game()
game.main()