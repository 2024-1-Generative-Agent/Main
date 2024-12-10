import json
import os
from tqdm import tqdm

def main(args):

    total_dict = dict()

    print("loading metadata in",args.metadata_path)
    data_path = os.path.join(args.dataname, args.metadata_path)
    with open(data_path, "r") as reader:
        metadata = json.load(reader)
    total_dict['metadata'] = metadata
    print("metadata loading done")
    
    for filelist in args.filelist: #List
        print(f"concating json in",filelist)
        
        data_path = os.path.join(args.dataname,filelist)
        data_dirs = sorted(os.listdir(data_path))
        print(f"find {len(data_dirs)} steps...")
        
        concat_dict = dict()
        for json_name in tqdm(data_dirs):
            cur_path = os.path.join(data_path,json_name)
            cur_step = json_name.split(".")[0] # x.json -> x
            
            with open(cur_path,"r") as reader:
                cur_json = json.load(reader)
            concat_dict[f"step_{cur_step}"] = cur_json
        
        total_dict["filelist"] = concat_dict
        print("concat end")

    print(f"savename:",f"{args.dataname}/concated_json.json")
    with open(f"{args.dataname}/concated_json.json","w") as writer:
        json.dump(total_dict,writer,indent=4)


if __name__=="__main__":
    class args:
        dataname = "testing1_20240710014500"
        metadata_path = "reverie/meta.json"
        filelist = ["movement"]
        
    main(args)