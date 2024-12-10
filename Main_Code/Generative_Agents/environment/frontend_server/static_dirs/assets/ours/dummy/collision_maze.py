import pandas as pd
import csv
import numpy as np
import json
import matplotlib.pyplot as plt

def main():
    
    array = np.zeros((98,56))
    
    array = array.reshape(-1)
    
    str_out = ""
    for v in array:
        str_out = str_out + str(int(v)) + ', '
    str_out = str_out[:-2]
    
    with open('../matrix/collision_maze.csv', 'w') as arena_file:
        arena_file.write(str_out)
    # with open('spatial_memory.json','w') as reader:
    #     json.dump(output,reader)
    
    #print(array)
    
if __name__=="__main__":
    main()