"""
Task 4 – Text-based Arithmetic Analyzer
--------------------------------------
Create a text-based analyzer that:
1. Counts non-space characters.
2. Counts words.
3. Extracts numbers and computes their sum and average.
Use helper functions:
- count_characters(text)
- count_words(text)
- extract_numbers(text)
- analyze_text(text)
Print formatted summary in main.
"""


def count_characters(text):
    """Count non-space characters in a string."""
    # TODO: implement
    return len(text.replace(" ", ""))


def count_words(text):
    """Count number of words in a string."""
    # TODO: implement
    return len(text.split())


def extract_numbers(text):
    """Return list of integers found in text."""
    # TODO: implement
    numbers = []
    for word in text.split():
        if word.isdigit():
            numbers.append(int(word))
    return numbers


def analyze_text(text):
    """Perform text-based arithmetic analysis."""
    # TODO: call helper functions and compute total, average, etc.
    char_count = count_characters(text)
    word_count = count_words(text)
    numbers = extract_numbers(text)
    num_sum = sum(numbers) if numbers else 0
    num_avg = num_sum / len(numbers) if numbers else 0
    return (char_count, word_count, numbers, num_sum, num_avg)


if __name__ == "__main__":
    # TODO: read input, call analyze_text(), and print results
    text = input("Enter a sentence with some numbers: ")
    if text.strip() == "":
        print("Error: Please enter a non-empty sentence.")
    else:
        result = analyze_text(text)
        print(f"Non-space character count: {result[0]}")
        print(f"Word count: {result[1]}")
        print(f"Numbers found: {result[2]}")
        print(f"Sum of numbers: {result[3]}")
        print(f"Average of numbers: {result[4]:.2f}")
