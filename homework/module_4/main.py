from openai import OpenAI
import os
import json
import time

client = OpenAI(
    api_key=os.environ['openai_key'], 
    base_url=os.environ['openai_base'], 
    )
tool_list = [
        {
            "type": "function",
            "function": {
                "name": "modify_config",
                "description": "Modify configuration",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service_name": {
                            "type": "string",
                            "description": 'the service name need to update, example: gateway, k8s',
                        },
                         "key": {
                            "type": "string",
                            "description": 'the configuration name need to change, example: vendor, image',
                        },
                         "value": {
                            "type": "string",
                            "description": 'the new value of the config key, example: alipay, 1213',
                        },
                    },
                },
                "required": ["service_name", "key", "value"],
            },
        },
        {
            "type": "function",
            "function": {
                "name": "restart_service",
                "description": "Restart service",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service_name": {
                            "type": "string",
                            "description": 'the service name need to restart, example: gateway',
                        },
                    },
                },
                "required": ["service_name"],
            },
        },
        {
            "type": "function",
            "function": {
                "name": "apply_manifest",
                "description": "deploy a service",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "resource_type": {
                            "type": "string",
                            "description": 'the resource name need to deploy, example: application',
                        },
                         "image": {
                            "type": "string",
                            "description": 'the image used to deploy, example: image',
                        },                       
                    },
                },
                "required": ["resource_type","image"],
            },
        }
    ]


def modify_config(service_name, key, value):
    print("\nThe input service:", service_name)
    return json.dumps({"log": key+"is changed to "+value})

def restart_service (service_name):
    print("\nThe restart service is:", service_name)
    return json.dumps({"log": service_name+" is already restart"})

def apply_manifest  (resource_type, image):
    print("\nDeployment is :", resource_type)
    return json.dumps({"log": resource_type+"is deployed with image "+image})

def run_conversation():

# step 1: put all the pre-defined function to chatgpt
    user_input = input("input your instruction:")
    messages = [
        {
            "role": "system",
            "content": "you are a ops expert, your work is to solve client's problems",
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]
    tools = tool_list
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    print("\nChatGPT want to call function: ", tool_calls)

# step 2: To check whether chatgpt got the correct function 

    if tool_calls is None:
        print("no tool call to use")
    if tool_calls:
        avaible_functions= {
            "modify_config": modify_config,
            "restart_service": restart_service,
            "apply_manifest": apply_manifest,
        }

        messages.append(response_message)

# Step 3: got the function call response and app to chatgpt model
        for tool_call in tool_calls:
            function_name =  tool_call.function.name
            function_to_call  = avaible_functions[function_name]
            function_args =  json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)

            messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
            })

# Step 4: exchange the functioncall result with mode and got response
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )

            return response.choices[0].message
        
print("LLM Res: ", run_conversation())

