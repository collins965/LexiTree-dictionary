import os
import tempfile
import requests
import time
import pygame

# ANSI Terminal Colors for Pretty CLI Output
RESET   = "\033[0m"
BOLD    = "\033[1m"
GREEN   = "\033[1;32m"
CYAN    = "\033[1;36m"
YELLOW  = "\033[1;33m"
MAGENTA = "\033[1;35m"
RED     = "\033[1;31m"
BLUE    = "\033[1;34m"

class WordNode:
    """
    Represents a dictionary word with its phonetics, audio links, and definitions.
    This class supports:
    - Displaying formatted tree output for the CLI
    - Playing pronunciation audio using pygame
    """

    def __init__(self, word, phonetics=None, audio_urls=None):
        self.word = word
        self.phonetics = phonetics or []
        self.audio_urls = audio_urls or []
        self.meanings = []

    def add_meaning(self, part_of_speech, definitions):
        """Add a new meaning group (e.g., noun/verb) with its definitions."""
        self.meanings.append({
            "part_of_speech": part_of_speech,
            "definitions": definitions
        })

    def display_tree(self):
        """Nicely display the word, pronunciations, and definitions in the terminal."""
        print(f"\n{CYAN}{BOLD} Word Tree for: {self.word.upper()}{RESET}")

        # Display phonetics if available
        if self.phonetics:
            print(f"{YELLOW}Pronunciation(s): {', '.join(self.phonetics)}{RESET}")

        # Display meanings grouped by part of speech
        for meaning in self.meanings:
            print(f"\n{BLUE}{BOLD}🔹 Part of Speech: {meaning['part_of_speech'].capitalize()}{RESET}")
            for i, definition in enumerate(meaning['definitions'], 1):
                print(f"  {GREEN}{i}. {definition.get('definition')}{RESET}")

                if definition.get("example"):
                    print(f"     {MAGENTA}Example: {definition['example']}{RESET}")
                if definition.get("synonyms"):
                    print(f"     {YELLOW}Synonyms: {', '.join(definition['synonyms'])}{RESET}")
                if definition.get("antonyms"):
                    print(f"     {RED}Antonyms: {', '.join(definition['antonyms'])}{RESET}")

        # Ask user if they want to hear the pronunciation
        if self.audio_urls:
            choice = input(f"\n{CYAN}Would you like to hear the pronunciation? (y/n): {RESET}").strip().lower()
            if choice == 'y':
                self.play_pronunciation()

    def play_pronunciation(self, index=0):
        """
        Download and play the pronunciation audio using pygame.
        Defaults to the first audio URL in the list.
        """
        if index >= len(self.audio_urls):
            print(f"{RED}No valid audio available for this word.{RESET}")
            return

        url = self.audio_urls[index]

        try:
            # Try downloading the audio file
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # Save to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(response.content)
                    f.flush()
                    audio_file = f.name

                # Play the audio
                print(f"\n{YELLOW} Playing pronunciation for '{self.word}'...{RESET}\n")
                pygame.mixer.init()
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()

                # Wait for playback to complete
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

                # Cleanup
                pygame.mixer.quit()
                os.remove(audio_file)
            else:
                print(f"{RED}Failed to download audio (HTTP {response.status_code}).{RESET}")
        except Exception as e:
            print(f"{RED}Error playing audio: {e}{RESET}")
