import tkinter as tk
from tkinter import ttk, messagebox
import uuid

# Dish Classes
class Dish:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    def __str__(self):
        return f"{self._name} - rs.{self._price:.2f}"

class Appetizer(Dish): pass
class MainCourse(Dish): pass
class Dessert(Dish): pass

# Menu Class
class Menu:
    def __init__(self):
        self._appetizers = []
        self._main_courses = []
        self._desserts = []

    def add_dish(self, category, dish):
        if category.lower() == "appetizer":
            self._appetizers.append(dish)
        elif category.lower() == "main":
            self._main_courses.append(dish)
        elif category.lower() == "dessert":
            self._desserts.append(dish)

    def get_menu_dict(self):
        return {
            "Appetizers": self._appetizers,
            "Main Courses": self._main_courses,
            "Desserts": self._desserts
        }

# Order Class
class Order:
    def __init__(self):
        self._items = []

    def add_item(self, dish):
        self._items.append(dish)

    def remove_item(self, dish_name):
        for dish in self._items:
            if dish.name.lower() == dish_name.lower():
                self._items.remove(dish)
                return True
        return False

    def calculate_total(self):
        return sum(dish.price for dish in self._items)

    def get_order_items(self):
        return self._items

    def clear_order(self):
        self._items.clear()

# Customer Class
class Customer:
    def __init__(self, name, contact):
        self._name = name
        self._contact = contact

    @property
    def name(self):
        return self._name

    @property
    def contact(self):
        return self._contact

# Billing Class
class Billing:
    def __init__(self, customer, order):
        self._customer = customer
        self._order = order
        self._invoice_id = str(uuid.uuid4())[:8]

    def generate_invoice(self):
        invoice = f"Invoice ID: {self._invoice_id}\n"
        invoice += f"Customer: {self._customer.name}\n"
        invoice += f"Contact: {self._customer.contact}\n"
        invoice += "\nItems:\n"
        for dish in self._order.get_order_items():
            invoice += f"- {dish.name}: rs.{dish.price:.2f}\n"
        invoice += f"\nTotal: rs.{self._order.calculate_total():.2f}\n"
        return invoice

    def save_invoice_to_file(self, invoice_text):
        try:
            with open("invoices.txt", "a") as file:
                file.write(invoice_text + "\n" + "-"*50 + "\n")
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to save invoice: {e}")

# GUI Application
class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Ordering System")
        self.root.geometry("800x600")

        self.menu = self.setup_menu()
        self.order = Order()
        self.customer = None

        self.create_widgets()

    def setup_menu(self):
        menu = Menu()
        # Appetizers
        menu.add_dish("appetizer", Appetizer("Spring Rolls", 500))
        menu.add_dish("appetizer", Appetizer("Garlic Bread", 400))
        menu.add_dish("appetizer", Appetizer("Chicken Wings", 600))
        menu.add_dish("appetizer", Appetizer("Spicy Chips", 200))
        menu.add_dish("appetizer", Appetizer("Stuffed Mushrooms", 300))
        # Main Courses
        menu.add_dish("main", MainCourse("Grilled Chicken", 1200))
        menu.add_dish("main", MainCourse("Pasta Alfredo", 1100))
        menu.add_dish("main", MainCourse("Beef Steak", 1500))
        menu.add_dish("main", MainCourse("Veggie Burger", 500))
        menu.add_dish("main", MainCourse("Fish and Chips", 1300))
        # Desserts
        menu.add_dish("dessert", Dessert("Cheesecake", 200.99))
        menu.add_dish("dessert", Dessert("Ice Cream", 300.99))
        menu.add_dish("dessert", Dessert("Brownie", 50.99))
        menu.add_dish("dessert", Dessert("Cupcake", 60.59))
        menu.add_dish("dessert", Dessert("Fruit Salad", 400.79))
        return menu

    def create_widgets(self):
        # Welcome
        welcome_label = ttk.Label(self.root, text="Namaste! Welcome to our Restaurant", font=("Helvetica", 16, "bold"))
        welcome_label.pack(pady=10)

        # Customer Entry
        customer_frame = ttk.Frame(self.root, padding=10)
        customer_frame.pack(fill=tk.X)

        ttk.Label(customer_frame, text="Name:").grid(row=0, column=0, padx=5)
        self.name_entry = ttk.Entry(customer_frame)
        self.name_entry.grid(row=0, column=1, padx=5)

        ttk.Label(customer_frame, text="Contact:").grid(row=0, column=2, padx=5)
        self.contact_entry = ttk.Entry(customer_frame)
        self.contact_entry.grid(row=0, column=3, padx=5)

        # Main Area
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Menu Tabs
        menu_notebook = ttk.Notebook(main_frame)
        menu_notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.menu_listboxes = {}
        for category, dishes in self.menu.get_menu_dict().items():
            frame = ttk.Frame(menu_notebook)
            menu_notebook.add(frame, text=category)
            listbox = tk.Listbox(frame, width=40)
            listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
            for dish in dishes:
                listbox.insert(tk.END, str(dish))
            self.menu_listboxes[category] = listbox

        ttk.Button(main_frame, text="Add to Order", command=self.add_to_order).pack(pady=5)

        # Order View
        order_frame = ttk.Frame(main_frame)
        order_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(order_frame, text="Your Order", font=("Arial", 14)).pack(pady=5)
        self.order_listbox = tk.Listbox(order_frame, width=40)
        self.order_listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        ttk.Button(order_frame, text="Remove Selected", command=self.remove_from_order).pack(pady=5)
        ttk.Button(order_frame, text="Checkout", command=self.checkout).pack(pady=5)
        ttk.Button(order_frame, text="Clear Order", command=self.clear_order).pack(pady=5)

        self.total_label = ttk.Label(order_frame, text="Total: rs.0.00", font=("Arial", 12))
        self.total_label.pack(pady=5)

    def add_to_order(self):
        try:
            for category, listbox in self.menu_listboxes.items():
                selected = listbox.curselection()
                if selected:
                    index = selected[0]
                    dish = self.menu.get_menu_dict()[category][index]
                    self.order.add_item(dish)
                    self.order_listbox.insert(tk.END, str(dish))
            self.update_total()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {e}")

    def remove_from_order(self):
        try:
            selected = self.order_listbox.curselection()
            for index in reversed(selected):
                dish_str = self.order_listbox.get(index)
                dish_name = dish_str.split(" - rs.")[0]
                if self.order.remove_item(dish_name):
                    self.order_listbox.delete(index)
            self.update_total()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove item: {e}")

    def clear_order(self):
        try:
            self.order.clear_order()
            self.order_listbox.delete(0, tk.END)
            self.update_total()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear order: {e}")

    def checkout(self):
        try:
            name = self.name_entry.get().strip()
            contact = self.contact_entry.get().strip()
            if not name or not contact:
                messagebox.showwarning("Missing Info", "Please enter name and contact.")
                return
            if not self.order.get_order_items():
                messagebox.showwarning("Empty Order", "Your order is empty.")
                return

            self.customer = Customer(name, contact)
            billing = Billing(self.customer, self.order)
            invoice = billing.generate_invoice()
            billing.save_invoice_to_file(invoice)
            messagebox.showinfo("Invoice", invoice)

            self.clear_order()
        except Exception as e:
            messagebox.showerror("Checkout Error", f"An error occurred during checkout: {e}")

    def update_total(self):
        try:
            total = self.order.calculate_total()
            self.total_label.config(text=f"Total: rs.{total:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update total: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()
