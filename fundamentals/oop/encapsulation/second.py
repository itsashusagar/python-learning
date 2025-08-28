class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # private

    # Deposit money
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited {amount}. New balance: {self.__balance}")
        else:
            print("Deposit must be positive!")

    # Withdraw money
    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient funds!")
        elif amount <= 0:
            print("Invalid amount!")
        else:
            self.__balance -= amount
            print(f"Withdrew {amount}. New balance: {self.__balance}")

    # Getter for balance
    def get_balance(self):
        return self.__balance

account = BankAccount("Ashu", 1000)
account.deposit(500)
account.withdraw(800)  # Insufficient funds!
print(account.get_balance())  # 1500
