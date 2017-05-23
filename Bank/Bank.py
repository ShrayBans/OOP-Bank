import random

class MoneyMediator:
    def __init__(self):
        self.bank_accounts = []
        self.users = []

    def withdraw(self):
        if len(self.bank_accounts) < 1:
            print("Sorry you have no bank accounts!")
            return False

        # TODO: Implement withdraw functionality
        # for account in self.bank_accounts:
        #     if account.get_acct_num() == account_num:
        #         account.subtract_amount(amount)

    def add_user(self, user):
        self.users.append(user)
        if len(self.users) == 1:
            self.current_user = self.users[0]

    def check_interest(self):
        if len(self.bank_accounts) < 1:
            print("Sorry you have no bank accounts!")
            return False

        for account in self.bank_accounts:
            print("{}: {} dollars of interest".format(str(account), account.calculate_interest()))

    def switch_users(self):
        print("Your user is currently a(n) {}".format(str(self.current_user)))
        message = """

Which user would you like to be?
1 - Adult (More permissions)
2 - Child (Less permissions)
Input Number: """
        input_number = validateInputNumber(message, [1, 2])
        self.current_user = self.users[input_number - 1]
        print("You have switched your user to a(n) {}".format(str(self.current_user)))




class Teller(MoneyMediator):
    def __init__(self):
        super().__init__()

    def add_account(self):
        message = """

Which account would you like to open up?
1 - CD Account (More savings, less flexibility)
2 - Checkings Account (More flexibility, less savings)
3 - Savings Account (Moderate flexibility, moderate savings)
Input Number: """
        input_number = validateInputNumber(message, [1, 2, 3])
        input_amount = validatePositiveNumber("Please specify an amount you would like to start your account with: ")
        if input_number == 1:
            new_acc = CDAccount(input_amount, self)
            self.current_user.subtract_amount(input_amount)
            self.bank_accounts.append(new_acc)
        if input_number == 2:
            self.current_user.subtract_amount(input_amount)
            new_acc = CheckingsAccount(input_amount, self)
            self.bank_accounts.append(new_acc)
        if input_number == 3:
            self.current_user.subtract_amount(input_amount)
            new_acc = SavingsAccount(input_amount, self)
            self.bank_accounts.append(new_acc)

        print("You have added a new {}".format(str(new_acc)))

    def remove_account(self, account):
        self.bank_accounts.append(account)

    def deposit(self):
        if len(self.bank_accounts) < 1:
            print("Sorry you have no bank accounts!")
            return False

        print("Your bank accounts: ")
        for account in self.bank_accounts:
            print(str(account))


        notFound = True
        while notFound:
            account_num = validatePositiveNumber(
                "Please enter one of the account numbers that you would like to deposit money to: ")

            for account in self.bank_accounts:
                if account.get_acct_num() == account_num:
                    deposit_amount = validatePositiveNumber("Please specify an amount you would like to deposit: ")
                    account.add_amount(deposit_amount)
                    self.current_user.subtract_amount(deposit_amount)
                    print("{} has been deposited to Account #{} to make the total {}".format(deposit_amount, account_num, account.get_amount()))
                    notFound = False


    def ask_bank_info(self):
        message = '''
What would you like to learn about today?
1 - How can I deposit money into an account?
Input Number: '''
        input_number = validateInputNumber(message, [1])
        if input_number == 1:
            print("First you must add an account. Then, you can see me to deposit some money into that account.")

    def ask_general_info(self):
        message = '''

Hello! What would you like to do today?
1 - Add Account
2 - Withdraw Money From Account ** TODO **
3 - Deposit Money To Account
4 - Check Accrued Interest of Accounts
5 - Ask For Bank Information ** IN PROGRESS **
6 - Switch Users
7 - Leave Bank (Exit Program)
Input Number: '''
        input_number = validateInputNumber(message, [1, 2, 3, 4, 5, 6])
        if input_number == 1:
            Teller.add_account(self)
        if input_number == 2:
            Teller.withdraw(self)
        if input_number == 3:
            Teller.deposit(self)
        if input_number == 4:
            Teller.check_interest(self)
        if input_number == 5:
            Teller.ask_bank_info(self)
        if input_number == 6:
            Teller.switch_users(self)
        if input_number == 7:
            exit()

def validateInputNumber(inputNumMessage, possible_nums):
    while True:
        try:
            userInput = int(input(inputNumMessage))
        except ValueError:
            print("This is not a number!")
            continue

        if userInput in possible_nums:
            return userInput
        else:
            print("Sorry! Not a valid option!")
            continue

def validatePositiveNumber(inputNumMessage):
    while True:
        try:
            userInput = int(input(inputNumMessage))
        except ValueError:
            print("This is not a number!")
            continue

        if userInput >= 0:
            return userInput
        else:
            print("Sorry! Not a positive number! Try again!")
            continue


class User:
    def __init__(self, teller):
        self._teller = teller
        self.cash_balance = 10000

    def __str__(self):
        return "{} with {} dollars".format(self._type, self.cash_balance)

    def subtract_amount(self, amount):
        self.cash_balance -= amount
        print("User now has {} dollars".format(self.cash_balance))

    def add_amount(self, amount):
        self.cash_balance += amount
        print("User now has {} dollars").format(self.cash_balance)

class Adult(User):
    def __init__(self, teller):
        super().__init__(teller)
        self._type = "adult"

class Child(User):
    def __init__(self, teller):
        super().__init__(teller)
        self._type = "child"




class BankAccount:
    def __init__(self, init_amount, teller):
        self._teller = teller
        self._account_balance = init_amount
        self._account_num = random.randint(1, 1000)

    def get_acct_num(self):
        return self._account_num

    def get_amount(self):
        return self._account_balance

    def subtract_amount(self, amount):
        self._account_balance -= amount
        return self._account_balance

    def add_amount(self, amount):
        self._account_balance += amount
        return self._account_balance

    # TODO: need to factor in time into the calculation
    def calculate_interest(self):
        return self.interest_rate * self._account_balance

class CDAccount(BankAccount):
    def __init__(self, init_amount, teller):
        super().__init__(init_amount, teller)
        self.interest_rate = 0.05

    def __str__(self):
        return "CD Account #{} - {} dollar balance".format(self._account_num, self._account_balance)

class SavingsAccount(BankAccount):
    def __init__(self, init_amount, teller):
        super().__init__(init_amount, teller)
        self.interest_rate = 0.02

    def __str__(self):
        return "Savings Account #{} - {} dollar balance".format(self._account_num, self._account_balance)

class CheckingsAccount(BankAccount):
    def __init__(self, init_amount, teller):
        super().__init__(init_amount, teller)
        self.interest_rate = 0.005

    def __str__(self):
        return "Checkings Account #{} - {} dollar balance".format(self._account_num, self._account_balance)





def main():
    print("Welcome to the Bank of Shray!")
    # INIT teller
    teller = Teller()

    # INIT Users and establish adult as first user
    adult = Adult(teller)
    child = Adult(teller)
    teller.add_user(adult)
    teller.add_user(child)

    while True:
        teller.ask_general_info()



if __name__ == "__main__":
    main()