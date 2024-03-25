import os
from time import sleep
#from packaging import version (omit version check for now)
from flask import Flask, request, jsonify, render_template, abort
import openai
from openai import OpenAI
import api.functions as functions
#import functions
import json
import requests
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


# Check OpenAI version is correct(omit version check for now)
"""
required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
if current_version < required_version:
  raise ValueError(f"Error: OpenAI version {openai.__version__}"
                   " is less than the required version 1.1.1")
else:
  print("OpenAI version is compatible.")
"""

# Start Flask app
app = Flask(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Init client
client = OpenAI(
    api_key=OPENAI_API_KEY)  # should use env variable OPENAI_API_KEY

# Create new assistant or load existing
assistant_id = functions.create_assistant(client)


# Start conversation thread
@app.route('/start', methods=['GET'])
def start_conversation():
  # Create new assistant or load existing
  print("Returned id ", assistant_id) # Debugging line
  print("Starting a new conversation...")  # Debugging line
  thread = client.beta.threads.create()
  print(f"New thread created with ID: {thread.id}")  # Debugging line
  return jsonify({"thread_id": thread.id})

@app.route('/payment_check', methods=['GET', 'POST'])
def payment_check():
  data = request.json
  print("\n\nWebhook on payment_check endpoint: \n\n", data)
  # Get the referrer
  referrer = request.referrer

  if referrer:
    if data["type"] == "PAYMENT_COMPLETED":
      # The URL you're sending the POST request to
      url = "https://biryani-order-dashboard-sqng.vercel.app/orders"

      # The header to indicate JSON data is being sent
      headers = {"Content-Type": "application/json"}

      # The data you're sending, formatted as JSON
      data = {"action": "PUBLISH_THE_ORDER"}

      # Sending the POST request
      response = requests.post(url, json=data, headers=headers)

      if response.status_code == 200:
        print("Payment succeeded event sent the request on orders")
      else:
        print("Payment succeeded event failed to send the request on orders")
      
      return render_template('successful_payment.html')
    
    if data["type"] == "PAYMENT_FAILED":
      # The URL you're sending the POST request to
      url = "https://biryani-order-dashboard-sqng.vercel.app/orders"

      # The header to indicate JSON data is being sent
      headers = {"Content-Type": "application/json"}

      # The data you're sending, formatted as JSON
      data = {"action": "DELETE_THE_ORDER"}

      # Sending the POST request
      response = requests.post(url, json=data, headers=headers)

      if response.status_code == 200:
        print("Payment failed event sent the request on orders")
      else:
        print("Payment failed event failed (haha, double failure) to send the request on orders") 
      
      return render_template('error_payment.html')
  else:
    return "There direct access to this page is prohibited!" 


@app.route('/error_payment', methods=['GET', 'POST'])
def error_payment():
  
  data = request.json
  
  # Get the referrer
  referrer = request.referrer

    # Check if the referrer matches the pattern
  if referrer:
    return render_template('error_payment.html')
  else:
    return abort(403)

# Generate response
@app.route('/chat', methods=['POST'])
def chat():
  data = request.json
  thread_id = data.get('thread_id')
  user_input = data.get('message', '')

  if not thread_id:
    print("Error: Missing thread_id")  # Debugging line
    return jsonify({"error": "Missing thread_id"}), 400

  print(f"Received message: {user_input} for thread ID: {thread_id}"
        )  # Debugging line

  # Add the user's message to the thread
  response = client.beta.threads.messages.create(thread_id=thread_id,
                                      role="user",
                                      content=user_input)
  
  # Run the Assistant
  run = client.beta.threads.runs.create(thread_id=thread_id,
                                        assistant_id=assistant_id)
  
  # Check if the Run requires action (function call)
  while True:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                   run_id=run.id)
    print(f"Run status: {run_status.status}")
    if run_status.status == 'completed':
      break
    sleep(1)  # Wait for a second before checking again
    if run_status.status == "requires_action":
      print("Action in progress...")
      # Handle the function call
      for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
        if tool_call.function.name == "start_payment":
          # Pizza order accepted
          arguments = json.loads(tool_call.function.arguments)

          print("\n\n\n\nRetrieved arguments:\n", arguments, "\n\n\n\n") #debugging line

          output = functions.start_payment(arguments["items"])
          client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id,
                                                       run_id=run.id,
                                                       tool_outputs=[{
                                                           "tool_call_id":
                                                           tool_call.id,
                                                           "output":
                                                           json.dumps(output)
                                                       }])
        """
        if tool_call.function.name == "post_order":
          # Pizza order accepted
          arguments = json.loads(tool_call.function.arguments)
          
          print("\n\n\n\nRetrieved arguments:\n", arguments, "\n\n\n\n") #debugging line

          output = functions.post_order(arguments["items"])
          client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id,
                                                       run_id=run.id,
                                                       tool_outputs=[{
                                                           "tool_call_id":
                                                           tool_call.id,
                                                           "output":
                                                           json.dumps(output)
                                                       }])
          
          if tool_call.function.name == "start_payment":
          # Payment Started
          arguments = json.loads(tool_call.function.arguments)
          output = functions.start_payment(arguments["method"])
          client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id,
                                                       run_id=run.id,
                                                       tool_outputs=[{
                                                           "tool_call_id":
                                                           tool_call.id,
                                                           "output":
                                                           json.dumps(output)
                                                       }])
          """                                             
  # Retrieve and return the latest message from the assistant
  messages = client.beta.threads.messages.list(thread_id=thread_id)
  response = messages.data[0].content[0].text.value     

  print(f"Assistant response: {response}")  # Debugging line
  return jsonify({"response": response})

"""
# Test function 1
@app.route('/hellotest', methods=['GET'])
def print_hello():
    return 'Hello Worrrrld!'

# Test function 2
@app.route('/')
def print_main_pahe():
    return 'You are on the main page!'
"""

# Run server
if __name__ == '__main__':
  app.run(debug=True)
