import os
import time
import openai
import urllib.request
from PIL import Image
from io import BytesIO
import time
import itertools
import glob
from imutils import build_montages

import torch
prompts = torch.load('mit_prompts.pth')
openai.api_key = 'YOUR_OPENAI_API_KEY'
imgs = []
for prom in prompts:
    sat,obj,p = prom[0],prom[1],prom[2]
    if ' ' in sat:
        sat = sat.replace(' ',"_")
    if ' ' in obj:
        obj = obj.replace(' ','_')
    n=len(glob.glob('./mit_generation/'+obj+'/'+sat+'/*.jpg'))
    print(sat,obj,n)
    if not os.path.isdir('./mit_generation/'+obj+'/'+sat+'/'):
        os.makedirs('./mit_generation/'+obj+'/'+sat+'/')
    elif n==5:
        continue
    for i in range(n,5):
        print(p,i)
        response = openai.Image.create(
            model="dall-e-3",
            prompt=p,
            n=1,
            quality='standard',
            size="1024x1024",
        )
        with urllib.request.urlopen(response["data"][0]["url"]) as url:
            img = Image.open(url)
            img.convert('RGBA')
        img.save('./mit_generation/'+obj+'/'+sat+'/'+"%02d" % i+'.jpg')
    time.sleep(60)
