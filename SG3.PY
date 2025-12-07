"""
Programming Language: Python 3
Development Environment: Thonny IDE (Windows 11)

SG3 – Small Group 3 Final Project
Group Members: (Fill in)
Last Modified: (Fill in)
CS 4500 – Fall 2025

DESCRIPTION:
------------
This program is a GUI-based version of the previous SG0–SG2 text-processing system.
It supports:
• Opening up to ten .txt files
• Extracting legal words using regex
• Searching for a word across all open files
• Creating a concordance for ONE selected file
• Closing open files
• Writing concordance and extra lists to external files
• Displaying all results inside scrollable GUI windows

GUI Framework:
--------------
This program uses Tkinter and ttk (Python standard GUI libraries).
It is fully compatible with Thonny on Windows 11.

External Resources Used:
------------------------
• Tkinter docs: https://docs.python.org/3/library/tkinter.html
• ttk tutorials
• Various regex documentation resources

All functions are documented, and the program follows SG3 formatting requirements.
"""

import os
import re
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext


###############################################
# WORD EXTRACTION AND CORE LOGIC (FROM SG1/SG2)
###############################################

def extract_words(text):
    """Extract legal words from text using regex."""
    text = re.sub(r"-\n", "", text)   # remove hyphen splits
    return re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", text)


def count_word(words_array, counted_word):
    """Counts how many times counted_word appears in words_array."""
    return sum(1 for word in words_array if word.lower() == counted_word.lower())


def build_concordance(filenames, word_arrays):
    """Build concordance: word → list of (file_num, line_num, position)."""
    concordance = {}

    for file_num, filename in enumerate(filenames, start=1):
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, start=1):
            line = line.replace("-\n", "")
            line_words = re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", line)

            for pos, word in enumerate(line_words, start=1):
                w = word.lower()
                if w not in concordance:
                    concordance[w] = []
                concordance[w].append((file_num, line_num, pos))

    return concordance


def format_concordance(concordance):
    """Format concordance into multi-line string."""
    output_lines = []
    for word in sorted(concordance.keys()):
        locations = sorted(concordance[word])
        part = "; ".join(f"{f}.{l}.{p}" for f, l, p in locations) + "."
        output_lines.append(f"{word} {part}")
    return "\n".join(output_lines)


###############################################
# EXTRA LIST GENERATION
###############################################

def generate_extra_lists(filenames, word_arrays, concordance):
    """Generate 3 lists: top ten, words in all files, words in only one file."""
    word_stats = {}

    for word, locs in concordance.items():
        word_stats[word] = {
            "count": len(locs),
            "files": set(loc[0] for loc in locs)
        }

    top_ten = generate_top_ten(word_stats)
    words_in_all = generate_words_in_all_files(word_stats, len(filenames))
    words_in_one = generate_words_in_one_file(word_stats)

    result = top_ten + "\n\n" + words_in_all + "\n\n" + words_in_one

    with open("ExtraLists.txt", "w", encoding="utf-8") as f:
        f.write(result)

    return result


def generate_top_ten(word_stats):
    """Return top ten frequent words."""
    sorted_words = sorted(word_stats.items(),
                          key=lambda x: (-x[1]['count'], x[0]))[:10]

    if not sorted_words:
        return "Top Ten Words:\n(No words found)"

    out = ["Top Ten Most Frequent Words", ""]
    out.append(f"{'Word':<20}{'Count':<10}{'Files'}")
    out.append("-" * 40)

    for word, stats in sorted_words:
        out.append(f"{word:<20}{stats['count']:<10}{len(stats['files'])}")

    return "\n".join(out)


def generate_words_in_all_files(word_stats, file_count):
    words = sorted([w for w, s in word_stats.items() if len(s["files"]) == file_count])

    if not words:
        return "Words in All Files:\n(No such words)"

    out = ["Words Appearing in All Files", ""]
    out.extend(words)
    return "\n".join(out)


def generate_words_in_one_file(word_stats):
    items = sorted([(w, list(s["files"])[0])
                    for w, s in word_stats.items()
                    if len(s["files"]) == 1])

    if not items:
        return "Words Appearing in One File:\n(No such words)"

    out = ["Words Appearing in One File", ""]
    for w, fnum in items:
        out.append(f"{w:<20} File {fnum}")
    return "\n".join(out)


###############################################
# GUI APPLICATION
###############################################

class SG3App:
    """Main GUI application for SG3."""

    def __init__(self, root):
        self.root = root
        self.root.title("SG3 Text Processing Program")
        self.root.geometry("1000x600")

        # Track files
        self.filenames = []
        self.word_arrays = []

        # Build GUI
        self.build_layout()

    ###############################################
    # GUI LAYOUT
    ###############################################

    def build_layout(self):
        """Create main menu and output panel."""
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        # Left Menu
        menu = ttk.Frame(frame, width=200)
        menu.pack(side="left", fill="y")

        ttk.Label(menu, text="MAIN MENU", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Button(menu, text="1. Open a Text File", command=self.open_file).pack(fill="x", pady=5)
        ttk.Button(menu, text="2. Find a Word", command=self.search_word).pack(fill="x", pady=5)
        ttk.Button(menu, text="3. Build Concordance", command=self.build_concordance_gui).pack(fill="x", pady=5)
        ttk.Button(menu, text="4. Close a File", command=self.close_file).pack(fill="x", pady=5)
        ttk.Button(menu, text="5. Quit", command=self.quit_app).pack(fill="x", pady=5)

        # Output Panel
        output_frame = ttk.Frame(frame)
        output_frame.pack(side="right", fill="both", expand=True)

        self.output_box = scrolledtext.ScrolledText(output_frame, wrap="word", font=("Consolas", 11))
        self.output_box.pack(fill="both", expand=True)

    def display(self, text):
        """Writes text to output panel."""
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, text)

    ###############################################
    # MENU OPTION 1: OPEN FILE
    ###############################################

    def open_file(self):
        if len(self.filenames) >= 10:
            messagebox.showerror("Error", "You already opened the maximum of 10 files.")
            return

        filename = filedialog.askopenfilename(
            title="Select a .txt file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not filename:
            return

        if not filename.lower().endswith(".txt"):
            messagebox.showerror("Error", "Only .txt files are allowed.")
            return

        if filename in self.filenames:
            messagebox.showerror("Error", "File already opened.")
            return

        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            words = extract_words(text)

        self.filenames.append(filename)
        self.word_arrays.append(words)

        self.display(f"File opened:\n{filename}\nTotal words: {len(words)}")

    ###############################################
    # MENU OPTION 2: SEARCH WORD
    ###############################################

    def search_word(self):
        if not self.filenames:
            messagebox.showerror("Error", "No files are open.")
            return

        def run_search():
            word = entry.get().strip().lower()
            if not re.fullmatch(r"[A-Za-z]+(?:-[A-Za-z]+)*", word):
                messagebox.showerror("Error", "Illegal word.")
                return

            output = [f"Search results for '{word}':\n"]
            for fname, words in zip(self.filenames, self.word_arrays):
                count = sum(1 for w in words if w.lower() == word)
                output.append(f"{os.path.basename(fname):<40} {count}")

            self.display("\n".join(output))
            win.destroy()

        win = tk.Toplevel(self.root)
        win.title("Search Word")

        ttk.Label(win, text="Enter a legal word:").pack(pady=5)
        entry = ttk.Entry(win, width=40)
        entry.pack(pady=5)

        ttk.Button(win, text="Search", command=run_search).pack(pady=5)

    ###############################################
    # MENU OPTION 3: BUILD CONCORDANCE
    ###############################################

    def build_concordance_gui(self):
        if not self.filenames:
            messagebox.showerror("Error", "No files are open.")
            return

        def run_concordance():
            idx = listbox.curselection()
            if not idx:
                return

            index = idx[0]
            chosen_file = self.filenames[index]

            # Build concordance for ALL files (per SG spec)
            concordance = build_concordance(self.filenames, self.word_arrays)
            formatted = format_concordance(concordance)

            with open("CONCORDANCE.TXT", "w", encoding="utf-8") as f:
                f.write(formatted)

            extra = generate_extra_lists(self.filenames, self.word_arrays, concordance)

            self.display("CONCORDANCE.TXT created.\n\n" + formatted +
                         "\n\n\nExtra Lists Created:\n" + extra)

            win.destroy()

        win = tk.Toplevel(self.root)
        win.title("Select file for concordance")

        ttk.Label(win, text="Select a file:").pack(pady=5)

        listbox = tk.Listbox(win, width=70, height=10)
        listbox.pack()
        for f in self.filenames:
            listbox.insert(tk.END, f)

        ttk.Button(win, text="Build Concordance", command=run_concordance).pack(pady=10)

    ###############################################
    # MENU OPTION 4: CLOSE FILE
    ###############################################

    def close_file(self):
        if not self.filenames:
            messagebox.showerror("Error", "No files open.")
            return

        def run_close():
            idx = listbox.curselection()
            if not idx:
                return

            index = idx[0]
            fname = self.filenames[index]

            del self.filenames[index]
            del self.word_arrays[index]

            self.display(f"Closed file:\n{fname}")
            win.destroy()

        win = tk.Toplevel(self.root)
        win.title("Close a File")

        ttk.Label(win, text="Choose a file to close:").pack(pady=5)

        listbox = tk.Listbox(win, width=70, height=10)
        listbox.pack()

        for f in self.filenames:
            listbox.insert(tk.END, f)

        ttk.Button(win, text="Close File", command=run_close).pack(pady=10)

    ###############################################
    # MENU OPTION 5: QUIT
    ###############################################

    def quit_app(self):
        self.root.destroy()


###############################################
# MAIN PROGRAM ENTRY
###############################################

def main():
    root = tk.Tk()
    app = SG3App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
