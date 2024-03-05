import os.path
from Database import DB

sample = DB()

def menu_interface(): 
   print("---------------MENU----------------\n")
   print("1. Create new database\n")
   print("2. Open database\n")
   print("3. Close database\n")
   print("4. Read record\n")
   print("5. Display record\n")
   print("6. Update record\n")
   print("7. Create report\n")
   print("8. Add record\n")
   print("9. Delete record\n")
   print("10. Quit\n")
   print("------------------------------------\n")
   userInput = input("Please choose an option from the menu: ")
   return int(userInput)

def create_database(): 
   #prompts user for valid csv file and calls createDB method of DB class
   while True:
      created_db_file = input("Enter csv file name: ")
      if not os.path.isfile(created_db_file + str(".csv")):
         print(str(created_db_file)+".csv not found")
      else:
         sample.createDB(created_db_file)
         break

def open_database(): 
   #Checks to see if a database is already open. If not, prompts the user to open an available database
   if sample.isOpen():
      print("Database already open. Close database to continue.")
   else:
      selected_database = input("Enter database to open: ")
      sample.OpenDB(selected_database)

def read_record(): 
   #Get specific record by seeking to that place. If no database is open, print error message.
   if sample.isOpen():
      number = input("Enter record to read: ")
      if int(number) < (sample.num_records):
         sample.getRecord(int(number))
         print("Record "+ str(number) + ", ID: "+sample.record["ID"]+"\t first_name: "+sample.record["first_name"]+"\t last_name: "+sample.record["last_name"]+"\t age: "+str(sample.record["age"])+"\t ticket_num: "+sample.record["ticket_num"]+"\t fare: "+sample.record["fare"]+"\t date_of_purchase: "+sample.record["date_of_purchase"])
      else: 
         print("Out of bounds. Choose something between 0 and " + str(sample.num_records - 1))
   else:
      print("Database is closed. Open to use.")

def display_record(): 
   #Displays record by using binary search to find corresponding ID. 
   if sample.isOpen(): 
      number = input("Enter id to find: ")
      found=sample.binarySearch(int(number))
      if found:
         print("ID: "+sample.record["ID"]+"\t first_name: "+sample.record["first_name"]+"\t last_name: "+sample.record["last_name"]+"\t age: "+str(sample.record["age"])+"\t ticket_num: "+sample.record["ticket_num"]+ "\t fare: "+sample.record["fare"]+"\t date_of_purchase: "+sample.record["date_of_purchase"]+ "\tRecord Number: " + str(sample.recordNum))
      else:
         print("ID "+number +  " not found. Location to insert: ",sample.recordNum)  
   else: 
      print("Database is closed. Open to use.")

def update_record(): 
   if sample.isOpen(): 
      number = input("Enter id to update: ")
      if sample.UpdateDB(number): 
         print("Successfully updated.")
      else: 
         print("Operation Failed. ")
   else: 
      print("Database is closed. Open to use.")

      
def create_report(): 
    # Print the report header
    print("First 10 Records (sorted by ID):\n")
    print("ID".ljust(5), "First Name".ljust(15), "Last Name".ljust(20), "Age".ljust(5), "Ticket Number".ljust(20), "Fare".ljust(5), "Date of Purchase".ljust(15))
    print("-"*85)
    
    # Print the first 10 records where the ID exists
    found_records = 0
    for i in range(1, sample.num_records):
        found = sample.binarySearch(str(i).rjust(5, '0'))
        if found: 
            print(sample.record["ID"].ljust(5), sample.record["first_name"].ljust(15), sample.record["last_name"].ljust(20), sample.record["age"].ljust(5), sample.record["ticket_num"].ljust(20), sample.record["fare"].ljust(5), sample.record["date_of_purchase"].ljust(15))
            found_records += 1
        if found_records == 10:
            break


def delete_record(): 
   if sample.isOpen(): 
      id_input = input("Enter id to delete record: ")
      if sample.deleteDB(id_input): 
         print(f"Successfully deleted record.")
      else: 
         print("Operation Failed. ")
   else: 
      print("Database is closed. Open to use.")

def add_record(): 
   if sample.isOpen(): 
      print("Enter values of the new record: ")
      id_input = input("ID: ")
      fname = input("First Name: ")
      lname = input("Last Name: ")
      age = input("Age: ")
      ticket = input("Ticket Number: ")
      fare = input("Fare: ")
      date = input("Date of Purchase: ")
      sample.addDB(id_input, fname, lname, age, ticket, fare, date)
   else: 
      print("Database is closed. Open to use.")

# Menu Function
def main():
    quit = False
    while quit == False:
         userInput = int(menu_interface())
         if userInput == 1:
            #Creates database
            create_database()

         elif userInput == 2:
            #Opens database
            open_database()

         elif userInput == 3:
            #Closes database
            sample.CloseDB()

         elif userInput == 4:
            #Reads record
            read_record()

         elif userInput == 5:
            #Displays record using binary search
            display_record()

         elif userInput == 6:
            #Updates specific attribute of record specified by user
            update_record()

         elif userInput == 7:
            #prints first 10 records
            create_report()

         elif userInput == 8:
               print("Adding record")
               add_record()

         elif userInput == 9:
            #deletes record upon id input
            delete_record()

         elif userInput == 10:
            if sample.isOpen():
               print ("Please close the database first.")
            else:
               print("Quitting")
               quit = True
         else:
            print("Invalid option. Try again. ")
         
            
         

if __name__ == "__main__":
    main()
