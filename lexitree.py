import pyttsx3
import threading
import time
from core.db_manager import initialize_db, save_word
from core.loader import load_word

# ANSI Terminal Colors for Enhanced CLI Output
RESET   = "\033[0m"
BOLD    = "\033[1m"
RED     = "\033[1;31m"
GREEN   = "\033[1;32m"
YELLOW  = "\033[1;33m"
BLUE    = "\033[1;34m"
CYAN    = "\033[1;36m"
MAGENTA = "\033[1;35m"

# Global States
engine = None               # pyttsx3 engine instance
speech_thread = None        # Thread for speaking
stop_speech_flag = False    # Flag to interrupt speech

# Initialize Text-to-Speech Engine
def init_speech_engine(gender="female", rate=160):
    """
    Set up pyttsx3 with the preferred voice and rate.
    Tries to select a voice by gender keyword (Windows: Zira/David).
    """
    global engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    selected_voice = voices[0].id  # Default voice

    for voice in voices:
        if gender == "female" and "zira" in voice.name.lower():
            selected_voice = voice.id
            break
        elif gender == "male" and "david" in voice.name.lower():
            selected_voice = voice.id
            break

    engine.setProperty('voice', selected_voice)
    engine.setProperty('rate', rate)

    print(f"{YELLOW} Using voice: {selected_voice.split('.')[-1]}{RESET}")
    return engine

# Background Speech Playback
def speak_text(text):
    """
    Speak text aloud using a background thread.
    Lets user interrupt the speech manually.
    """
    global speech_thread, stop_speech_flag

    def _speak():
        global stop_speech_flag
        engine.say(text)
        engine.runAndWait()
        stop_speech_flag = False  # Reset after completion

    speech_thread = threading.Thread(target=_speak, daemon=True)
    speech_thread.start()

    # Wait for user to interrupt
    input(f"\n{MAGENTA} Press Enter to pause/interrupt speech...{RESET}")
    stop_speech_flag = True
    engine.stop()
    print(f"{YELLOW} Speech stopped.{RESET}")

# === Build Readable Text for TTS ===
def build_speech_text(word_node):
    """
    Constructs a full sentence block from the WordNode for speaking.
    Covers word, pronunciation, definitions, examples, and synonyms/antonyms.
    """
    lines = [f"Word: {word_node.word}."]

    if word_node.phonetics:
        lines.append(f"Pronunciation: {', '.join(word_node.phonetics)}.")

    for meaning in word_node.meanings:
        lines.append(f"Part of speech: {meaning['part_of_speech']}.")
        for i, d in enumerate(meaning["definitions"], 1):
            lines.append(f"Definition {i}: {d.get('definition', '')}.")
            if d.get("example"):
                lines.append(f"For example: {d['example']}.")
            if d.get("synonyms"):
                lines.append(f"Synonyms include: {', '.join(d['synonyms'])}.")
            if d.get("antonyms"):
                lines.append(f"Antonyms include: {', '.join(d['antonyms'])}.")
    
    return " ".join(lines)

# Main Application Loop
def run():
    """
    Main entry point for the LexiTree dictionary tool.
    - Initializes DB
    - Asks user for words
    - Loads definitions via API
    - Optionally speaks them
    - Saves them to local DB
    """
    initialize_db()
    print(f"\n{CYAN}{BOLD}Welcome to LexiTree Dictionary!{RESET}")

    # Ask user for voice preference
    voice_preference = input(f"{YELLOW} Choose voice [male/female]: {RESET}").strip().lower()
    init_speech_engine(gender=voice_preference)

    while True:
        word = input(f"\n{BLUE}Enter a word to look up and save (or type 'exit' to quit): {RESET}").strip()

        if word.lower() == "exit":
            print(f"\n{CYAN}Goodbye! Thanks for using LexiTree.{RESET}")
            break

        # Load word info using API
        result = load_word(word)

        if isinstance(result, dict) and "error" in result:
            print(f"\n{RED}Error: {result['error']}{RESET}")
        else:
            # Display the word in CLI tree format
            result.display_tree()

            # Optionally speak the word and its definitions
            if input(f"\n{YELLOW}🔈 Read aloud? (y/n): {RESET}").lower() == "y":
                speech_text = build_speech_text(result)
                speak_text(speech_text)

            # Save to local database
            save_word(result)
            print(f"{GREEN}Word saved successfully to your dictionary!{RESET}")

# Entry Point
if __name__ == "__main__":
    run()
