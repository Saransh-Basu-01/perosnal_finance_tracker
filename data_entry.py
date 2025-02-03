from datetime import datetime
date_format="%d-%m-%Y"
CATEGORIES={
    "I":"income",
    "E":"expense"
}
def getdate(prompt,allow_default=False):
    date_str=input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    try:
        valid_date=datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format.Please enter the date in dd-mm-yyy format")
        return getdate(prompt,allow_default)
    

def get_amount():
    try:
        amount=float(input("enter the amount:"))
        if(amount<=0):
            raise ValueError("amount must be a non negative non zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    
def get_category():
    category=input("enter the category ('I' for income or 'E' for expense):").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Invalid Category")
    return get_category

def get_decription():
    return input("enter description:")