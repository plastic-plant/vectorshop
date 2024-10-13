# python 3-generate-product-descriptions.py
#
# Generating product description for alarm clocks/20.
#  - Adding user review in English language.
#  - Adding user review in English language.
#  - Adding user review in French language.
#
# Generating product description for alarm clocks/200.
#  - Adding user review in English language.
#  - Adding user review in German language.
#
# Generating product description for alarm clocks/303.
#  - Adding user review in English language.
#  - Adding user review in English language.
#
# Generating product description for alarm clocks/348.
#  - Adding user review in English language.
#  - Adding user review in Portugese language.
#  - Adding user review in English language.
#  - Adding user review in Dutch language.
#  - Adding user review in English language.
#
# Generating product description for alarm clocks/369.
#  - Adding user review in French language.

import os
import json
import random
import openai

def generate_product_data(model, category, productnr):
    print(f"Generating product description for {category}/{productnr}.")
    product_dir = f'public/products/{category}/{productnr}'
    product_images = [f for f in os.listdir(product_dir) if f.endswith('.png')]
    
    product_ranking = random.randint(1, 5)
    product_availability = random.randint(1, 25)
    
    product_name = openai.chat.completions.create(model=model, messages=[{"role": "user", "content": f"Generate a unique, engaging product name in the category of {category}. Respond in English language without adding any introduction or concuding remarks."}], max_tokens=10).choices[0].message.content.strip()
    product_price = openai.chat.completions.create(model=model, messages=[{"role": "user", "content": f"Generate a price in euros for a product in the category of {category} as a number in eurocents. Return just the number."}], max_tokens=10).choices[0].message.content.removesuffix('eurocents.').strip()
    product_description = openai.chat.completions.create(model=model, messages=[{"role": "user", "content": f"Generate a unique, engaging sales description for a household product in the category of {category}. The description for product name {product_name} should be fully made up but not include {product_name} itself, you may reference to a shortened alias for that. Also, should consist of two to five paragraphs. Focus on highlighting the product's benefits, features, and appeal to potential customers. Respond in english language without adding any introduction or concuding remarks."}], max_tokens=150).choices[0].message.content.strip()
    
    reviews = []
    for _ in range(random.randint(2, 5)):
        user_language = random.choices(
            ['English', 'German', 'French', 'Spanish', 'Dutch', 'Portuguese'],
            weights=[90, 2, 2, 2, 2, 2],
            k=1
        )[0]
        print(f" - Adding user review in {user_language} language.")
        user_review = openai.chat.completions.create(model=model, temperature=1.2, messages=[{"role": "user", "content": f"Generate a user review of a virtual household product {product_name} in the category of {category}. Other users have ranked the product with {product_ranking} stars. Write a review that matches a tone of voice for that ranking. If the product was ranked with 1 star, you will not like product at all and generally write shorter texts with maybe some spelling errors and maybe some missing punctuation. If the product was ranked with many stars, you give the text more attention and write a positive review detailing how nice it is in use. Respond in {user_language} language without adding any introductionaly or concuding remarks. Do not mention the name of the product."}], max_tokens=100).choices[0].message.content.strip()
        reviews.append({"review": user_review, "language": user_language})
    
    product_data = {
        "nr": productnr,
        "name": product_name,
        "price": product_price,
        "ranking": product_ranking,
        "availability": product_availability,
        "description": product_description,
        "images": product_images,
        "reviews": reviews
    }
    
    with open(os.path.join(product_dir, 'product.json'), 'w') as json_file:
        json.dump(product_data, json_file, indent=4)


# openai.base_url = 'https://api.openai.com/v1/' # 'http://localhost:1234/v1/'
openai.api_key = 'sk-proj-ryev9N14xKd-an-openai-api-key-5VdvEZSE05bX' # 'lm_studio'
model = 'gpt-4o-mini' # 'lm_studio'
base_dir = 'public/products'

for category in os.listdir(base_dir):
    category_dir = os.path.join(base_dir, category)
    if os.path.isdir(category_dir):
        for productnr in os.listdir(category_dir):
            product_dir = os.path.join(category_dir, productnr)
            if os.path.isdir(product_dir):
                generate_product_data(model, category, productnr)

