#user_id  "admin" and password "admin"
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from tkinter import Scrollbar, Canvas, Frame


def connect_db():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Payal@7137",
        database="inventory_db"
    )


def login():
    """Check credentials and open main window if correct."""
    user_id = entry_user_id.get()
    password = entry_password.get()

    # Simulate credential check (replace with real authentication if needed)
    if user_id == "admin" and password == "admin":
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Error", "Invalid ID or Password")


def open_main_window():
    """Set up and open the main application window."""
    global app

    app = tk.Tk()
    app.title("E-Commerce Inventory Manager")

    # Create a notebook widget for different sections
    notebook = ttk.Notebook(app)
    notebook.pack(fill='both', expand=True)

    # Create frames for each section
    frame_stock = tk.Frame(notebook)
    frame_selling = tk.Frame(notebook)
    frame_shipping = tk.Frame(notebook)
    frame_orders = tk.Frame(notebook)

    notebook.add(frame_stock, text="Stock Management")
    notebook.add(frame_selling, text="Sales Management")
    notebook.add(frame_shipping, text="Shipping Management")
    notebook.add(frame_orders, text="Order Management")

    # Populate Stock Management frame
    populate_stock_management(frame_stock)

    # Populate Sales Management frame
    populate_selling_frame(frame_selling)

    # Populate Shipping Management frame
    populate_shipping_frame(frame_shipping)

    # Populate Order Management frame
    populate_orders_frame(frame_orders)

    app.mainloop()


def populate_stock_management(frame):
    """Populate the Stock Management frame with widgets."""
    tk.Label(frame, text="Manage Stock").pack(pady=10)

    # Stock Management controls
    tk.Label(frame, text="Item ID").pack(pady=5)
    entry_item_id = tk.Entry(frame)
    entry_item_id.pack(pady=5)

    tk.Label(frame, text="Item Name").pack(pady=5)
    entry_name = tk.Entry(frame)
    entry_name.pack(pady=5)

    tk.Label(frame, text="Price").pack(pady=5)
    entry_price = tk.Entry(frame)
    entry_price.pack(pady=5)

    tk.Label(frame, text="Quantity").pack(pady=5)
    entry_quantity = tk.Entry(frame)
    entry_quantity.pack(pady=5)

    tk.Button(frame, text="Add Item", command=lambda: add_item(entry_name, entry_price, entry_quantity)).pack(pady=5)
    tk.Button(frame, text="Update Item",
              command=lambda: update_item(entry_item_id, entry_name, entry_price, entry_quantity)).pack(pady=5)
    tk.Button(frame, text="Delete Item", command=lambda: delete_item(entry_item_id)).pack(pady=5)
    tk.Button(frame, text="Fetch Items", command=fetch_items).pack(pady=5)

    # Search functionality
    tk.Label(frame, text="Search by Name").pack(pady=5)
    entry_search = tk.Entry(frame)
    entry_search.pack(pady=5)
    tk.Button(frame, text="Search", command=lambda: search_items(entry_search)).pack(pady=5)

    # Create a frame for the listbox with a scrollbar
    frame_list = tk.Frame(frame)
    frame_list.pack(fill=tk.BOTH, expand=True)

    canvas = Canvas(frame_list)
    scrollbar = Scrollbar(frame_list, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a scrollable frame inside the canvas
    scrollable_frame = Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Listbox to display fetched items
    global listbox_items
    listbox_items = tk.Listbox(scrollable_frame, width=80, height=20)
    listbox_items.pack()


def populate_selling_frame(frame):
    """Populate the Sales Management frame with widgets."""
    tk.Label(frame, text="Sales Overview").pack(pady=10)
    # Add widgets related to selling here
    tk.Label(frame, text="Selling functionality coming soon...").pack(pady=10)


def populate_shipping_frame(frame):
    """Populate the Shipping Management frame with widgets."""
    tk.Label(frame, text="Shipping Overview").pack(pady=10)
    # Add widgets related to shipping here
    tk.Label(frame, text="Shipping functionality coming soon...").pack(pady=10)


def populate_orders_frame(frame):
    """Populate the Order Management frame with widgets."""
    tk.Label(frame, text="Order Management").pack(pady=10)
    # Add widgets related to orders here
    tk.Label(frame, text="Order management functionality coming soon...").pack(pady=10)


def add_item(name_entry, price_entry, quantity_entry):
    """Add a new item to the database."""
    name = name_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    if name and price and quantity:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO items (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Item added successfully")
            clear_entries(name_entry, price_entry, quantity_entry)
            fetch_items()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")


def fetch_items():
    """Fetch and display all items from the database."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        rows = cursor.fetchall()
        conn.close()

        listbox_items.delete(0, tk.END)
        for row in rows:
            listbox_items.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Price: ₹{row[2]:.2f}, Quantity: {row[3]}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def search_items(entry_search):
    """Search for items by name."""
    name = entry_search.get()
    if name:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM items WHERE name LIKE %s", ('%' + name + '%',))
            rows = cursor.fetchall()
            conn.close()

            listbox_items.delete(0, tk.END)
            for row in rows:
                listbox_items.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Price: ₹{row[2]:.2f}, Quantity: {row[3]}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please enter a search term")


def update_item(id_entry, name_entry, price_entry, quantity_entry):
    """Update an existing item in the database."""
    item_id = id_entry.get()
    name = name_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    if item_id and name and price and quantity:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE items SET name=%s, price=%s, quantity=%s WHERE item_id=%s",
                           (name, price, quantity, item_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Item updated successfully")
            clear_entries(name_entry, price_entry, quantity_entry)
            fetch_items()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")


def delete_item(id_entry):
    """Delete an item from the database."""
    item_id = id_entry.get()

    if item_id:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE item_id=%s", (item_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Item deleted successfully")
            clear_entries(id_entry)
            fetch_items()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please enter item ID")


def clear_entries(*entries):
    """Clear all input fields."""
    for entry in entries:
        entry.delete(0, tk.END)


# Set up the login window
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="User ID").grid(row=0, column=0, padx=5, pady=5)
entry_user_id = tk.Entry(login_window)
entry_user_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(login_window, text="Password").grid(row=1, column=0, padx=5, pady=5)
entry_password = tk.Entry(login_window, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5)

tk.Button(login_window, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)

login_window.mainloop()
