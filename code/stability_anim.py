# Test code 
# using gRPC API stability animation 

# pip install "stability_sdk[anim_ui]"   # Install the Animation SDK


import os
from dotenv import load_dotenv
from stability_sdk import api
from stability_sdk.animation import AnimationArgs, Animator

from stability_sdk.utils import create_video_from_frames
from utills import get_resized_image_from_path, images_to_video
from tqdm import tqdm
import time

get_resized_image_from_path('./images/풍경그림.png',w=512,h=512,save_image=True)
load_dotenv()
# The API Context class is used to manage the connection.

context = api.Context(os.environ.get('STABILITY_HOST'), os.environ.get('STABILITY_KEY'))

# To configure the animation settings, create an instance of the AnimationArgs class and set the desired parameters. 
# Configure the animation
args = AnimationArgs()

args.interpolate_prompts = True
args.locked_seed = True
args.max_frames = 24
args.seed = 42
args.strength_curve = "0:(0)"
args.diffusion_cadence_curve = "0:(4)"
args.cadence_interp = "film"
args.init_image = './resized_image.png'

# Animator 클래스는 각 프레임의 렌더를 조절하는데, 사용
animation_prompts = {
    0: "",               # animation prompts 꼭 들어가야함.
}
negative_prompt = "ark, split screen, photoshop, blurry, extra fingers, disfigured, kitsch, ugly, oversaturated, grain, low-res, blurry"


##############################################################################
########################## SAVE EACH FRAME TO IMAGE ##########################
##############################################################################
# Create Animator object to orchestrate the rendering
# animator = Animator(
#     api_context=context,
#     animation_prompts=animation_prompts,
#     negative_prompt=negative_prompt,
#     args=args
# )

# Render each frame of animation  -> save each frame to image 
# for idx, frame in enumerate(animator.render()):
#     frame.save(f"frame_{idx:05d}.png")


##############################################################################
########################## SAVE EACH FRAME TO VIDEO ##########################
##############################################################################

start = time.time()
# if you want to save each frame to video 
animator = Animator(
    api_context=context,
    animation_prompts=animation_prompts,
    negative_prompt=negative_prompt,
    args=args,
    out_dir="./generated_video_sample"
)

for _ in tqdm(animator.render(), total=args.max_frames):
    pass

# create_video_from_frames(animator.out_dir, "video.mp4", fps=12)
images_to_video('./generated_video_sample','ani_video',fps=12)
end = time.time()
#RUNNING TIME : 212.5384750366211
print("RUNNING TIME : {}".format(end - start))





# try:
#     for _ in animator.render():
#         pass
# except ClassifierException:
#     print("Animation terminated early due to NSFW classifier.")
# except OutOfCreditsException as e:
#     print(f"Animation terminated early, out of credits.\n{e.details}")
# except Exception as e:
#     print(f"Animation terminated early due to exception: {e}")

# A built-in retry mechanism is in place so that connection errors will not cause the animation to fail. You can override the default settings on the Context object.
# context._max_retries = 5   # Number of times to retry.
# context._retry_delay = 1.0 # Base delay in seconds between retries, each attempt will double.
