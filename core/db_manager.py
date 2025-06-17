import sqlite3

DB_NAME = "lexitree.db"

#  ANSI Terminal Colors for Feedback 
RESET   = "\033[0m"
GREEN   = "\033[1;32m"
RED     = "\033[1;31m"
YELLOW  = "\033[1;33m"
CYAN    = "\033[1;36m"

# Get a database connection with foreign key support 
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Initialize tables: words and meanings 
def initialize_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Create `words` table to store basic word info
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE,
                phonetics TEXT
            )
        ''')

        # Create `meanings` table to store definitions and related data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meanings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_id INTEGER,
                part_of_speech TEXT,
                definition TEXT,
                example TEXT,
                synonyms TEXT,
                antonyms TEXT,
                FOREIGN KEY(word_id) REFERENCES words(id)
            )
        ''')

        conn.commit()
        print(f"{CYAN} Database initialized successfully!{RESET}")

# Save a WordNode (word + meanings) into the database
def save_word(word_node):
    with get_connection() as conn:
        cursor = conn.cursor()
        phonetics_str = ", ".join(word_node.phonetics)

        try:
            # Insert word and its phonetics
            cursor.execute(
                "INSERT INTO words (word, phonetics) VALUES (?, ?)",
                (word_node.word, phonetics_str)
            )
            word_id = cursor.lastrowid

        except sqlite3.IntegrityError:
            # Handle duplicate word gracefully
            print(f"{YELLOW}'{word_node.word}' already exists in the database.{RESET}")
            return

        else:
            # Insert related meanings and definitions
            for meaning in word_node.meanings:
                for d in meaning["definitions"]:
                    cursor.execute('''
                        INSERT INTO meanings (
                            word_id, part_of_speech, definition, example, synonyms, antonyms
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        word_id,
                        meaning["part_of_speech"],
                        d.get("definition"),
                        d.get("example"),
                        ", ".join(d.get("synonyms", [])),
                        ", ".join(d.get("antonyms", []))
                    ))

            conn.commit()
            print(f"{GREEN}Word '{word_node.word}' saved successfully!{RESET}")

# === Retrieve a word from the local database and reconstruct WordNode ===
def get_saved_word(word):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Fetch basic word data
        cursor.execute("SELECT id, phonetics FROM words WHERE word = ?", (word,))
        row = cursor.fetchone()

        if not row:
            print(f"{RED}Word '{word}' not found in local database.{RESET}")
            return None

        word_id, phonetics_str = row

        # Delayed import to prevent circular dependency
        from core.tree_builder import WordNode

        word_node = WordNode(
            word,
            phonetics=phonetics_str.split(", ") if phonetics_str else []
        )

        # Fetch and group meanings by part of speech
        cursor.execute('''
            SELECT part_of_speech, definition, example, synonyms, antonyms 
            FROM meanings WHERE word_id = ?
        ''', (word_id,))

        meanings_map = {}

        for part_of_speech, definition, example, synonyms, antonyms in cursor.fetchall():
            if part_of_speech not in meanings_map:
                meanings_map[part_of_speech] = []

            meanings_map[part_of_speech].append({
                "definition": definition,
                "example": example,
                "synonyms": synonyms.split(", ") if synonyms else [],
                "antonyms": antonyms.split(", ") if antonyms else []
            })

        # Add meanings back into the WordNode object
        for pos, definitions in meanings_map.items():
            word_node.add_meaning(pos, definitions)

        print(f"{CYAN}Retrieved '{word}' from local database.{RESET}")
        return word_node
