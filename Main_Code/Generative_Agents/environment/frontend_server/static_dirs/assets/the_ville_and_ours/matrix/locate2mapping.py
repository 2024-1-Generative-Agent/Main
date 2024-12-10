import pandas as pd
import csv
import numpy as np
import json

def main():

    with open('spatial_memory.json','r') as reader:
        hiearchial_space = json.load(reader)

    num = 32000
            
    # Game objects
    with open('game_object_blocks.csv', 'w', newline='') as game_file:
        game_writer = csv.writer(game_file)
        for key1 in hiearchial_space.keys():
            for key2 in hiearchial_space[key1].keys():
                for key3 in hiearchial_space[key1][key2].keys():
                    for key4 in hiearchial_space[key1][key2][key3]:
                        num += 1
                        game_object = [num, key1, key2, key3, key4]
                        game_writer.writerow(game_object)

    # Arena objects
    with open('arena_blocks.csv', 'w', newline='') as arena_file:
        arena_writer = csv.writer(arena_file)
        for key1 in hiearchial_space.keys():
            for key2 in hiearchial_space[key1].keys():
                for key3 in hiearchial_space[key1][key2].keys():
                    num += 1
                    arena_object = [num, key1, key2, key3]
                    arena_writer.writerow(arena_object)


    # Sector objects
    with open('sector_blocks.csv', 'w', newline='') as sector_file:
        sector_writer = csv.writer(sector_file)
        for key1 in hiearchial_space.keys():
            for key2 in hiearchial_space[key1].keys():
                num += 1
                sector_object = [num, key1, key2]
                sector_writer.writerow(sector_object)
    

    
if __name__=="__main__":
    main()