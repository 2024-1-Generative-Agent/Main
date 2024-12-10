import unittest
from fastapi.testclient import TestClient
import os
import json
import cv2
from io import BytesIO
import numpy as np

from simulation.main import app  # 엔드포인트가 정의된 파일을 임포트
from simulation.main import *

client = TestClient(app)

class TestGetTimeStep(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_get_time_step_success(self):
        response = client.get("/step/1", )#params={"step": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.json().keys()),['persona','meta'] )
        print("\n================== get timestep example ==========")
        print("Dylan Yoon",response.json()['persona']['Dylan Yoon'])
        print("==================================================")

    def test_get_time_step_fail(self):
        response = client.get("/step/1000", )#params={"step": 1})
        self.assertEqual(response.status_code, 404)

    def test_get_piece_url_success(self):
        response = client.get("/piece/")
        print("\n======= Get Piece URL example ====")
        print(response.json()['out'][0])
        print('==================================')
        self.assertEqual(response.status_code, 200)

    def test_get_npc_response(self):
        response = client.get("/user_interrupt/",params={
                                                    "query": "what are you doing?",
                                                    "npc_name": "Dylan Yoon",
                                                    "cur_timestamp": 300,
                                                    "num_memory": 20
                                                  }
                            )
        self.assertEqual(response.status_code, 200)

    def test_image_url_get(self):
        """
        #########3 WARNING #################
        
        이미지 request로 읽을 때에는 {API 주소}/piece/image_url/{piece에서 받은 url} 이렇게 해야 합니다.
        
        ##################################
        """

        response = client.get("/piece/image_url/_A_famous_painting_by_Vincent_van_Gogh_depicting_a_night_sky")
        self.assertEqual(response.status_code, 200)

        #print(response.content)
        #image_bytes = BytesIO(response.content)
        #image_np = np.frombuffer(image_bytes.read(), np.uint8)
        #image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        #cv2.imshow("image",image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
if __name__ == "__main__":
    unittest.main(verbosity=2)
