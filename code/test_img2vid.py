'''
## Test img2vid API by pytest
'''
import os
from dotenv import load_dotenv
import requests
import random
from utills import get_resized_image_from_path, make_video_slow, make_video_reverse
from datetime import datetime
import asyncio 
import pytest
import image2video as i2v

# TODO : API로 만들기 
# TODO : 파라미터 튜닝하기 
# TODO : 영상 길이 늘리기 또는 반복재생으로 하기 

'''
input : single image path 

- resize
- image to video 
- reverse video
- slow video 

output : 8 sec video 
'''



@pytest.mark.asyncio
async def test_API():

    # dotenv 환경변수 apikey 로드 
    load_dotenv()
    my_api = os.environ.get("STABILITY_KEY")

    # 이미지 resize 
    IMAGE_DIR_PATH = './images/sample'
    resize_image, resize_img_path = get_resized_image_from_path(os.path.join(IMAGE_DIR_PATH,'human0.png'),
                                                             save_image=True,
                                                             out_dir=IMAGE_DIR_PATH)
    
    
    generation_id = i2v.img2vid_post(
        input_img_path=resize_img_path, 
        seed = random.randint(0,1000),
        cfg_scale=3.0,
        motion_bucket_id=60,
        api_key=my_api
                                    )
    
    # output video file path 설정
    timestamp = datetime.now().strftime("%m%d%H%M%S")
    output_vid_path = f"./outputvideos/video_{timestamp}.mp4"

    generated_vid_path = i2v.img2vid_get(
        generation_id = generation_id,
        output_vid_path = output_vid_path,
        api_key= my_api              
                                         )
    
    reverse_vid_path = f"./outputvideos/video_reverse_{timestamp}.mp4"
    make_video_reverse(
        input_video_path = generated_vid_path,
        output_video_path = reverse_vid_path
    )

    slow_vid_path = f"./outputvideos/video_slow_{timestamp}.mp4"
    result_path = make_video_slow(
        input_video_path = reverse_vid_path,
        output_video_path = slow_vid_path
    )
    
    assert slow_vid_path == result_path







