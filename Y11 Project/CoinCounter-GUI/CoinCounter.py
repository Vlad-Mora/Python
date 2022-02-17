import json
import time
from threading import *
from tkinter import *

# TOOLS:

### Use the following object for all volunteers data
##{
##    "volunteerName": {
##        "bagsCounted": number,
##        "bagsCorrectlyCounted": number,
##        "accuracy": number
##        }
##    }

### Window interface
##createWindow(
##    variableName: string;
##    windowName: string;
##    labels?: string[];
##    inputWithLabel?: string[];
##    optionsMenu?: string[];
##    buttons?: { [key: string]: function }[];
##    )


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

# Generic function used to create a GUI window
def createWindow(**kwargs):
    # To avoid having the same name for each different window, there is a name for each window passed as an argument
    kwargs["variableName"] = Tk()
    # Set the name of the window
    kwargs["variableName"].title(kwargs["windowName"])
    # Set the default size of the window
    kwargs["variableName"].geometry("400x300")
    # feedbackLabel is a label used for displaying errors or messages. This is a global variable so it can be used outside this function
    global feedbackLabel
    # global array of the input fields so the data can be taken from outside this function    
    global inputs
    inputs = []
    # This checks if the array isn't empty. If so, it will loop throughthe array and make a label with the text and an input for that label
    if len(kwargs["inputWithLabel"]) > 0:
        for entryField in kwargs["inputWithLabel"]:
            # Creates a label
            windowLabel = Label(kwargs["variableName"], text=entryField)
            windowLabel.pack()

            # Creates an input field and appends it to the array of inputs
            inputs.append(Entry(kwargs["variableName"]))
            inputs[len(inputs) - 1].pack()

    # This checks if the array isn't empty. If so, it will loop throughthe array and make a label with the text
    if len(kwargs["labels"]) > 0:
        for label in kwargs["labels"]:
            # Create label
            windowLabel = Label(kwargs["variableName"], text=label)
            windowLabel.pack()

    # This checks if the array isn't empty. If so, it will loop throughthe array and make a label with the text
    if len(kwargs["optionsMenu"]) > 0:
        # Sets a default value to the dropdown
        default = StringVar(kwargs["variableName"])
        default.set("Click to choose")
        # Create dropdown menu
        windowMenu = OptionMenu(kwargs["variableName"], default, *kwargs["optionsMenu"], command=menu)
        windowMenu.pack()

    # This checks if the array isn't empty. If so, it will loop throughthe array and make a label with the text
    if len(kwargs["buttons"]) > 0:        
        for button in kwargs["buttons"].keys():
            # Create button (check structure at the top of the file to determine how the parameters are used
            windowButton = Button(kwargs["variableName"], text=button, command=kwargs["buttons"][button])
            windowButton.pack()

    # Make a feedbackLabel that will be used for errors/confirmation of processes
    feedbackLabel = Label(kwargs["variableName"], text="")
    feedbackLabel.pack()

# function used to manage file (create/read/write)
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
                # Returns file content as an object
                return json.loads(file.read())

# This function is used to convert input data to only integers so it can be used within the programs
def parseText(text):
    # Remove '£' and add two 0's at the end (input e.g '£1' => '100')
    if "£" in text:
        text = text.replace("£", "") + "00"
    # Remove 'p' (input e.g '10p' => '10')    
    elif "p" in text:
        text = text.replace("p", "")
    # Remove 'g' (input e.g '200g' => '200')
    elif "g" in text:
        text = text.replace("g", "")

    # Return the parsed text
    return text

# This function is used to validate the inputs of the user
def validateRecord(data):
    # Count used to check amount of checks passed (3 required to pass checks)
    checkCount = 0
    # Checks if the name is invalid and throws an error or adds 1 to the checkCount
    if len(data[0]) < 1 or "'" in data[0] or data[0].isdecimal():
        feedbackLabel.config(text="Invalid input. Please re-enter your name.")
        return False
    else:
        checkCount += 1
        
    # Checks if the coin type is invalid and throws an error or adds 1 to the checkCount
    if len(data[1]) < 1 or parseText(data[1]) not in file_content["coinProps"]:
        feedbackLabel.config(text="Invalid input. Please re-enter coin type.")
        return False
    else:
        checkCount += 1
    
    # Checks if the bag weight is invalid and throws an error or adds 1 to the checkCount
    if len(str(data[2])) < 1 or not parseText(data[2]).isdecimal():
        feedbackLabel.config(text="Invalid input. Please re-enter bag weight.")
        return False
    else:
        checkCount += 1

    # If the count is 3 then it returns True
    if checkCount == 3:    
        checkRecord(data)
        return True

# This function is used to evaluate the bag of coins
def checkRecord(data):
    # Removes any special characters from the string (e.g £)
    data[1] = parseText(data[1])
    # Converts the string of the bag weight into an integer
    data[2] = int(parseText(data[2]))
    # Calculate the expected bag weight based on the coin type
    expectedBagWeight = (file_content["coinProps"][data[1]]["bagValue"] / int(data[1])) * file_content["coinProps"][data[1]]["coinWeight"]
    total = 0
    correctlyCounted = 0
    # Checks if it's the expected bag weight and displays result
    if float(data[2]) == expectedBagWeight:
        feedbackLabel.config(text="Correct weight. No need to add / remove coins.")
        # Adds the counted money to the total count        
        file_content["totalValue"] += file_content["coinProps"][data[1]]["bagValue"]
        total += 1
        correctlyCounted += 1
    else:
        # Checks if it's higher than the expected bag weight and displays result
        if float(data[2]) >= expectedBagWeight:
            # Calculate the amount of coins to remove
            weightDifference = data[2] - expectedBagWeight
            removableCoins = int(weightDifference / file_content["coinProps"][data[1]]["coinWeight"])
            feedbackLabel.config(text=f"Remove {removableCoins} coin/s.")
            total += 1
        # Checks if it's lower than the expected bag weight and displays result
        elif float(data[2]) <= expectedBagWeight:
            # Calculate the amount of coins to add
            weightDifference = expectedBagWeight - data[2]
            removableCoins = int(weightDifference / file_content["coinProps"][data[1]]["coinWeight"])
            feedbackLabel.config(text=f"Add {removableCoins} coin/s.")
            # First append 
            total += 1
    
    write_data(data, total, correctlyCounted)

# This function is used to register the entered data and actually write it to the object that will later be written in the file
def write_data(data, total, correctlyCounted):
        # Appends each volunteer's name to the array volunteerList
    volunteerList = []
    for volunteer in file_content["volunteers"]:
        volunteerName = list(volunteer.keys())[0]
        volunteerList.append(volunteerName)
    # Checks if the array of volunteers isn't empty
    if len(file_content["volunteers"]) > 0 or data[0] not in volunteerList:
        # currentVolunteer is the entered volunteer. This variable will get the object
        currentVolunteer = file_content["volunteers"][volunteerList.index(data[0])][data[0]]
        # If so, it will update the data
        currentVolunteer["bagsCounted"] += total
        currentVolunteer["bagsCountedCorrectly"] += correctlyCounted
        # update accuracy
        currentVolunteer["accuracy"] = round((currentVolunteer["bagsCountedCorrectly"] / currentVolunteer["bagsCounted"]) * 100)
    else:
        # Else it will append new data to the array of volunteers
        file_content["volunteers"].append(
            {data[0]: {
                "bagsCounted": total,
                "bagsCountedCorrectly": correctlyCounted,
                "accuracy": round((correctlyCounted/total) * 100)
            }})

def displayVolunteers():
    # Sort array of volunteers in order of accuracy
    file_content["volunteers"] = sorted(file_content["volunteers"], key=lambda d: tuple(d.items())[0][1]["accuracy"], reverse=True)
    # Index used to enumerate volunteers
    index = 1
    # An array of labels that will be passed to the GUI
    labelArray = ["""
        =================================
        List of volunteers sorted by accuracy in descending order:
        e.g Name [bagsCounted / bagsCorrectlyCounted / Accuracy]
        =================================
        """]
    # Formats volunteers' data into one-line string and appends it to the array of labels
    for volunteer in file_content["volunteers"]:
        volunteerName = list(volunteer.keys())[0]
        volunteerAccuracy = volunteer[volunteerName]["accuracy"]
        volunteerBags = volunteer[volunteerName]["bagsCounted"]
        volunteerCorrectBags = volunteer[volunteerName]["bagsCountedCorrectly"]
        labelArray.append(f"{index}. {volunteerName} [{volunteerBags}, {volunteerCorrectBags} , {volunteerAccuracy}%]")
        # increment index
        index += 1

    # make the GUI
    createWindow(
        variableName = "volunteers",
        windowName = "Volunteers",
        labels = labelArray,
        inputWithLabel = [],
        optionsMenu = [],
        buttons = {}
    )


def displayTotal():
    # converts from pennies to pounds
    totalValue = round(file_content["totalValue"] / 100)
    # variable to count the total amount of bags counted
    totalBags = 0
    # variable to count the total amount of bags counted correctly
    totalCorrectBags = 0
    # loop through each volunteer and updates the variables totalBags & totalCorrectBags
    for volunteer in file_content["volunteers"]:
        volunteerName = list(volunteer.keys())[0]
        totalBags += volunteer[volunteerName]["bagsCounted"]
        totalCorrectBags += volunteer[volunteerName]["bagsCountedCorrectly"]

    # make the GUI
    createWindow(
        variableName = "total",
        windowName = "Total Stats",
        labels = [f"""
        ===========================================
        Overall results:
        Total value: £{totalValue}.00
        Counted bags: {totalBags}
        Correctly counted bags: {totalCorrectBags}
        Overall accuracy: {round(totalCorrectBags/totalBags)*100}%
        ===========================================
        """],
        inputWithLabel = [],
        optionsMenu = [],
        buttons = {}
    )
    
# function to decide the menu
def menu(choice):
    # choice[0] is the representing number of the option from the menu. This makes it easier to check for the choice
    if int(choice[0]) == 1:
        # make the GUI
        createWindow(
            windowName = "Register Volunteer",
            labels = [],
            inputWithLabel = ["Name", "Coin Type", "Bag Value"],
            optionsMenu = [],
            buttons = { "Confirm": interfaceToArray }
        )
    elif int(choice[0]) == 2:
        # either call function displayVolunteers() or display the lack of volunteers depending on the number of volunteers registered
        if len(file_content["volunteers"]) > 0:
            displayVolunteers()
        else:
            feedbackLabel.config(text="No volunteers yet registered.")
    elif int(choice[0]) == 3:
        # either call function displayTotal() or display the lack of data depending on the number of volunteers registered
        if len(file_content["volunteers"]) > 0:
            displayTotal()
        else:
            feedbackLabel.config(text="No data yet registered.")
    elif int(choice[0]) == 4:
        # write data to the file and exit program
        manageFile("w")
        quit()

# function used to get the input values from the GUI
def interfaceToArray():
    tempArray = []
    for inputVar in inputs:
        tempArray.append(str(inputVar.get()))

    checkVar = validateRecord(tempArray)
    while checkVar != True:
        interfaceToArray()
        
    return checkVar

def main():
    # Read file and make variable global so it can be used anywhere in the program
    global file_content
    # Reads file on the opening of the program
    file_content = manageFile("r")

    # Create GUI menu
    createWindow(
        variableName = "menu",
        windowName = "Menu",
        labels = ["""
        =================================
        Please select an option from the following:
        1. Register new record
        2. Display all volunteers
        3. Display total counts
        4. Quit
        =================================
        """],
        inputWithLabel = [],
        optionsMenu = ["1. Register volunteer", "2. Show volunteers", "3. Show all data", "4. Quit"],
        buttons = {}
    )

main()
