# utils.py

def get_products_from_query(customer_msg):
    # Extract product information from the query message
    # This is a placeholder implementation
    products_by_category = "SmartX ProPhone, FotoSnap DSLR Camera, TVs"
    return products_by_category

def read_string_to_list(products_by_category):
    # Convert the product information string to a list
    # This is a placeholder implementation
    category_and_product_list = products_by_category.split(', ')
    return category_and_product_list

def get_mentioned_product_info(category_and_product_list):
    # Retrieve detailed information about the products
    # This is a placeholder implementation
    product_info = {
        "SmartX ProPhone": {"features": "12MP dual camera, 5G, 128GB storage", "price": "$899.99"},
        "FotoSnap DSLR Camera": {"features": "1080p video, 3-inch LCD, 24.2MP sensor", "price": "$599.99"},
        "TVs": [
            {"name": "CineView 4K TV", "features": "55-inch display, 4K resolution, HDR, Smart TV", "price": "$599"},
            {"name": "CineView 8K TV", "features": "65-inch display, 8K resolution, HDR, Smart TV", "price": "$2999.99"},
            {"name": "CineView OLED TV", "features": "55-inch display, 4K resolution, HDR, Smart TV", "price": "$1499.99"}
        ]
    }
    return product_info

def answer_user_msg(user_msg, product_info):
    # Generate an answer to the user's query
    # This is a placeholder implementation
    answer = f"The SmartX ProPhone has {product_info['SmartX ProPhone']['features']} and costs {product_info['SmartX ProPhone']['price']}. "
    answer += f"The FotoSnap DSLR Camera has {product_info['FotoSnap DSLR Camera']['features']} and costs {product_info['FotoSnap DSLR Camera']['price']}. "
    answer += "For TVs, we have:\n"
    for tv in product_info["TVs"]:
        answer += f"- {tv['name']} with {tv['features']} priced at {tv['price']}.\n"
    return answer