# python launch.py --api (stable diffusion)
# python 2-generate-product-images.py
#
# Generating images with Stable Diffusion.
# Generated 4 images for product 1 in 42 seconds.
# Generated 3 images for product 2 in 51 seconds.
# Generated 1 images for product 3 in 52 seconds.
# Generated 2 images (Shaving creams) for product 101 in 27 seconds.
# Generated 1 images (Watches) for product 102 in 15 seconds.
# Generated 4 images (Umbrellas) for product 103 in 56 seconds.
# Generated 2 images (Bookshelves) for product 104 in 22 seconds.
# Generated 1 images (Handbags) for product 105 in 14 seconds.
# Generated 4 images (Curtains) for product 106 in 48 seconds.
# Generated 2 images (Dinner plates) for product 107 in 30 seconds.
# Generated 2 images (Socks) for product 128 in 32 seconds.
# Generated 1 images (Paintings) for product 177 in 16 seconds.
# Generated 4 images (Pillows) for product 178 in 44 seconds.
# ...

import os
import requests
import csv
import time
import base64

output_dir = "public/products"
batch_size = 4 # Number of images per product, probably nice to randomise 1 to 6.

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def generate_images(prompt, batch_size, productnr, category, batch_num):
    payload = {
        "prompt": prompt,
        "batch_size": batch_size,
        "steps": 35, # 50,
        "cfg_scale": 7, # 7.5,
        "width": 512, # 512,
        "height": 512 # 512,
    } # v1-5-pruned-emaonly
    
    response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload)
    
    if response.status_code == 200:
        images = response.json()['images']
        product_dir = os.path.join(output_dir, category.lower(), productnr)

        if not os.path.exists(product_dir):
            os.makedirs(product_dir)

        for i, image in enumerate(images):
            image_data = base64.b64decode(image)
            image_filename = os.path.join(product_dir, f"product_{productnr}_{str(i+1).zfill(2)}.png")
            with open(image_filename, "wb") as image_file:
                image_file.write(image_data)
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Generate product images with the given prompt on each row in CSV file.
with open("2-generate-product-images.csv", newline='') as csvfile:
    start_time = time.time()
    csvreader = csv.DictReader(csvfile)
    
    print(f"Generating images with Stable Diffusion.")
    for i, row in enumerate(csvreader):
        # if i < 5735:
        #     continue
        productnr = row['productnr']
        category = row['category']
        prompt = row['prompt']
        
        # Generate images for each product prompt.
        start_time_product = time.time()
        generate_images(prompt, batch_size, productnr, category, i)
        print(f"Generated {batch_size} images ({category}) for product {productnr} in {round(time.time() - start_time_product, 0)} seconds.")

print(f"Done in {round((time.time() - start_time) / 60, 0)} minutes")
