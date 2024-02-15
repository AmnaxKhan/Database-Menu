import csv
import os.path

class DB:

    #default constructor
    def __init__(self):
        self.filestream = None
        self.num_records = 0
        self.record_size = 0
        self.fileptr = None

    #create database
    def createDB(self,filename):
        #Generate file names
        csv_filename = filename + ".csv"
        text_filename = filename + ".data"
        config_filename = filename + ".config"
        
        # Read the CSV file and write into data files
        with open(csv_filename, "r") as csv_file:
            data_list = list(csv.DictReader(csv_file,fieldnames=('ID','first_name','last_name','age','ticket_num', 'fare', 'date_of_purchase')))

        
		# Formatting files with spaces so each field is fixed length, i.e. ID field has a fixed length of 86
        def writeDB(filestream, dict):
            filestream.write("{:5.5}".format(dict["ID"]))
            filestream.write("{:15.15}".format(dict["first_name"]))
            filestream.write("{:20.20}".format(dict["last_name"]))
            filestream.write("{:5.5}".format(dict["age"]))
            filestream.write("{:20.20}".format(dict["ticket_num"]))
            filestream.write("{:5.5}".format(dict["fare"]))
            filestream.write("{:15.15}".format(dict["date_of_purchase"]))
            filestream.write("\n")
            


        count = 0
        with open(text_filename,"w") as outfile:
            for dict in data_list:
                writeDB(outfile,dict)
                emptyRecord = {"ID": "0", "first_name": "Null", "last_name": "Null", "age": "0", "ticket_num": "0", "fare": "0", "date_of_purchase": "Null"}
                writeDB(outfile, emptyRecord)
                count += 2

        # Opening a config file for writing details
        self.num_records = count
        self.record_size = 86
        config_fileptr = open(config_filename, "w")
        config_fileptr.write(str(self.num_records) + "\n")
        config_fileptr.write(str(self.record_size) + "\n")
        config_fileptr.close()

    #seeking to a specific record method
    def getRecord(self, recordNum):

        self.flag = False
        ID = first_name = last_name = age = ticket_num = fare = date_of_purchase = "None"

        if recordNum >=0 and recordNum < self.num_records:
            self.fileptr.seek(0,0)
            self.fileptr.seek(recordNum*self.record_size)
            line = self.fileptr.readline().rstrip('\n')
            self.flag = True
        else:
            #print("You are going out of bounds. You will see an empty record. Choose something between 0 and " + str(self.num_records - 1))
            self.flag = False
            self.record = dict({"ID": "0", "first_name": "Null", "last_name": "Null", "age": "0", "ticket_num": "0", "fare": "0", "date_of_purchase": "Null"})
        
        if self.flag:
            ID = line[0:5]
            first_name = line[5:20]
            last_name = line[20:40]
            age = line[40:45]
            ticket_num = line[45:65]
            fare = line[65:70]
            date_of_purchase = line[70:85]
            self.record = dict({"ID":ID,"first_name":first_name,"last_name":last_name,"age":age,"ticket_num":ticket_num, "fare": fare, "date_of_purchase": date_of_purchase})

    #Binary Search by record id
    def binarySearch(self, input_ID):
        low = 0
        high = self.record_size - 1
        found = False
        self.recordNum = None  # Initialize the insertion point

        while not found and high >= low:
            self.middle = (low + high) // 2
            self.getRecord(self.middle)
            mid_id = self.record["ID"]

            if mid_id.strip() == "0":
                non_empty_record = self.findNearestNonEmpty(self.middle, low, high)
                if non_empty_record == -1:
                    # If no non-empty record found, set recordNum for potential insertion
                    self.recordNum = high 
                    print("Could not find record with ID..", input_ID)
                    return False

                self.middle = non_empty_record
                self.getRecord(self.middle)
                mid_id = self.record["ID"]
                if int(mid_id) > int(input_ID):
                    self.recordNum = self.middle - 1
                else:
                    self.recordNum = self.middle + 1

            if mid_id != "0":
                try:
                    if int(mid_id) == int(input_ID):
                        found = True
                        self.recordNum = self.middle
                    elif int(mid_id) > int(input_ID):
                        high = self.middle - 1
                    elif int(mid_id) < int(input_ID):
                        low = self.middle + 1
                except ValueError:
                    # Handle non-integer IDs
                    high = self.middle - 1

        if not found and self.recordNum is None:
            # Set recordNum to high + 1 if no suitable spot is found
            self.recordNum = high 
            print("Could not find record with ID", input_ID)

        return found

    def findNearestNonEmpty(self, start, low_limit, high_limit):
        step = 1  # Initialize step size

        while True:
            # Check backward
            if start - step >= low_limit:
                self.getRecord(start - step)
                if self.record["ID"].strip() != "0":
                    #print(self.record)
                    return start - step

            # Check forward
            if start + step <= high_limit:
                self.getRecord(start + step)
                if self.record["ID"].strip() != "0":
                    #print(self.record)
                    return start + step

            # Increase step size and repeat
            step += 1

            # Terminate if beyond the search range
            if start - step < low_limit and start + step > high_limit:
                break

        return -1  # No non-empty record found


    #open the database/also acting as my read data method
    def OpenDB(self, nameDB):
        if self.isOpen():
           print("You already have a database open.  Please close it first.")
        else:
           data_file = nameDB + ".data"
           config_file = nameDB + ".config"
        
           if not os.path.isfile(data_file):
              print(str(data_file)+" not found")
           else:
              if not os.path.isfile(config_file):
                 print(str(config_file)+" not found")
              else:
                 self.fileptr = open(data_file, "r+")
                 config_fileptr = open (config_file, "r")
                 self.num_records = int(config_fileptr.readline())
                 self.record_size = int(config_fileptr.readline())
                 config_fileptr.close()

    #check if a database is already open or not
    def isOpen(self):
        if self.fileptr == None:
            return False
        else:
            return True


    #close the database
    def CloseDB(self):
        if self.fileptr:
            self.fileptr.close()
            self.num_records = 0
            self.record_size = 0
            self.fileptr = None
            self.filestream = None
            print("Database closed!")
        else:
            print("You do not have any databases open to close them.")

    #update record
    def UpdateDB(self, inputID): 
        if self.isOpen(): 
            found=self.binarySearch(int(inputID))
            if found: 
                print("Record to update: ")
                print("ID: "+self.record["ID"]+"\t first_name: "+self.record["first_name"]+"\t last_name: "+self.record["last_name"]+"\t age: "+str(self.record["age"])+"\t ticket_num: "+self.record["ticket_num"]+ "\t fare: "+self.record["fare"]+"\t date_of_purchase: "+self.record["date_of_purchase"]+ "\tRecord Number: " + str(self.recordNum))
                print("Choose the field you want to update:")
                print("1. First Name")
                print("2. Last Name")
                print("3. Age")
                print("4. Ticket Number")
                print("5. Fare")
                print("6. Date of Purchase")
                field_choice = int(input("Enter the number of the field to update: "))
                
                self.fileptr.seek(self.recordNum * self.record_size)

                if field_choice == 1:
                    fname = input("Enter new first name: ")
                    self.record['first_name'] = fname

                elif field_choice == 2:
                    lname = input("Enter new last name: ")
                    self.record['last_name'] = lname

                elif field_choice == 3:
                    age = input("Enter new age: ")
                    self.record['age'] = age
                elif field_choice == 4:
                    ticket = input("Enter new ticket: ")
                    self.record['ticket_num'] = ticket
                elif field_choice == 5:
                    fare = input("Enter new fare: ")
                    self.record['fare'] = fare
                elif field_choice == 6:
                    date_of_purchase = input("Enter new date of purchase: ")
                    self.record['date_of_purchase'] = date_of_purchase
                else:
                    print("Invalid field choice.")
                    return False
                # Write the updated record to the file
                self.fileptr.seek(self.recordNum * self.record_size)
                self.fileptr.write("{:5.5}".format(self.record["ID"]))
                self.fileptr.write("{:15.15}".format(self.record["first_name"]))
                self.fileptr.write("{:20.20}".format(self.record["last_name"]))
                self.fileptr.write("{:5.5}".format(self.record["age"]))
                self.fileptr.write("{:20.20}".format(self.record["ticket_num"]))
                self.fileptr.write("{:5.5}".format(self.record["fare"]))
                self.fileptr.write("{:15.15}".format(self.record["date_of_purchase"]))
                self.fileptr.write("\n")

                return True
            else:
                print(f"Record with ID {inputID} not found.")
                return False
        else:
            print("Database is not open.")
            return False

    #Deletes record by replacing with empty record.     
    def deleteDB(self, inputID):
        if self.isOpen(): 
            found=self.binarySearch(int(inputID))
            if found: 
                self.record = dict({"ID": "0", "first_name": "Null", "last_name": "Null", "age": "0", "ticket_num": "0", "fare": "0", "date_of_purchase": "Null"})
                self.fileptr.seek(self.recordNum * self.record_size)
                self.fileptr.write("{:5.5}".format(self.record["ID"]))
                self.fileptr.write("{:15.15}".format(self.record["first_name"]))
                self.fileptr.write("{:20.20}".format(self.record["last_name"]))
                self.fileptr.write("{:5.5}".format(self.record["age"]))
                self.fileptr.write("{:20.20}".format(self.record["ticket_num"]))
                self.fileptr.write("{:5.5}".format(self.record["fare"]))
                self.fileptr.write("{:15.15}".format(self.record["date_of_purchase"]))
                self.fileptr.write("\n")
                return True
            else: 
                return False
        else: print("Database is not open. ")
        return False

    def addDB(self, id, fname, lname, age, ticket, fare, date): 
        found=self.binarySearch(int(id))



#emptyRecord = {"ID": "0", "first_name": "Null", "last_name": "Null", "age": "0", "ticket_num": "0", "fare": "0", "date_of_purchase": "Null"}
