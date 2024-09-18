import json
import os
import panel as pn
pn.extension()
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

OpenAI.api_key  = os.environ['OPENAI_API_KEY']

# LLM Function
client = OpenAI()
def get_completion_from_messages(messages, model="gpt-4o-mini", temperature=0, max_tokens=200):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

# Retrieval System Functions
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

# Load the product information and reviews from the JSON files
product_information = load_json_file('product_information.json')
review_information = load_json_file('customer_reviews.json')

def get_product_by_name(product_name):
    return product_information.get(product_name, None)

def get_reviews_by_product(product_name):
    # Retrieve a list of reviews for the given product name
    reviews = [review for review in review_information if review["product"] == product_name]
    #print(reviews)
    return reviews

def get_products_by_category(category_name):
    return [product for product in product_information.values() if product["category"] == category_name]

# Formatter
def read_string_to_list(input_string):
    if input_string is None:
        return None
    try:
        input_string = input_string.replace("'", "\"")  # Replace single quotes with double quotes for valid JSON
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None

def generate_output_string(data_list):
    output_string = ""

    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "products" in data:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        output_string += json.dumps(product, indent=4) + "\n"
                        # Fetch and add reviews for the product
                        reviews = get_reviews_by_product(product_name)
                        for review in reviews:
                            output_string += json.dumps(review, indent=4) + "\n"
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    output_string += json.dumps(product, indent=4) + "\n"
                    # Fetch and add reviews for each product in the category
                    reviews = get_reviews_by_product(product["name"])
                    for review in reviews:
                        output_string += json.dumps(review, indent=4) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string


def process_user_messages_1(user_message_1, context):
    # Prompting the System Behavior Using Chain Prompting
    delimiter = "####"
    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be delimited with \
    {delimiter} characters.
    Output a python list of objects, where each object has \
    the following format:
        'category': <one of Computers and Laptops, \
        Smartphones and Accessories, \
        Televisions and Home Theater Systems, \
        Gaming Consoles and Accessories, \
        Audio Equipment, Cameras and Camcorders>,
    OR
        'products': <a list of products that must \
        be found in the allowed products below>

    Where the categories and products must be found in \
    the customer service query.
    If a product is mentioned, it must be associated with \
    the correct category in the allowed products list below.
    If no products or categories are found, output an \
    empty list.

    Allowed products: 

    Computers and Laptops category:
    TechPro Ultrabook
    BlueWave Gaming Laptop
    PowerLite Convertible
    TechPro Desktop
    BlueWave Chromebook

    Smartphones and Accessories category:
    SmartX ProPhone
    MobiTech PowerCase
    SmartX MiniPhone
    MobiTech Wireless Charger
    SmartX EarBuds

    Televisions and Home Theater Systems category:
    CineView 4K TV
    SoundMax Home Theater
    CineView 8K TV
    SoundMax Soundbar
    CineView OLED TV

    Gaming Consoles and Accessories category:
    GameSphere X
    ProGamer Controller
    GameSphere Y
    ProGamer Racing Wheel
    GameSphere VR Headset

    Audio Equipment category:
    AudioPhonic Noise-Canceling Headphones
    WaveSound Bluetooth Speaker
    AudioPhonic True Wireless Earbuds
    WaveSound Soundbar
    AudioPhonic Turntable

    Cameras and Camcorders category:
    FotoSnap DSLR Camera
    ActionCam 4K
    FotoSnap Mirrorless Camera
    ZoomMaster Camcorder
    FotoSnap Instant Camera

    Only output the list of objects, with nothing else.
    """
    '''
    # User Prompt Processing
    user_message_1 = f"""
    Tell me about the SmartX ProPhone and \
    the FotoSnap DSLR Camera. Also, tell me about your TVs.
    """
    '''



    # create interaction with user:
    # enter the prompt
    '''
    while True:
        # Follow-Up
        follow_up_message = input("\nWant to continue (Yes or No): ")
        if follow_up_message.lower() == 'no':
            print("Thank you for using our service. Have a great day!")
            break
        elif follow_up_message.lower() == 'yes':
    '''

    #user_message_3 = f"""tell me about your phones products """

    #user_message_1 = input("provide your prompt: ")
            
    messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": f"{delimiter}{user_message_1}{delimiter}"}
    ]

    response_1 = get_completion_from_messages(messages)
    #print("debugging response1",response_1)

    category_product_list = read_string_to_list(response_1)
    #print("debugging category_product_list",category_product_list)

    # Enrich the response with details of products and categories from the text file / from the database
    product_category_information_for_user = generate_output_string(category_product_list)

    #print("debugging3 : Product and Review Information:\n")
    #print(product_category_information_for_user)
            



    system_message_2 = f"""
            You are a customer service assistant for a \
            large electronic store. \
            Respond in a friendly and helpful tone, \
            with very concise answers and give it in a paragraph for each product or category. \
            Make sure to consider all reviews to either recommend \
            it or not and mention whether to recommend the product or not.
            Make sure to ask the user relevant follow-up questions.
            """

    messages_2 = [
                {'role': 'system', 'content': system_message_2},
                *context,
                {'role': 'user', 'content': user_message_1},
                {'role': 'assistant', 'content': f"Relevant product information:\n{product_category_information_for_user}"},
            ]


            # Uncomment the following line to get the final response from the assistant
    final_response = get_completion_from_messages(messages_2)
    #print(final_response)
    return final_response, context



def collect_messages(debug=False):
    
    user_input = my_inp.value_input
    #if debug: print(f"User Input = {user_input}")
    if user_input == "":
        return
    
    my_inp.value = ''
    global my_context
    
    #response, context = process_user_message(user_input, context, utils.get_products_and_category(),debug=True)
    # response = process_user_messages_1(user_input)
    response, my_context = process_user_messages_1(user_input, my_context)
    
    my_context.append({'role':'assistant', 'content':f"{response}"})
    my_panel.append(
        pn.Row('User:', pn.pane.Markdown(user_input, width=600)))
    my_panel.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600)))
 
    return pn.Column(*my_panel)




# interface for chat bot
my_panel = []

# create context as a list of dictionaries. each dictionary represents a role
# my_context = [{'role':'system', 'content':"You are Service Assistant"}]

# create input box 
my_inp = pn.widgets.TextInput( placeholder='Enter text here…')

my_button = pn.widgets.Button(name="Service Assistant")

button_binder = pn.bind(collect_messages, my_button)

# mydash board
'''
dashboard = pn.Column(
    my_inp,
    pn.Row(my_button),
    pn.panel(button_binder, loading_indicator=True, height=300),
)
'''
scrollable_panel = pn.Column(*my_panel, height=300, scroll=True)

dashboard = pn.Column(
    my_inp,
    pn.Row(my_button),
    pn.panel(button_binder, loading_indicator=True, height=300),
    scrollable_panel
)


dashboard.show()