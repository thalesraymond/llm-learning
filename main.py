import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

def main():
    args = parse_input()
    # Now we can access `args.user_prompt`

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    result = gemini_api_call(messages)

    print_results(messages, result, args.verbose)
    messages[0].parts

def parse_input():
    parser = argparse.ArgumentParser(description="Chatbot")
    
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    parser.add_argument("user_prompt", type=str, help="User prompt")
    
    return parser.parse_args()


def gemini_api_call(messages):
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    result =client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    return result

def print_results(messages, gemini_result, verbose=False):
    messages_texts = [part.text for message in messages for part in message.parts]

    if gemini_result.usage_metadata != None and verbose:
        print(f"User prompt: {",".join(messages_texts)}")
        print(f"Prompt tokens: {gemini_result.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {gemini_result.usage_metadata.candidates_token_count}")

    print("Response:" + gemini_result.text)

if __name__ == "__main__":
    main()
