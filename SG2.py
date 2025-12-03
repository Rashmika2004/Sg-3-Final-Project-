'''

Programming Language: Python
IDE Utilized: Thonny

Team Members: Ryan Berry, Kayla Gaynor, Matthew Kik, Aaron Kofman

Last Modified: 13 November 2025

Usage: Program accepts a .txt files that must reside within the same directory as this program.There can be no more than 10 files opened
After file is accepted and verified as a .txt text file, the file should only contain a set of Legal defined words.
No punctuation except hyphens is allowed. The user will be prompted to continue counting legal words or not. After words are entered and verified,
the list of words will be added to a concordance and summarized by file number, line number, and word count.
After concrodance there are three additional lists created, the first first list will contain the top ten words utilized from every file.
The second list will be every word that appears once in each file, with the third file contain the words that appear once.

This program is meant to be broken up into subprograms/fucntions then called through a simple main logic to control code readability, writability, and comparmentalize how the program works. 

Data Structure: Array - We utilized a simple array to store the words.

'''

'''
Regular expression (re) library is utilized for parsing text.
With os (Miscellaneous operating system interfaces) used for determining file directory, and if the file exists.
Sys library for closing
'''
import re
import os
import sys

def extract_words(text):
    
    '''
    Splits text into words while removing the line-break hyphens
    Returns an array of words.
    https://docs.python.org/3/library/re.html
    https://www.geeksforgeeks.org/python/file-handling-python/
    https://docs.python.org/3/library/os.path.html
    '''

    # Remove hyphen and newline
    text = re.sub(r"-\n","", text)
    # Extract words (letters and hyphens)
    wordsArray = re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", text)
    return wordsArray

'''
This function control the required file operations; maximum number of files are set to 10.
Files are incremented with checking to detect duplicates. File names are stored onto an array to return.
Words are stored onto an array and then each file of words is then appended to another array.
File extensions are not case sensitive. Example: .tXT is allowed. User are prompted if additional files are opened.
'''

def open_file():

    max_files = 10
    file_opened = 0
    response = True
    filenames = []  # Track filenames to check for duplicates
    word_arrays = []  # Store separate word array for each file
    
    while file_opened < max_files and response:
        print("Please Input a Filename, you may only access a maximum of ten.")
        print("Only files with .txt extension are allowed, this is not case sensitive\n")
        filename = input("Enter filename: ")
        
        name, extension = os.path.splitext(filename)
        
        if extension.upper() != ".TXT":
            print("Error: filename must end in .TXT")
        elif not os.path.isfile(filename):
            print("Error: File is not in current directory.")
        elif filename in filenames:  # Check for duplicate
            print("Error: You have already entered this filename.")
        else:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
                words_array = extract_words(text)
                filenames.append(filename)
                word_arrays.append(words_array)
                file_opened += 1
                
                if file_opened == max_files:
                    print("Maximum allowed files reached.\n")
                    break
                    
                response = ask_continue()
    
    return filenames, word_arrays
            
            

def get_legal_word():
    '''
    Prompt the user for a legal word and give the definition of a legal word
    Rules for a legal word:
        -Only letters A-Z (case-insensitive)
        -Optional hyphens are allowed
        -No spaces, punctuation, or numbers allowed
    Returns the valid word (lowercased)
    https://docs.python.org/3/library/re.html
    '''
    
    while True:
        print("Legal words may only contain letters (A-Z) and optional hyphens (-).\nA word is defined as a series of alphabetic characters, uninterrupted by a blank or a punctuation mark (excluding a hyphen).")
        word = input("Enter a legal word: ").strip()
        # Regex validates word based on rules
        if re.fullmatch(r"[A-Za-z]+(?:-[A-Za-z]+)*", word):
            return word
        else:
            print("Error: Word must only contain legal characters: abcdefghijklmnopqrstuvwxyz-\n")


def ask_continue():
    '''
    Ask user if they want to continue. Will accept Yes/No (Y/N) which is made case insensitive
    Loop until a valid response is given
    '''
    while True:
        response = input("Do you want to continue? (Yes/No): ").strip().lower()
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            print("Error: Please enter Yes, No, Y, or N.")

def count_word(words_array, counted_word):
    #Counts words in word array for displaying total.
    return sum(1 for word in words_array if word.lower() == counted_word.lower())

'''
This function prints a summary of all the files giving each files
total and distinct word count

https://www.geeksforgeeks.org/dsa/print-unique-words-string/
'''
def print_file_summary(filenames, word_arrays):
    #Format the table 
    print("\nFile Summary:")
    print(f"{'Filename':<25}{'Total Words':>15}{'Distinct Words':>20}")
    print("-" * 60)

    #count the total number of words and the number of distinct words
    for i in range(len(filenames)):
        total = len(word_arrays[i])
        distinct = len(set(word.lower() for word in word_arrays[i]))
        print(f"{filenames[i]:<25}{total:>15}{distinct:>20}\n")

'''
This function lets the user search for a word and it returns how many times that word came up in each file.
Word Count is displayed when user inputs is entered, afterwards they are prompted the ask continue function.
If not, user will be prompted to press enter to exit. (Need to rewrite modified to move towards concordance)
'''
def word_search(filenames, word_arrays):
   
    user_continues = True

    while user_continues:
        # ask user to enter a legal word
        word = get_legal_word()

        print(f"\nSearch results for '{word}':")
        print(f"{'Filename':<25}{'Count':>10}")
        print("-" * 35)

        total_count = 0

        # loop through each file
        for i in range(len(filenames)):
            count = 0  # reset count for each file

            # loop through every word in the current file
            for w in word_arrays[i]:
                if w.lower() == word.lower():
                    count += 1

            total_count += count
            print(f"{filenames[i]:<25}{count:>10}")

        print("-" * 35)
        print(f"{'Total':<25}{total_count:>10}\n")

        
        if not ask_continue():
            user_continues = False
            print("\nDone with word search! Moving to concordance generation.")
            input("\nPress Enter to continue...")
            return
        
'''
Builds concordance by taking in all file names, and the array for stored words.
'''

def build_concordance(filenames, word_arrays):
    concordance = {}
    
    #Process each file
    for file_num, words in enumerate(word_arrays, start=1):
        filename = filenames[file_num - 1]
        
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        #Processes each line
        for line_num, line in enumerate(lines, start=1):
            
            line = line.replace('-\n', '')
            
            line_words = re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", line)
            
            #Records position of each word.
            for word_pos, word in enumerate(line_words, start=1):
                word_lower = word.lower()
                
                if word_lower not in concordance:
                    concordance[word_lower] = []
                
                #Stores location as required.
                concordance[word_lower].append((file_num, line_num, word_pos))
    
    return concordance

'''
Formats the concordance dictionary into a string for display and file output.
Words are sorted alphabetically (hyphen comes before 'a').
Locations are sorted by file, then line, then word position.
'''
def format_concordance(concordance):
   
    output_lines = []
    
    #Sorts words alphabetically (hyphen naturally sorts before letters)
    sorted_words = sorted(concordance.keys())
    
    for word in sorted_words:
        #Sorts locations by file, line, then position
        locations = sorted(concordance[word])
        
        #Formats locations as X.Y.Z
        location_strings = [f"{file_num}.{line_num}.{word_pos}" 
                           for file_num, line_num, word_pos in locations]
        
        #Joins with semicolon and space, end with period
        location_str = '; '.join(location_strings) + '.'
        
        #Creates the line: word followed by space, then locations
        line = f"{word} {location_str}"
        output_lines.append(line)
    
    return '\n'.join(output_lines)

'''
    Creates and outputs the concordance to both screen and file.
 '''

def write_concordance(filenames, word_arrays):
    
    print("\nGenerating concordance...")
    
    #Builds the concordance
    concordance = build_concordance(filenames, word_arrays)
    
    #Formats the concordance
    formatted = format_concordance(concordance)
    
    print("\nCONCORDANCE:")
    print(formatted)
    
    #Write to the concordance file
    with open('CONCORDANCE.TXT', 'w', encoding='utf-8') as f:
        f.write(formatted)
    
    print("\nConcordance written to CONCORDANCE.TXT")
    
    return concordance

 '''
Generates three extra lists from the concordance data:
1. Top ten most frequent words
2. Words appearing in all files
3. Words appearing in only one file
    
 Writes output to both screen and ExtraLists.txt file
'''

def generate_extra_lists(filenames, word_arrays, concordance):
  
    
    #Collects word counts / requirements
    word_stats = {}  # {word: {'count': total_count, 'files': set of file numbers}}
    
    for word, locations in concordance.items():
        total_count = len(locations)
        files_set = set(loc[0] for loc in locations)  # Get unique file numbers
        word_stats[word] = {'count': total_count, 'files': files_set}
    
    #Generates the three lists
    top_ten = generate_top_ten(word_stats)
    words_in_all = generate_words_in_all_files(word_stats, len(filenames))
    words_in_one = generate_words_in_one_file(word_stats)
    
    #Combines output
    output = top_ten + "\n\n" + words_in_all + "\n\n" + words_in_one
    
    #Prints to screen
    print("\n" + "="*60)
    print("EXTRA LISTS")
    print("="*60)
    print(output)
    
    #Writes to file
    with open('ExtraLists.txt', 'w', encoding='utf-8') as f:
        f.write(output)
    
    print("\nExtra lists written to ExtraLists.txt")


def generate_top_ten(word_stats):
    '''
    Creates the top ten most frequent words list.
    Shows word, count, and number of files it appears in.
    Right-justified columns with headers.
    '''
    #Sorts by count (descending), then alphabetically
    sorted_words = sorted(word_stats.items(), 
                         key=lambda x: (-x[1]['count'], x[0]))
    
    # Take top 10 (or fewer if less than 10 words exist)
    top_words = sorted_words[:10]
    
    if not top_words:
        return "Top Ten Most Frequent Words\n(No words found)"
    
    #Calculates column widths
    max_word_len = max(len(word) for word, _ in top_words)
    max_word_len = max(max_word_len, len("Word"))
    
    max_count_len = max(len(str(stats['count'])) for _, stats in top_words)
    max_count_len = max(max_count_len, len("Occurrences"))
    
    max_files_len = max(len(str(len(stats['files']))) for _, stats in top_words)
    max_files_len = max(max_files_len, len("Files"))
    
    #Builds output
    lines = []
    lines.append("Top Ten Most Frequent Words")
    lines.append("")
    
    #Headers
    header = (f"{'Word':>{max_word_len}}  "
             f"{'Occurrences':>{max_count_len}}  "
             f"{'Files':>{max_files_len}}")
    lines.append(header)
    lines.append("-" * len(header))
    
    #Data rows
    for word, stats in top_words:
        line = (f"{word:>{max_word_len}}  "
               f"{stats['count']:>{max_count_len}}  "
               f"{len(stats['files']):>{max_files_len}}")
        lines.append(line)
    
    return "\n".join(lines)

 '''
Creates list of words appearing in all files.
Single column, right-justified, with label.
'''

def generate_words_in_all_files(word_stats, num_files):
   
    #Finds words that appear in all files
    words_in_all = [word for word, stats in word_stats.items() 
                    if len(stats['files']) == num_files]
    
    #Sorts alphabetically
    words_in_all.sort()
    
    if not words_in_all:
        return "Words Appearing in All Files\n\n(No words appear in all files)"
    
    #Calculates column width
    max_word_len = max(len(word) for word in words_in_all)
    max_word_len = max(max_word_len, len("Word"))
    
    #Builds output
    lines = []
    lines.append("Words Appearing in All Files")
    lines.append("")
    lines.append(f"{'Word':>{max_word_len}}")
    lines.append("-" * max_word_len)
    
    for word in words_in_all:
        lines.append(f"{word:>{max_word_len}}")
    
    return "\n".join(lines)

  '''
Creates list of words appearing in only one file.
Two columns: word and file number, both right-justified.
 '''

def generate_words_in_one_file(word_stats):
  
    #Finds words that appear in only one file
    words_in_one = [(word, list(stats['files'])[0]) 
                    for word, stats in word_stats.items() 
                    if len(stats['files']) == 1]
    
    #Sorts alphabetically by word
    words_in_one.sort()
    
    if not words_in_one:
        return "Words Appearing in Only One File\n\n(No words appear in only one file)"
    
    #Calculates column widths
    max_word_len = max(len(word) for word, _ in words_in_one)
    max_word_len = max(max_word_len, len("Word"))
    
    max_file_len = max(len(str(file_num)) for _, file_num in words_in_one)
    max_file_len = max(max_file_len, len("File"))
    
    #Builds output
    lines = []
    lines.append("Words Appearing in Only One File")
    lines.append("")
    
    #Headers
    header = f"{'Word':>{max_word_len}}  {'File':>{max_file_len}}"
    lines.append(header)
    lines.append("-" * len(header))
    
    #Data rows
    for word, file_num in words_in_one:
        line = f"{word:>{max_word_len}}  {file_num:>{max_file_len}}"
        lines.append(line)
    
    return "\n".join(lines)

'''
Main handles file checking and ensuring correct directory, each function is called all previous versions of this program are called. Then concordance is created from each file, there can ONLY
be ten files uploaded. No more, after concordance is created three extra list .txt files are created

https://www.geeksforgeeks.org/python/file-handling-python/
https://docs.python.org/3/library/os.path.html

'''

print("Usage: This program accepts 'txt' files that must reside within the same directory as this program.\n"
      "After files are successfully uploaded. The words within each file will be parsed and counted.\n"
      "Afterwards you will be prompted to enter a word, this will check the occurrences of that word and display a count.\n"
      "You will then be prompted to continue entering words until you are complete.\n"
      "Once completed the list of words will be added to a concordance and summarized by file number, line number, and word count."
      "After concrodance there are three additional lists created, the first first list will contain the top ten words utilized from every file."
      "The second list will be every word that appears once in each file, with the third file contain the words that appear once."   )

filenames, word_arrays = open_file()
print_file_summary(filenames, word_arrays)
word_search(filenames, word_arrays)
concordance = write_concordance(filenames, word_arrays)
generate_extra_lists(filenames, word_arrays, concordance)
print("\nProgram complete!")



