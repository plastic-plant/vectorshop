# python launch.py --api (stable diffusion)
# python 1-generate-categories.py
#
# Generating images with Stable Diffusion.
# Generated 4 images for product 1 in 42.0 seconds.

import os
import requests
import csv
import time
import base64

output_dir = "public/products"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def generate_icon(category):
    payload = {
        "key": "",
        "prompt": f"vector illustration, {category}, orange, blue",
        "negative_prompt": "ugly, bad, blurry, low resolution, low quality, over saturated, b&w",
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "40",
        "safety_checker": "no",
        "enhance_prompt": "yes",
        "guidance_scale": 7,
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        }
        # https://stablediffusionapi.com/docs/stable-diffusion-api/text2img
        # <lora:Vector_illustration_V2:1> https://civitai.com/models/60132/vector-illustration / https://civitai.com/models/4201/realistic-vision-v60-b1?modelVersionId=125411
    
    response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload)
    
    if response.status_code == 200:
        image_data = base64.b64decode(response.json()['images'][0])
        category_dir = os.path.join(output_dir, category.lower())

        if not os.path.exists(category_dir):
            os.makedirs(category_dir)

        with open(os.path.join(category_dir, f"category.png"), "wb") as image_file:
            image_file.write(image_data)
    else:
        print(f"Error: {response.status_code} - {response.text}")

with open("1-generate-categories.txt", newline='') as txtfile:
    print("Generating category icons with Stable Diffusion.")
    categories = txtfile.read().split("\n")
    for index, category in enumerate(categories, start=1):
        generate_icon(category.strip())
        print(f"Generated icon for category {category.strip()}.")
