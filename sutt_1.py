import json
class RideRequest:
    def __init__(self,name,destination,periodofday,year,submitted_at):
        self.name = name 
        self.destination = destination 
        self.periodofday = periodofday 
        self.year = year 
        self.submitted_at = submitted_at 

def ask_year():
    while True:
        try:
            text = input("Enter the year of your study : ")
            year = int(text)
            pass
        except ValueError:
            print(f'{text} is not a valid year of study.')
            continue
        if year<=5 and year>=1:
            return year
        else:
            print(f'{year} is not a valid year of study.')

def ask_time():
    while True:
        slot = input("When are you going (Morning/Afternoon/Evening/Night)? ").strip().title()
        if slot in ["Morning","Afternoon","Evening","Night"]:
            return slot
        else:
            print("Time slot must be Morning, Afternoon, Evening or Night.")

def dest():
    while True:
        destination = input("Where are you going?").strip().title()
        if destination in ["Jaipur","Delhi"]:
            return destination
        else:
            print(f'You can only book cabs for either Delhi or Jaipur')


class Cab:
    def __init__(self,dname,seats,destination,time,studlist,left):
        self.dname = dname 
        self.seats = seats 
        self.destination = destination 
        self.time = time 
        self.left = left 
        self.studlist = studlist 
requests = []   
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
        requests.append(req)
        print(f"Request added for {name}.")

    elif choice == '2':
        print("Students in queue")
        if len(requests) == 0:
            print("Nobody is waiting.")
        else:
            for req in requests:
                print(f"{req.name} - {req.destination}, {req.periodofday}, year {req.year}")

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
    elif choice == '3':
        for cab in cabs:
            if cab.left:
                continue                      
            matching = []
            for req in requests:
                if req.destination == cab.destination and req.periodofday == cab.time:
                    matching.append(req)
            matching = matching[:cab.seats]   
            print(f"{cab.dname} - {cab.destination}, {cab.time}:")
            if len(matching) == 0:
                print("No students are waiting for this cab.")
            else:
                for req in matching:
                    print(f"{req.name} (year {req.year} is waiting for this cab)")
    elif choice == '4':
        destination = dest()
        time_slot = ask_time()

        chosen_cab = None
        for cab in cabs:
            if not cab.left and cab.destination == destination and cab.time == time_slot:
                chosen_cab = cab
                break                      # first open cab only

        if chosen_cab is None:
            print("No open cab for that trip.")
        else:                      
            matching = []
            for req in requests:
                if req.destination == chosen_cab.destination and req.periodofday == chosen_cab.time:
                    matching.append(req)
            matching = matching[:chosen_cab.seats]   
            print(f"{chosen_cab.dname} - {chosen_cab.destination}, {chosen_cab.time}:")
            if len(matching) == 0:
                print("No students are waiting for this cab.")
                continue
            else:
                chosen_cab.studlist.extend(matching)
                still_waiting = []
                for req in requests:
                    if req not in matching:
                        still_waiting.append(req)
                requests = still_waiting
                chosen_cab.left = True
                print(f"{chosen_cab.dname}'s cab has left with:")
                for req in matching:
                    print(f"{req.name} (year {req.year} has left in this cab)")       
    
    elif choice == '5':
        break