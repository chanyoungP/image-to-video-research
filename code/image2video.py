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

# API 요청 
response = requests.post(
    "https://api.stability.ai/v2alpha/generation/image-to-video",
    headers={
        "authorization": "Bearer "+ my_api,
    },
    data={
        "seed": random.randint(0,1000),
        "cfg_scale": 4.0,
        "motion_bucket_id": 30
    },
    files={
        "image": ("file", open(output_img_path, "rb"), "image/png")
    },
)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

data = response.json()
generation_id = data["id"]
print(generation_id)

##############################################################################
########################## GET THE VIDEO BY ID      ##########################
##############################################################################


response = requests.request(
    "GET",
    f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{generation_id}",
    headers={
        'Accept': None, # Use 'application/json' to receive base64 encoded JSON
        'authorization': my_api
    },
)
timestamp = datetime.now().strftime("%m%d%H%M")
output_vid_path = f"./outputvideos/video_{timestamp}.mp4"
if response.status_code == 202:
    print("Generation in-progress, try again in 10 seconds.")
elif response.status_code == 200:
    print("Generation complete!")
    with open(output_vid_path, 'wb') as file:
        file.write(response.content)
else:
    raise Exception("Non-200 response: " + str(response.json()))

# TODO : POST-GET 한 사이클로 코드 변경
# TODO : 변경 코드로 pytest 진행하기 (성공, 실패)
# TODO : 함수로 만들고 class화 시키기 
# TODO : API로 만들기 
# TODO : 파라미터 튜닝하기 
# TODO : 영상 길이 늘리기 또는 반복재생으로 하기 