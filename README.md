# Cab Pool Matcher

This is my submission for the SUTT back-end task 1. It's a command-line app in Python that takes cab requests from students, puts people going to the same place at the same time together, and gives seats to the most senior students first when there aren't enough seats.
I used `json` and `heapq`, which come with Python, so there's no requirements.txt.

## Running it

You need Python 3. Keep all the files in one folder, open a terminal in that folder and run:

```
python main.py
```

## Files

- `main.py` has the menu loop and what each option does
- `RideRequest.py` has the RideRequest class
- `cab.py` has the Cab class
- `helpers.py` has the functions that keep asking until the year, destination or time slot is valid
- `cabs.json` is the sample list of cabs, loaded when the app starts

## The cab file

`cabs.json` is a list with one entry per cab:

```json
[
  {"dname": "Rohan", "seats": "4", "destination": "Jaipur", "time": "Morning",   "studlist": [], "left": 0},
  {"dname": "Rahul", "seats": "3", "destination": "Jaipur", "time": "Afternoon", "studlist": [], "left": 0},
  {"dname": "Kamal", "seats": "3", "destination": "Delhi",  "time": "Evening",   "studlist": [], "left": 0},
  {"dname": "Manav", "seats": "4", "destination": "Delhi",  "time": "Evening",   "studlist": [], "left": 0}
]
```

`dname` is the driver's name and `seats` is how many seats the cab has (1 to 4, and it can be different for each cab). I turn it into a number with `int()` when loading, so it works either way. `destination` is Delhi or Jaipur and `time` is Morning, Afternoon, Evening or Night. `studlist` is the students already inside, so it should start as an empty list. `left` should be 0 for every cab at the start, because a cab marked 1 counts as already gone and can never be dispatched.

The cabs are always looked at in the order they appear in the file, so the app gives the same result every time.

## Using the menu

1. Add a new ride request. It asks for a name, destination, time slot and year. If you type a city we don't serve, a time slot that doesn't exist or something like year 7, it says what's wrong and asks again instead of crashing.
2. View everyone waiting (most senior first) and all the cabs, with the driver, the trip, how many seats are taken like 3/4, and whether it has left or it is still waiting.
3. Find a cab. For each open cab, in file order, this shows who would get a seat. If two cabs go to the same trip, the second one only sees the students the first one didn't take. It's only a preview, nobody is actually given a seat and the waiting list stays the same.
4. Dispatch a cab. You pick a destination and time slot, and the first open cab for that trip is filled with the most senior waiting students and marked as left.
5. Quit.

## How seniors-first works

Every trip (a destination plus a time slot, like Delhi and Evening) gets its own heap. They're stored in a dictionary called `queues`, with the trip as the key. So the queue belongs to the trip and not to any one cab.

`heapq` always gives back the smallest item first, but I want the biggest year first. So each waiting student goes into the heap as a tuple:

```
(-year, order_number, request)
```

The year is negative so that a 5th year (-5) comes out before a 3rd year (-3). The order number is a counter that goes up by one for every new request, and it decides ties. The last part is the RideRequest object itself.

Python compares tuples one item at a time from the left. The order number is different for every request, so the comparison always ends before it reaches the RideRequest object. That matters because comparing two RideRequest objects directly would crash. The `submitted_at` field in RideRequest holds this order number rather than a clock time, so two requests can never tie.

Find a cab works on a sorted copy of the trip's heap (`sorted(heap)`), so the real queue is never changed, and Dispatch uses `heapq.heappop`, which removes students. Both use the same ordering, so the preview matches who Dispatch would actually take. If two open cabs go to the same trip, the preview goes through the cabs in file order: the first cab gets the most senior students, and the next cab gets the students after those, the same way two dispatches in a row would work. That way nobody shows up under two cabs. In the sample file Kamal and Manav both go to Delhi in the evening, so you can see this by adding a few Delhi evening requests and choosing option 3. Dispatch always sends the first open cab for the trip in file order (Kamal here), so Manav's cab goes on the next dispatch.

## Tricky situations

**Half-empty cab.** A cab can leave even if it isn't full. Dispatch keeps taking students while the cab has free seats and someone is still waiting, then stops. If only 2 students are waiting for a 4-seat cab, those 2 go and it shows 2/4. After that it's marked as left, so nobody else can be added to it.

**No cabs left.** If every cab for a trip has already left and a new request comes in, the request still goes into that trip's queue and the student is told there's no open cab right now but they're still on the waiting list. Students only leave the queue when they board a cab, so nobody disappears. They still show up in option 2, and trying to dispatch that trip just prints a message and changes nothing.

**Same year.** This is what the order number in the tuple is for. If two students are in the same year, the first items match, so Python looks at the order numbers, and the student who asked first has the smaller number and gets the seat first.

**Lots of students.** Say n is the number of students waiting for one trip and c is the number of cabs.

- Adding one request is O(log n), because a heap push only moves the new item up about log n levels. After that the app checks whether an open cab exists by looping over the c cabs, which is a small number.
- Adding all 1,000 requests is O(n log n), since it's 1,000 pushes that each cost O(log n). That's roughly 10,000 steps.
- Sending off one cab is O(k log n) where k is at most 4, so basically O(log n). It does at most 4 heap pops that each cost O(log n), plus a look through the c cabs to find the one to send.
- Finding an open cab for a trip is O(c), because it goes through the cab list in order until it finds an open one for that trip. There are only a few cabs so it's quick. Keeping cabs in a dictionary by trip would make it O(1), but I didn't need that here.

The preview in option 3 and the sorted listing in option 2 cost a bit more than one push or pop, but those are only for display and aren't part of the timings above.

