import json
import time
from tkinter import *

# STEPS:
# input: Name, type of coin, weight of bag
# validate type of coin
# calculate coins to be removed / added
# keep track of bags counted & accuracy
# options: display a list of the volunteers (sorted by accuracy) showing [number of bags they counted, correctly counted bags as a percentage]
# TOOLS:
# Use the following object for all volunteers data
##{
##    "volunteerName": {
##        "bagsCounted": number,
##        "bagsCorrectlyCounted": number,
##        "accuracy": number
##        }
##    }

# Structure to be written in file when the file has been created IF it doesn't exist yet
coinProps = """{
    "coinProps" : {
        "200" : {"bagValue": 2000, "coinWeight": 12.00},
        "100" : {"bagValue": 2000, "coinWeight": 8.75},
        "50" : {"bagValue": 1000, "coinWeight": 8.00},
        "20" : {"bagValue": 1000,"coinWeight": 5.00},
        "10" : {"bagValue": 500,"coinWeight": 6.50},
        "5" : {"bagValue": 500,"coinWeight": 3.25},
        "2" : {"bagValue": 100,"coinWeight": 7.12},
        "1" : {"bagValue": 100,"coinWeight": 3.56}
        },
    "volunteers": [],
    "totalValue": 0
    }
    """

# subroutine used to manage file (create/read/write)
def manageFile(action):
    # This "try" statement will try to create a file and write default structure. If file already exists, it will jump to the code block "except:"
    try:
        # Will try to create a file and write the JSON structure defined in the variable 'coinProps'
        with open("CoinCounter.txt", "x") as file:
            pass
        with open("CoinCounter.txt", "w") as file:
            file.write(coinProps)
            file.close()
            print("File created.")
        # Since it is a possibility in the program to want to read the file if it's not created, this will continue the original action
        return manageFile("r")
    # If the file is already created then...
    except:
        # If to be written to, it will transform the object 'file_content' to a JSON formatted string
        if action == "w":
            with open("CoinCounter.txt", "w") as file:
                print("File updated.")
                # JSON format in file to be easy to read the .txt file                
                json.dump(file_content, file, indent=1)
                file.close()
        # If to be read from, it will return the data from the file after being transformed to a JSON object        
        elif action == "r":
            with open("CoinCounter.txt", "r") as file:
                print("File read.")
                # Returns file content as an object
                return json.loads(file.read())

def registerRecord():
    name = input("Please enter your name (avoid any apostrophes):\n")
    coinType = input("Please enter the coin type (e.g £2):\n")
    bagWeight = input("Please enter the weight of the bag:\n")

    return validateCoinBag(name, coinType, bagWeight)

def parseText(text):
    if "£" in text:
        text = text.replace("£", "") + "00"
    elif "p" in text:
        text = text.replace("p", "")
    elif "g" in text:
        text = text.replace("g", "")

    return text

def validateCoinBag(name, coinType, bagWeight):
    while len(name) < 1 or "'" in name or name.isdecimal():
        name = input("Invalid input. Please re-enter your name:\n")
    while len(coinType) < 1 or parseText(coinType) not in file_content["coinProps"]:
        coinType = input("Invalid input. Please re-enter coin type:\n")
    while len(bagWeight) < 1 or not parseText(bagWeight).isdecimal():
        bagWeight = input("Invalid input. Please re-enter bag weight:\n")

    return [name, parseText(coinType), bagWeight]

def checkRecord(data):
    data[2] = int(parseText(data[2]))
    expectedBagWeight = (file_content["coinProps"][data[1]]["bagValue"] / int(data[1])) * file_content["coinProps"][data[1]]["coinWeight"]
    if float(data[2]) == expectedBagWeight:
        print("Correct weight. No need to add / remove coins.")
        data.append(1)
        data.append(1)
    else:
        if float(data[2]) >= expectedBagWeight:
            weightDifference = data[2] - expectedBagWeight
            removableCoins = int(weightDifference / file_content["coinProps"][data[1]]["coinWeight"])
            print(f"Remove {removableCoins} coin/s.")
            data.append(1)
            data.append(0)
        elif float(data[2]) <= expectedBagWeight:
            weightDifference = expectedBagWeight - data[2]
            removableCoins = int(weightDifference / file_content["coinProps"][data[1]]["coinWeight"])
            print(f"Add {removableCoins} coin/s.")
            data.append(1)
            data.append(0)

    write_data(data)
    
def write_data(data):
    volunteerList = []
    if len(file_content["volunteers"]) > 0:
        for volunteer in file_content["volunteers"]:
            volunteerName = list(volunteer.keys())[0]
            volunteerList.append(volunteerName)
        print(volunteerList)
        if data[0] in volunteerList:
            volunteer[data[0]]["bagsCounted"] += data[3]
            volunteer[data[0]]["bagsCountedCorrectly"] += data[4]
            volunteer[data[0]]["accuracy"] = round((volunteer[data[0]]["bagsCountedCorrectly"] / volunteer[data[0]]["bagsCounted"]) * 100)
        else:
            file_content["volunteers"].append({data[0]: {
                "bagsCounted": data[3],
                 "bagsCountedCorrectly": data[4],
                 "accuracy": round((data[4]/data[3]) * 100)
                }})
    else:
        file_content["volunteers"].append({data[0]: {
            "bagsCounted": data[3],
             "bagsCountedCorrectly": data[4],
             "accuracy": round((data[4]/data[3]) * 100)
            }})

    file_content["totalValue"] += file_content["coinProps"][data[1]]["bagValue"]

def displayVolunteers():
    # Sort array of volunteers in order of accuracy
    file_content["volunteers"] = sorted(file_content["volunteers"], key=lambda d: tuple(d.items())[0][1]["accuracy"], reverse=True)
    if len(file_content["volunteers"]) > 0:
        print("List of volunteers sorted by accuracy in descending order:")
        print("e.g Name [bagsCounted / bagsCorrectlyCounted / Accuracy]")
        for volunteer in file_content["volunteers"]:
            volunteerName = list(volunteer.keys())[0]
            volunteerAccuracy = volunteer[volunteerName]["accuracy"]
            volunteerBags = volunteer[volunteerName]["bagsCounted"]
            volunteerCorrectBags = volunteer[volunteerName]["bagsCountedCorrectly"]
            print(f"{volunteerName} [{volunteerBags}, {volunteerCorrectBags} , {volunteerAccuracy}%]")
            time.sleep(.5)
    else:
        print("No volunteers yet registered.")

def displayTotal():
    if len(file_content["volunteers"]) > 0:
        totalValue = round(file_content["totalValue"] / 100)
        totalBags = 0
        totalCorrectBags = 0
        for volunteer in file_content["volunteers"]:
            volunteerName = list(volunteer.keys())[0]
            totalBags += volunteer[volunteerName]["bagsCounted"]
            totalCorrectBags += volunteer[volunteerName]["bagsCountedCorrectly"]

        print(f"""
===========================================
    Overall results:
    Total value: £{totalValue}.00
    Counted bags: {totalBags}
    Correctly counted bags: {totalCorrectBags}
    Overall accuracy: {round(totalCorrectBags/totalBags)*100}%
===========================================
    """)
    else:
        print("No data yet registered.")
    

# Menu
def menu():
    optionsMenu = """
=================================
Please select an option from the following (e.g 2):
1. Register new record
2. Display all volunteers
3. Display total counts
4. Quit
=================================
"""
    option = input(optionsMenu)
    while option not in range(1, 5) or not option.isdecimal():
        option = int(input("Invalid input. Please enter a number of the option of your choice:\n"))
        
    if int(option) == 1:
        checkRecord(registerRecord())
    elif int(option) == 2:
        displayVolunteers()
    elif int(option) == 3:
        displayTotal()
    elif int(option) == 4:
        # Updates file on closure of program
        manageFile("w")
        quit()
    
def main():
    global file_content
    # Read file content and assign to global variable 'file_content' so the data can be used anywhere
    file_content = manageFile("r")
    # Forms an infinite loop until program is closed from the menu
    while True:
        menu()

##main()
# TESTING
def createWindow(**kwargs):
    # Creates an interface window
    window = Tk()
    window.title(kwargs["windowName"])
    window.geometry("250x300")
    inputFieldRow = 1
    for entryField in kwargs["inputWithLabel"]:
        # Creates the input label
        windowLabel = Label(window, text=entryField)
        windowLabel.pack()
        # Creates the input field
        windowInput = Entry(window)
        windowInput.pack()
        inputFieldRow += 1
        

    # Loops through the "buttons" array
    for button in kwargs["buttons"].keys():
        windowButton = Button(window, text=button, command=kwargs["buttons"][button])
        windowButton.pack()

# Test functions
def submit():
    print("Works")

def testFunction():
    print("Hello")

# Option 1 window
createWindow(
    windowName = "Register",
    inputWithLabel = [
            "Name:",
            "Coin Type:",
            "Bag weight:"
        ],
    buttons = {
            "Submit": submit,
            "Hello": testFunction
        }
    )
