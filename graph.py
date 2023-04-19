'''
Daniel LaForce
#001119118
C950
'''

import csv
dist_data = './Dist_Table.csv'

d_hash = [] #distance hash
dist_list = [] #distance Graph
address_hash = [] #location,street address, zip code

with open(dist_data) as dt:
    dataFilter = (line.replace('\n', '') for line in dt)
    fptr = csv.reader(dataFilter)
    r_id = 0
    dt.readline()
    for row in fptr:
        if r_id is 0:
            address_id = 0
            for col in row:
                if col is not 0:
                    col = [address_id + 1, col]
                    row[address_id] = col
                    address_id += 1
        temp_list = [r_id]
        temp_list.extend(row)
        d_hash.append(temp_list)
        r_id += 1

    for row in d_hash:
        if row[0] is 0:
            del row[0]
            street_address = "4001 South 700 East"
            row[0][1] = street_address
            address_hash.append([0, street_address])
        s = str(row[2])
        for c in s:
            if c is "(":
                i = s.index(c) #zipcode
                address_id = row[0]
                address_id = address_id - 1 #indexing starts from zero
                zipcode = s[i + 1:-1]
                street_address = s[1:i]

                row[2] = street_address #hash address table
                address_hash.append([address_id, street_address, zipcode])
                break

        if isinstance(row[0], list) is False: #distance graph
            temp_list = [row[0] - 1]
            all_miles_in_current_node = row[3::]
            temp_list.extend(all_miles_in_current_node)
            dist_list.append(temp_list)


def sort_adj_mat():
    distances_only_table = d_hash[1:]
    for t in distances_only_table:
        del t[0]
        del t[0]
        del t[0]

    new_dist = []
    u = 0
    v = 1

    for d in distances_only_table:
        for e in distances_only_table[u]:
            if e is '':
                d[v-1] = (v-1, float(d_hash[v][u]))
            else:
                d[v-1] = (v-1, float(d[v-1]))
            v += 1
        v = 1
        u += 1
        d.sort(key=lambda x: x[1])
        new_dist.append(d)
    return new_dist


def adj_matrix():
    for row in dist_list:
        row[-1] = '' #remove blank spaces
        for r, col in enumerate(row):
            if col is '':
                u = row[0] #row hash id
                a_to_b = dist_list[r - 1][u + 1] #weight
                if a_to_b is not '':
                    row[r] = a_to_b
                else:
                    row[r] = '0.0' #last element should be set to 0.0

    r, c = 0, 0

    for row in dist_list:
        for col in row:
            dist_list[r][c] = float(col) #string to float conversion for processing
            c += 1
        c = 0
        r += 1

        del row[0]
    return dist_list #returning adresses as adjacency matrix

    r, c = 0, 0
    for row in dist_list:
        for col in row:
            dist_list[r][c] = float(col)
            c += 1
        c = 0
        r += 1
        print(row)
    return dist_list


class Graph:
    def __init__(self):
        self.adj_list = adj_matrix()
        self.sort_dist = sort_adj_mat()
        self.address_list = address_hash


g = Graph()




