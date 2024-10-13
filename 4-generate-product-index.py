# python 4-generate-product-index.py
#
# Creating products collection in Typesense database.
# Storing in database: assets\products\alarm clocks\200\product.json
# Storing in database: assets\products\alarm clocks\303\product.json
# Storing in database: assets\products\alarm clocks\348\product.json
# ...
#
# Summary of products by category in the collection:
#
#  - Listed 123 products in category alarm clocks.
#  - Listed 234 products in category backpacks.
#    ...
#
# Test with semantic text search in description and user reviews for a wake-up device:
#
#  - See category alarm clocks for product 200: "Snooze Sphere"
#
# Test with semantic search in product images for a black bag:
#
#  - See category backpacks for product 125: AdventureHaul Backpack
#
# Test with semantic search for a picture with three clocks:
#
#  - See category alarm clocks for product 662: DreamChaser Alarm Clock
#
# Test with auto-completion for 'trail':
#
#  - You mean TrailBlazer Pack? See category backpacks for product 235.
#  - You mean TrailBlazer Pack? See category backpacks for product 203.
#  - You mean Trailblazer Nomad Pack? See category backpacks for product 166.
#  - You mean TrailBlazer Backpack? See category backpacks for product 188.

import base64
import os
import json
import glob
import typesense
import time

client = typesense.Client({
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': 'xyz',
    'connection_timeout_seconds': 5
})

schema = {
    'name': 'products',
    'fields': [
        # Fields for relational search imported from the product.json files.
        { 'name': 'nr', 'type': 'string' },
        { 'name': 'name', 'type': 'string' },
        { 'name': 'price', 'type': 'int32', 'sort': True },
        { 'name': 'ranking', 'type': 'int32', 'sort': True },
        { 'name': 'availability', 'type': 'int32', 'sort': True },
        { 'name': 'description', 'type': 'string' },
        { 'name': 'images', 'type': 'string[]' },
        { 'name': 'reviews', 'type': 'object[]' },

        # Fields imported from file system product parent directory.
        { 'name': 'category', 'type': 'string', "index": True, 'sort': True, "facet": True },

        # Fields calculated for auto-embedding, vector search, etc.
        { 'name': 'reviews_flat', 'type': 'string[]', "store": False },
        {
            "name": "text_embedding",
            "type": "float[]",
            "embed": {
              "from": [
                "description",
                "reviews_flat"
              ],
              "model_config": {
                "model_name": "ts/all-MiniLM-L12-v2"
              }
            }
          },
          { "name": "image_flat", "type": "image", "store": False },
          {
            "name": "image_embedding",
            "type": "float[]",
            "embed": {
              "from": [
                "image_flat"
              ],
              "model_config": {
                "model_name": "ts/clip-vit-b-p32"
              }
            }
          }
    ],

    # Default sorting field for search results.
    'default_sorting_field': 'price',
    'enable_nested_fields': True
}

print("Creating products collection in Typesense database.")
if 'products' in [collection['name'] for collection in client.collections.retrieve()]:
    client.collections['products'].delete()
    print("Collection already exists. Deleting and recreating it.")
try:
    client.collections.create(schema)
except typesense.exceptions.ObjectAlreadyExists:
    print("Deleting outdated collection failed. For unknown reason deleting collections might fail, so we'll try again and wait 10 seconds. In production, work with collection aliases.")
    client.collections['products'].delete()
    time.sleep(10)
    client.collections.create(schema)

print("Collecting product folders on disk.")
for file_path in glob.glob(r'public\products\*\*\product.json')[:20]:  # limit to 20 products for now
    print(f"Storing in database: {file_path}")
    with open(file_path, 'r') as file:
        product_data = json.load(file)
        product_data['price'] = int(product_data['price'])
        product_data['category'] = file_path.split(os.sep)[2]
        product_data['reviews_flat'] = [review['review'] for review in product_data['reviews']]
        product_data['image_flat'] = base64.b64encode(open(os.path.join(os.path.dirname(file_path), product_data['images'][0]), 'rb').read()).decode('utf-8')
        try:
            client.collections['products'].documents.create(product_data)
        except typesense.exceptions.ObjectAlreadyExists:
            client.collections['products'].documents.update(product_data)

print("Summary of products by category in the collection:")
search_results = client.collections['products'].documents.search({
    'q': '*',
    'query_by': 'category',
    'facet_by': 'category'
})
for facet in search_results['facet_counts']:
    if facet['field_name'] == 'category':
        for category in facet['counts']:
            print(f" - Listed {category['count']} products in category {category['value']}.")

print("\nTest with semantic text search in description and user reviews for a wake-up device:\n") # furniture to sleep in, etc
search_results = client.collections['products'].documents.search({
    "q": "wake up device",
    "query_by": "text_embedding",
    "collection": "products",
    "prefix": "false",
    "exclude_fields": "description,reviews,text_embedding,image_embedding",
    "per_page": 1
})
# print(search_results)
for hit in search_results['hits']:
    print(f" - See category {hit['document']['category']} for product {hit['document']['nr']}: {hit['document']['name']}")

print("\nTest with semantic search in product images for a blue bed:\n") 
search_results = client.collections['products'].documents.search({
    "q": "blue bed",
    "query_by": "image_embedding",
    "collection": "products",
    "prefix": "false",
    "exclude_fields": "description,reviews,text_embedding,image_embedding",
    "per_page": 1
})
for hit in search_results['hits']:
    print(f" - See category {hit['document']['category']} for product {hit['document']['nr']}: {hit['document']['name']}")

print("\nTest with semantic search for a picture with three clocks:\n")
search_results = client.collections['products'].documents.search({
    "q": "three clocks",
    "query_by": "image_embedding",
    "collection": "products",
    "prefix": "false",
    "exclude_fields": "description,reviews,text_embedding,image_embedding",
    "per_page": 1
})
for hit in search_results['hits']:
    print(f" - See category {hit['document']['category']} for product {hit['document']['nr']}: {hit['document']['name']}")

print("\nTest with auto-completion for 'trail' -> TrailBlazer Pack:\n")
search_results = client.collections['products'].documents.search({
    "q": "trail",
    "query_by": "name",
    "collection": "products"
})
for hit in search_results['hits']:
    print(f" - You mean {hit['document']['name']}? See category {hit['document']['category']} for product {hit['document']['nr']}.")

