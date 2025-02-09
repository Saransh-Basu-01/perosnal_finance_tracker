import pandas as pd
import csv
from datetime import datetime
from data_entry import  get_amount,get_category,get_decription,getdate
import matplotlib.pyplot as plt
class CSV:
    CSV_FILE="finance_data.csv"
    COLUMNS=["date","amount","category","description"]
    FORMAT="%d-%m-%Y"
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df=pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE,index=False)
    @classmethod
    def add_entry(cls,date,amount,category,decription):
        new_entry={
            "date":date,
            "amount":amount,
            "category":category,
            "description":decription
        }
        with open(cls.CSV_FILE ,"a",newline="") as csvfile:
            writer=csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added sucessfully")
    @classmethod
    def get_transaction(cls,start_date,end_date):
        df=pd.read_csv(cls.CSV_FILE)
        df["date"]=pd.to_datetime(df["date"],format=CSV.FORMAT)
        start_date=datetime.strptime(start_date,CSV.FORMAT)
        end_date=datetime.strptime(end_date,CSV.FORMAT)

        mask=(df["date"]>=start_date) & (df["date"]<=end_date)
        filtered_df=df.loc[mask]
        if filtered_df.empty:
            print("no transaction found in the given date range")
        else:
            print(f"Trransaction from{start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False,formatters={"date":lambda x:x.strftime(CSV.FORMAT)}))

        total_income=filtered_df[filtered_df["category"]=="income"]["amount"].sum()
        total_expense= filtered_df[filtered_df["category"]=="expense"]["amount"].sum()
        print("\nSummary...")
        print(f"Total Income:${total_income:.2f}")                        
        print(f"Total expense:${total_expense:.2f}")    
        print(f"net_savings:${(total_income-total_expense):.2f}") 

def add():  
    CSV.initialize_csv()
    date=getdate("enter the date of the transaction(dd-mm-yyyy) or enter for today's date",allow_default=True)
    amount=get_amount()
    category=get_category()
    decription=get_decription()
    CSV.add_entry(date,amount,category,decription)

def plot_transaction(df):
    df.set_index('date',implace=True)
    income_df=df[df["category"]=="Income"].resample("D").sum().reindex(df.index,fill_value=0)
    expense_df=df[df["category"]=="Expense"].resample("D").sum().reindex(df.index,fill_value=0)
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df["amount"],label="Income",color="g")
    plt.plot(expense_df.index,expense_df["amount"],label="Expense",color="r")
    plt.xlabel("date")
    plt.ylabel("amount")
    plt.title("income and expense over time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1.Add a new transaction")
        print("2.View transactions and summary within a date range")
        print("3.exit")
        choice=input("enter your choice:")
        if(choice=="1"):
            add()
        elif(choice=="2"):
            start_date=getdate("enter the  start date(dd-mm-yyyy):")
            end_date=getdate("enter the  end date(dd-mm-yyyy):")
            df=CSV.get_transaction(start_date,end_date)
            if df is not None and not df.empty:  
                plot_choice = input("Do you want to see a plot? (y/n): ").lower()
                if plot_choice == 'y':
                    plot_transaction(df)  
            
        elif choice=="3":
            print("exiting.....")
            break
        else:
            print("invalid choice.")
if __name__=="__main__":
    main()