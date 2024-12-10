import pandas as pd
import csv
import numpy as np
import json
import matplotlib.pyplot as plt

def main():
    
    #mapping = pd.read_csv('../special_blocks/game_object_blocks.csv', header=None)
    object2int = dict()
    with open('../matrix/special_blocks/game_object_blocks.csv', newline='', encoding='cp949') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            pixel = int(row[0])
            data = ' '.join(row[1:])
            object2int[data] = pixel

    array = np.zeros((98,56))
    #output = dict()
    
    with open('mapping.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        #num=0
        for row in reader:
            pixel = eval(row[0][1:-1])
            data = ' '.join(row[1:])
            
            #data = row[1:] #data = List
            
            # if output.get(data[0])==None:
            #     output[data[0]] = dict()
            # if output[data[0]].get(data[1])==None:
            #     output[data[0]][data[1]] = dict()         
            # if output[data[0]][data[1]].get(data[2])==None:
            #     output[data[0]][data[1]][data[2]] = dict()   
            
            # try:
            #     output[data[0]][data[1]][data[2]].append(data[3])
            # except:
            #     output[data[0]][data[1]][data[2]] = [data[3]]                
            #print(object2int[data])
            
            array[pixel[0]][pixel[1]] = object2int[data]
            #array[pixel[0],pixel[1]] = 32001 + num
            #num+=1
    
    plt.imshow(array.T, cmap='viridis')
    plt.colorbar()  # 컬러바 추가
    plt.show()
    
    #print(array)
    array = array.reshape(-1)
    
    str_out = ""
    for v in array:
        str_out = str_out + str(int(v)) + ', '
    str_out = str_out[:-2]
    
    with open('../matrix/maze/game_object_blocks.csv', 'w') as arena_file:
        arena_file.write(str_out)
    # with open('spatial_memory.json','w') as reader:
    #     json.dump(output,reader)
    
    #print(array)
    
if __name__=="__main__":
    main()