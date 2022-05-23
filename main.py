# Default Modules
import os
import json
import time
from typing import List

from sqlalchemy import false

# CLASSES 
class Account():
    ##Hesap classi
    def __init__(self, username : str, password : str, balance : int):
        self.username = username
        self.password = password
        self.balance = balance

    def withdrawMoney(self, amount : int):
        if(isinstance(amount, int)):
            if amount < 0:
                print("ERROR: Can't deposit negative amount")
                return -1
            elif self.balance - amount < 0:
                print("Not enough balance")
                return -1

            self.balance -= amount
            print("Transaction complete")

    def depositMoney(self, amount : int):
        if(isinstance(amount, int)):
            if amount < 0:
                print("ERROR: Can't deposit negative amount")
                return -1

            self.balance += amount
            print("Transaction complete")

    def loadBalance(self):
        print("Balance:", self.balance)

    def __str__(self) -> str:
        return f"Username: {self.username}, Balance: {self.balance}"

    def getJson(self):
        json_dict = {
            "username" : self.username,
            "password" : self.password,
            "balance" : self.balance
        }

        return json_dict

# Global
accounts : List[Account] = []
current_account : Account = None
clear = lambda: os.system('cls') # To clear console

# Methodlar
def loadAccounts():
    global accounts
    with open('accounts.json', 'r', encoding='utf-8') as f:
        account_data = json.load(f)
        for account in account_data["accounts"]:
            accounts.append(Account(account["username"], account["password"], account["balance"]))
    
    f.close()

def updateAccounts():

    account_jsons = [account.getJson() for account in accounts]

    with open('accounts.json', 'w', encoding='utf-8') as f:
        json.dump({"accounts" : account_jsons}, f, ensure_ascii= False, indent = 4)
    
    f.close()

def login() -> bool:
    ''' 
    Set the current_account to the account with the provided information 

    :return: Returns true if login is successful
    :rtype: bool
    '''       
    global current_account

    tries = 0
    while tries < 3:
        clear()
        print("ACCOUNT LOGIN")
        username = input("Username: ")
        password = input("Password: ")
        
        for account in accounts:
            if account.username == username and account.password == password:
                current_account = account
                return True
        
        tries += 1
        print("ERROR: Wrong username or password")
        time.sleep(1)
    
    return False


def isInputAcceptable(input : str, min_choice: int, max_choice : int):

    # Para yeterli mi
    try:
        choice = int(input)
        return choice >= min_choice and choice <= max_choice
    # Degilse hata
    except Exception as e:
        print("ERROR: isInputAcceptable: ", str(e))
        return false

def eftMoney(eft_to, amount):
    target = None
    for account in accounts:
        if account.username == eft_to:
            target = account
    
    if target != None:
        if current_account.withdrawMoney(amount) != -1:
            target.depositMoney(amount)

#UI
def userInterface()
    
    if login() == False:
        return

    while True:
        # Clear the console
        clear()
        
        print("BANK")
        print("(1) My Account")
        print("(2) Account actions")
        print("(3) Exit")
        
      
        choice = input("Choice: ")
        if isInputAcceptable(choice, 1, 3):

            choice = int(choice)

            # Clear the console
            clear()
            
            # Hesap
            if (choice == 1):
                print("MY ACCOUNT:")
                current_account.loadBalance()
           
            # -> Hesap aksiyonlari
            elif (choice == 2):
                # Secondary loop for the actions
                while True:
                    
                    # Clear the console
                    clear()

                    print("ACCOUNT ACTIONS")
                    print("(1) Deposit Money")
                    print("(2) Withdraw Money")
                    print("(3) EFT Money")
                    print("(4) Back")

                    choice = input("Choice: ")
                    if isInputAcceptable(choice, 1, 4):
                        # Type cast
                        choice = int(choice)

                        # Clear the console
                        clear()

                        # -> Deposit Money
                        if (choice == 1):
                            amount = int(input("Amount: "))
                            current_account.depositMoney(amount)
                        # _> Withdraw Money
                        elif (choice == 2):
                            amount = int(input("Amount: "))
                            current_account.withdrawMoney(amount)
                        # -> EFT Money
                        elif (choice == 3):
                            amount = int(input("Amount: "))
                            target = input("Target: ")
                            eftMoney(target, amount)
                        # -> Back
                        elif (choice == 4):
                            break
                
            # -> Exit
            elif (choice == 3):
                # Clear console
                clear()

                # Print books
                print("Books: ")
                for account in accounts:
                    print(account)
                

                break
            
            time.sleep(1)

    # Save accounts
    updateAccounts()
    return

if __name__ == "__main__":
    # Load accounts
    loadAccounts()

    # Init UI
    userInterface()