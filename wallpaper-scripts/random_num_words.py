from num2words import num2words
import random

#make a list of random numbers between 0 and 100
random_numbers = [random.randint(0,100) for i in range(20)]

for number in random_numbers:
    #print the number and its word form
    print(num2words(number))
