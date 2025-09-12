# E-Commerce Inventory Manager

**Developed by Payal Chaudhari**

This is a comprehensive inventory management system for e-commerce businesses. Originally built as a desktop GUI using Tkinter and MySQL, it has been adapted to a web app using Flask and Postgres for cloud deployment. The app allows users to manage stock (add, update, delete items), sales, shipping, and orders through an intuitive interface.

## Live Demo
The application is **live and running** on Render! Access it here:
- [https://e-commerce-inventory-manager.onrender.com/](https://e-commerce-inventory-manager.onrender.com/)

**Default Login Credentials**:
- Username: `admin`
- Password: `admin`

**Status**: Successfully deployed and operational. Login to manage your inventory.

## Features
- **Stock Management**: Add, update, delete items (name, price, quantity).
- **Sales Management**: Track sales (placeholder for future enhancements).
- **Shipping Management**: Handle shipping (placeholder for future enhancements).
- **Order Management**: Manage orders (placeholder for future enhancements).
- **Search Functionality**: Search items by name.
- **Database Integration**: Uses Postgres for persistent data storage.
- **Login System**: Secure login with hardcoded admin credentials (expandable for multiple users).

## How the App Works (Based on Code)
- **Login**: Users enter credentials to access the main dashboard (simulated check for "admin"/"admin").
- **Main Interface**: Uses a tabbed notebook for sections (Stock, Sales, Shipping, Orders).
- **Stock Operations**:
  - Add item: Insert into database via form.
  - Update/Delete: Modify or remove by ID.
  - Fetch/Search: Display all items or search by name in a scrollable list.
- **Database**: Connects to MySQL (local) or Postgres (Render) with functions like `connect_db()`, `add_item()`, `fetch_items()`, etc.
- **Error Handling**: Shows message boxes for success/errors.
- **GUI**: Built with Tkinter (desktop version); web version uses HTML forms with Flask routes.

## Installation (Local Desktop Version - Tkinter)
1. Clone the repository: 
git clone https://github.com/payalchaudhari8443/E-Commerce-Inventory-Manager.git
cd E-Commerce-Inventory-Manager
2. Set up MySQL database:
- Install MySQL and create `inventory_db` with table `items` (columns: `item_id`, `name`, `price`, `quantity`).
- Update `Project2(code).py` with your MySQL credentials (host="localhost", user="root", password="your_password").
3. Run the app:
