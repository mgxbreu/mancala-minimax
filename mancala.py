from pygame.sprite import Group as Layer
import pygame
from pygame_objects import *

# Colores
COL_GRAY = (45, 49, 82)

FPS = 60
WIDTH, HEIGHT = 960, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MANCALA")

LAYERS = [Layer()]
BGS = []

bg1 = pygame.Surface((WIDTH, HEIGHT)).convert()
bg1.fill(COL_GRAY)

BGS.append(bg1)

table = Table((WIDTH/2, HEIGHT/2))
for cluster in table.clusters:
    LAYERS[0].add(cluster)

    for stone in cluster.stones:
        LAYERS[0].add(stone)

mancala = Mancala(table)
         
def main():

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        

        clock.tick(FPS)

        for bg in BGS:
            WIN.blit(bg, (0,0))

        current_player = mancala.get_current_player()
        
        for cluster in table.clusters:
            if cluster.is_played:
                cluster_id = cluster.get_id()
                # print(cluster_id, "sdsss")
                last_cluster = current_player.stream(cluster_id)
                print("sd", last_cluster)
                cluster.is_played = False
                table.update_table()


        for layer in LAYERS:
            layer.update()
            layer.draw(WIN)


        pygame.display.flip()

main()