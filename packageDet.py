'''
Daniel LaForce
#001119118
C950
'''

import csv
from graph import address_hash
pkgFile = './Package File.csv'

pkg_tbl_hash = [] #developing a package hash table
with open(pkgFile) as pf:
    reader = csv.reader(pf)
    line_number = 0
    delivery_status = 'at hub'
    pf.readline()
    for row in reader:
        # set variables for insert function
        package_id_number = int(row[0])
        delivery_address = row[1]
        delivery_deadline = row[5]
        delivery_city = row[2]
        delivery_state = row[3]
        delivery_zip_code = row[4]
        package_weight = row[6]
        special_notes = row[7]
        pkg_tbl_hash.append([package_id_number, delivery_address, delivery_deadline, delivery_city, delivery_state,
                             delivery_zip_code, package_weight, delivery_status, special_notes])

pwdelivery_deadlines = ["Delivery Deadlines"]
pwodelivery_deadlines = ["No Delivery Deadline"]

pwspecial_notes = ["Special Notes"]
pwospecial_notes = ["No Special Needs"]

delayed_pack = ["Delayed Flights"]
grouped_deliveries = ["Grouped Deliveries"]
T1 = ["Load on this Truck one only"]
T2 = ["Load on this Truck two only"]
T3 = ["Load on this Truck two only"]
incorrect_address = ["Wrong Address"]

zipcode_sort = ["By Zipcode"]
m_package_id_list = []
m_package_list = []


class Package:
    # init class
    def __init__(self, package_list, package_key):
        m_package_list.append(self)
        #each package details
        self.package_info_list = package_list[package_key - 1]
        self.p_id_num = package_key
        package_key -= 1
        self.d_address = self.package_info_list[1]
        self.zip = ''
        self.address_id = -1
        self.d_deadline = self.package_info_list[2]
        self.load_t = ''
        self.delivery_t = ''
        self.d_city = self.package_info_list[3]
        self.d_state = self.package_info_list[4]
        self.d_zip = self.package_info_list[5]
        self.p_weight = self.package_info_list[6]
        self.d_status = 'at hub'
        self.special_notes = self.package_info_list[8]
        self.required_truck = ''
        self.loaded_on_truck = ''

        # O(N)
        for a in address_hash:
            if a[1] == self.d_address:
                self.address_id = a[0] - 1
                break
        if self.address_id is -1:
            self.address_id = 23

        # place package into correct special notes list to be loaded onto appropriate trucks in trucks.py
        p_id = self.p_id_num
        s = self.special_notes
        d = self.d_deadline

        if self.d_deadline != 'EOD':
            pwdelivery_deadlines.append([p_id, d])
        else:
            pwodelivery_deadlines.append([p_id, d])
            self.d_deadline = ''

        if self.special_notes:
            pwspecial_notes.append([p_id, s])

        if 'Can only be on truck' in s:

            split = s.split()

            for i in split:
                if i.isdigit():
                    truck_number = i

            truck = 'T' + str(truck_number)
            self.required_truck = truck

            if truck is 'T1':
                T1.append([p_id, truck])
            elif truck == 'T2':
                T2.append([p_id, truck])
            elif truck == 'T3':
                T3.append([p_id, truck])
            else:
                print("Truck does not exist. Check your truck string OR create a new Truck object from the Truck Class."
                      )

        if 'Delayed' in s: #delayed packages info
            delayed_pack.append([p_id, s])

        if 'Wrong address listed' in s:
            incorrect_address.append([p_id, s])

        if 'Must be' in s:
            grouped_deliveries.append([p_id, s])

        #   the packages in this list will be added last to fill the remaining spots in the trucks
        no_deadline = False
        for i in pwodelivery_deadlines[1:]:
            if p_id == i[0]:
                no_deadline = True
        if no_deadline and not s:
            pwospecial_notes.append(p_id)

        if p_id not in m_package_id_list:
            m_package_id_list.append(p_id)
        else:
            print("Package Id already exists. Please try again.")

    def info(self):
        info = '''
        Package Id Number: {}
        Delivery Address: {}
        Delivery Address ID: {}
        Delivery Deadline: {}
        Delivery Time: {}
        Delivery City: {}
        Delivery State: {}
        Delivery Zip Code: {}
        Package Weight: {}
        Delivery Status: {}
        Loaded on Truck Number: {}
        Special Notes: {}
        '''.format(self.p_id_num, self.d_address, self.address_id, self.d_deadline, self.delivery_t,
                   self.d_city, self.d_state, self.d_zip, self.p_weight,
                   self.d_status, self.loaded_on_truck, self.special_notes)
        return info

def mp_list_build(package_list):
    for p in package_list:
        package_id = p[0]
        Package(package_list, package_id)


def new_pack(package_id, delivery_address, delivery_deadline, delivery_city, delivery_zipcode,
             package_weight, delivery_status, special_notes):

    if package_id not in m_package_id_list:
        pkg_tbl_hash.append([package_id, delivery_address, delivery_deadline, delivery_city, delivery_state,
                            delivery_zipcode, package_weight, delivery_status, special_notes])
    Package(pkg_tbl_hash, package_id)

    return True

def pack_on_time(package, delivered):
    pd = package.d_deadline

    deadline_hours = pd[0:2]
    deadline_minutes = pd[3:5]
    d_meri = pd[-2:]

    delivered.split(":")
    delivered_hours = delivered[0]
    delivered_minutes = delivered[2] + delivered[3]
    delivered_meridies = delivered[-2:]

    if (deadline_hours >= delivered_hours and deadline_minutes >= delivered_minutes) \
            or \
            (d_meri is 'AM' and delivered_meridies is 'PM'):
        return False
    else:
        return True

mp_list_build(pkg_tbl_hash)

for p in pkg_tbl_hash:
    print(p) # The package ID is unique






