# Write a Python program to read an entire text file and prints as a list of the words that appear only once.


def file_read(fname):
    with open(fname, "r") as f:
        # Store the entire text file in a variable
        f_text = f.read()
        # Split the text file into words
        words = f_text.split()
        # Create a list to store the words that appear only once
        unique_words = []
        for word in words:
            # Check if the word appears only once
            if words.count(word) == 1:
                # Add the word to the list
                unique_words.append(word)
        print(unique_words)


file_read("test_files/files_with_list.txt")


# Write a Python program to read a file line by line and find the longest word in the file?
def longest_word(fname):
    with open(fname, "r") as f:
        # Store the entire text file in a variable
        f_text = f.read()
        # Split the text file into words
        words = f_text.split()
        # Create a variable to store the longest word
        longest_word = ""
        for word in words:
            # Check if the current word is longer than the longest word
            if len(word) > len(longest_word):
                # Update the longest word
                longest_word = word
        print(longest_word)


longest_word("test_files/files_with_list.txt")


# write longest_word method with sort method
def longest_word_with_sort(fname):
    with open(fname, "r") as f:
        # Store the entire text file in a variable
        f_text = f.read()
        # Split the text file into words
        words = f_text.split()
        # Sort the list of words by length
        words.sort(key=len)
        # Print the last word in the list
        print(words[-1])


longest_word_with_sort("test_files/files_with_list.txt")


# Write a Python program to read a file line by line and find the smallest word in the file?
def smallest_word(fname):
    with open(fname, "r") as f:
        # Store the entire text file in a variable
        f_text = f.read()
        # Split the text file into words
        words = f_text.split()
        # Create a variable to store the smallest word
        smallest_word = words[0]
        for word in words:
            # Check if the current word is smaller than the smallest word
            if len(word) < len(smallest_word):
                # Update the smallest word
                smallest_word = word
        print(smallest_word)


smallest_word("test_files/files_with_list.txt")


def smallest_word_with_sort(fname):
    with open(fname, "r") as f:
        # Store the entire text file in a variable
        f_text = f.read()
        # Split the text file into words
        words = f_text.split()
        # Sort the list of words by length
        words.sort(key=len, reverse=True)
        # Print the last word in the list
        print(words[-1])


smallest_word_with_sort("test_files/files_with_list.txt")
