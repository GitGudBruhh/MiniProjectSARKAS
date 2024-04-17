import tlsh
import random
import numpy as np
import csv

def get_rnd_string_and_hash():
    my_string = "1234"
    slots = 50
    new_string = ''
    binary_representation = bytes()

    for j in range(slots):
        new_string = new_string + random.choice(my_string)

    binary_representation = new_string.encode()
    secret_hashed = tlsh.oldhash(binary_representation)
    return (new_string, secret_hashed)

def get_matches_below_thr(threshold: int, secret_hashed: str, strings_file: str):

    diff_n = 0
    num = 0

    list_of_matches = []
    list_of_hashes = []
    list_of_diff = []
    with open(strings_file, newline='') as csvfile:
        reader_obj = csv.reader(csvfile, delimiter=',', quotechar='|')

        if(not secret_hashed == 'TNULL'):
            for row in reader_obj:
                if(not row[1] == 'TNULL'):
                    diff_n = tlsh.diff(secret_hashed, row[1])
                    if(diff_n < threshold):
                        num += 1
                        list_of_matches.append(row[0])
                        list_of_hashes.append(row[1])
                        list_of_diff.append(diff_n)

    return (num, list_of_matches, list_of_hashes, list_of_diff)

def find_diff_string(st_1: str, st_2: str):
    diff_str = ''
    for i in range(len(st_1)):
        if(st_1[i] == st_2[i]):
            diff_str += ' '
        else:
            diff_str += 'D'
    return diff_str

def find_D_blocks(least_idx: int, diff_str: str):
    block_list = []

    is_block = False
    start_idx = None
    end_idx = None

    for idx in range(len(diff_str)):
        if(not is_block):
            if(diff_str[idx] == 'D'):
                is_block = True
                start_idx = idx
                end_idx = idx
            else:
                continue
        else:
            if(diff_str[idx] == 'D'):
                end_idx = idx
            else:
                is_block = False
                block_list.append((start_idx, end_idx))
                start_idx = None
                end_idx = None

    if(is_block):
        block_list.append((start_idx, end_idx))

    return block_list

def mutate(probability: float, start_idx: int, end_idx: int, inp_str: str, all_char_str: str):
    inp_list = list(inp_str)
    for idx in range(start_idx, end_idx+1):
        test = random.random()
        if(test <= probability):
            while(1):
                new_char = random.choice(all_char_str)
                if(new_char != inp_list[idx]):
                    inp_list[idx] = new_char
                    break
    return ''.join(inp_list)

def crossover(string1: str, string2: str, start_idx:int, end_idx: int, all_char_str: str):
    return (string1[0:start_idx] + string2[start_idx:end_idx+1] + string1[end_idx+1::],
            string2[0:start_idx] + string1[start_idx:end_idx+1] + string2[end_idx+1::])

def key_for_pvp_sim(element):
    return element[1][2]

def children_sort_key(inp_tup):
    return inp_tup[1]

############################################################################################################

s_and_h = get_rnd_string_and_hash()
secret_string = s_and_h[0]
ss_hash = s_and_h[1]
matches = get_matches_below_thr(80, ss_hash, "string_hashing.txt")

diff_array = np.zeros((len(matches[1]), len(matches[1])))

for i in range(len(matches[1])):
    for j in range(i, len(matches[1])):
        b1 = matches[1][i].encode()
        b2 = matches[1][j].encode()
        diff_array[i][j] = tlsh.diff(tlsh.oldhash(b1), tlsh.oldhash(b2))

diff_vector = np.array(matches[3])
print("Diff array:\n", diff_array, "\n")
print("Diff vector:\n", diff_vector.T, "\n")
print("Shape of diff_array: ", np.shape(diff_array))
print('='*80)

eligible_parents_check = []

for i in range(len(matches[1])):
    for j in range(i, len(matches[1])):
        if(diff_array[i][j] > diff_vector[i] or diff_array[i][j] > diff_vector[j]):
            eligible_parents_check.append((secret_string, matches[1][i], matches[1][j], i, j))

str_idxs_and_sims = []

for ss, p1, p2, i, j in eligible_parents_check:
    if(not p1 == p2):
        a = find_diff_string(ss, p1)
        print(a, "- NOT VISIBLE TO PLAYER")
        b = find_diff_string(ss, p2)
        print(b, "- NOT VISIBLE TO PLAYER")
        c = find_diff_string(p1, p2)
        print(c)

        count_of_spaces = [0,0,0]
        for idx in range(len(a)):
            if(a[idx] == ' '):
                count_of_spaces[0] += 1
            if(b[idx] == ' '):
                count_of_spaces[1] += 1
            if(c[idx] == ' '):
                count_of_spaces[2] += 1
        str_idxs_and_sims.append(((i,j),tuple(count_of_spaces), (diff_vector[i], diff_vector[j], diff_array[i][j])))

sorted_sias = sorted(str_idxs_and_sims, key=key_for_pvp_sim, reverse=True)

pvs_diff_upper_bound = 100
for elem in sorted_sias:
    idx = sorted_sias.index(elem)
    if(
    (elem[2][1] > pvs_diff_upper_bound or
    elem[2][2] > pvs_diff_upper_bound)):
        sorted_sias[idx] = 0

while(1):
    try:
        (sorted_sias.index(0))
        sorted_sias.pop(sorted_sias.index(0))
    except:
        break

n_parent_tuples = 0
parent_threshold = 1000
children = []
for sias in sorted_sias:
    if(n_parent_tuples > parent_threshold):
        break

    n_parent_tuples += 1

    p1 = matches[1][sias[0][0]]
    p2 = matches[1][sias[0][1]]

    sim_p1_p2 = sias[1][2]
    diff_p1_s = sias[2][0]
    diff_p2_s = sias[2][1]
    diff_p1_p2 = sias[2][2]

    diff_string = find_diff_string(p1, p2)
    least_idx = 0
    block_list = find_D_blocks(least_idx, diff_string)

    for s_e in block_list:
        start = s_e[0]
        end = s_e[1]

        c1, c2 = crossover(p1, p2, start, end, '1234')
        c1_hash = tlsh.oldhash(c1.encode())
        c2_hash = tlsh.oldhash(c2.encode())

        if(c1_hash != 'TNULL'):
            diff_c1_s = tlsh.diff(ss_hash, c1_hash)
            if(diff_c1_s < diff_p1_s):
                children.append((c1, diff_p1_s - diff_c1_s, diff_p1_s))

        if(c2_hash != 'TNULL'):
            diff_c2_s = tlsh.diff(ss_hash, c2_hash)
            if(diff_c2_s < diff_p2_s):
                children.append((c2, diff_p2_s - diff_c2_s, diff_p2_s))

print(len(children))

sorted_children = sorted(children, key=children_sort_key, reverse = True)
for i in range(100):
    print(sorted_children[i], i)
    # if(sorted_children[i][1] == 9):
    #     break
