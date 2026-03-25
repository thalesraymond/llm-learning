import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    result = gemini_api_call(messages)

    print_results(result)


def gemini_api_call(messages):
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    result =client.models.generate_content(model="gemini-2.5-flash", contents=messages)

    return result

def print_results(gemini_result):
    if gemini_result.usage_metadata != None:
        print(f"Prompt tokens: {gemini_result.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {gemini_result.usage_metadata.candidates_token_count}")

    print("Response:" + gemini_result.text)

if __name__ == "__main__":
    main()
