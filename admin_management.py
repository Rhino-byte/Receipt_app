import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import hashlib
from datetime import datetime

class StaffManagement:
    def __init__(self, parent, db_name):
        self.parent = parent
        self.db_name = db_name
        self.create_staff_management_window()
    
    def create_staff_management_window(self):
        """Create staff management window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Staff Management - Merry Mary Restaurant")
        self.window.geometry("800x600")
        self.window.configure(bg='#1a1a1a')
        
        # Header
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Staff Management", font=('Arial', 18, 'bold'), 
                bg='#2c3e50', fg='white').pack(expand=True)
        
        # Main content
        main_frame = tk.Frame(self.window, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left panel - Add/Edit Staff
        left_panel = tk.Frame(main_frame, bg='#2d2d2d')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Add Staff section
        add_frame = tk.LabelFrame(left_panel, text="Add New Staff", font=('Arial', 12, 'bold'), 
                                 bg='#2d2d2d', fg='#ffffff')
        add_frame.pack(fill='x', pady=10)
        
        # Username
        tk.Label(add_frame, text="Username:", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        self.username_var = tk.StringVar()
        username_entry = tk.Entry(add_frame, textvariable=self.username_var, 
                                 font=('Arial', 10), bg='#3d3d3d', fg='#ffffff',
                                 insertbackground='#ffffff', relief='flat')
        username_entry.pack(fill='x', padx=10, pady=5)
        
        # Full Name
        tk.Label(add_frame, text="Full Name:", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        self.fullname_var = tk.StringVar()
        fullname_entry = tk.Entry(add_frame, textvariable=self.fullname_var, 
                                 font=('Arial', 10), bg='#3d3d3d', fg='#ffffff',
                                 insertbackground='#ffffff', relief='flat')
        fullname_entry.pack(fill='x', padx=10, pady=5)
        
        # PIN
        tk.Label(add_frame, text="PIN:", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        self.pin_var = tk.StringVar()
        pin_entry = tk.Entry(add_frame, textvariable=self.pin_var, 
                            font=('Arial', 10), bg='#3d3d3d', fg='#ffffff',
                            insertbackground='#ffffff', relief='flat', show='*')
        pin_entry.pack(fill='x', padx=10, pady=5)
        
        # User Type
        tk.Label(add_frame, text="User Type:", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        self.usertype_var = tk.StringVar(value="staff")
        usertype_combo = ttk.Combobox(add_frame, textvariable=self.usertype_var, 
                                     values=["staff", "admin"], state='readonly', font=('Arial', 10))
        usertype_combo.pack(fill='x', padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(add_frame, bg='#2d2d2d')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(button_frame, text="Add Staff", command=self.add_staff,
                 font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                 relief='flat', padx=20, pady=5).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Clear", command=self.clear_form,
                 font=('Arial', 10, 'bold'), bg='#95a5a6', fg='white',
                 relief='flat', padx=20, pady=5).pack(side='left', padx=5)
        
        # Right panel - Staff List
        right_panel = tk.Frame(main_frame, bg='#2d2d2d')
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Staff List section
        list_frame = tk.LabelFrame(right_panel, text="Staff List", font=('Arial', 12, 'bold'), 
                                  bg='#2d2d2d', fg='#ffffff')
        list_frame.pack(fill='both', expand=True, pady=10)
        
        # Staff listbox
        self.staff_listbox = tk.Listbox(list_frame, font=('Arial', 10), bg='#3d3d3d', fg='#ffffff')
        self.staff_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        self.staff_listbox.bind('<Double-Button-1>', self.edit_staff)
        
        # Action buttons
        action_frame = tk.Frame(list_frame, bg='#2d2d2d')
        action_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(action_frame, text="Edit Staff", command=self.edit_staff,
                 font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="Delete Staff", command=self.delete_staff,
                 font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="Refresh", command=self.load_staff,
                 font=('Arial', 10, 'bold'), bg='#f39c12', fg='white',
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        # Load staff list
        self.load_staff()
    
    def add_staff(self):
        """Add new staff member"""
        username = self.username_var.get().strip()
        fullname = self.fullname_var.get().strip()
        pin = self.pin_var.get().strip()
        usertype = self.usertype_var.get()
        
        if not all([username, fullname, pin]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        if len(pin) < 4:
            messagebox.showerror("Error", "PIN must be at least 4 characters!")
            return
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already exists!")
            conn.close()
            return
        
        # Hash the PIN
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
        
        # Insert new staff
        cursor.execute('''
            INSERT INTO users (username, pin, user_type, full_name, created_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, hashed_pin, usertype, fullname, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Staff member {fullname} added successfully!")
        self.clear_form()
        self.load_staff()
    
    def clear_form(self):
        """Clear the form"""
        self.username_var.set("")
        self.fullname_var.set("")
        self.pin_var.set("")
        self.usertype_var.set("staff")
    
    def load_staff(self):
        """Load staff list"""
        self.staff_listbox.delete(0, tk.END)
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT username, full_name, user_type FROM users ORDER BY full_name")
        staff = cursor.fetchall()
        conn.close()
        
        for username, fullname, usertype in staff:
            self.staff_listbox.insert(tk.END, f"{fullname} ({username}) - {usertype}")
    
    def edit_staff(self, event=None):
        """Edit selected staff member"""
        selection = self.staff_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a staff member to edit!")
            return
        
        # Get selected staff
        selected_text = self.staff_listbox.get(selection[0])
        username = selected_text.split("(")[1].split(")")[0]
        
        # Load staff details
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        staff = cursor.fetchone()
        conn.close()
        
        if staff:
            self.show_edit_dialog(staff)
    
    def show_edit_dialog(self, staff):
        """Show edit dialog for staff"""
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Edit Staff Member")
        edit_window.geometry("400x300")
        edit_window.configure(bg='#2d2d2d')
        
        # Form fields
        tk.Label(edit_window, text="Edit Staff Member", font=('Arial', 14, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(pady=10)
        
        # Username (read-only)
        tk.Label(edit_window, text=f"Username: {staff[1]}", font=('Arial', 10), 
                bg='#2d2d2d', fg='#ffffff').pack(pady=5)
        
        # Full Name
        tk.Label(edit_window, text="Full Name:", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=20, pady=5)
        fullname_var = tk.StringVar(value=staff[4])
        fullname_entry = tk.Entry(edit_window, textvariable=fullname_var, 
                                 font=('Arial', 10), bg='#3d3d3d', fg='#ffffff',
                                 insertbackground='#ffffff', relief='flat')
        fullname_entry.pack(fill='x', padx=20, pady=5)
        
        # New PIN
        tk.Label(edit_window, text="New PIN (leave blank to keep current):", 
                font=('Arial', 10, 'bold'), bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=20, pady=5)
        pin_var = tk.StringVar()
        pin_entry = tk.Entry(edit_window, textvariable=pin_var, 
                            font=('Arial', 10), bg='#3d3d3d', fg='#ffffff',
                            insertbackground='#ffffff', relief='flat', show='*')
        pin_entry.pack(fill='x', padx=20, pady=5)
        
        # User Type
        tk.Label(edit_window, text="User Type:", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=20, pady=5)
        usertype_var = tk.StringVar(value=staff[3])
        usertype_combo = ttk.Combobox(edit_window, textvariable=usertype_var, 
                                     values=["staff", "admin"], state='readonly', font=('Arial', 10))
        usertype_combo.pack(fill='x', padx=20, pady=5)
        
        def save_changes():
            new_fullname = fullname_var.get().strip()
            new_pin = pin_var.get().strip()
            new_usertype = usertype_var.get()
            
            if not new_fullname:
                messagebox.showerror("Error", "Full name cannot be empty!")
                return
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            if new_pin:
                if len(new_pin) < 4:
                    messagebox.showerror("Error", "PIN must be at least 4 characters!")
                    conn.close()
                    return
                hashed_pin = hashlib.sha256(new_pin.encode()).hexdigest()
                cursor.execute('''
                    UPDATE users SET full_name = ?, pin = ?, user_type = ? WHERE username = ?
                ''', (new_fullname, hashed_pin, new_usertype, staff[1]))
            else:
                cursor.execute('''
                    UPDATE users SET full_name = ?, user_type = ? WHERE username = ?
                ''', (new_fullname, new_usertype, staff[1]))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Staff member updated successfully!")
            edit_window.destroy()
            self.load_staff()
        
        # Save button
        tk.Button(edit_window, text="Save Changes", command=save_changes,
                 font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                 relief='flat', padx=20, pady=5).pack(pady=20)
    
    def delete_staff(self):
        """Delete selected staff member"""
        selection = self.staff_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a staff member to delete!")
            return
        
        selected_text = self.staff_listbox.get(selection[0])
        username = selected_text.split("(")[1].split(")")[0]
        
        if username == 'admin':
            messagebox.showerror("Error", "Cannot delete the admin user!")
            return
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {selected_text}?"):
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Staff member deleted successfully!")
            self.load_staff()

class ItemManagement:
    def __init__(self, parent, db_name):
        self.parent = parent
        self.db_name = db_name
        self.create_item_management_window()
    
    def create_item_management_window(self):
        """Create item management window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Item Management - Merry Mary Restaurant")
        self.window.geometry("1000x700")
        self.window.configure(bg='#1a1a1a')
        
        # Header
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Item Management", font=('Arial', 18, 'bold'), 
                bg='#2c3e50', fg='white').pack(expand=True)
        
        # Main content
        main_frame = tk.Frame(self.window, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left panel - Add/Edit Items
        left_panel = tk.Frame(main_frame, bg='#2d2d2d')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Add Item section
        add_frame = tk.LabelFrame(left_panel, text="Add New Item", font=('Arial', 12, 'bold'), 
                                 bg='#2d2d2d', fg='#ffffff')
        add_frame.pack(fill='x', pady=10)
        
        # Item Name
        tk.Label(add_frame, text="Item Name:", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        self.itemname_var = tk.StringVar()
        itemname_entry = tk.Entry(add_frame, textvariable=self.itemname_var, 
                                 font=('Arial', 10), bg='#3d3d3d', fg='#ffffff',
                                 insertbackground='#ffffff', relief='flat')
        itemname_entry.pack(fill='x', padx=10, pady=5)
        
        # Category
        tk.Label(add_frame, text="Category:", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(add_frame, textvariable=self.category_var, 
                                     values=["Snacks", "Food", "Kuku", "Drinks"], state='readonly', 
                                     font=('Arial', 10))
        category_combo.pack(fill='x', padx=10, pady=5)
        
        # Price
        tk.Label(add_frame, text="Price (KES):", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        self.price_var = tk.StringVar()
        price_entry = tk.Entry(add_frame, textvariable=self.price_var, 
                              font=('Arial', 10), bg='#3d3d3d', fg='#ffffff',
                              insertbackground='#ffffff', relief='flat')
        price_entry.pack(fill='x', padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(add_frame, bg='#2d2d2d')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(button_frame, text="Add Item", command=self.add_item,
                 font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                 relief='flat', padx=20, pady=5).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Clear", command=self.clear_form,
                 font=('Arial', 10, 'bold'), bg='#95a5a6', fg='white',
                 relief='flat', padx=20, pady=5).pack(side='left', padx=5)
        
        # Right panel - Items List
        right_panel = tk.Frame(main_frame, bg='#2d2d2d')
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Items List section
        list_frame = tk.LabelFrame(right_panel, text="Items List", font=('Arial', 12, 'bold'), 
                                  bg='#2d2d2d', fg='#ffffff')
        list_frame.pack(fill='both', expand=True, pady=10)
        
        # Items treeview
        columns = ('Name', 'Category', 'Price')
        self.items_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=150)
        
        self.items_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.items_tree.bind('<Double-Button-1>', self.edit_item)
        
        # Action buttons
        action_frame = tk.Frame(list_frame, bg='#2d2d2d')
        action_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(action_frame, text="Edit Item", command=self.edit_item,
                 font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="Delete Item", command=self.delete_item,
                 font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="Refresh", command=self.load_items,
                 font=('Arial', 10, 'bold'), bg='#f39c12', fg='white',
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        # Load items
        self.load_items()
    
    def add_item(self):
        """Add new item"""
        name = self.itemname_var.get().strip()
        category = self.category_var.get()
        price = self.price_var.get().strip()
        
        if not all([name, category, price]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        try:
            price = float(price)
            if price < 0:
                messagebox.showerror("Error", "Price cannot be negative!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid price!")
            return
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Check if item already exists
        cursor.execute("SELECT * FROM items WHERE name = ?", (name,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Item already exists!")
            conn.close()
            return
        
        # Insert new item
        cursor.execute('''
            INSERT INTO items (name, category, price, created_date)
            VALUES (?, ?, ?, ?)
        ''', (name, category, price, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Item {name} added successfully!")
        self.clear_form()
        self.load_items()
    
    def clear_form(self):
        """Clear the form"""
        self.itemname_var.set("")
        self.category_var.set("")
        self.price_var.set("")
    
    def load_items(self):
        """Load items list"""
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, category, price FROM items ORDER BY category, name")
        items = cursor.fetchall()
        conn.close()
        
        for name, category, price in items:
            self.items_tree.insert('', 'end', values=(name, category, f"{price} KES"))
    
    def edit_item(self, event=None):
        """Edit selected item"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to edit!")
            return
        
        item = self.items_tree.item(selection[0])
        item_name = item['values'][0]
        
        # Load item details
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE name = ?", (item_name,))
        item_data = cursor.fetchone()
        conn.close()
        
        if item_data:
            self.show_edit_item_dialog(item_data)
    
    def show_edit_item_dialog(self, item_data):
        """Show edit dialog for item"""
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Edit Item")
        edit_window.geometry("400x300")
        edit_window.configure(bg='#2d2d2d')
        
        # Form fields
        tk.Label(edit_window, text="Edit Item", font=('Arial', 14, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(pady=10)
        
        # Item Name (read-only)
        tk.Label(edit_window, text=f"Item Name: {item_data[1]}", font=('Arial', 10), 
                bg='#2d2d2d', fg='#ffffff').pack(pady=5)
        
        # Category
        tk.Label(edit_window, text="Category:", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=20, pady=5)
        category_var = tk.StringVar(value=item_data[2])
        category_combo = ttk.Combobox(edit_window, textvariable=category_var, 
                                     values=["Snacks", "Food", "Kuku", "Drinks"], state='readonly', 
                                     font=('Arial', 10))
        category_combo.pack(fill='x', padx=20, pady=5)
        
        # Price
        tk.Label(edit_window, text="Price (KES):", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=20, pady=5)
        price_var = tk.StringVar(value=str(item_data[3]))
        price_entry = tk.Entry(edit_window, textvariable=price_var, 
                              font=('Arial', 10), bg='#3d3d3d', fg='#ffffff',
                              insertbackground='#ffffff', relief='flat')
        price_entry.pack(fill='x', padx=20, pady=5)
        
        def save_changes():
            new_category = category_var.get()
            new_price = price_var.get().strip()
            
            if not new_category or not new_price:
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            
            try:
                new_price = float(new_price)
                if new_price < 0:
                    messagebox.showerror("Error", "Price cannot be negative!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid price!")
                return
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE items SET category = ?, price = ? WHERE name = ?
            ''', (new_category, new_price, item_data[1]))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Item updated successfully!")
            edit_window.destroy()
            self.load_items()
        
        # Save button
        tk.Button(edit_window, text="Save Changes", command=save_changes,
                 font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                 relief='flat', padx=20, pady=5).pack(pady=20)
    
    def delete_item(self):
        """Delete selected item"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to delete!")
            return
        
        item = self.items_tree.item(selection[0])
        item_name = item['values'][0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {item_name}?"):
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE name = ?", (item_name,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Item deleted successfully!")
            self.load_items()
