from core.api_handler import fetch_word_info

# Main function to handle user input and display dictionary data
def run():
    # Ask the user to type a word
    word = input("Enter a word: ").strip()

    # Fetch word information using the API handler
    result = fetch_word_info(word)

    # If there was an error (e.g., word not found, network issue)
    if "error" in result:
        print(f"\nError: {result['error']}")
    else:
        print(f"\nWord: {result['word']}")

        # Display pronunciation(s) if available
        if result["phonetics"]:
            print(f" Pronunciation: {', '.join(result['phonetics'])}")

        # Loop through each meaning (part of speech)
        for meaning in result["meanings"]:
            print(f"\n Part of Speech: {meaning['partOfSpeech']}")

            # Loop through the definitions under this part of speech
            for i, d in enumerate(meaning["definitions"], 1):
                print(f"  {i}. {d['definition']}")

                # Optional details: example, synonyms, antonyms
                if d["example"]:
                    print(f"Example: {d['example']}")
                if d["synonyms"]:
                    print(f"Synonyms: {', '.join(d['synonyms'])}")
                if d["antonyms"]:
                    print(f"Antonyms: {', '.join(d['antonyms'])}")

# Run the function when this script is executed directly
if __name__ == "__main__":
    run()