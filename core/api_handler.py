import requests

#ANSI Terminal Colors for Visual CLI Feedback
RESET  = "\033[0m"
GREEN  = "\033[1;32m"
RED    = "\033[1;31m"
YELLOW = "\033[1;33m"

def fetch_word_info(word):
    """
    Fetches detailed information about a given word from the Free Dictionary API.
    
    Parameters:
        word (str): The English word to search for.
    
    Returns:
        dict: A structured dictionary containing the word, phonetics, and meanings,
              or an error message if the word is not found or a network issue occurs.
    """
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        # Send a GET request with a timeout to prevent hanging
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise exception for HTTP error codes

        data = response.json()

        # Check if the response contains valid word data
        if isinstance(data, list) and data:
            entry = data[0]

            # Start building structured word information
            word_info = {
                "word": entry.get("word"),
                "phonetics": entry.get("phonetics", []),
                "meanings": []
            }

            # Process each meaning (part of speech + definitions)
            for meaning in entry.get("meanings", []):
                definitions = []

                for d in meaning.get("definitions", []):
                    definitions.append({
                        "definition": d.get("definition"),
                        "example": d.get("example"),
                        "synonyms": d.get("synonyms"),
                        "antonyms": d.get("antonyms")
                    })

                word_info["meanings"].append({
                    "partOfSpeech": meaning.get("partOfSpeech"),
                    "definitions": definitions
                })

            print(f"{GREEN}Successfully fetched info for: '{word}'{RESET}")
            return word_info

        elif response.status_code == 404:
            # Handle case where word is not found in the dictionary
            error_msg = f"The word '{word}' was not found in the dictionary."
            print(f"{YELLOW}{error_msg}{RESET}")
            return {"error": error_msg}

        else:
            # Handle unexpected but valid responses
            error_msg = f"Unexpected error occurred. Status code: {response.status_code}"
            print(f"{RED}{error_msg}{RESET}")
            return {"error": error_msg}

    except requests.exceptions.RequestException as e:
        # Handle network errors or API unavailability
        error_msg = f"Network error: {str(e)}"
        print(f"{RED}{error_msg}{RESET}")
        return {"error": error_msg}
