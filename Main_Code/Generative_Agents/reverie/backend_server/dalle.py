import openai
from PIL import Image
import requests
from io import BytesIO
import os
import json

def make_dalle_image(location:dict, index:int, description:str) -> None:

    description = description.replace(' ','_').replace("\n","").replace(".","")
    image_path = f"./image/{description}.png"
    print(description)
    
    with open(f"./image/image2url.json",'r') as reader:
        image2url = json.load(reader)    
    
    if not os.path.exists(image_path):    
        
        #get dalle image
        response = openai.Image.create(
            prompt=f"{description}",
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']

        #make image as png
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        #save into local folder
        image.save(image_path)
        
        sector = location["sector"].replace(" ","_")
        arena = location['arena'].replace(" ","_")
        game_object = location["game_object"].replace(" ","_")
        image2url[f"{sector}-{arena}-{game_object}"] = {"prompt":description, "url":image_url}
    
    with open(f"./image/image2url.json",'w') as writer:
        json.dump(image2url,writer,indent=4)
        