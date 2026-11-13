import heapq
import json
from RideRequest import RideRequest
from cab import Cab
from helpers import ask_year, ask_time, dest



queues = {}
cabs = []
with open("cabs.json","r") as cabs_available:
    cab_list = json.load(cabs_available)

for d in cab_list:
    cab = Cab(d["dname"], int(d["seats"]), d["destination"], d["time"], d["studlist"], d["left"])
    cabs.append(cab)


counter = 0
while True:
    print("Enter 1 for adding a new ride request.")
    print("Enter 2 to view the waiting list and the list of all available and left cabs.")
    print("Enter 3 to find a cab.")
    print("Enter 4 to Dispatch a cab.")
    print("Enter 5 to quit.")
    choice = input("Your choice : ")
    
    if choice in ['1','2','3','4','5']:
        pass
    else:
        print("Enter a valid choice.")

    
    if choice == '1':
        name = input("Enter your name : ").strip()
        destination = dest().title()
        time_slot = ask_time().title()
        year = ask_year()
        counter = counter + 1
        req = RideRequest(name, destination, time_slot, year, counter)
        key = (destination, time_slot)
        if key not in queues:
            queues[key] = []
        heapq.heappush(queues[key],(-year,counter,req))
        print(f"Request added for {name}.")

    elif choice == '2':
        print("Students in queue")
        waiting = 0
        for heap in queues.values():
            for item in sorted(heap):
                req = item[2]
                print(f"{req.name} - {req.destination}, {req.periodofday}, year {req.year}")
                waiting += 1
        if waiting == 0:
            print("Nobody is waiting.")

        print("All cabs:")
        if len(cabs) == 0:
            print("No cabs available.")
        else:
            for cab in cabs:
                if cab.left:
                    status = "Left"
                else:
                    status = "Waiting"
                print(f"{cab.dname} - {cab.destination}, {cab.time}, {len(cab.studlist)}/{cab.seats} seats filled, {status}")

    elif (choice == '3'):
        for cab in cabs:
            if cab.left:
                continue
            key = (cab.destination, cab.time)
            print(f"{cab.dname} - {cab.destination}, {cab.time}:")
            if key not in queues or len(queues[key]) == 0:
                print("   No students are waiting for this cab.")
            else:
                preview = heapq.nsmallest(cab.seats, queues[key])
                for item in preview:
                    req = item[2]
                    print(f"   {req.name} (year {req.year})")

    elif choice == '4':
        destination = dest()
        time_slot = ask_time()
        key = (destination, time_slot)

        chosen_cab = None
        for cab in cabs:
            if not cab.left and cab.destination == destination and cab.time == time_slot:
                chosen_cab = cab
                break

        if chosen_cab is None:
            print("No open cab for that trip.")
        elif key not in queues or len(queues[key]) == 0:
            print("Nobody is waiting for that trip.")
        else:
            boarded = []
            while len(boarded) < chosen_cab.seats and len(queues[key]) > 0:
                item = heapq.heappop(queues[key])
                boarded.append(item[2])

            chosen_cab.studlist.extend(boarded)
            chosen_cab.left = True
            print(f"{chosen_cab.dname}'s cab has left with:")
            for req in boarded:
                print(f"   {req.name} (year {req.year})")      
    
    elif choice == '5':
        break