import os
from dataclasses import dataclass
from typing import Dict, List, Optional


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


@dataclass
class MenuItem:
    id: int
    name: str
    price: float
    category: str


@dataclass
class CartItem:
    item: MenuItem
    quantity: int

    @property
    def subtotal(self) -> float:
        return self.item.price * self.quantity


@dataclass
class Order:
    id: int
    items: List[CartItem]
    customer_name: str

    @property
    def total(self) -> float:
        return sum(ci.subtotal for ci in self.items)


class Menu:
    def __init__(self):
        self.items: Dict[int, MenuItem] = {}
        self._next_id = 1
        self._load_defaults()

    def _load_defaults(self):
        defaults = [
            ("Zinger Burger", 450.0, "Fast Food"),
            ("Chicken Biryani", 350.0, "Rice"),
            ("Mutton Curry", 900.0, "Curry"),
            ("Club Sandwich", 400.0, "Fast Food"),
            ("Chicken Shawarma", 250.0, "Fast Food"),
            ("Vegetable Pulao", 300.0, "Rice"),
            ("Chicken Tikka", 500.0, "BBQ"),
            ("Soft Drink", 100.0, "Beverage"),
            ("Fresh Lime", 150.0, "Beverage"),
            ("Chocolate Lava Cake", 350.0, "Dessert"),
        ]
        for name, price, category in defaults:
            self.add_item(name, price, category)

    def add_item(self, name: str, price: float, category: str) -> MenuItem:
        item = MenuItem(self._next_id, name, price, category)
        self.items[item.id] = item
        self._next_id += 1
        return item

    def remove_item(self, item_id: int) -> bool:
        return self.items.pop(item_id, None) is not None

    def get_item(self, item_id: int) -> Optional[MenuItem]:
        return self.items.get(item_id)

    def by_category(self) -> Dict[str, List[MenuItem]]:
        grouped: Dict[str, List[MenuItem]] = {}
        for item in self.items.values():
            grouped.setdefault(item.category, []).append(item)
        return grouped


class Cart:
    def __init__(self):
        self.entries: Dict[int, CartItem] = {}

    def add(self, item: MenuItem, quantity: int = 1):
        if item.id in self.entries:
            self.entries[item.id].quantity += quantity
        else:
            self.entries[item.id] = CartItem(item, quantity)

    def remove(self, item_id: int) -> bool:
        return self.entries.pop(item_id, None) is not None

    def update_quantity(self, item_id: int, quantity: int) -> bool:
        if item_id not in self.entries:
            return False
        if quantity <= 0:
            del self.entries[item_id]
        else:
            self.entries[item_id].quantity = quantity
        return True

    def total(self) -> float:
        return sum(ci.subtotal for ci in self.entries.values())

    def is_empty(self) -> bool:
        return len(self.entries) == 0

    def clear(self):
        self.entries.clear()


class OrderManager:
    def __init__(self):
        self.orders: List[Order] = []
        self._next_id = 1

    def place_order(self, cart: Cart, customer_name: str) -> Order:
        order = Order(self._next_id, list(cart.entries.values()), customer_name)
        self.orders.append(order)
        self._next_id += 1
        cart.clear()
        return order

    def get_order(self, order_id: int) -> Optional[Order]:
        for order in self.orders:
            if order.id == order_id:
                return order
        return None


class FoodOrderingApp:
    def __init__(self):
        self.menu = Menu()
        self.cart = Cart()
        self.order_manager = OrderManager()

    def run(self):
        clear_screen()
        print("=" * 40)
        print("   ONLINE FOOD ORDERING SYSTEM")
        print("=" * 40)
        while True:
            self._show_main_menu()
            choice = input("Choose an option: ").strip()
            clear_screen()
            if choice == "1":
                self._show_menu()
            elif choice == "2":
                self._add_to_cart()
            elif choice == "3":
                self._view_cart()
            elif choice == "4":
                self._remove_from_cart()
            elif choice == "5":
                self._checkout()
            elif choice == "6":
                print("Thank you for visiting!")
                break
            else:
                print("Invalid option, try again.")

            input("\nPress Enter to continue...")
            clear_screen()

    def _show_main_menu(self):
        print("\n1. View Menu")
        print("2. Add Item to Cart")
        print("3. View Cart")
        print("4. Remove Item from Cart")
        print("5. Checkout")
        print("6. Exit")

    def _show_menu(self):
        print("\n--- MENU ---")
        for category, items in self.menu.by_category().items():
            print(f"\n{category}")
            for item in items:
                print(f"  [{item.id}] {item.name:<25} Rs. {item.price:.2f}")

    def _add_to_cart(self):
        self._show_menu()
        try:
            item_id = int(input("\nEnter item ID to add: ").strip())
            item = self.menu.get_item(item_id)
            if not item:
                print("Item not found.")
                return
            quantity = int(input("Enter quantity: ").strip())
            if quantity <= 0:
                print("Quantity must be positive.")
                return
            self.cart.add(item, quantity)
            print(f"Added {quantity} x {item.name} to cart.")
        except ValueError:
            print("Invalid input.")

    def _view_cart(self):
        if self.cart.is_empty():
            print("\nYour cart is empty.")
            return
        print("\n--- CART ---")
        for ci in self.cart.entries.values():
            print(f"  {ci.item.name:<25} x{ci.quantity:<3} Rs. {ci.subtotal:.2f}")
        print(f"\nTotal: Rs. {self.cart.total():.2f}")

    def _remove_from_cart(self):
        self._view_cart()
        if self.cart.is_empty():
            return
        try:
            item_id = int(input("\nEnter item ID to remove: ").strip())
            if self.cart.remove(item_id):
                print("Item removed.")
            else:
                print("Item not in cart.")
        except ValueError:
            print("Invalid input.")

    def _checkout(self):
        if self.cart.is_empty():
            print("\nYour cart is empty. Add items before checkout.")
            return
        self._view_cart()
        confirm = input("\nConfirm order? (y/n): ").strip().lower()
        if confirm != "y":
            print("Order cancelled.")
            return
        name = input("Enter your name: ").strip() or "Guest"
        order = self.order_manager.place_order(self.cart, name)
        print(f"\nOrder #{order.id} placed successfully!")
        print(f"Customer: {order.customer_name}")
        for ci in order.items:
            print(f"  {ci.item.name:<25} x{ci.quantity:<3} Rs. {ci.subtotal:.2f}")
        print(f"Total: Rs. {order.total:.2f}")


if __name__ == "__main__":
    app = FoodOrderingApp()
    app.run()