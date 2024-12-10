import pandas as pd
import csv
import numpy as np
import json
import matplotlib.pyplot as plt

def main():
    
    #mapping = pd.read_csv('../special_blocks/game_object_blocks.csv', header=None)
    object2int = dict()
    with open('../matrix/special_blocks/arena_blocks.csv', newline='', encoding='cp949') as csvfile:
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
        
        min_pair = [100,100]
        max_pair = [0,0]
        fill_value = 0
        
        
        prev_data = ''
        
        for row in reader:
            #print(row)
            pixel = eval(row[0][1:-1])
            pixel = [pixel[0],pixel[1]]
            #data = ' '.join(row[1:])
            data = ' '.join(row[1:-1]) #arena까지만 고려
                        
            if (data==prev_data):
                min_pair[0]=pixel[0] if min_pair[0] > pixel[0] else min_pair[0]
                min_pair[1]=pixel[1] if min_pair[1] > pixel[1] else min_pair[1]
                
                max_pair[0]=pixel[0] if max_pair[0] < pixel[0] else max_pair[0]
                max_pair[1]=pixel[1] if max_pair[1] < pixel[1] else max_pair[1]
                
                fill_value = object2int[data]
            else:
                array[min_pair[0]-1:max_pair[0]+1, min_pair[1]-1:max_pair[1]+1] = fill_value
                
                print(min_pair,max_pair)
                
                min_pair = pixel.copy()
                max_pair = pixel.copy()
                fill_value = object2int[data]
            
            prev_data = data

            array[min_pair[0]-1:max_pair[0]+1, min_pair[1]-1:max_pair[1]+1] = fill_value

            
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
            
            #array[pixel[0]][pixel[1]] = object2int[data]
            #array[pixel[0],pixel[1]] = 32001 + num
            #num+=1
    
    plt.imshow(array.T, cmap='viridis',interpolation='nearest')
    plt.colorbar()  # 컬러바 추가
    plt.show()
    
    #print(array)
    array = array.reshape(-1)
    
    str_out = ""
    for v in array:
        str_out = str_out + str(int(v)) + ', '
    str_out = str_out[:-2]
    
    with open('../matrix/maze/arena_maze.csv', 'w') as arena_file:
        arena_file.write(str_out)
    #with open('spatial_memory.json','w') as reader:
    #     json.dump(output,reader)
    
    #print(array)
    
if __name__=="__main__":
    main()