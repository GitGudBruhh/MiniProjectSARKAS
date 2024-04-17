import random
import numpy as np

def normalize(string,slots):
    # Initialize an array with 4 rows and the length of the string columns, all elements set to 0
    array = [[0 for _ in range(len(string))] for _ in range(slots)]
    
    i = 0
    while i < len(string):
        j = i + 1
        while j < len(string) and string[i] == string[j]:
            j += 1
        array[int(string[i]) - 1][j - i - 1] += 1
        i = j

    return array



my_str = '1234'
length = 50
n_test = 10000
my_arr = [np.zeros(length), np.zeros(length), np.zeros(length), np.zeros(length)]

def calc_avg_blocks():
    for _ in range(n_test):
        new_str = ''.join(random.choices(my_str, k=length))
        result_array = normalize(new_str, len(my_str))

        for i in range(len(my_str)):
            my_arr[i] += np.array(result_array[i])/n_test

    for row in my_arr:
        print(row)

    avg = np.zeros(length)
    for row in my_arr:
        avg += row

    avg = avg/len(my_str)
    print()
    print("AVERAGE BLOCK SIZE FREQUENCY:")
    print(avg)

# new_str = '1112223334'
# print(new_str)
# result_array = normalize(new_str, len(my_str))
# print("Array:")
# for row in result_array:
#     print(row)

calc_avg_blocks()
