import random

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
length = 10
new_str = ''.join(random.choices(my_str, k=length))

print(new_str)
result_array = normalize(new_str,4)
print("Array:")
for row in result_array:
    print(row)
