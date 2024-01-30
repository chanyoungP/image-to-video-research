from utills import get_resized_image_from_path
import os
from datetime import datetime


IMAGE_DIR_PATH = './images/sample'
resize_image, output_file_path = get_resized_image_from_path(os.path.join(IMAGE_DIR_PATH,'human0.png'),save_image=True,out_dir=IMAGE_DIR_PATH)


timestamp = datetime.now().strftime("%m%d%H%M")
output_vid_path = f"./outputvideos/video_{timestamp}.mp4"


print(output_vid_path)