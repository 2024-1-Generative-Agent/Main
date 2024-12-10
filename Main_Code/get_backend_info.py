import os
import json
from typing import List, Tuple, Union

MOVEMENT_DIR = "./Generative_Agents/environment/frontend_server/storage/testing1/movement"
IMAGE_DIR = "./Generative_Agents/reverie/backend_server"

def get_image_url(txt_name:str='image_description.txt') -> Union[int,List[Tuple]]:
    """
    get image information from txt file [(주어, 서술어, 보어, 설명, url), ...]
    """
    target = os.path.join(IMAGE_DIR,txt_name)
    
    if not os.path.exists(target):
        return -1

    image_info_list = list()
    with open(target, 'r', encoding='utf-8') as reader:
        for line in reader:
            image_info = tuple(line.strip().split('\t'))
            image_info_list.append(image_info)
        
    return image_info_list

def get_movement_json(step:int=0) -> Union[int,dict]:
    """
    Get specific movment.json file
    """
    target = os.path.join(MOVEMENT_DIR,f"{step}.json")
    
    if not os.path.exists(target):
        return -1
    
    with open(target,'r') as reader:
        output = json.load(reader)
        
    return output

if __name__=="__main__":
    x = get_movement_json(0)
    print(x)
    y = get_image_url()
    print(y)