'''
Daniel LaForce
#001119118
C950
'''

import packageDet
from graph import g
import math

delivered_packages = []
address_for_package_found = []
loaded_packages = []
drivers = [1, 1]


def driver_count():
    if len(drivers) == 0:
        return False
    else:
        return True


class Truck:
    def __init__(self, truck):
        truck_ids_list = ['T1', 'T2', 'T3'] #Trucks in our system
        if truck in truck_ids_list:
            self.name = truck
        else:
            print("Truck ID not found ")
        self.number_of_packages = 0 #total packages on truck
        self.max_packages = 16 #max package a truck can have
        self.average_speed = float(18) #truck avg speed
        self.driver = 0
        self.time = 8 #day starts at 8
        self.package_notes = 'No notes.'
        self.distance = float(0) #total dist
        self.all_package_info = [] #packages loaded on the truck
        self.at_hub = True #is package on hub
        self.full_truck = False #truck full capacity reached
        self.mileage = 0
        self.l_time_hr = 8
        self.l_time_min = 0
        self.hours = 0
        self.hours_str = ''
        self.minutes = 0
        self.minutes_str = ''
        self.delivery_time = 0

    def set_d_time(self, miles):
        frac, whole = math.modf(miles / self.average_speed)
        self.hours = round(whole) + self.l_time_hr
        self.minutes = round(frac * 60) + self.l_time_min
        if self.minutes > 60:
            self.minutes = self.minutes - 60
        if len(str(self.minutes)) < 2:
            self.minutes = '0' + str(self.minutes)
        if self.hours > 11:
            meri = ' PM'
        else:
            meri = ' AM'
        self.delivery_time = str(self.hours) + ':' + str(self.minutes) + meri
        return self.delivery_time

    def init_loadtime(self):
        leave_time_minutes = self.l_time_min
        if len(str(leave_time_minutes)) < 2:
            leave_time_minutes = '0' + str(self.l_time_min)
        if self.hours > 11:
            meridies = ' PM'
        else:
            meridies = ' AM'
        return str(self.l_time_hr) + ':' + str(leave_time_minutes) + meridies

    def insert_package(self, package_id):
        if self.number_of_packages < self.max_packages and package_id not in self.all_package_info:
            self.number_of_packages += 1
            if package_id in packageDet.m_package_id_list:
                package_index = package_id - 1
                package_memory_address = packageDet.m_package_list[package_index]
                package_memory_address.loaded_on_truck = self.name
                self.all_package_info.append(package_memory_address)
                loaded_packages.append(package_id)
        else:
            self.full_truck = True
        if self.full_truck is True:
            print("Truck is full.")

    def l_truck(self, package_list):
        if package_list:
            if self.at_hub and self.full_truck is False: #Truck is full or not
                print('Loading truck....', self.name)
                for package in package_list[1:]:
                    if self.full_truck is True:
                        return
                    else:
                        if isinstance(package, list):
                            package_id = package[0]
                            if package_id in packageDet.m_package_id_list:
                                self.insert_package(package_id)
                        else:
                            package_id = package
                            if package_id in packageDet.m_package_id_list:
                                self.insert_package(package_id)

    def d_package(self, package):
        delivered_packages.append(package.p_id_num)
        package.d_status = 'delivered'
        packageDet.m_package_id_list.remove(package.p_id_num)
        package.delivery_t = self.set_d_time(self.mileage)
        if package.d_status == 'delivered':
            package.delivery_t = self.set_d_time(self.mileage)
            if packageDet.pack_on_time(package, package.delivery_t) is False:
                print("Package", package.p_id_num, "was delivered late.")
            else:
                print("Package", package.p_id_num, "was delivered on time.")

    def path(self, start_vertex, package_list):
        if driver_count() is True:
            self.driver = 1
            drivers.pop()
        else:
            print("No available drivers.")
            return

        if not package_list: #if no package then terminate
            return
        for p in package_list:
            p.d_status = 'en route' #set all packages delivery status to shipped
            p.load_t = self.init_loadtime()

        unvisited_queue = [] #list of locations where package is not delivered
        package_list = address_find_list(package_list)# location list sey to package list
        # build a list of address ids to track unvisited package locations
        for p in package_list:
            package_location = p[0]
            if package_location not in unvisited_queue:
                unvisited_queue.append(package_location)
                
        route = []
        address_id = 0
        while len(unvisited_queue) > 0: # choose next location which closest to current location
            hub = g.sort_dist[0]
            if start_vertex == 0:
                route.append(0)
                flag = False
                for vertex in hub:
                    for p in package_list:
                        if p[0] == vertex[0]:
                            packages = p[2:]
                            address_id = p[0]
                            miles = vertex[1]
                            self.mileage += miles
                            for package in packages:
                                if package.p_id_num in packageDet.m_package_id_list:
                                    self.d_package(package)
                            flag = True
                            break
                    if flag:
                        break
                unvisited_queue.remove(address_id)
                route.append(address_id)
                next_vertex = g.sort_dist[address_id]
                start_vertex = 1
            for vertex in next_vertex[1:]:
                vertex_id = vertex[0]
                if vertex_id in unvisited_queue:
                    adj_vertex = vertex_id
                    miles = vertex[1]
                    self.mileage += miles
                    # deliver package
                    for p in package_list:
                        if p[0] == adj_vertex:
                            packages_with_same_address = p[2:]
                            for package in packages_with_same_address:
                                if package.p_id_num in packageDet.m_package_id_list:
                                    self.d_package(package)
                            package_list.remove(p)
                    route.append(unvisited_queue.pop(unvisited_queue.index(adj_vertex)))
                    next_vertex = g.sort_dist[adj_vertex]
                    break
        hub = g.adj_list
        last_index_in_route = route[-1]
        miles_back_to_hub = hub[last_index_in_route][0]
        self.mileage += miles_back_to_hub
        route.append(0)
        self.delivery_time = self.set_d_time(self.mileage)
        self.driver = 0
        drivers.append(1)
        return route


def address_find_list(packages_list):
    package_addresses = []
    if packages_list:
        for p in packages_list:
            package_id = p.p_id_num
            package_addresses.append(p)
            address_for_package_found.append(package_id)
    same_delivery_address = []
    found_package_list = []
    for p in package_addresses:
        street_address = p.d_address
        address_id = p.address_id
        package_id = p.p_id_num
        if [address_id, street_address] not in same_delivery_address:
            same_delivery_address.append([address_id, street_address, p])
        for s in same_delivery_address:
            if s[1] == street_address:
                index = same_delivery_address.index(s)
                if package_id not in found_package_list:
                    found_package_list.append(package_id)
            if p not in same_delivery_address[index]:
                same_delivery_address[index].append(p)
    return same_delivery_address


T1 = Truck('T1')# 0 packages
T1.l_truck(packageDet.T1)# 14 packages
T1.l_truck(packageDet.pwdelivery_deadlines)# until full
T1.l_truck(packageDet.pwospecial_notes)
T1.path(0, T1.all_package_info)
T1.set_d_time(T1.mileage)


T2 = Truck('T2')
T2.l_time_hr = T1.hours
T2.l_time_min = T1.minutes


T3 = Truck('T3')
T3.l_truck(packageDet.pwdelivery_deadlines)
T3.l_truck(packageDet.grouped_deliveries)
T3.l_truck(packageDet.pwospecial_notes)
T3.l_truck(packageDet.pwodelivery_deadlines)
T3.path(0, T3.all_package_info)
T3.set_d_time(T3.mileage)

undelivered_packages = packageDet.m_package_id_list #missed packages are checked
undelivered_packages.insert(0, "undelivered")

#address Correction
packageDet.m_package_list[8].d_address = '410 S State St'
packageDet.m_package_list[8].address_id = 19
T2.l_time_min = T1.minutes
T2.l_truck(undelivered_packages) #no package is missed
T2.path(0, T2.all_package_info)
T2.set_d_time(T2.mileage)

miles_total = T1.mileage + T2.mileage + T3.mileage
print('Total Mileage for All 3 Trucks:', miles_total)

delivered_packages.sort()
print('Delivered Packages:', delivered_packages)

if len(delivered_packages) == len(packageDet.m_package_list):
    print("All packages were delivered.")
else:
    for p in packageDet.m_package_list:
        if p.p_id_num not in delivered_packages:
            print("Undelivered:", p.p_id_num)



