import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day1_input.txt')
lines = input.readlines()
input.close()

position = 50
password = 0
password2 = 0
wasAt0 = False

for line in lines:

    # Clear the newline
    line = line.strip()
    
    # Determine direction for L or R
    if line[0] == 'L':
        sign = -1
    else:
        sign = 1

    # Parse out the distance we are spinning
    length = int(line[1:])

    # R514 would be the same as R14 with 5 clicks past zero, so shortcut those full circles
    if length >= 100:
        password2 += (length // 100)
    length = length % 100
    
    # Move the dial to its new position
    position += (length * sign)

    # If we were at 30 and we're now at 110, we know we passed zero
    # If we were at 30 and we're now at -90, we know we passed zero
    # But if we were at 0 and we're now at -90, we did not actually pass zero. 
    # So any value above 100, and value value below 0 (unless we started at zero), means we passed 0
    if (not wasAt0 and position < 0) or position > 100:
        password2 += 1

    wasAt0 = False

    # Clamp the value back to the 0-99 dial. -90 translates to 10    
    position = abs(position % 100)

    # We ended on zero, which increments both passwords
    if position == 0:
        wasAt0 = True
        password += 1
        password2 += 1
    
print("The first password (the number of turns that ended on 0) is:", password)
print("The second password (the number of times we passed or ended on 0) is:", password2)