import json
import os
import requests
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

assistant_file_path = "assistant.json"

def start_payment_post_order(items, total_sum):
    
  payment_successful = False

  print(f"Calling Rapyd API to complete the payment of {total_sum} kronas")

  print(f"The amount of {total_sum} was successfully paid")

  payment_went_through = True

  if payment_went_through:
     payment_successful = True
  
  if payment_successful:
  
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
    else:
        print('Failed to post order. Status code:', response.status_code)

  else:
     print("Payment is unsuccessful, revertin back...")

def create_assistant(client):
  if os.environ.get("MAKE_NEW_ASSISTANT") != "YES":
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file_txt = client.files.create(file=open("BiryaniGPT_Menu.txt", "rb"),
        purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
          You are the assistant tasked with initiating interactions by inquiring about the customer's preferred language, ensuring that communication is both comfortable and effective. If asked about your functions, you should clearly articulate your role in facilitating the selection of Syrian cuisine at the Biryani restaurant, emphasizing your ability to communicate in any preferred language.

  Do not make the first response lengthy. Not more than 4 sentences.

  Your communications must be direct and efficient, aimed at simplifying the customer's decision-making process. You should offer personalized dish recommendations based on the customer's expressed preferences or, alternatively, provide suggestions based on your expertise. After presenting the menu options, you need to ascertain whether the customer is prepared to place an order or requires further information.

  Upon the customer's readiness to order, you must summarize the selected items, detailing names, quantities, and prices, and propose the addition of complementary snacks such as hummus (890 Icelandic kronas) and fries (990 Icelandic kronas) instead of beverages. Before passing the order to API always reassure the correctness of the order by asking the customer to confirm the details of the orders.

  When confronted with the request for recommendations, you should allow the customer to specify their dietary preferences or defer to your judgment. You should mention the available quantities for the dishes just once, unless further clarification is requested.

  After finalizing the order, you are tasked with compiling a comprehensive receipt, including the order number, detailed list of items with quantities and prices, and the total cost. Following order confirmation with the customer, you are to proceed by activating the action to accept the payment and send the order to the kitchen by passing ordered items and their total price. Right before activating the action warn the customer that by pressing 'confirm' button during the action call they commit to the order.

  It's imperative that you limit your recommendations to the items specified in the provided menu to ensure accuracy and efficiency in service delivery. By meticulously forming the order and securing confirmation from the customer before proceeding, you aim to ensure a smooth and enjoyable dining experience at Biryani.
          """,
                                              model="gpt-4-1106-preview",
                                              tools=[
                                                {
                                                    "type": "function",
                                                    "function": {
                                                        "name": "start_payment_post_order",
                                                        "description": "Starts the payment process and upon successful payment sends the accepted order to the kitchen",
                                                        "parameters": {
                                                            "type": "object",
                                                            "properties": {
                                                                "items": {
                                                                   "type": "object",
                                                                    "description": "The list of dictionaries of names of items to order along with the quantity"
                                                                },
                                                                "total_sum": {
                                                                    "type": "integer",
                                                                    "description": "The total cost of the order in Icelandic Kronas" 
                                                                }
                                                            },
                                                            "required": ["items", "total_sum"],
                                                        },
                                                    },
                                                },
                                                          
                                                      #{"type": "function",
                                                          #"function": {
                                                              #"name": "start_payment",
                                                              #"description": "Starts the payment process with the specified inferred from the conversation payment method before registering the order",
                                                              #"parameters": {
                                                                  #"type": "object",
                                                                  #"properties": {
                                                                      #"method": {"type": "string", "enum": 
                                                                    #["PayPal", "Card"]},
                                                                  #},
                                                                  #"required": ["method"],
                                                              #},
                                                          #},
                                                      #},
                                                      {
                                                  "type": "retrieval"
                                              }],
                                              file_ids=[file_txt.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
