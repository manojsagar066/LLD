# design atm
# entities - atm, user, account, display, cash dispenser, card, bank service
# functionalities - show balance, withdraw, deposit cash
import uuid
from datetime import datetime


class Card:
    def __init__(self, card_number, expiry, pin, account):
        self.card_number = card_number
        self.expiry = expiry
        self.pin = pin
        self.account = account

    def validate_pin(self, input_pin):
        return self.pin == input_pin


class Account:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance
        self.transaction_history = []

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount >= self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, to_account, amount):
        if self.withdraw(amount):
            to_account.deposit(amount)
            return True
        return False


class Transaction:
    def __init__(self, amount):
        self.id = str(uuid.uuid4())
        self.amount = amount
        self.date = datetime.now()
        self.status = "Pending"

    def execute(self):
        pass


class BalanceInquiry(Transaction):
    def __init__(self, account):
        super().__init__(0)
        self.account = account

    def execute(self):
        self.status = "Success"
        return self.account.get_balance()


class CashWithdrawal(Transaction):
    def __init__(self, amount, account):
        super().__init__(amount)
        self.account = account

    def execute(self):
        if self.account.withdraw(self.amount):
            self.status = "Success"
            return True
        self.status = "Failed"
        return False


class CashDeposit(Transaction):
    def __init__(self, amount, account):
        super().__init__(amount)
        self.account = account

    def execute(self):
        self.account.deposit(self.amount)
        self.status = "Success"
        return True


class FundTransfer(Transaction):
    def __init__(self, from_account, to_account, amount):
        super().__init__(amount)
        self.from_account = from_account
        self.to_account = to_account

    def execute(self):
        if self.from_account.transer(self.to_account, self.amount):
            self.status = "Success"
            return True
        self.status = "Failed"
        return False


class BankService:
    def __init__(self):
        self.cards = {} # card_number: card

    def register_card(self, card):
        self.cards[card.card_number] = card

    def validate_card(self, card_number):
        return card_number in self.cards

    def validate_pin(self, card_number, pin):
        return self.cards[card_number].validate_pin(pin)

    def get_account(self, card_number):
        return self.cards[card_number].account


# components
class CashDispenser:
    def __init__(self, available_cash=100000):
        self.available_cash = available_cash

    def dispense(self, amount):
        if self.available_cash >= amount:
            self.available_cash -= amount
            return True
        return False

    def refill(self, amount):
        self.available_cash += amount


class CardReader:
    @staticmethod
    def read_card(card_number, bank_service):
        if bank_service.validate_card(card_number):
            return bank_service.cards[card_number]
        return None

    @staticmethod
    def eject():
        print("Card Ejected")


class Screen:
    @staticmethod
    def display(message):
        print(f"[SCREEN]: {message}")


class Keypad:
    @staticmethod
    def get_input(prompt="Enter input: "):
        return input(prompt)


class ATM:
    def __init__(self, bank_service):
        self.card_reader = CardReader()
        self.key_pad = Keypad()
        self.screen = Screen()
        self.cash_dispenser = CashDispenser()
        self.bank_service = bank_service
        self.current_card = None
        self.current_account = None

    def insert_card(self, card_number):
        self.current_card = self.card_reader.read_card(card_number, self.bank_service)
        if not self.current_card:
            self.screen.display("Invalid Card")
            return False
        self.screen.display("Card Inserted")
        return True

    def authenticate(self):
        pin = self.key_pad.get_input("Enter Pin: ")
        if not self.current_card.validate_pin(pin):
            self.screen.display("Invalid pin")
            return False
        self.screen.display("Authentication successful")
        self.current_account = self.current_card.account
        return True

    def show_menu(self):
        self.screen.display("1. Balance\n2. Withdraw\n3. Deposit\n4. Transfer\n5. Exit")

    def perform_transaction(self):
        while True:
            self.show_menu()
            choice = self.key_pad.get_input("Choose option: ")

            if choice == '1':
                tx = BalanceInquiry(self.current_account)
                balance = tx.execute()
                self.screen.display(f"Balance: ₹{balance}")

            elif choice == '2':
                amount = float(self.key_pad.get_input("Withdraw amount: "))
                tx = CashWithdrawal(amount, self.current_account)
                tx.execute()
                if tx.status == "Success" and self.cash_dispenser.dispense(amount):
                    self.screen.display("Withdrawal successful.")
                else:
                    self.screen.display("Withdrawal failed.")

            elif choice == '3':
                amount = float(self.key_pad.get_input("Deposit amount: "))
                tx = CashDeposit(amount, self.current_account)
                tx.execute()
                self.screen.display("Deposit successful.")

            elif choice == '4':
                to_card_number = self.key_pad.get_input("Enter recipient card number: ")
                amount = float(self.key_pad.get_input("Transfer amount: "))
                if not self.bank_service.validate_card(to_card_number):
                    self.screen.display("Invalid recipient.")
                    continue
                to_account = self.bank_service.get_account(to_card_number)
                tx = FundTransfer(self.current_account, to_account, amount)
                tx.execute()
                if tx.status == "Success":
                    self.screen.display("Transfer successful.")
                else:
                    self.screen.display("Transfer failed.")

            elif choice == '5':
                break
            else:
                self.screen.display("Invalid option.")

    def eject_card(self):
        self.card_reader.eject()
        self.current_card = None
        self.current_account = None


bank = BankService()

acc1 = Account("ACC123", 10000)
acc2 = Account("ACC999", 5000)

card1 = Card("CARD123", "12/26", "1234", acc1)
card2 = Card("CARD999", "01/27", "4321", acc2)

bank.register_card(card1)
bank.register_card(card2)

atm = ATM(bank)

if atm.insert_card("CARD123"):
    if atm.authenticate():
        atm.perform_transaction()
    atm.eject_card()
