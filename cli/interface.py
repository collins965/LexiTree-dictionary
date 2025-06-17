from core.loader import load_word

#ANSI Color Codes for CLI Styling 
RESET   = "\033[0m"
BOLD    = "\033[1m"
CYAN    = "\033[1;36m"
GREEN   = "\033[1;32m"
YELLOW  = "\033[1;33m"
RED     = "\033[1;31m"

# Introductory Banner
def print_welcome():
    print(f"{CYAN}{'=' * 40}{RESET}")
    print(f"{BOLD}📚 Welcome to LexiTree Dictionary CLI{RESET}")
    print(f"{CYAN}{'=' * 40}{RESET}")
    print("Type a word to look it up.")
    print("Type 'exit' to quit.\n")

# Main User Interaction Loop 
def main_menu():
    print_welcome()

    try:
        while True:
            # Prompt user for input
            word = input(" Enter a word: ").strip()

            # Handle 'exit' command
            if word.lower() == "exit":
                print(f"\n{GREEN}Goodbye! Thanks for using LexiTree.{RESET}\n")
                break

            # Handle empty input
            if not word:
                print(f"{YELLOW}Please enter a valid word.\n{RESET}")
                continue

            # Fetch word data using the loader module
            print(f"{CYAN}Fetching details from the dictionary...{RESET}")
            result = load_word(word)

            # Handle errors from API or loader
            if isinstance(result, dict) and "error" in result:
                print(f"{RED}Error: {result['error']}{RESET}\n")
            else:
                # Successfully loaded word — display as a tree
                result.display_tree()
                print(f"\n{GREEN}Word loaded successfully!\n{RESET}")

    except KeyboardInterrupt:
        # Graceful exit when user hits Ctrl+C
        print(f"\n\n{GREEN}Exiting LexiTree gracefully. See you again!{RESET}")

# === Entry Point ===
if __name__ == "__main__":
    main_menu()
