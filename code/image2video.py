'''
# Limitations
- The generated videos are rather short (<= 4sec), and the model does not achieve perfect photorealism.
- The model may generate videos without motion, or very slow camera pans.
- The model cannot be controlled through text.
- The model cannot render legible text.
- Faces and people in general may not be generated properly.
- The autoencoding part of the model is lossy.
'''

'''
# parameters 
- image : input image supported dim : (1024x576) (576x1024) (768x768)
- seed : Default: 0 , number [ 0 .. 2147483648 ]
- cfg_scale	: Default: 2.5, number [ 0 .. 10 ] : How strongly the video sticks to the original image.
- motion_bucket_id	: Default: 40 , number [ 1 .. 255 ] : Lower values generally result in less motion in the output video, while higher values generally result in more motion
'''

import os
from dotenv import load_dotenv
import requests
import time
import tqdm 
import random
from utills import get_resized_image_from_path
from datetime import datetime


# dotenv 환경변수(api key) 로드 
load_dotenv()
my_api = os.environ.get('STABILITY_KEY')

# 이미지 리사이즈 
IMAGE_DIR_PATH = './images/sample'
resize_image, output_img_path = get_resized_image_from_path(os.path.join(IMAGE_DIR_PATH,'human0.png'),
                                                             save_image=True,
                                                             out_dir=IMAGE_DIR_PATH)


##############################################################################
########################## POST THE VIDEO BY IMAGE PATH ######################
##############################################################################
def img2vid_post(input_img_path = None, seed = 0, cfg_scale = 2.5, motion_bucket_id = 40, api_key = None):
    start_time = time.time()

    if input_img_path == None:
        raise Exception("Empty input image path error")
    elif api_key == None:
        raise Exception("Check your API KEY setting ")
    
    # API 요청 
    response = requests.post(
        "https://api.stability.ai/v2alpha/generation/image-to-video",
        headers={
            "authorization": "Bearer "+ api_key,
        },
        data={
            "seed": seed,
            "cfg_scale": cfg_scale,
            "motion_bucket_id": motion_bucket_id
        },
        files={
            "image": ("file", open(input_img_path, "rb"), "image/png")
        },
    )
    # response error check
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    # id 저장
    generation_id = data["id"]
    print("Successfully requested the API and received the ID")
    end_time = time.time()
    print("POST RUNTIME : {}".format(end_time - start_time))
    
    return generation_id

##############################################################################
########################## GET THE VIDEO BY ID      ##########################
##############################################################################

def img2vid_get(generation_id = None, output_vid_path = './', api_key = None):
    start_time = time.time()

    if generation_id == None:
        raise Exception("Empty id error, please check generation id")
    elif api_key == None:
        raise Exception("Check your API KEY setting")

    
    # # output video file path 설정
    # timestamp = datetime.now().strftime("%m%d%H%M")
    # output_vid_path = f"./outputvideos/video_{timestamp}.mp4"

    # Stability API GET 요청 (생성까지 계속 요청 )
    flag = 1
    while flag != 200:
        response = requests.request(
            "GET",
            f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{generation_id}",
            headers={
                'Accept': None, # Use 'application/json' to receive base64 encoded JSON
                'authorization': api_key
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

    print("IMG2VID RUNNING TIME : {}".format(end_time - start_time))
    return output_vid_path

# TODO : POST-GET 한 사이클로 코드 변경
# TODO : 변경 코드로 pytest 진행하기 (성공, 실패)
# TODO : 함수로 만들고 class화 시키기 
# TODO : API로 만들기 
# TODO : 파라미터 튜닝하기 
# TODO : 영상 길이 늘리기 또는 반복재생으로 하기 