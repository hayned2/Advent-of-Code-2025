import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day3_input.txt')
lines = input.readlines()
input.close()
lines = [line.strip() for line in lines]

# Part 1
sum = 0
for bank in lines:
    # Find the first digit -- largest number that isn't the last digit
    first = 0
    for x in range(9, 0, -1):
        if str(x) in bank[0:-1]:
            first = x
            break
    index = bank.find(str(first))
    second = 0
    # Find the second digit -- largest number that comes after the first digit
    for x in range(9, 0, -1):
        if str(x) in bank[index + 1:]:
            second = x
            break
    # Calculate the joltage and add it to the total sum
    answer = first * 10 + second
    sum += answer
print("The maximum joltage possible from activating 2 batteries in each bank is", sum)

# Part 2
sum2 = 0
# Let's do this a little smarter, let's make a helper function
def find_biggest_number(number, limit):
    answer = ""
    # We start with the number of digits we need to find as the limit (i.e. 12)
    for x in range(limit, 0, -1):
        # If we only have x digits left and we need x more digits, return everything we have left
        if len(number) == x:
            answer += number
            break
        # If we only need one more digit, just grab the largest remaining digit
        elif x == 1:
            answer += max(number)
            break
        # Yeah... as it turns out the max() function works just fine with numbers as strings. max("249123") == "9"
        # So find the largest digit we can that has enough digits after it to finish our 12-digit number
        digit = max(number[:-x + 1])
        answer += digit
        index = number.find(digit)
        # Truncate the number to give us just the remaining digits we are concerned with
        number = number[index + 1:]
    return int(answer)

for bank in lines:
    sum2 += find_biggest_number(bank, 12)
print("The maximum joltage possible from activating 12 batteries in each bank is", sum2)
