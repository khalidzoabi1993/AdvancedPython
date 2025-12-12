import re

def find_match(text):
    if re.search("khalid", text):
        return "Match found!"
    else:
        return "No match!"

#
# print(find_match("My name is khalid"))
# print(find_match("My name is Ahmed"))
# print(find_match("khalid is my name"))
# print(find_match("Hello world"))


def find_all_matches(text, pattern):
    matches = re.findall(pattern, text)
    return matches


# print(find_all_matches("I love Python. Python is great for data science.",r"Python"))
# print(find_all_matches("I have a Cat, a Dog, and Fish ",r"Cat|Dog|Fish"))

def find_date(text, pattern):
    date = re.search(pattern, text)
    if date:
        return "Date found: " + date.group()
    else:
        return "No date found."


print(find_date("Today's date is 2025-11-14.", r"\d{4}-\d{2}-\d{2}"))