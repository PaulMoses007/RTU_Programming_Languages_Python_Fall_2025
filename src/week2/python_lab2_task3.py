"""
Lab 3.3 – Operator Frequency Counter

Goals:
- Practice using strings and dictionaries.
- Count character frequencies in user-provided text.

Instructions:
1. Ask the user for an arithmetic expression, e.g. "3 + 5 * (2 - 1) + 7 / 2".
2. Count how many times each operator occurs:
   +  -  *  /  (  )
3. Store counts in a dictionary.
4. Print the result.
"""

expression = input("Enter an arithmetic expression: ")

operators = ["+", "-", "*", "/", "(", ")"]

operator_counts = {}
for op in operators:
    operator_counts[op] = 0  # Start count at 0 for each operator

for char in expression:
    if char in operators:  # Check if char is one of the operators
        operator_counts[char] += 1  # Increment its count

print("Operator counts:", operator_counts)
