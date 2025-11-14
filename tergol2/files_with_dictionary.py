# Write code that reads the file and creates a dictionary so that SOURCE/FILENAME.json is the key and TARGET is the value.
# file is : books.txt
# line example: php-programming/php.json,php-programming
# output: {'php-programming/php.json': 'php-programming', 'python-programming/python.json': 'python-programming'}


def create_dictionary(fname):
    with open(fname, "r") as f:
        # Store the entire text file in a variable
        f_text = f.read()
        # Split the text file into lines
        lines = f_text.splitlines()
        # Create a variable to store the dictionary
        dictionary = {}
        for line in lines:
            # Split the line into key and value
            key, value = line.split("/")
            # Update the dictionary
            dictionary[key] = value
        print(dictionary)


create_dictionary("test_files/books.txt")


# print only the keys of the dictionary
def print_keys(fname):
    with open(fname, "r") as f:
        # Store the entire text file in a variable
        f_text = f.read()
        # Split the text file into lines
        lines = f_text.splitlines()
        # Create a variable to store the dictionary
        dictionary = {}
        for line in lines:
            # Split the line into key and value
            key, value = line.split(",")
            # Update the dictionary
            dictionary[key] = value
        print(dictionary.keys())


print_keys("test_files/books.txt")


# print only the values of the dictionary
def print_values(fname):
    with open(fname, "r") as f:
        # Store the entire text file in a variable
        f_text = f.read()
        # Split the text file into lines
        lines = f_text.splitlines()
        # Create a variable to store the dictionary
        dictionary = {}
        for line in lines:
            # Split the line into key and value
            key, value = line.split(",")
            # Update the dictionary
            dictionary[key] = value
        print(dictionary.values())


print_values("test_files/books.txt")


# write a function that read a log file and print the number of times each IP address appears in the file
def count_ip_addresses(fname):
    with open(fname, "r") as f:
        # Store the entire text file in a variable
        f_text = f.read()
        # Split the text file into lines
        lines = f_text.splitlines()
        # Create a variable to store the dictionary
        dictionary = {}
        for line in lines:
            # Split the line into key and value
            ip_address = line.split()[0]
            # Update the dictionary
            if ip_address in dictionary:
                dictionary[ip_address] += 1
            else:
                dictionary[ip_address] = 1
        print(dictionary)


count_ip_addresses("test_files/apache_access.log")
