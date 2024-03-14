import random 
import tlsh 
import binascii

my_string = "1234"
strings = []
slots = 50
hashes = []
with open('string_hashing.txt','w') as f:
    for i in range(50000):
        new_string = ""
        for j in range(slots):
            new_string = new_string + random.choice(my_string)
            binary_representation = new_string.encode()
        f.write(new_string  + "," + tlsh.oldhash(binary_representation) + "\n")
        

        
