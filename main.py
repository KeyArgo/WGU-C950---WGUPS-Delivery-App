'''
Daniel LaForce
#001119118
C950
'''

import packageDet
import trucks


def format_time(time):
    if 8 < len(time) < 7:
        print("Time Invalid")
        menu()

    meri = time[-2:]
    st_split = time.split(':')
    hrs = int(st_split[0])
    min = int(time[-5:-3])

    if hrs not in range(1, 24, 1):
        print("Input Invalid")
        menu()

    if min not in range(0, 60, 1):
        print("Minutes Invalid")
        menu()

    min = min / 60

    if meri.upper() not in ['AM', 'PM']:
        print("Invalid Input. It should be AM or PM")
        menu()

    if meri.upper() == 'PM':
        if hrs == 12:
            hrs = hrs
        else:
            hrs = hrs + 12

    time = hrs + min
    return time


def menu():
    userIn = -1
    while userIn != '4':
        userIn = \
            input("********************MENU************************\n"
                  "press 1 to get information about 1 package\n"
                  "press 2 to get information about all packages\n"
                  "press 3 to enter a new package\n"
                  "press 4 to exit\n"
                  )

        if userIn.lower() not in ['1', '2', '3', '4']:
            print("Invalid input")
            menu()

        if userIn.lower() == '4':
            return

        if userIn == '1':
            package_id = input("Package Id?")
        if userIn == '1' or userIn == '2':
            status_list = [] #package Status List
            sTime = input("Start Time(HH:MM AM/PM)?")
            sTime = format_time(sTime)
            eTime = input("End Time(HH:MM AM/PM)?")
            eTime = format_time(eTime)

            for pack in packageDet.m_package_list: # Printing package Details
                if pack.delivery_t == '':
                    print('Delivery Unsuccessful', pack.info())

                lTime = format_time(pack.load_t)

                delivery_time = format_time(pack.delivery_t)
                if pack.load_t != '' and (sTime >= lTime) and (delivery_time > eTime):
                   # status_list.append(pack.pId)
                    pack.dStatus = 'in route'

                if pack.delivery_t != '' and delivery_time < eTime:
                    status_list.append(pack.p_id_num)
                    pack.dStatus = 'delivered'

                if pack.p_id_num not in status_list:
                    pack.d_status = 'hub'
                    pack.loaded_on_truck = 'TBD'

                if userIn == '1':
                    if pack.p_id_num == int(package_id):
                        print(pack.info())
                        break

                if userIn == '2':
                    print(pack.info())

        if userIn == '3':
            pID = int(input("Package id?"))
            dAddress = str(input("Address?"))
            dDeadline = str(input("Deadline?"))
            dCity = str(input("City?"))
            dZipCode = str(input("Zipcode?"))
            pWeight = str(input("Package Weight?"))
            status = str(input("Status?"))
            sNote = str(input("Special Note?"))
            if packageDet.new_pack(pID, dAddress, dDeadline, dCity,dZipCode, pWeight, status, sNote):
                print("Package inserted successfully", packageDet.m_package_list[pID - 1].info())
                menu()
            else:
                print("Some Error occured try again")
                menu()

menu()




