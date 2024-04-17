import random 
import tlsh 
import binascii

import sys

my_string = "1234"
# choose = '111111110'
# a_pad = "a"*1000

strings = []
slots = 50
hashes = []
with open(sys.argv[1],'w') as f:
    for i in range(50000):
        new_string = ""
        while(len(new_string) < 50):
            t = random.randint(0,50)
            if(t == 1):
                new_string = new_string + random.choice(my_string)*4
            else:
                new_string = new_string + random.choice(my_string)
        new_string = new_string[0:50]
        binary_representation = new_string.encode()
            
#         new_string = a_pad + new_string + a_pad
        f.write(new_string  + "," + tlsh.oldhash(binary_representation) + "\n")
