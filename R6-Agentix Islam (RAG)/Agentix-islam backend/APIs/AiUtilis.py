import re

import firebase_admin
from firebase_admin import credentials, firestore


def calculate_gemini_cost(usage_data, model_name="gemini-2.5-flash"):
    """
    Calculates the total cost for Gemini API usage based on the specified model.

    Args:
        usage_data (dict): A dictionary containing token counts, e.g.,
                           {
                               "prompt_token_count": int,
                               "candidates_token_count": int,
                               "total_token_count": int,
                               "thoughts_token_count": int,
                           }
        model_name (str): The name of the Gemini model to use for pricing.
                          Accepted values are 'flash-lite', 'flash', and 'pro'.
                          Defaults to 'flash'.

    Returns:
        dict: The updated usage_data dictionary including the "total_cost" field.
    """
    # Define pricing per 1M tokens for each model
    PRICING = {
        # Pricing for Gemini 2.5 Flash-Lite
        "gemini-2.5-flash-lite": {
            "input": 0.10,
            "output": 0.40,
        },
        # Pricing for Gemini 2.5 Flash
        "gemini-2.5-flash": {
            "input": 0.30,
            "output": 2.50,
        },
        # Pricing for Gemini 2.5 Pro
        "gemini-2.5-pro": {
            "input": 1.25,
            "output": 10.00,
        },
    }

    # Retrieve the correct pricing based on the model_name
    prices = PRICING.get(model_name.lower())
    if not prices:
        print(f"Error: Model '{model_name}' not found. Using default 'flash' pricing.")
        prices = PRICING["gemini-2.5-flash"]

    # Convert token counts to millions of tokens for calculation
    prompt_tokens_in_millions = usage_data.get("prompt_token_count", 0) / 1_000_000
    candidates_tokens_in_millions = usage_data.get("candidates_token_count", 0) / 1_000_000

    # Calculate the cost for input and output tokens
    input_cost = prompt_tokens_in_millions * prices["input"]
    output_cost = candidates_tokens_in_millions * prices["output"]

    # Calculate the total cost
    total_cost = input_cost + output_cost

    # Add the total_cost to the usage_data dictionary
    usage_data["total_cost"] = total_cost

    return usage_data



def extract_pages(text: str) -> list[int]:
    match = re.search(r'--Resources--\s*\[(.*?)\]', text, re.DOTALL)
    if match:
        pages_str = match.group(1)
        page_numbers = [int(p.strip()) for p in pages_str.split(',')]

        return page_numbers

    # Return an empty list if the pattern is not found.
    return []


def extract_and_remove_resources(text: str) -> tuple[str, list[int]]:
    try:
        pages = extract_pages(text)
        cleaned_text = re.sub(r'--Resources--.*', '', text, flags=re.DOTALL).strip()
        return cleaned_text, pages
    except:
        return text, []



