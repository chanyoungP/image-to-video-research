'''
# Limitations
- The generated videos are rather short (<= 4sec), and the model does not achieve perfect photorealism.
- The model may generate videos without motion, or very slow camera pans.
- The model cannot be controlled through text.
- The model cannot render legible text.
- Faces and people in general may not be generated properly.
- The autoencoding part of the model is lossy.
'''
import requests
import time

##############################################################################
########################## POST THE VIDEO BY IMAGE PATH ######################
##############################################################################
def img2vid_post(input_img_path = None, seed = 0, cfg_scale = 2.5, motion_bucket_id = 40, api_key = None):
    '''
    To Post request to Stability image2video REST API
    ### parameters 
    - image : input image path(supported image dim : (1024x576) (576x1024) (768x768))
    - seed : Default: 0 , number [ 0 .. 2147483648 ]
    - cfg_scale	: Default: 2.5, number [ 0 .. 10 ] : How strongly the video sticks to the original image.
    - motion_bucket_id	: Default: 40 , number [ 1 .. 255 ] : Lower values generally result in less motion in the output video, while higher values generally result in more motion
    '''
    start_time = time.time()
    
    # img path 와 api key 입력 X에 대한 에러 발생 
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
    
    # store request response
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
    '''
    To Get our video from Stability REST API by generated_id from POST request

    ### Parameters
    generation_id : recieved id when you request post 
    output_vid_path : where you save generated video
    api_key : api_key from stability ai 
    '''
    start_time = time.time()

    # 예외 처리 
    if generation_id == None:
        raise Exception("Empty id error, please check generation id")
    elif api_key == None:
        raise Exception("Check your API KEY setting")

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
        # flag에 status code 할당 
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
