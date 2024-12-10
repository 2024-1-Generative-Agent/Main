import os
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi import Response
from fastapi.responses import FileResponse

from starlette.status import HTTP_403_FORBIDDEN
from fastapi.responses import JSONResponse, FileResponse
import json
from pydantic import BaseModel
from openai import OpenAI

class FileNameRequest(BaseModel):
    filename: str

api_key = "Your_OpenAI_API_Key"

app = FastAPI()
client = OpenAI(api_key=api_key)

API_KEY_NAME = "Authorization"
USERS = {}

# Load users from the user.json file
USER_JSON_PATH = "./config/users.json"

if os.path.exists(USER_JSON_PATH):
    with open(USER_JSON_PATH, 'r') as user_file:
        USERS = json.load(user_file)
else:
    print(f"User JSON file not found at {USER_JSON_PATH}")
    exit()

UPLOAD_DIRECTORY = "./file/"
MAIN_JSON_NAME = "concated_json.json"  # include all metadata + state for each step
IMAGE_ABSOLUTE_PATH = "../Generative_Agents/reverie/backend_server/image"
MAIN_IMAGE_NAME = 'image2url.json'
TREELOCATION2COORDINADE = "mapping_tree.json"

if not os.path.exists(UPLOAD_DIRECTORY):
    print("non existent directory, exiting...")
    exit()

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header in [user["api_key"] for user in USERS.values()]:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


def generate_response(concat_description, query):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a NPC of virtual world. You have to answer question like a human.\
                                           Here is the history of the NPC's memory. History {concat_description}"},
            {"role": "user", "content": f"Question: {query}."}
        ]
    )
    return completion.choices[0].message.content


@app.get("/")
async def ping():
    return {"message": "pong"}

@app.post("/filelist/")
async def get_file_list(api_key: APIKey = Depends(get_api_key)):
    files = os.listdir(UPLOAD_DIRECTORY)
    return JSONResponse(content=files)

@app.post("/sendfile/")
async def get_send_file(request: FileNameRequest, api_key: APIKey = Depends(get_api_key)):
    requested_filename = request.filename
    file_path = os.path.join(UPLOAD_DIRECTORY, requested_filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, "r") as f:
            file_contents = json.load(f)
    except (IOError, json.JSONDecodeError):
        raise HTTPException(status_code=500, detail="Error reading the file")

    return JSONResponse(content=file_contents)

@app.get("/latestfile/")
async def get_latest_file(api_key: APIKey = Depends(get_api_key)):
    files = os.listdir(UPLOAD_DIRECTORY)
    if not files:
        raise HTTPException(status_code=404, detail="No files found")

    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(UPLOAD_DIRECTORY, x)))
    latest_file_path = os.path.join(UPLOAD_DIRECTORY, latest_file)

    try:
        with open(latest_file_path, "r") as f:
            file_contents = json.load(f)
    except (IOError, json.JSONDecodeError):
        raise HTTPException(status_code=500, detail="Error reading the latest file")

    return JSONResponse(content=file_contents)

#==============================================================================================#

@app.get("/step/{step}")
async def get_time_step(step: int, api_key: APIKey = Depends(get_api_key)):
    json_path = os.path.join(UPLOAD_DIRECTORY, MAIN_JSON_NAME)

    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail='no file found')

    with open(json_path, 'r') as reader:
        concated_json = json.load(reader)

    cur_step_metadata = concated_json['filelist'].get(f"step_{step}")
    if cur_step_metadata is None:
        raise HTTPException(status_code=404, detail=f'step {step} not exists')

    return JSONResponse(content=cur_step_metadata, status_code=200)


@app.get("/piece/image_url/{image_location}")
async def get_image_from_url(image_location: str):
    image_path = os.path.join(f"{IMAGE_ABSOLUTE_PATH}", f"{image_location}.png")

    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/jpeg")
    else:
        return JSONResponse(content="image not found", status_code=404)


PREV_PIECE_DICT = dict()

@app.get("/piece/")
async def get_piece_url(api_key: APIKey = Depends(get_api_key)):
    #============= load image ======================
    path = f"{IMAGE_ABSOLUTE_PATH}/{MAIN_IMAGE_NAME}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail='no file found')

    with open(path, "r") as reader:
        image2url = json.load(reader)  # key: Dict[key[prompt, url]
    #================================================#

    #============= load tree and coordinate ======================
    path = f"{UPLOAD_DIRECTORY}/{TREELOCATION2COORDINADE}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail='no file found')

    with open(path, "r") as reader:
        tree2coordinate = json.load(reader)  # key: Dict[key[prompt, url]
    #================================================#

    result = {}
    def flatten_dict(d, parent_key=''):
        for k, v in d.items():
            new_key = f"{parent_key}_{k}".replace(' ', '_')
            if isinstance(v, dict):
                flatten_dict(v, new_key)
            else:
                result[new_key] = v

    flatten_dict(tree2coordinate)

    output = list()
    for key, coordinate in result.items():
        for cur, url in image2url.items():
            cur = cur.lower().replace("-", '_')
            if cur in key:
                output.append((coordinate, url['prompt']))  # url['url']: openai url, ['prompt'] image.png name
    #================================================#

    return JSONResponse(content={"out": output}, status_code=200)


@app.get("/user_interrupt/")
async def get_npc_response(query: str,
                           npc_name: str,
                           cur_timestamp: int,
                           num_memory: int = 999,
                           api_key: APIKey = Depends(get_api_key)):
    """
    query: user query
    npc_name: npc which user wants to interact
    cur_timestamp: current timestamp
    num_memory: how many memory gpt can use
    """

    #============== load metadata ==============================================#
    json_path = os.path.join(UPLOAD_DIRECTORY, MAIN_JSON_NAME)

    if not os.path.exists(json_path):
        raise HTTPException(status_code=401, detail='no file found')

    with open(json_path, 'r') as reader:
        concated_json = json.load(reader)
    #============================================================================#

    description_list = []
    min_timestamp = max(0, cur_timestamp - num_memory)
    for step in range(min_timestamp, cur_timestamp + 1):
        cur_step_metadata = concated_json['filelist'].get(f"step_{step}")
        if cur_step_metadata is None:
            raise HTTPException(status_code=402, detail=f'step {step} not exists')
        cur_step_npc_info = cur_step_metadata['persona'].get(npc_name)
        if cur_step_npc_info is None:
            raise HTTPException(status_code=403, detail=f'npc {npc_name} not exists')
        description_list.append(f"step {step}: " + cur_step_npc_info['description'])
    description_concat = '\n'.join(description_list)

    output = generate_response(description_concat, query)

    return JSONResponse(content={"out": output}, status_code=200)

#==============================================================================================#

# To run the server, use the following command:
# uvicorn filename:app --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # uvicorn main:app --host 0.0.0.0 --port 8000 --reload
