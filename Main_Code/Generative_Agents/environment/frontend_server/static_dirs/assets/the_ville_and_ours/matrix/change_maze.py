import csv
import json
import numpy as np
import cv2


IDX = 0

CHOICE = {0: ('arena_maze.csv', 'arena_blocks.csv'),
          1: ('game_object_maze.csv','game_object_blocks.csv'),
          2: ('sector_maze.csv', 'sector_blocks.csv'),
          3: ('spawning_location_maze.csv','spawning_location_blocks.csv'),
          4: ('collision_maze.csv','spawning_location_blocks.csv')} #we do not have collision_block


MAZE_POSTFIX = CHOICE[IDX][0]
INDEX_POSTFIX = CHOICE[IDX][1]

READ_LINE_NUM = 2**17

NEW_OURS_MAZE_SAVE_PATH = f'./maze/{MAZE_POSTFIX}'

OLD_VILLE_MAZE_PATH = f'./old_ville_maze/{MAZE_POSTFIX}'
OLD_OURS_MAZE_PATH = f'./old_ours_maze/{MAZE_POSTFIX}'

#-------------- for new index mapping ------------#
OLD_OURS_INDEX_PATH = f'./old_ours_maze/special_blocks/{INDEX_POSTFIX}'
NEW_OURS_INDEX_PATH = f'./special_blocks/{INDEX_POSTFIX}'
#-------------------------------------------------#

#------------- our map shape ---------------------#
VILLE_SHAPE = (100,140)#(140,100)
OURS_SHAPE = (98,56) #지금 56,98 크기로 해야 하는데 잘못 mapping했음;
#-------------------------------------------------#

def remap_index_of_ours(prev_ours:np.array) -> np.array:
    
    oldidx2newidx = dict()
    oldidx2newidx[0] = 0 #empty space
    
    new_ours_line = '-1'
    old_ours_line = '-1'
    attempt = 0
    with open(OLD_OURS_INDEX_PATH, 'r') as old_ours_reader:
        with open(NEW_OURS_INDEX_PATH, 'r') as new_ours_reader:
            while('Gallery' not in new_ours_line and attempt<1000):
                attempt+=1
                new_ours_line = new_ours_reader.readline()
            old_ours_line = old_ours_reader.readline()
            
            while(len(new_ours_line)!=0):       
                new_ours_list = new_ours_line.split(',')
                old_ours_list = old_ours_line.split(',')
                save = new_ours_list[0] #for dealing sector
                
                oldidx2newidx[int(old_ours_list[0])] = int(new_ours_list[0])
                
                new_ours_line = new_ours_reader.readline()
                old_ours_line = old_ours_reader.readline()

            while(len(old_ours_line)!=0): #for dealing sector (5 space integrated in 1 index)
                old_ours_list = old_ours_line.split(',')
                oldidx2newidx[int(old_ours_list[0])] = int(save)                
                old_ours_line = old_ours_reader.readline()
                
    
    print(oldidx2newidx)
    
    new_ours = np.vectorize(oldidx2newidx.get)(prev_ours)
        
    return new_ours

def read_matrix(MAZE_PATH, SHAPE) -> np.array:
    
    with open(MAZE_PATH, 'r') as arena_file:
        non_processed = arena_file.read(READ_LINE_NUM)
    
    processed = non_processed.split(',') #split string "0, 0, 0" into ['0','0','0']
    processed = [int(x) for x in processed] #transform type to int
    processed = np.array(processed) #for convinient, #[14000] shape

    processed = processed.reshape(SHAPE)
    
    return processed
    

def main():
    
    #----------------- read csv map and transform into 2d np array -------#
    old_ville = read_matrix(OLD_VILLE_MAZE_PATH, VILLE_SHAPE) #100,140
    old_ours = read_matrix(OLD_OURS_MAZE_PATH, OURS_SHAPE).T #98,56 -> #56,98
    #---------------------------------------------------------------------#
    
    #---------------- our target ------------------#
    #final shape: (56 + 100, 140)
    old_ours_left_padded = np.zeros((OURS_SHAPE[1],VILLE_SHAPE[1])  ) #56, 140
    old_ours_left_padded[-OURS_SHAPE[1]:,-OURS_SHAPE[0]:] = old_ours
    old_ours_left_padded = remap_index_of_ours(old_ours_left_padded)
    
    new_map = np.concatenate((old_ours_left_padded,old_ville),axis=0) # 56,140 + 100,140 -> 156,140
    assert new_map.shape == (156,140), f'size not match {new_map.shape}'
    #----------------------------------------------#

    new_map = new_map.astype(np.uint16)

    resized_new_map = cv2.resize(new_map, (new_map.shape[0]*2,new_map.shape[0]*2),cv2.INTER_LINEAR)
    cv2.imshow(f"Maze of {MAZE_POSTFIX}", resized_new_map)

    new_map = new_map.reshape(-1)

    save_string = ''
    for x in new_map:
        save_string = save_string + str(int(x)) + ', '
    save_string = save_string[:-2]

    with open(NEW_OURS_MAZE_SAVE_PATH, 'w') as new_writer:
        new_writer.write(save_string)

if __name__=='__main__':
    
    for i in range(len(CHOICE.keys())):
        IDX=i
        MAZE_POSTFIX = CHOICE[IDX][0]
        INDEX_POSTFIX = CHOICE[IDX][1]
        NEW_OURS_MAZE_SAVE_PATH = f'./maze/{MAZE_POSTFIX}'
        OLD_VILLE_MAZE_PATH = f'./old_ville_maze/{MAZE_POSTFIX}'
        OLD_OURS_MAZE_PATH = f'./old_ours_maze/{MAZE_POSTFIX}'
        OLD_OURS_INDEX_PATH = f'./old_ours_maze/special_blocks/{INDEX_POSTFIX}'
        NEW_OURS_INDEX_PATH = f'./special_blocks/{INDEX_POSTFIX}'
        main()
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()