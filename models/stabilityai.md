# Stability ai API 

## Getting Started 

### 1. Authentication(인증)
> 어떻게 계정을 생성하고 key들을 관리하는지를 배운다 

- API 를 호출하려면 먼저 stability ai 의 계정을 만들어야 key를 얻을 수 있다. 
- API 키에 대한 접근 관리는 account page에서 관리할 수 있다. 
- 모든 stability ai account는 account 생성 시 default API 키가 할당
- API 키 패널에는 계정의 활성화된 모든 API key를 볼 수 있다. <br>
🚨 Your API key needs to be kept secret. Avoid committing your secrets to source control. Someone could drain your credits if your key is compromised! If you suspect your key has been leaked, first create a new one from your [Account](https://platform.stability.ai/account) page, and then delete the old one.

---
### 2.  Credits + Billing
> Stability API 를 이용하기위해서는 credit이 필요함. 
> 모든 새 유저에게는 25 free credits이 주어짐. 

- What is credit? 
	- 크레딧은 API를 통해서 요청한 task를 수행하는데 필요한 돈과 같은 단위
	- 요구되는 컴퓨팅이 많아질 수록 크레딧도 늘어남. 
- Buying Credits 
	- After depleting your free credits, additional credits can be purchased via your [Billing](https://platform.stability.ai/account/billing) dashboard. (free credit 다 끝나면, billing 보드에서 새 크레딧 구매 가능)
- Credits Usage
	- The API defaults to **`512 x 512` Pixels and `30` Steps**, which differs in comparison to DreamStudio, where the default is `512 x 512` Pixels and `50` Steps.
---
### 3. Stable Video Diffusion API 
> **This state-of-the-art video model is currently available via an alpha REST API**. It signifies a major milestone in our ongoing quest to develop versatile models for diverse applications.
> **이번 SOTA video model은 alpha REST API를 통해서 제공**
	[Rest API](./base_term_explain/rest_api.md)
    
- How to use? 
	- video diffusion은 image diffusion model에 비해서 많은 시간이 소요되기 때문에, SVD API는 비동기로 진행된다. 
	- video generation request 이후에, API는 id를 리턴하고, id는 [[Poll for the result]]에 사용된다. 
- How long are results stored? 
	- API results는 생성되고 24시간동안 저장된다. 이후에는 삭제되니까. 빠르게 다운로드를 하는게 좋음.
- Quality of Results
	- image model 처럼 아직 robust 하지 않음. 
	- 그래서 원하는 결과물을 얻으려면, trial and error 방식으로 여러번 시도해야할 수 있음. 
	- `seed` `cfg_scale` `motion_bucket_id` 파라미터를 잘 찾아야함. 
---
### 4. Python gRPC SDK
> [gRPC](./base_term_explain/gRPC.md) [SDK](./base_term_explain/SDK.md)
간단한 이미지 생성 예제를 통해 Stability Ai를 사용하는 방법을 알아볼 것임. 
이는 image generation 예제이므로 video 생성 API 를 가져와서 사용하는 것과 다를 수 있음. 
---

### Basic Installation
- stability-sdk pip로 다운로드 
```
%pip install stability-sdk
```

### API 키 얻기 
![image](/images/howgetAPI_1.png) <br>
![Pasted image 20240123191956.png](/images/howgetAPI_2.png)

### connect to the API
```
import getpass

# org-Sis1mpCaAg9CKB7JS59FhPrf

  
  

# NB: host url is not prepended with \"https\" nor does it have a trailing slash.

STABILITY_HOST = 'grpc.stability.ai:443'

  

# To get your API key, visit https://beta.dreamstudio.ai/membership

STABILITY_KEY = getpass.getpass('your API key')
```
- 실행하면 또 입력하는 창이 나오는데, 거기다가 또 API 키 입력하면 연결 가능
```
import io

import warnings

from IPython.display import display

from PIL import Image

# clinet 사용을 위해서 기본적으로 불러오고 
from stability_sdk import client

#지금 예시가 image generate 예시라서 generation 으로 보임.
from stability_sdk.client import generation

  
  
# API clinet 연결 -> 통신으로 데이터를 주고받을 수 있게 됨.
stability_api = client.StabilityInference(

host=STABILITY_HOST,

key=STABILITY_KEY,

verbose=True,

)
```

### Image generate example 
```
# prompt="rocket ship launching from forest with flower garden under a blue sky, masterful, ghibli",

  

answers = stability_api.generate(

prompt="what you want",

seed=121245125, # if provided, specifying a random seed makes results deterministic

steps=50, # defaults to 30 if not specified

)

  
  

# iterating over the generator produces the api response

for resp in answers:

	for artifact in resp.artifacts:

		if artifact.finish_reason == generation.FILTER:

			warnings.warn( # 아마 warning 뜨면 다음 문구 출력하라는 의미일듯

				"Your request activated the API's safety filters and could not be processed."

				"Please modify the prompt and try again.")

		if artifact.type == generation.ARTIFACT_IMAGE:

			img = Image.open(io.BytesIO(artifact.binary))

			display(img)
```
---
## git clone 해서 하는 방법 

### 0. 가상환경 세팅 

```
python3 -m venv venv # 생성

source venv/bin/activate # activate
# 또는 
conda create -n env_name

conda activate env_name
```
###  1. Clone the `stability-sdk` repository from GitHub...
```
git clone --recurse-submodules https://github.com/Stability-AI/stability-sdk

cd stability-sdk


```

### 2. Install the python SDK 
```
pip install .
```
### 3. optionally, set the Stability HOST and Stability KEY environment variables
- Note that `export` is Linux / MacOS syntax. If you are using Windows, you will need to use the `set` command instead.
```
# Sign up for an account at the following link to get an API Key. 
# https://platform.stability.ai/ 
# Click on the following link once you have created an account to be taken to your API Key. 
# https://platform.stability.ai/account/keys # Paste your API Key below. 


export STABILITY_HOST=grpc.stability.ai:443 
export STABILITY_KEY=yourkeyhere
```

### 4. Invoke the API to test your setup 
```
python -m stability_sdk generate "A stunning house."
```
---
