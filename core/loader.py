from core.api_handler import fetch_word_info
from core.tree_builder import WordNode

# ANSI Terminal Colors for CLI Feedback
RESET   = "\033[0m"
BOLD    = "\033[1m"
GREEN   = "\033[1;32m"
YELLOW  = "\033[1;33m"
RED     = "\033[1;31m"
CYAN    = "\033[1;36m"

def load_word(word):

    print(f"\n{YELLOW}Looking up: '{word}'...{RESET}")

    # Step 1: Query the Dictionary
    result = fetch_word_info(word)

    # Step 2: Handle API errors
    if "error" in result:
        print(f"{RED}Error fetching word: {result['error']}{RESET}")
        return {"error": result["error"]}

    # Step 3: Extract phonetics and audio URLs from response 
    phonetic_texts = []
    audio_urls = []

    for phonetic in result.get("phonetics", []):
        if phonetic.get("text"):
            phonetic_texts.append(phonetic["text"])
        if phonetic.get("audio"):
            audio_urls.append(phonetic["audio"])

    # Step 4: Create a WordNode instance for this word 
    word_node = WordNode(
        word=result["word"],
        phonetics=phonetic_texts,
        audio_urls=audio_urls
    )

    # Step 5: Add meanings and definitions grouped by part of speech
    for meaning in result.get("meanings", []):
        part_of_speech = meaning.get("partOfSpeech")
        definitions = meaning.get("definitions", [])
        word_node.add_meaning(part_of_speech, definitions)

    print(f"{GREEN} Successfully loaded: {word.upper()}{RESET}")
    return word_node
