from PIL import Image
import matplotlib.pyplot as plt
import cv2
import os 


def get_resized_image_from_path(image_path, w=768, h=768, save_image = False):
    desired_size = (w,h)

    #load image
    image = Image.open(image_path)

    #resize image
    resized_image = image.resize(desired_size)

    if save_image:
        resized_image.save("./resized_image.png")

    return resized_image

def images_to_video(image_folder, video_name, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()