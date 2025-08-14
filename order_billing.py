# Menu, FoodItem, Order, Bill
from typing import Dict


class FoodItem:
    def __init__(self, item_id: str, name: str, price: float, category: str):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.category = category


# singleton class
class Menu:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.menu = {}  # {food_item_id: FoodItem}
        return cls._instance

    def add_food_item(self, food_item: FoodItem):
        self.menu[food_item.item_id] = food_item

    def view_menu(self):
        items_list = []
        for id, food_item in self.menu.items():
            items_list.append({
                "id": id,
                "name": food_item.name,
                "price": food_item.price
            })
        return items_list

    def get_item(self, food_item_id):
        return self.menu[food_item_id]


class OrderItem:
    def __init__(self, item: FoodItem, quantity: int, price: float):
        self.item = item
        self.quantity = quantity
        self.price = price


# order(one) -> OrderItem(many)
class Order:
    def __init__(self):
        self._items: Dict[str, OrderItem] = {}
        self._total_price = 0

    def add_item(self, food_item: FoodItem, quantity: int):
        price = food_item.price * quantity
        order_item = OrderItem(food_item, quantity, price)
        self._items[food_item.item_id] = order_item
        self._total_price += price

    def remove_item(self, food_item: FoodItem):
        if food_item.item_id in self._items:
            self._total_price -= self._items[food_item.item_id].price
            del self._items[food_item.item_id]

    def show_order_summary(self):
        for item_id, order_item in self._items.items():
            print(f"{order_item.item.name} * {order_item.quantity} = {order_item.price}")
        print(f"---------------------")
        print(f"Total = {self._total_price}\n")

    @property
    def total_price(self):
        return self._total_price


class Bill:
    def __init__(self, order: Order):
        self.order = order

    def print_bill(self):
        self.order.show_order_summary()


class OrderManager:
    def __init__(self):
        self.menu = Menu()
        self.order = Order()

    def perform_action(self):
        while True:
            print(f"1. show menu \t 2. add item \t 3. order summary 4. order food")
            user_input = input("Enter your choice: ")
            if user_input == "1":
                print(self.menu.view_menu())
                continue
            elif user_input == "2":
                item_id = input("Enter food_item id: ")
                quantity = int(input("Enter quantity: "))
                food_item = self.menu.get_item(item_id)
                self.order.add_item(food_item, quantity)
                continue
            elif user_input == "3":
                bill = Bill(self.order)
                bill.print_bill()
            elif user_input == "4":
                print(f"Please pay {self.order.total_price}")
                break
            else:
                print("Invalid choice")
                break


menu = Menu()

food_item1 = FoodItem("1", "Idly", 50, "Breakfast")
food_item2 = FoodItem("2", "Dosa", 70, "Breakfast")

menu.add_food_item(food_item1)
menu.add_food_item(food_item2)

order_manager = OrderManager()
order_manager.perform_action()
