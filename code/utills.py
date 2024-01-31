from PIL import Image
import matplotlib.pyplot as plt
import cv2
import os 


def get_resized_image_from_path(image_path, w=768, h=768, save_image = False, out_dir = './'):
    '''
    - image_path : original image_path 
    - Resize image by setting w, h value 
    - determine wether save image or not by setting save_image = True(False)
    - also you can set which directory save to image 
    - automatically set output image file name : 're_<original_image_name>.png
    - Return resized_image, resized_image_path 
    - --------------------------------------------
    ``` 
    IMAGE_DIR_PATH = './images/sample'
    resize_image, output_file_path = get_resized_image_from_path(os.path.join(IMAGE_DIR_PATH,'human0.png'),
                                                                    save_image=True,out_dir=IMAGE_DIR_PATH)  
    ```
    '''
    desired_size = (w,h)

    #load image
    image = Image.open(image_path)
    image_name = image_path.split('/')[-1]

    print("Image Name : {}".format(image_name))

    #resize image
    resized_image = image.resize(desired_size)

    FULL_PATH = os.path.join(out_dir, f"re_{image_name}")

    if save_image:
        resized_image.save(FULL_PATH)

    return resized_image, FULL_PATH

def make_video_reverse(input_video_path, output_video_path):
    '''
    # forward_play + backward_play 
    - make a video play time to double by combining forward_play video with backward_play video
    '''
    # 비디오 캡쳐 객체 생성
    cap = cv2.VideoCapture(input_video_path)

    # 비디오 속성 가져오기
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(5))

    # 비디오 작성 객체 생성
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # 비디오 재생
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 출력 비디오에 현재 프레임 쓰기
        out.write(frame)

    # 비디오 역재생을 위해 비디오 캡쳐 객체 초기화
    cap.release()

    # 역재생을 위한 비디오 캡쳐 객체 생성
    cap = cv2.VideoCapture(input_video_path)

    # 비디오 역재생 및 역재생 비디오 작성
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 출력 비디오에 현재 프레임 쓰기
        frames.append(frame)

    # 비디오 재생이 완료되면 객체 해제
    cap.release()

    # 역재생 비디오 작성
    for frame in reversed(frames):
        out.write(frame)

    # 비디오 작성 객체 해제
    out.release()

    return output_video_path
    
def make_video_slow(input_video_path, output_video_path):
    '''
    # re-write video frame into double frame to make video more longer but slow
    - make original video frame : [frame1, frame2, frame3 ...] -> [frame1, frame1, frame2, frame2, frame3, frame3...]
    '''
    # 비디오 캡쳐 객체 생성
    cap = cv2.VideoCapture(input_video_path)

    # 비디오 속성 가져오기
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(5))

    # 비디오 작성 객체 생성
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # 비디오 재생
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 출력 비디오에 현재 프레임을 두 번 씩 작성 
        out.write(frame)
        out.write(frame)

    # 비디오 역재생을 위해 비디오 캡쳐 객체 초기화
    cap.release()

    return output_video_path
