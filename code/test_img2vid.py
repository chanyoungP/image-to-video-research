'''
## Test img2vid API by pytest
'''
import os
from dotenv import load_dotenv
import requests
import time
import random
from utills import get_resized_image_from_path
from datetime import datetime
import asyncio 
import pytest

@pytest.mark.asyncio
async def test_API():
    #시간 측정 
    start_time = time.time()
    # dotenv 환경변수 apikey 로드 
    load_dotenv()
    my_api = os.environ.get("STABILITY_KEY")

    # 이미지 resize 
    IMAGE_DIR_PATH = './images/sample'
    resize_image, output_img_path = get_resized_image_from_path(os.path.join(IMAGE_DIR_PATH,'human0.png'),
                                                             save_image=True,
                                                             out_dir=IMAGE_DIR_PATH)
    
    # Stability API POST part
    response = requests.post(
        "https://api.stability.ai/v2alpha/generation/image-to-video",
        headers={
            "authorization": "Bearer "+ my_api,
        },
        data={
            "seed": random.randint(0,1000),
            "cfg_scale": 3.0,
            "motion_bucket_id": 50
        },
        files={
            "image": ("file", open(output_img_path, "rb"), "image/png")
        },
    )

    # 정상요청이 응답이 아닐 경우 에러 메시지 출력 
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    
    # generation id 저장
    data = response.json()
    generation_id = data["id"]
    print(generation_id)

    # output video file path 설정
    timestamp = datetime.now().strftime("%m%d%H%M")
    output_vid_path = f"./outputvideos/video_{timestamp}.mp4"

    # Stability API GET 요청 (생성까지 계속 요청 )
    flag = 1
    while flag != 200:
        response = requests.request(
            "GET",
            f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{generation_id}",
            headers={
                'Accept': None, # Use 'application/json' to receive base64 encoded JSON
                'authorization': my_api
            },
        )
        flag = response.status_code
        if flag == 202:
            print("Generation in-progress... automatically try again after 10 sec.")
            time.sleep(10)
        elif flag == 200:
            print("Generation complete")
            with open(output_vid_path,'wb') as file:
                file.write(response.content)
            print(f"video Saved at {output_vid_path}")
        else:
            raise Exception("Non-200 response : " + str(response.json()))
    end_time = time.time()

    print("RUNNING TIME : {}".format(end_time - start_time)) 
    # flag == 200 이면 정상처리 
    assert flag == 200






