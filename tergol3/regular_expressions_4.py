# Write a regular expression to find all instances of a simplified email format in a given text. The email format for this exercise should be: username@domain.com, where:
# The username part can include English letters and numbers.
# The domain part can only include English letters.
# The email should end with .com.


import re

# The text to search for email addresses
text = """
Feel free to send your queries to info123@service.com or contact admin@yvc.com . 
For technical support, email test@gmail.com . Note that we do not accept emails 
sent to non .com addresses like user@example.net or admin@site.org .
"""

# Regular expression pattern to match the simplified email format
email_pattern = r"\b[A-Za-z0-9]+@[A-Za-z]+\.[cC][oO][mM]\b"

# Preprocess the text to remove space before '.com'
processed_text = re.sub(r"\s+\.", ".", text)

# Find all matches in the processed text
matches = re.findall(email_pattern, processed_text)

# Print the found email addresses
for email in matches:
    print(email)


# Explanation:

# \b indicates a word boundary.
# [A-Za-z0-9]+ matches the username part, which includes English letters and numbers.
# @ is a literal character representing the at-symbol in the email address.
# [A-Za-z]+ matches the domain part, which includes English letters.
# \.[cC][oO][mM] matches .com, allowing for any case (lowercase or uppercase).
# Applying this pattern to the text, the extracted email addresses are:
