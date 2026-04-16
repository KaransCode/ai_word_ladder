import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import time

# ==========================================
# 🧠 THE AI LOGIC (Backend)
# ==========================================
class WordLadderSolver:
    def __init__(self, dictionary_words):
        self.word_set = set(word.lower() for word in dictionary_words)

    def get_neighbors(self, word):
        """Generates all valid 1-letter transformations of a word."""
        neighbors = []
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for i in range(len(word)):
            for char in alphabet:
                if char != word[i]:
                    new_word = word[:i] + char + word[i+1:]
                    if new_word in self.word_set:
                        neighbors.append(new_word)
        return neighbors

    def solve_bfs(self, start_word, target_word):
        """Runs BFS and returns both the path and algorithm analytics."""
        start_word = start_word.lower()
        target_word = target_word.lower()

        if start_word not in self.word_set or target_word not in self.word_set:
            return {"error": "Both words must be in the dictionary."}
        if len(start_word) != len(target_word):
            return {"error": "Words must be the same length."}

        start_time = time.time()
        queue = deque([(start_word, [start_word])])
        visited = set([start_word])
        max_queue_size = 1

        # The BFS Loop
        while queue:
            # Track memory usage (Queue size)
            if len(queue) > max_queue_size:
                max_queue_size = len(queue)

            current_word, path = queue.popleft()

            # Goal Test
            if current_word == target_word:
                end_time = time.time()
                return {
                    "path": path,
                    "visited_count": len(visited),
                    "max_queue": max_queue_size,
                    "time_ms": round((end_time - start_time) * 1000, 2)
                }

            # Generate and enqueue neighbors
            for neighbor in self.get_neighbors(current_word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return {"error": "No valid path found."}

def load_dictionary(filepath):
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        return None

# ==========================================
# 🎨 THE USER INTERFACE (Frontend)
# ==========================================
class WordLadderApp:
    def __init__(self, root, solver):
        self.root = root
        self.solver = solver
        self.root.title("AI Pathfinding: Word Ladder BFS")
        self.root.geometry("850x600")
        self.root.configure(bg="#2b2d42") # Modern dark background
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background="#2b2d42", foreground="#edf2f4", font=("Segoe UI", 11))
        style.configure('Header.TLabel', font=("Segoe UI", 24, "bold"), foreground="#ef233c")
        style.configure('SubHeader.TLabel', font=("Segoe UI", 14, "bold"), foreground="#8d99ae")
        style.configure('TButton', font=("Segoe UI", 12, "bold"), background="#ef233c", foreground="white", padding=10)
        style.map('TButton', background=[('active', '#d90429')])

        # Title
        ttk.Label(root, text="Word Ladder Search Agent", style='Header.TLabel').pack(pady=(20, 5))
        ttk.Label(root, text="Powered by Breadth-First Search (BFS)", style='SubHeader.TLabel').pack(pady=(0, 20))

        # Main Layout: Left (Input/Output) and Right (Analytics/Explanation)
        main_frame = tk.Frame(root, bg="#2b2d42")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        left_panel = tk.Frame(main_frame, bg="#3a3c55", bd=2, relief="groove")
        left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_panel = tk.Frame(main_frame, bg="#3a3c55", bd=2, relief="groove")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # --- LEFT PANEL: Interaction ---
        ttk.Label(left_panel, text="1. Enter Parameters", font=("Segoe UI", 14, "bold"), background="#3a3c55").pack(pady=10)
        
        input_frame = tk.Frame(left_panel, bg="#3a3c55")
        input_frame.pack(pady=5)
        
        ttk.Label(input_frame, text="Start Word:", background="#3a3c55").grid(row=0, column=0, padx=5, pady=5)
        self.start_entry = ttk.Entry(input_frame, font=("Courier", 14), width=12, justify="center")
        self.start_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Target Word:", background="#3a3c55").grid(row=1, column=0, padx=5, pady=5)
        self.target_entry = ttk.Entry(input_frame, font=("Courier", 14), width=12, justify="center")
        self.target_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(left_panel, text="Initialize Search", command=self.run_solver).pack(pady=15)

        # Result Box
        self.result_text = tk.Text(left_panel, font=("Consolas", 12), width=35, height=12, bg="#edf2f4", fg="#2b2d42", state="disabled")
        self.result_text.pack(pady=10, padx=10)

        # --- RIGHT PANEL: AI Explanation & Analytics ---
        ttk.Label(right_panel, text="2. Algorithm Analytics", font=("Segoe UI", 14, "bold"), background="#3a3c55").pack(pady=10)

        # Stats Area
        self.stats_var = tk.StringVar()
        self.stats_var.set("Awaiting execution...\n\nNodes Explored: 0\nMax Queue Size: 0\nExecution Time: 0 ms")
        stats_label = tk.Label(right_panel, textvariable=self.stats_var, font=("Consolas", 11), bg="#2b2d42", fg="#a8dadc", justify="left", padx=10, pady=10)
        stats_label.pack(fill="x", padx=15, pady=5)

        # Explanation Text
        explanation = (
            "How it works:\n\n"
            "1. State Space: The AI dynamically generates all valid 1-letter "
            "transformations of the current word.\n\n"
            "2. The Queue (FIFO): BFS evaluates words in 'ripples'. It checks all "
            "words 1 step away, then 2 steps away. This mathematically guarantees "
            "the shortest path.\n\n"
            "3. The Visited Set: To prevent infinite loops (e.g. COLD -> CORD -> COLD), "
            "every checked word is stored in an O(1) Hash Set."
        )
        exp_box = tk.Text(right_panel, font=("Segoe UI", 10), wrap="word", bg="#3a3c55", fg="#edf2f4", bd=0, height=12)
        exp_box.insert(tk.END, explanation)
        exp_box.config(state="disabled")
        exp_box.pack(padx=15, pady=15, fill="both", expand=True)

    def run_solver(self):
        start = self.start_entry.get().strip()
        target = self.target_entry.get().strip()

        if not start or not target:
            messagebox.showwarning("Input Error", "Please enter both words.")
            return

        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Executing BFS...\n")
        self.result_text.config(state="disabled")
        self.stats_var.set("Searching state space...")
        self.root.update()

        # Run AI
        result = self.solver.solve_bfs(start, target)

        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)

        if "error" in result:
            self.result_text.insert(tk.END, f"[!] {result['error']}")
            self.stats_var.set("Execution Failed.")
        else:
            path = result["path"]
            # Update Left Panel (Path)
            self.result_text.insert(tk.END, f"OPTIMAL PATH FOUND: {len(path) - 1} steps\n")
            self.result_text.insert(tk.END, "="*35 + "\n\n")
            for i, word in enumerate(path):
                self.result_text.insert(tk.END, f" {i+1}. {word.upper()}\n")
            
            # Update Right Panel (Analytics)
            stats = (
                f"Search Complete!\n\n"
                f"Nodes Explored (Visited): {result['visited_count']}\n"
                f"Peak Memory (Queue Max):  {result['max_queue']} words\n"
                f"Compute Time:             {result['time_ms']} ms"
            )
            self.stats_var.set(stats)
            
        self.result_text.config(state="disabled")

# ==========================================
# 🚀 APP EXECUTION
# ==========================================
if __name__ == "__main__":
    words = load_dictionary("words.txt")
    if words is None:
        words = ["cold", "cord", "card", "ward", "warm"]
        
    ai_solver = WordLadderSolver(words)
    root = tk.Tk()
    app = WordLadderApp(root, ai_solver)
    root.mainloop()