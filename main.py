import argparse
import csv
import datetime


class Entry:
    def __init__(self, id, date, description, amount):
        if not isinstance(id, int):
            raise ValueError("ID must be an Int")
        if not isinstance(date,datetime.date):
            raise ValueError("The Date must be an Date Object")
        if not isinstance(description, str):
            raise ValueError("The Description must be a String")
        if not isinstance(amount, float):
            raise ValueError("The Amount has to be an Float")
        self.id = id
        self.date = date
        self.description = description
        self.amount = round(amount, 2)

    def getID(self):
        return self.id
    
    def getDate(self):
        return self.date
    
    def getDescription(self):
        return self.description
    
    def getAmount(self):
        return self.amount
    
    def setID(self, id):
        if not isinstance(id, int):
            raise ValueError("ID must be an Int")
        else:
            self.id = id

    def setDate(self, date):
        if not isinstance(date, datetime.date):
            raise ValueError("The Date must be an Date Object")
        else:
            self.date = date
            
    def setDescription(self, description):
        if not isinstance(description, str):
            raise ValueError("The Description must be a String")
        else:
            self.description = description

    def setAmount(self, amount):
        if not isinstance(amount, float):
            raise ValueError("The Amount has to be an Float")
        else:
            self.amount = round(amount, 2)    

class Tracker:
    def __init__(self, document):
        self.document = document
        self.entrys = []
        self.id_count = 1
        with open(document, newline='') as csvfile:
            data_bank = csv.reader(csvfile, delimiter=' ', quotechar='"')
    
            for i, data_row in enumerate(data_bank):
               # print(data_row[0])
                data = data_row[0].split(",")
                for i in range(len(data)):
                    data[i] = data[i].strip('"')
                #print(data)
                if i == 0:
                    self.id_count = int(data_row[0])
                    print(f"Next ID will be {self.id_count}")
                    continue
                
                #print(f"ID: {data[0]} Date: {data[1]} Description: {data[2]} Amount: {data[3]}")
                entry = Entry(int(data[0]), datetime.date.fromisoformat(data[1]), data[2].replace("_", " "), float(data[3]))
                self.entrys.append(entry)
                


    def save(self):
      with open(self.document, 'w', newline='') as f:
        f.truncate()
        writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow([str(self.id_count)])
        for entry in self.entrys:
            writer.writerow([entry.getID(), entry.getDate(), entry.getDescription().replace(" ", "_"), entry.getAmount()])

    def create_entry(self, amount, description):
           
        entry = Entry(self.id_count, datetime.date.today(), description, float(amount))
        self.id_count += 1
        self.add_entry(entry)
        print(f"Expense added successfully (ID: {entry.getID()})")

    def add_entry(self, entry):
        if not isinstance(entry, Entry):
            raise ValueError("The Entry musst be of the Entry Class!")
        
        self.entrys.append(entry)
        

    def delete_entry(self, id):
        for i, entry in enumerate(self.entrys):
            if entry.getID() == id:
                self.entrys.pop(i)
        print(f"Expense deleted successfully")


    def list(self):
        print("List")
        print("ID  Date       Description  Amount")
        for entry in self.entrys:
            print(f'{entry.getID()}   {entry.getDate()}  {entry.getDescription()}      ${entry.getAmount()}')

    def summary(self, month):
        sum = 0
        if month == 0:
            for entry in self.entrys:
                sum += entry.getAmount()
            sum = round(sum,2)
            print(f"Total expenses: ${sum}")

        elif month > 0 and month < 13:
            for entry in self.entrys:
                if entry.date.month == month:
                    sum += entry.getAmount()
            sum = round(sum,2)
            print(f"Total expenses for {datetime.date(1999, month, 1).strftime("%B")}: $ {sum}")

    def update_entry(self, id, flag, value):

        for i, entry in enumerate(self.entrys):
            if entry.getID() == id:
                if flag == "amount":
                    self.entrys[i].setAmount(value)
                    print(f"Amount from expense (ID: {id}) changed to {value}")
                if flag == "description":
                    self.entrys[i].setDescription(value)
                    print(f"Description from expense (ID: {id}) changed to {value}")



            



        



def command_add(args):
    #print("Add")

    amount = args.amount
    description = args.description
    tracker = args.tracker

    tracker.create_entry(amount, description)



    

def command_list(args):
    tracker = args.tracker
    tracker.list()
    


def command_delete(args):
    id = args.id
    tracker = args.tracker
   
    tracker.delete_entry(id)
    
def command_summary(args):
    month = args.month
    tracker.summary(month)

def command_update(args):
    id = args.id
    amount = args.amount
    description = args.description
    tracker = args.tracker

    if amount != False:
        tracker.update_entry(id, "amount", round(float(amount),2))
    
    if description != False:
        tracker.update_entry(id, "description", description)





"""

entrys = []
with open('data.csv', newline='') as csvfile:
    data_bank = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in data_bank:
        data = row[0].split(",")
        print(row)
        entry = Entry(data[0], data[1], data[2], float(data[3]))
        entrys.append(entry)
        

"""

tracker = Tracker('data.csv')

parser = argparse.ArgumentParser(prog="expense-tracker")
subparsers = parser.add_subparsers(help="IDK1")




add_sp = subparsers.add_parser("add", help="Add an Expense")
add_sp.add_argument("--description", "-d",type=str, help="Description for the Expense")
add_sp.add_argument("--amount", "-a", type=float,help="Set the amount of the Expense")
add_sp.set_defaults(cmd="add", func=command_add)
add_sp.set_defaults(tracker=tracker)


update_sp = subparsers.add_parser("update", help="Update an Expense")
update_sp.add_argument("--id", "-i", type=int,help="Which ID to Update")
update_sp.add_argument("--description", "-d",type=str, help="Update the Description for the Expense")
update_sp.add_argument("--amount", "-a", type=float,help="Update the amount of the Expense")
update_sp.set_defaults(cmd="update", func=command_update)
update_sp.set_defaults(tracker=tracker)
update_sp.set_defaults(description=False)
update_sp.set_defaults(amount=False)


list_sp = subparsers.add_parser("list", help="List all Expenses")
list_sp.set_defaults(tracker=tracker)
list_sp.set_defaults(cmd="list", func=command_list)

delete_sp = subparsers.add_parser("delete", help="Delete an Expense")
delete_sp.add_argument("--id", "-i", type=int,help="Which ID to delete")
delete_sp.set_defaults(tracker=tracker)
delete_sp.set_defaults(cmd="delete", func=command_delete)


summary_sp = subparsers.add_parser("summary", help="Summary all Expenses")
summary_sp.add_argument("--month", "-m", type=int,help="Which Month to Summerize")
summary_sp.set_defaults(tracker=tracker)
summary_sp.set_defaults(month=0)
summary_sp.set_defaults(cmd="summary", func=command_summary)



args = parser.parse_args()
if hasattr(args, 'func'):
    args.func(args)
else:
    parser.print_help()




"""
with open('data.csv', 'w', newline='') as f:
    f.truncate()
    writer = csv.writer(f)
    for entry in entrys:
        writer.writerow([entry.getID(), entry.getDate(), entry.getDescription(), entry.getAmount()])
"""

tracker.save()