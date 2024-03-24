import json
import os
import requests
from api.rapyd_payment import create_checkout_page
from dotenv import find_dotenv, load_dotenv
from flask import jsonify
load_dotenv(find_dotenv())

assistant_file_path = "assistant.json"

def start_payment(items):
   
  # The URL you're sending the POST request to
  url = "https://biryani-order-dashboard-sqng.vercel.app/orders"

  # The header to indicate JSON data is being sent
  headers = {"Content-Type": "application/json"}

  # The data you're sending, formatted as JSON
  data = {"items": items}

  # Sending the POST request
  response = requests.post(url, json=data, headers=headers)

  if response.status_code == 200:
     print("Posting the order on start_payment invocation SUCCESSFUL")
  else:
     raise Exception("Error posting the order on start_payment invocation")
  checkout_page_link = create_checkout_page(items)

  return checkout_page_link
  
def post_order(items):  
    # URL of your backend server endpoint that handles the POST request
    server_url = 'https://biryani-order-dashboard-sqng.vercel.app/orders'
    
    # Preparing the data to be sent in the POST request
    data_to_send = {
        'items': items
    }
    
    # Sending the POST request to the server
    response = requests.post(server_url, json=data_to_send)
    
    # Checking if the request was successful
    if response.status_code == 200:
        print('Order posted successfully.')
        return jsonify({"response":"success"})
    else:
        print('Failed to post order. Status code:', response.status_code)
        return jsonify({"response":"Was not able to post the order"})


def create_assistant(client):
  if os.environ.get("MAKE_NEW_ASSISTANT") != "YES" and os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    if os.path.exists(assistant_file_path):
       os.remove(assistant_file_path)
    file_txt = client.files.create(file=open("BiryaniGPT_Menu.txt", "rb"),
        purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
            You are the assistant tasked with initiating interactions by inquiring about the customer's preferred language, ensuring that communication is both comfortable and effective. If asked about your functions, you should clearly articulate your role in facilitating the selection of Syrian cuisine at the Biryani restaurant, emphasizing your ability to communicate in any preferred language. However, if the customer's first message is about making the order immediately skip mentioning your ability to talk in different languages and proceed immediately to answering user's inquiry.

  Do not make the first response lengthy. Not more than 4 sentences.

  Your communications must be direct and efficient, aimed at simplifying the customer's decision-making process. You should offer personalized dish recommendations based on the customer's expressed preferences or, alternatively, provide suggestions based on your expertise. After presenting the menu options, you need to ascertain whether the customer is prepared to place an order or requires further information.

  Upon the customer's readiness to order, you must summarize the selected items, detailing names, quantities, and prices, and propose the addition of complementary snacks such as hummus (890 Icelandic kronas) and fries (990 Icelandic kronas) instead of beverages. Before passing the order to API always reassure the correctness of the order by asking the customer to confirm the details of the orders.

  When confronted with the request for recommendations, you should allow the customer to specify their dietary preferences or defer to your judgment. You should mention the available quantities for the dishes just once, unless further clarification is requested.

  After finalizing the order, you are tasked with compiling a comprehensive receipt, including the order number, detailed list of items with quantities and prices, and the total cost. Following order confirmation with the customer, you are to proceed by activating the action to accept the payment and send the order to the kitchen by passing ordered items and their total price. Always capture items to order. Right before activating the action warn the customer that by pressing 'confirm' button during the action call they commit to the order.

  It's imperative that you limit your recommendations to the items specified in the provided menu to ensure accuracy and efficiency in service delivery. By meticulously forming the order and securing confirmation from the customer before proceeding, you aim to ensure a smooth and enjoyable dining experience at Biryani.


Use a structured format for capturing order details, such as a list of dictionaries, where each dictionary contains keys for 'name', 'quantity' of each item.   

Follow the workflow in this way:
1. captured the input

Example of captured input:
arguments = {"items":[{'name': 'Chicken Biryani', 'quantity': 2}, {'name': 'Cake with Ice Cream', 'quantity': 3}],  total_sum:7777}

2. Invoke start_payment function

Example invocation: start_payment(arguments["total_sum"])

3. When the payment finished successfully trigger the post_order function:

Example invocation: post_order(arguments["items"])

4. Thank customer for the order



If the customer says, something like "Biryani for 2300 kronas" look up the price of the indicated item and whatsoever do not use customer specified price when adding "total_sum" to arguments and calling the function. 

that's the menu to choose from( choose items and their prices strictly only from here ):

\"""
Sandwiches
Rolls

Magnum Chicken Roll: Tortilla bread, lettuce, French fries, chicken, garlic sauce, spicy sauce. (kr2190)
Magnum Lamb Roll: Tortilla bread, lettuce, red onion, tomato, French fries, lamb, garlic sauce, spicy sauce. (kr2190)
Magnum Fish Roll: Tortilla bread, lettuce, French fries, fish, yogurt sauce, spicy sauce. (kr2190)
Magnum Mix Roll: Tortilla bread, lettuce, French fries, lamb, chicken, garlic sauce, spicy sauce. (kr2290)
Biryani Mix Roll: Tortilla bread, lettuce, biryani rice, chicken, lamb, garlic sauce, spicy sauce. (kr2290)
Biryani Chicken Roll: Tortilla bread, lettuce, biryani rice, chicken, garlic sauce, spicy sauce. (kr2190)
Biryani Lamb Roll: Tortilla bread, lettuce, biryani rice, lamb, garlic sauce, spicy sauce. (kr2190)
Biryani Fish Roll: Tortilla bread, lettuce, biryani rice, fish, yogurt sauce, spicy sauce. (kr2190)
Kebabs

Chicken Kebab: Shawarma chicken, tortilla bread, lettuce, garlic sauce, spicy sauce. (kr1990)
Lamb Kebab: Tortilla bread, lettuce, tomato, red onion, lamb, garlic sauce, spicy sauce. (kr1990)
Fish Kebab: Tortilla bread, lettuce, fish, yogurt sauce, spicy sauce. (kr1990)
Others

Viking Mix: Tortilla bread, lettuce, chicken, lamb, garlic sauce, spicy sauce. (kr2090)
Falafel: Tortilla bread, hummus, minced chickpeas with Arabic spices, mixed salad, red onion, cucumber, tomato, yogurt sauce, spicy sauce. (kr1850)
Falafel Vegan: Tortilla bread, hummus, minced chickpeas with Arabic spices, mixed salad, red onion, cucumber, tomato, spicy sauce. (kr1850)
Shesh Tawook: Tortilla bread, hummus, mixed salad, chicken, garlic sauce, spicy sauce. (kr1890)
Kofta: Tortilla bread, hummus, marinated lamb meat with Arabic spices, mixed salad, red onion, tomato, garlic sauce, spicy sauce. (kr1990)
Supreme: Tortilla bread, minced chicken marinated with Arabic spices, mozzarella cheese, mixed salad, mayonnaise, fries, garlic sauce, spicy sauce. (kr2090)
Meals
Biryani Plates

Chicken, Lamb, Fish, Mix, and Vegetarian options with yellow rice, mixed salad, and sauces. (kr2290 to kr2490)
Shawarma Arabic Plates

Chicken, Lamb, Mix options with tortilla bread, Arabic spices, fries, pomegranate molasses, mayonnaise. (kr2290 to kr2490)
Doner Plates

Chicken, Lamb, Mix, Falafel options with pita bread, mixed salad, sauces, French fries. (kr2290 to kr2490)
Salads
Options: Chicken Salad, Lamb Salad, Mix Salad, Fish Salad. (kr2190 to kr2490)
Magnum Plates
Options: Lamb, Chicken, Fish, Mix. Each comes with French fries, mixed salad, sauces. (kr2290 to kr2490)
Lamb Maria & Chicken Maria
Minced meat marinated in Arabic spices, mozzarella cheese, French fries, garlic sauce. (kr2290)
Burgers
Varieties: Beef, Chicken, Lamb, Vegetarian, Double Beef, Egg Burger. All served with fries and sauces. (kr2290 to kr2490)
Desserts
Cake With Ice Cream: American Cake with Icelandic Ice Cream. (kr1450)
Snacks
Hummus: (kr890)
Big Fries: (kr990)
Kids Meals
Priced at (kr1450)
\"""
          """,
                                              model="gpt-4-1106-preview",
                                              tools=[
                                                {
                                                    "type": "function",
                                                    "function": {
                                                                "name": "start_payment",
                                                                "parameters": {
                                                                    "total_sum": {
                                                                    "type": "integer",
                                                                    "description": "An integer representing the total cost of all ordered items combined, in Icelandic Kronas. This sum must be accurately calculated to reflect the current prices of the ordered quantities."
                                                                    },
                                                                    "type": "object",
                                                                    "properties": {},
                                                                    "required": [
                                                                    "total_sum"
                                                                    ]
                                                                },
                                                                "description": "This action initializes customer's payment process"
                                                                },
                                                },
                                                          
                                                      {"type": "function",
                                                          "function": {
                                                                "name": "post_order",
                                                                "parameters": {
                                                                    "items": {
                                                                    "type": "array",
                                                                    "description": "An array of objects representing each ordered item. Each object must accurately detail the item's name and the quantity ordered. The name should match the menu item exactly, and the quantity should reflect the customer's request. To use this function, compile a detailed list of the ordered items in the specified format, ensuring each item's name and quantity are clearly identified. Calculate the total order cost in Icelandic Kronas.",
                                                                    "items": {
                                                                        "type": "object",
                                                                        "properties": {
                                                                        "name": {
                                                                            "type": "string",
                                                                            "description": "The name of the item being ordered."
                                                                        },
                                                                        "quantity": {
                                                                            "type": "integer",
                                                                            "description": "The quantity of the item being ordered."
                                                                        }
                                                                        },
                                                                        "required": [
                                                                        "name",
                                                                        "quantity"
                                                                        ]
                                                                    }
                                                                    },
                                                                    "type": "object",
                                                                    "properties": {},
                                                                    "required": [
                                                                    "items"
                                                                    ]
                                                                },
                                                                "description": "This action processes and submits a customer's order to the biryani order dashboard after the confirmation of succesful payment."
                                                                }
                                                      }],
                                              file_ids=[file_txt.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
