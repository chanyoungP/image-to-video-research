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




# def images_to_video(image_folder, video_name, fps):
#     images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
#     frame = cv2.imread(os.path.join(image_folder, images[0]))
#     height, width, layers = frame.shape

#     video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

#     for image in images:
#         video.write(cv2.imread(os.path.join(image_folder, image)))

#     cv2.destroyAllWindows()
#     video.release()