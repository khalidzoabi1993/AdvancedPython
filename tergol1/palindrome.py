# write a program return if string is palindrome or not
def palindrome(string):
    if string == string[::-1]:
        return True
    else:
        return False


print(palindrome("racecar"))
print(palindrome("hello"))
print(palindrome("madam"))

# How can you find the number of palindromes in a string without manually searching for them
# and counting them?


def palindrome_count_option1(string):
    s = str(string)
    length = len(s)
    count = 0

    for center in range(2 * length - 1):
        left = center // 2
        right = left + center % 2
        while left >= 0 and right < length and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1

    return count


def palindrome_count_option2(string):
    count = 0
    for i in range(len(string)):
        for j in range(i, len(string)):
            if palindrome(string[i : j + 1]):
                print(string[i : j + 1])
                count += 1
    return count


print(palindrome_count_option1("abbaabbacabbaabba"))
print(palindrome_count_option2("abbaabbacabbaabba"))
