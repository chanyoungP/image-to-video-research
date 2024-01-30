## [Handbook_Animation](https://docs.google.com/document/d/1iHcAu_5rG11guGFie8sXBXPGuM4yKzqdd13MJ_1LU8U/edit?usp=sharing)

### 3가지 기능

1. Text to Animation. Via this method, you can prompt as you normally would with Stable Diffusion and after tweaking the various parameters arrive at an animation.
    

2. Text input + initial image input. Via this method, you’ll be able to provide an initial image that will be the starting point of your animation, and your text prompt will be used in conjunction with that to arrive at a final output animation.
    
3. Input video + text input. Via this method, you’ll be able to provide an initial video to base your animation on, and by tweaking the various parameters arrive at a final output animation that is additionally guided by your text prompt.

### prompt 방법
```
animation_prompts = { 
0: "a photo of a cute cat",  # 프레임 넘버 : "프롬프트"
24: "a photo of a cute dog", # 프레임 넘버와 프롬프트 지정으로 멀티 프롬프트가 가능
} 
negative_prompt = "blurry, low resolution"


```
### Negative prompt 예시 
“ark, split screen, photoshop, blurry, extra fingers, disfigured, kitsch, ugly, oversaturated, grain, low-res, Deformed, too many fingers, bad anatomy, poorly drawn face, extra limb, poorly drawn hands, missing limb, blurry, floating limbs, disconnected limbs, malformed hands, logo, watermarks, watermark”

## How to use 
```
# 가상환경 생성 및 세팅
...

# stability Ai Animation SDK 
# Install the Animation SDK (use [anim_ui] if you'd also like to use the UI). 

pip install "stability-sdk[anim]"

```

```
# KEY 설정 및 api 커넥션 

from stability_sdk import api

STABILITY_HOST = "grpc.stability.ai:443" 
STABILITY_KEY = ""     # API key from https://platform.stability.ai/account/keys

# The API `Context` class is used to manage the connection.
context = api.Context(STABILITY_HOST, STABILITY_KEY)
```

```
from stability_sdk.animation import AnimationArgs, Animator

# Configure the animation 
args = AnimationArgs() 
args.interpolate_prompts = True 
args.locked_seed = True 
args.max_frames = 48 
args.seed = 42 
args.strength_curve = "0:(0)" 
args.diffusion_cadence_curve = "0:(4)" 
args.cadence_interp = "film" 
animation_prompts = { 
0: "a photo of a cute cat", 
24: "a photo of a cute dog", 
} 
negative_prompt = ""

```

```
# Create Animator object to orchestrate the rendering 
animator = Animator( api_context=context, animation_prompts=animation_prompts, negative_prompt=negative_prompt, args=args )

# Render each frame of animation 
for idx, frame in enumerate(animator.render()): 
	frame.save(f"frame_{idx:05d}.png")

# 또는 비디오로 변환해서 저장 

```

```
from stability_sdk.utils import create_video_from_frames 
from tqdm import tqdm

#rendering
animator = Animator( api_context=api_context, animation_prompts=animation_prompts, negative_prompt=negative_prompt, args=args, out_dir="video_01" )

#프레임 생성
for _ in tqdm(animator.render(), total=args.max_frames): 
	pass 


create_video_from_frames(animator.out_dir, "video.mp4", fps=24)
```
![](/images/stability_anim_error_handle.png)



