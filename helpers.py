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
