import requests

# Function to fetch word details from the free Dictionary API
def fetch_word_info(word):
    # Construct the URL for the API request
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        # Send GET request to the API
        response = requests.get(url)

        # If the word is found and request is successful
        if response.status_code == 200:
            # Parse the first result from the JSON response
            data = response.json()[0]

            # Initialize a dictionary to hold all relevant word info
            word_info = {
                "word": data.get("word"),
                "phonetics": [
                    p.get("text") for p in data.get("phonetics", []) if p.get("text")
                ],
                "meanings": []
            }

            # Loop through meanings (parts of speech like noun, verb, etc.)
            for meaning in data.get("meanings", []):
                definition_list = []

                # Each meaning has a list of definitions, examples, synonyms, etc.
                for definition in meaning.get("definitions", []):
                    definition_list.append({
                        "definition": definition.get("definition"),
                        "example": definition.get("example"),
                        "synonyms": definition.get("synonyms"),
                        "antonyms": definition.get("antonyms")
                    })

                # Append the meaning and its definitions to our main word_info dict
                word_info["meanings"].append({
                    "partOfSpeech": meaning.get("partOfSpeech"),
                    "definitions": definition_list
                })

            return word_info

        # If the word is not found
        elif response.status_code == 404:
            return {"error": f"The word '{word}' was not found in the dictionary."}

        # Handle any other unexpected response
        else:
            return {"error": f"Unexpected error: {response.status_code}"}

    # If there's a connection issue or request fails
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
