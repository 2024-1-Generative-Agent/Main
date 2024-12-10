import pandas as pd
import csv
import numpy as np
import json

PREFIX = "special_blocks"

def update_memory(memory,word,sector,arena,game_object):

    print(word,sector,arena,game_object)
    
    if(memory[word].get(sector)==None):
        memory[word][sector] = dict()        

    if(memory[word][sector].get(arena)==None):
        memory[word][sector][arena] = list()
        
    try:
        memory[word][sector][arena].append(game_object)
    except:
        memory[word][sector][arena] = list()
        memory[word][sector][arena].append(game_object)
        
    return memory

def main():
    
    memory = dict()
    with open('old_spatial_memory.json','r') as reader:
        memory = json.load(reader)
           
    #print(memory) 
    # Game objects
    with open(f'{PREFIX}/game_object_blocks.csv', 'r') as game_file:
        data = '1'
        while(len(data)!=0):
            data = game_file.readline()
            if data.endswith('\n'):
                data = data[:-1]
            if 'Gallery' in data:
                data = data.split(',')[1:]
                
                word = data[0].strip()
                sector = data[1].strip()
                arena = data[2].strip()
                game_object = data[3].strip()
                
                memory = update_memory(memory,word,sector,arena,game_object)

                
    with open('spatial_memory.json','w') as reader:
        json.dump(memory,reader)           
    
    
if __name__=="__main__":
    main()