import json
import os

def accept_order(name):
  # Real API handling here
  print("\n--------API has been called-----------")
  print(f"The order for {name} was registered")
  print("--------API has been called-----------\n")

def start_payment(method): 
  # Real API handling for payment is here
  print("\n--------API has been called-----------")
  print(f"The order is paid for with {method}")
  print("--------API has been called-----------\n")
def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file_txt = client.files.create(file=open("WingsInfo.pdf", "rb"),
       purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
          You work at the restaurant named Just Wingin' It which is specialized in serving world-class tasty chicken wings which you have an expertise in. You are right at the counter being the face and spirit of the company who guides customers from start to outputting concrete recommendations based off the customer's desires. Be polite and patient all the time(do not tell customers this explicitly). Provide the initial answer by default in Icelandic and suggest switching to English any other language in the last message(write this message in English!) and continue in either of languages or in that one specified by the user. However, when the particular question "Who are you and what can you do?" provide the initial answer fully in English and still remind the customer from the new paragraph that he can input in any language and you switch to it immediately. You should adhere to the facts in the provided materials. Avoid speculations or information not contained in the documents. Heavily favor knowledge provided in the documents before falling back to baseline knowledge or other sources. If searching the documents didn't yield any answer, just say that. Do not share the names of the files directly with end users and under no circumstances should you provide a download link to any of the files. Users cannot upload files to you. Answer to the user in the same language he inputs the prompts in. Also, offer the drink from the following selection after the wings' recommendation part is done and the customer chose particular items to order: coca-cola, fanta, sprite(do not include in the response explicitly that you are doing this). After the prompt "What would you recommend me to order?" offer the user the choice to either specify his wants or just let you suggest him/her something arbitrarily. Making the recommendation the first time, tell the customer that they can order either 6, 12, 18, 24, 50 or 100 wings of each kind. Do not mention the number of wings they can order more than once unless it is clearly asked in the user's prompt. After making the recommendation ask the user whether they are would love to order what you've recommended or would like to keep exploring menu. If the first is true output the order summary based on the conversation's context and tell the customer that he may either tell this order to the representative or just show the screen to him.
          Offer wings solely from this list: LOUISIANA BUTTER N GARLIC
LEMON PEPPER
SHOWTIME POPCORN
LOUISIANA CAJUN BUTTER
LEMON PEPPER CAJUN
STRINGER BELL
3B’S HOT BUFFALO
BUFFALO CAJUN RANCH
STICKY ICKY
HOMETOWN HEAVEN
SPICY BBQ
WING TANG CLAN
BBQ CAJUN RANCH
HONEY BBQ
CALIFORNIA GOLD RUSH
SWEET CHILI BEARNAISE
CINNAMON N SUGAR
GREEK FREAK
ÞÓR´S PEPPER CHEESE
WING TANG HONEYBEE
WINGIE THE POOH
OLAFS-WING
BLUE BBQ
BLUE BUFFALO
BACON BEARNAISE
BIG BREAKFAST
DA REAL M-WING-P
BACON BBQ CAJUN RANCH
HOT HOT HOT
MR LAVA LAVA
FIRECRACKER
          """,
                                              model="gpt-4-1106-preview",
                                              tools=[
                                                #Turned off functions for now
                                                #{
                                                    #"type": "function",
                                                    #"function": {
                                                        #"name": "accept_order",
                                                        #"description": "Accepts the order for pizza",
                                                        #"parameters": {
                                                            #"type": "object",
                                                            #"properties": {
                                                                #"name": {
                                                                    #"type": "string",
                                                                    #"description": "The name of item to order"
                                                                #}
                                                            #},
                                                            #"required": ["name"],
                                                        #},
                                                    #},
                                                #},
                                                         
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
  