import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

from promps import system_prompt
from call_function import available_functions, call_function

def main():
    args = parse_input()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        result = gemini_api_call(messages)

        if not result.candidates:
            print("No candidates returned from Gemini API.")
            return 1

        for candidate in result.candidates:
            if candidate.content:
                messages.append(candidate.content)

        if args.verbose:
            messages_texts = [part.text for message in messages for part in message.parts if getattr(part, "text", None)]
            handle_metadata(result, args.verbose, messages_texts)

        function_responses = handle_functions_calls(result, args.verbose)
        if function_responses:
            messages.append(types.Content(role="user", parts=function_responses))
            continue

        handle_response(result)
        return 0

    print("Reached max iterations (20) without a final response.")
    return 1

def parse_input():
    parser = argparse.ArgumentParser(description="Chatbot")
    
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    parser.add_argument("user_prompt", type=str, help="User prompt")
    
    return parser.parse_args()


def gemini_api_call(messages):
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    #result = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    result = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(
         system_instruction=system_prompt
        ,tools=[available_functions]
        )
    )
    
    return result

def handle_response(gemini_result):
    if not gemini_result.text:
        return
    
    print("Response:" + gemini_result.text)
    
    

def handle_metadata(gemini_result, verbose, messages_texts):
    if gemini_result.usage_metadata == None or not verbose:
        return
    
    print(f"User prompt: {",".join(messages_texts)}")
    print(f"Prompt tokens: {gemini_result.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {gemini_result.usage_metadata.candidates_token_count}")
    
    

def handle_functions_calls(gemini_result, verbose):
    function_results_parts = []
    function_calls = gemini_result.function_calls or []

    for function_call in function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
        call_function_result = call_function(function_call, verbose)
        
        if not call_function_result.parts:
            raise Exception("No response from function call")
        
        function_response = call_function_result.parts[0].function_response
        
        if function_response == None:
            raise Exception("No function response from function call")
        
        function_results_parts.append(call_function_result.parts[0])
        
        if verbose:
            print(f"-> {call_function_result.parts[0].function_response.response}")

    return function_results_parts
        

if __name__ == "__main__":
    sys.exit(main())
