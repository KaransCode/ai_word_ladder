import sys
import os

# Force UTF-8 encoding for terminal (if you want to keep emojis, otherwise harmless)
sys.stdout.reconfigure(encoding='utf-8')
from collections import deque

class WordLadderSolver:
    def __init__(self, dictionary_words):
        # We convert the list of words to a Set for O(1) ultra-fast lookups
        self.word_set = set(word.lower() for word in dictionary_words)

    def get_neighbors(self, word):
        """Generates all valid 1-letter transformations of a word."""
        neighbors = []
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        
        # Loop through each character position in the word
        for i in range(len(word)):
            # Try replacing it with every letter in the alphabet
            for char in alphabet:
                if char != word[i]:
                    # Build the new word
                    new_word = word[:i] + char + word[i+1:]
                    
                    # If it's a real word, it's a valid neighbor!
                    if new_word in self.word_set:
                        neighbors.append(new_word)
        return neighbors

    def solve_bfs(self, start_word, target_word):
        """Uses BFS to find the shortest path between two words."""
        start_word = start_word.lower()
        target_word = target_word.lower()

        if start_word not in self.word_set or target_word not in self.word_set:
            return "Error: Both words must be in the dictionary."
        if len(start_word) != len(target_word):
            return "Error: Words must be the same length."

        # The queue stores a tuple: (current_word, path_taken_so_far)
        queue = deque([(start_word, [start_word])])
        
        # The visited set prevents infinite loops (e.g., cold -> cord -> cold)
        visited = set([start_word])

        while queue:
            current_word, path = queue.popleft()

            # Goal Test: Did we reach the target?
            if current_word == target_word:
                return path

            # Generate neighbors and add them to the queue
            for neighbor in self.get_neighbors(current_word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    # Add the neighbor to the queue, and append it to our path history
                    queue.append((neighbor, path + [neighbor]))

        return "No valid path found between the words."

def load_dictionary(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file]

# ==========================================
# 🚀 INTERACTIVE EXECUTION
# ==========================================

if __name__ == "__main__":
    print("Loading dictionary...")
    try:
        # Make sure you have a 'words.txt' file in the same folder as this script!
        real_dictionary = load_dictionary('words.txt')
        ai_solver = WordLadderSolver(real_dictionary)
    except FileNotFoundError:
        print("❌ Error: 'words.txt' not found! Please make sure the file is in the same folder.")
        sys.exit()

    print("\n" + "="*40)
    print("  🧠 THE AI WORD LADDER SOLVER  ")
    print("="*40)

    # Use input() to capture the words from the user
    start = input("Enter the Start word: ").strip()
    target = input("Enter the Target word: ").strip()

    print(f"\nSearching for the shortest path from '{start.upper()}' to '{target.upper()}'...\n")

    # Run BFS
    result_path = ai_solver.solve_bfs(start, target)

    # Output the results
    if isinstance(result_path, list):
        print(f"Success! Shortest path found in {len(result_path) - 1} steps:")
        print(" ➔ ".join(word.upper() for word in result_path))
        print("\n")
    else:
        print(f"❌ {result_path}\n")