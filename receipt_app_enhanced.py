import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import uuid
from datetime import datetime
import os
import hashlib
from admin_management import StaffManagement, ItemManagement
from PIL import Image, ImageTk  # Add this import at the top

# Item categories with prices (in Kenyan Shillings)
DEFAULT_ITEM_PRICES = {
    "Snacks": {
        "chapo": 30,
        "Ndazi": 20,
        "Tm": 30,
        "cake": 30,
        "Hcake": 30,
        "Eggs": 40,
        "Omelet": 50,
        "Sausage/Smokie": 50
    },
    "Food": {
        "ChapoMix": 90,
        "Walimix": 150,
        "Ugalimix": 150,
        "PilauMix": 180,
        "ChapoMinji": 140,
        "Waliminji": 200,
        "Ugaliminji": 200,
        "PilauMinji": 200,
        "BeefChapo": 190,
        "BeefUgali": 250,
        "BeefRice": 250,
        "BeefPilau": 300,
        "UgaliMatumbo": 200,
        "RiceMatumbo": 200,
        "ChapoMatumbo": 140,
        "PilauMatumbo": 200,
        "UgaliManagu": 150,
        "RiceManagu": 150,
        "ChapoManagu": 90,
        "PilauManagu": 200,
        "UgaliFryManagu": 300,
        "RiceFryManagu": 300,
        "ChapoFryManagu": 240,
        "PilauFryManagu": 300,
        "UgaliMatumboManagu": 200,
        "RiceMatumboManagu": 200,
        "ChapoMatumboManagu": 200,
        "PilauMatumboManagu": 200,
        "UgaliMboga": 100,
        "RiceMboga": 100,
        "ChapoMboga": 40,
        "UgaliPlain": 50,
        "MchelePlain": 100,
        "PilauPlain": 100,
        "ServiceNyama": 75
    },
    "Kuku": {
        "KukuChapo": 290,
        "KukuUgali": 350,
        "KukuRice": 350,
        "KukuPilau": 400,
        "UgaliKukuManagu": 400,
        "RiceKukuManagu": 400,
        "ChapoKukuManagu": 340,
        "PilauKukuManagu": 400
    },
    "Drinks": {
        "Tea": 30,
        "BlackCoffee": 30,
        "WhiteCofee": 50,
        "LemonTea": 30,
        "Concusion": 50,
        "Predator": 70,
        "Soda": 50,
        "PlasticSoda": 50,
        "Dasani_.5ltr": 50,
        "Dasani_1ltr": 100,
        "Water_.5ltr": 40,
        "Water_1ltr": 80,
        "MinuteMaid": 80
    }
}

class EnhancedReceiptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Merry Mary Restaurant - Receipt System")
        
        # Get screen dimensions for responsive design
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate window size based on screen size
        if screen_width >= 1920:  # Large screens
            window_width = 1600
            window_height = 1000
        elif screen_width >= 1366:  # Medium screens
            window_width = 1400
            window_height = 900
        elif screen_width >= 1024:  # Small screens
            window_width = 1200
            window_height = 800
        else:  # Very small screens
            window_width = 1000
            window_height = 700
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#1a1a1a')
        
        # Store screen dimensions for responsive design
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window_width = window_width
        self.window_height = window_height
        
        # Initialize variables
        self.db_name = "enhanced_receipt_database.db"
        self.current_receipt = []
        self.current_user = None
        self.current_user_type = None
        self.receipt_id = ""
        self.item_prices = {}
        
        # Initialize database
        self.init_database()
        
        # Load items from database or use defaults
        self.load_items_from_database()
        
        # Create GUI
        self.create_login_screen()
    
    def get_responsive_font(self, base_size, size_type='normal'):
        """Get responsive font size based on screen size"""
        if self.screen_width >= 1920:  # Large screens
            multiplier = 1.2
        elif self.screen_width >= 1366:  # Medium screens
            multiplier = 1.0
        elif self.screen_width >= 1024:  # Small screens
            multiplier = 0.9
        else:  # Very small screens
            multiplier = 0.8
        
        if size_type == 'large':
            multiplier *= 1.2
        elif size_type == 'small':
            multiplier *= 0.8
        
        return int(base_size * multiplier)
    
    def get_responsive_padding(self, base_padding):
        """Get responsive padding based on screen size"""
        if self.screen_width >= 1920:  # Large screens
            multiplier = 1.3
        elif self.screen_width >= 1366:  # Medium screens
            multiplier = 1.0
        elif self.screen_width >= 1024:  # Small screens
            multiplier = 0.8
        else:  # Very small screens
            multiplier = 0.6
        
        return int(base_padding * multiplier)
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create receipts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipts (
                receipt_id TEXT PRIMARY KEY,
                staff_name TEXT,
                staff_id TEXT,
                total_amount REAL,
                created_date TEXT,
                items TEXT
            )
        ''')
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                pin TEXT,
                user_type TEXT,
                full_name TEXT,
                created_date TEXT
            )
        ''')
        
        # Create items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                category TEXT,
                price REAL,
                created_date TEXT
            )
        ''')
        
        # Insert default admin user if not exists
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            hashed_pin = hashlib.sha256("pass@word1".encode()).hexdigest()
            cursor.execute('''
                INSERT INTO users (username, pin, user_type, full_name, created_date)
                VALUES (?, ?, ?, ?, ?)
            ''', ('admin', hashed_pin, 'admin', 'Administrator', datetime.now().isoformat()))
        
        # Insert default items if not exists
        cursor.execute("SELECT COUNT(*) FROM items")
        if cursor.fetchone()[0] == 0:
            for category, items in DEFAULT_ITEM_PRICES.items():
                for item_name, price in items.items():
                    cursor.execute('''
                        INSERT INTO items (name, category, price, created_date)
                        VALUES (?, ?, ?, ?)
                    ''', (item_name, category, price, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def load_items_from_database(self):
        """Load items from database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, category, price FROM items ORDER BY category, name")
        items = cursor.fetchall()
        conn.close()
        
        self.item_prices = {}
        for name, category, price in items:
            if category not in self.item_prices:
                self.item_prices[category] = {}
            self.item_prices[category][name] = price
    
    def create_login_screen(self):
        """Create the login screen"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main login frame
        login_frame = tk.Frame(self.root, bg='#1a1a1a')
        login_frame.pack(expand=True, fill='both')
        
        # Center content
        center_frame = tk.Frame(login_frame, bg='#2d2d2d', relief='raised', bd=2)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_font_size = self.get_responsive_font(24, 'large')
        title_label = tk.Label(center_frame, text="Merry Mary Restaurant", 
                              font=('Arial', title_font_size, 'bold'), bg='#2d2d2d', fg='#ffffff')
        title_label.pack(pady=(30, 10))
        
        subtitle_font_size = self.get_responsive_font(12)
        subtitle_label = tk.Label(center_frame, text="Receipt Management System", 
                                 font=('Arial', subtitle_font_size), bg='#2d2d2d', fg='#cccccc')
        subtitle_label.pack(pady=(0, 30))
        
        # Login form
        form_frame = tk.Frame(center_frame, bg='#2d2d2d')
        form_frame.pack(pady=20, padx=40)
        
        # Username
        label_font_size = self.get_responsive_font(12, 'small')
        tk.Label(form_frame, text="Username:", font=('Arial', label_font_size, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', pady=(0, 5))
        
        self.username_var = tk.StringVar()
        entry_font_size = self.get_responsive_font(12)
        username_entry = tk.Entry(form_frame, textvariable=self.username_var, 
                                 font=('Arial', entry_font_size), width=25, bg='#3d3d3d', fg='#ffffff',
                                 insertbackground='#ffffff', relief='flat')
        username_entry.pack(pady=(0, 15))
        
        # PIN
        tk.Label(form_frame, text="PIN:", font=('Arial', label_font_size, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', pady=(0, 5))
        
        self.pin_var = tk.StringVar()
        pin_entry = tk.Entry(form_frame, textvariable=self.pin_var, 
                            font=('Arial', entry_font_size), width=25, bg='#3d3d3d', fg='#ffffff',
                            insertbackground='#ffffff', relief='flat', show='*')
        pin_entry.pack(pady=(0, 25))
        
        # Login button
        button_font_size = self.get_responsive_font(12, 'small')
        login_button = tk.Button(form_frame, text="LOGIN", command=self.authenticate_user,
                                font=('Arial', button_font_size, 'bold'), bg='#4CAF50', fg='white',
                                relief='flat', padx=40, pady=10, cursor='hand2')
        login_button.pack()
        
        # Bind Enter key
        username_entry.bind('<Return>', lambda e: pin_entry.focus())
        pin_entry.bind('<Return>', lambda e: self.authenticate_user())
        
        # Focus on username entry
        username_entry.focus()
    
    def authenticate_user(self):
        """Authenticate user login"""
        username = self.username_var.get().strip()
        pin = self.pin_var.get().strip()
        
        if not username or not pin:
            messagebox.showerror("Error", "Please enter both username and PIN!")
            return
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and user[2] == hashlib.sha256(pin.encode()).hexdigest():
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'user_type': user[3],
                'full_name': user[4]
            }
            self.current_user_type = user[3]
            
            if self.current_user_type == 'admin':
                self.create_admin_dashboard()
            else:
                self.create_staff_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or PIN!")
    
    def create_admin_dashboard(self):
        """Create admin dashboard"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = tk.Frame(self.root, bg='#1a1a1a')
        main_container.pack(fill='both', expand=True)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Merry Mary Restaurant - Admin Dashboard", 
                font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=20)
        
        # User info
        user_info = tk.Label(header_frame, text=f"Admin: {self.current_user['full_name']}", 
                            font=('Arial', 12), bg='#2c3e50', fg='#ecf0f1')
        user_info.pack(side='right', padx=20, pady=20)
        
        # Navigation buttons
        nav_frame = tk.Frame(main_container, bg='#34495e', height=60)
        nav_frame.pack(fill='x')
        nav_frame.pack_propagate(False)
        
        tk.Button(nav_frame, text="Manage Staff", command=self.manage_staff,
                 font=('Arial', 11, 'bold'), bg='#3498db', fg='white',
                 relief='flat', padx=20, pady=10).pack(side='left', padx=10, pady=10)
        
        tk.Button(nav_frame, text="Manage Items", command=self.manage_items,
                 font=('Arial', 11, 'bold'), bg='#e67e22', fg='white',
                 relief='flat', padx=20, pady=10).pack(side='left', padx=10, pady=10)
        
        tk.Button(nav_frame, text="Sales Analytics", command=self.sales_analytics,
                 font=('Arial', 11, 'bold'), bg='#9b59b6', fg='white',
                 relief='flat', padx=20, pady=10).pack(side='left', padx=10, pady=10)
        
        tk.Button(nav_frame, text="Logout", command=self.logout,
                 font=('Arial', 11, 'bold'), bg='#e74c3c', fg='white',
                 relief='flat', padx=20, pady=10).pack(side='right', padx=10, pady=10)
        
        # Main content area
        self.content_frame = tk.Frame(main_container, bg='#1a1a1a')
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_label = tk.Label(self.content_frame, 
                                text="Welcome to the Admin Dashboard!\nSelect an option from the navigation menu above.",
                                font=('Arial', 16), bg='#1a1a1a', fg='#ffffff')
        welcome_label.pack(expand=True)
    
    def create_staff_dashboard(self):
        """Create staff dashboard"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = tk.Frame(self.root, bg='#1a1a1a')
        main_container.pack(fill='both', expand=True)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_font_size = self.get_responsive_font(20, 'large')
        tk.Label(header_frame, text="Merry Mary Restaurant - Receipt System", 
                font=('Arial', header_font_size, 'bold'), bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=20)
        
        # User info
        user_font_size = self.get_responsive_font(12)
        user_info = tk.Label(header_frame, text=f"Staff: {self.current_user['full_name']}", 
                            font=('Arial', user_font_size), bg='#2c3e50', fg='#ecf0f1')
        user_info.pack(side='right', padx=20, pady=20)
        
        # Navigation
        nav_frame = tk.Frame(main_container, bg='#34495e', height=60)
        nav_frame.pack(fill='x')
        nav_frame.pack_propagate(False)
        
        nav_font_size = self.get_responsive_font(11, 'small')
        tk.Button(nav_frame, text="New Receipt", command=self.create_new_receipt,
                 font=('Arial', nav_font_size, 'bold'), bg='#27ae60', fg='white',
                 relief='flat', padx=20, pady=10).pack(side='left', padx=10, pady=10)
        
        tk.Button(nav_frame, text="View Receipts", command=self.view_receipts,
                 font=('Arial', nav_font_size, 'bold'), bg='#3498db', fg='white',
                 relief='flat', padx=20, pady=10).pack(side='left', padx=10, pady=10)
        
        tk.Button(nav_frame, text="Logout", command=self.logout,
                 font=('Arial', nav_font_size, 'bold'), bg='#e74c3c', fg='white',
                 relief='flat', padx=20, pady=10).pack(side='right', padx=10, pady=10)
        
        # Main content area
        self.content_frame = tk.Frame(main_container, bg='#1a1a1a')
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_font_size = self.get_responsive_font(16)
        welcome_label = tk.Label(self.content_frame, 
                                text=f"Welcome {self.current_user['full_name']}!\nClick 'New Receipt' to start creating receipts.",
                                font=('Arial', welcome_font_size), bg='#1a1a1a', fg='#ffffff')
        welcome_label.pack(expand=True)
    
    def create_new_receipt(self):
        """Create new receipt interface"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Main receipt frame
        receipt_frame = tk.Frame(self.content_frame, bg='#2d2d2d')
        receipt_frame.pack(fill='both', expand=True)
        
        # Left panel - Menu and Add Items
        left_panel = tk.Frame(receipt_frame, bg='#2d2d2d')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Menu section
        menu_font_size = self.get_responsive_font(12, 'small')
        menu_frame = tk.LabelFrame(left_panel, text="Menu Items", font=('Arial', menu_font_size, 'bold'), 
                                  bg='#2d2d2d', fg='#ffffff')
        menu_frame.pack(fill='both', expand=True, pady=10)
        
        # Category selection (moved to top)
        label_font_size = self.get_responsive_font(10, 'small')
        tk.Label(menu_frame, text="Category:", font=('Arial', label_font_size, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        
        self.category_var = tk.StringVar()
        combo_font_size = self.get_responsive_font(10)
        self.category_combo = ttk.Combobox(menu_frame, textvariable=self.category_var, 
                                          values=list(self.item_prices.keys()), state='readonly', 
                                          font=('Arial', combo_font_size))
        self.category_combo.pack(fill='x', padx=10, pady=5)
        self.category_combo.bind('<<ComboboxSelected>>', self.update_items_list)
        
        # Search frame (moved below category)
        search_frame = tk.Frame(menu_frame, bg='#2d2d2d')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Search Items:", font=('Arial', label_font_size, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_items)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                               font=('Arial', combo_font_size), width=20, bg='#3d3d3d', fg='#ffffff',
                               insertbackground='#ffffff', relief='flat')
        search_entry.pack(side='left', padx=(0, 10))
        
        # Items list
        tk.Label(menu_frame, text="Items:", font=('Arial', label_font_size, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        
        listbox_font_size = self.get_responsive_font(10)
        self.items_listbox = tk.Listbox(menu_frame, height=12, font=('Arial', listbox_font_size),
                                       bg='#3d3d3d', fg='#ffffff', selectbackground='#3498db')
        self.items_listbox.pack(fill='both', expand=True, padx=10, pady=5)
        self.items_listbox.bind('<Double-Button-1>', self.add_selected_item)
        
        # Add item section
        add_frame = tk.LabelFrame(left_panel, text="Add Item", font=('Arial', menu_font_size, 'bold'), 
                                 bg='#2d2d2d', fg='#ffffff')
        add_frame.pack(fill='x', pady=10)
        
        # Quantity
        tk.Label(add_frame, text="Quantity:", font=('Arial', label_font_size, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = tk.Entry(add_frame, textvariable=self.quantity_var, 
                                      font=('Arial', combo_font_size), width=10, bg='#3d3d3d', fg='#ffffff',
                                      insertbackground='#ffffff', relief='flat')
        self.quantity_entry.pack(anchor='w', padx=10, pady=5)
        
        # Add button
        button_font_size = self.get_responsive_font(10, 'small')
        tk.Button(add_frame, text="Add Item", command=self.add_item,
                 font=('Arial', button_font_size, 'bold'), bg='#3498db', fg='white',
                 relief='flat', padx=20, pady=5).pack(pady=10)
        
        # Right panel - Receipt
        right_panel = tk.Frame(receipt_frame, bg='#2d2d2d')
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Receipt section
        receipt_section = tk.LabelFrame(right_panel, text="Current Receipt", font=('Arial', menu_font_size, 'bold'), 
                                       bg='#2d2d2d', fg='#ffffff')
        receipt_section.pack(fill='both', expand=True, pady=10)
        
        # Receipt display
        receipt_font_size = self.get_responsive_font(10)
        self.receipt_text = scrolledtext.ScrolledText(receipt_section, height=15, font=('Courier', receipt_font_size), 
                                                     bg='#3d3d3d', fg='#ffffff')
        self.receipt_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Receipt actions
        actions_frame = tk.Frame(receipt_section, bg='#2d2d2d')
        actions_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(actions_frame, text="Remove Item", command=self.remove_item,
                 font=('Arial', button_font_size, 'bold'), bg='#e74c3c', fg='white',
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        tk.Button(actions_frame, text="Edit Price", command=self.edit_price,
                 font=('Arial', button_font_size, 'bold'), bg='#f39c12', fg='white',
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        tk.Button(actions_frame, text="Clear Receipt", command=self.clear_receipt,
                 font=('Arial', button_font_size, 'bold'), bg='#95a5a6', fg='white',
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        # Print receipt button
        print_frame = tk.Frame(right_panel, bg='#2d2d2d')
        print_frame.pack(fill='x', pady=10)
        
        print_font_size = self.get_responsive_font(14, 'large')
        tk.Button(print_frame, text="PRINT RECEIPT", command=self.print_receipt,
                 font=('Arial', print_font_size, 'bold'), bg='#27ae60', fg='white',
                 relief='flat', padx=30, pady=10).pack(fill='x')
    
    def filter_items(self, *args):
        """Filter items based on search term"""
        search_term = self.search_var.get().strip().lower()
        self.update_items_list()
        
        if search_term:
            # Filter items in listbox
            items_to_keep = []
            for i in range(self.items_listbox.size()):
                item_text = self.items_listbox.get(i)
                if search_term in item_text.lower():
                    items_to_keep.append(item_text)
            
            self.items_listbox.delete(0, tk.END)
            for item in items_to_keep:
                self.items_listbox.insert(tk.END, item)
    
    def update_items_list(self, event=None):
        """Update items list based on selected category"""
        self.items_listbox.delete(0, tk.END)
        category = self.category_var.get()
        if category in self.item_prices:
            for item_name in self.item_prices[category].keys():
                self.items_listbox.insert(tk.END, item_name)
    
    def add_selected_item(self, event=None):
        """Add selected item from listbox"""
        selection = self.items_listbox.curselection()
        if selection:
            item_name = self.items_listbox.get(selection[0])
            self.add_item_to_receipt(item_name)
    
    def add_item(self):
        """Add item manually"""
        selection = self.items_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item from the list!")
            return
        
        item_name = self.items_listbox.get(selection[0])
        self.add_item_to_receipt(item_name)
    
    def add_item_to_receipt(self, item_name):
        """Add item to receipt with quantity"""
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity!")
            return
        
        # Find price
        price = 0
        for category, items in self.item_prices.items():
            if item_name in items:
                price = items[item_name]
                break
        
        # Check if item already exists
        for item in self.current_receipt:
            if item['name'] == item_name:
                item['quantity'] += quantity
                item['total'] = item['quantity'] * item['price']
                self.update_receipt_display()
                return
        
        # Add new item
        self.current_receipt.append({
            'name': item_name,
            'price': price,
            'quantity': quantity,
            'total': price * quantity
        })
        
        self.update_receipt_display()
        
        # Clear inputs
        self.quantity_var.set("1")
    
    def remove_item(self):
        """Remove item from receipt"""
        if not self.current_receipt:
            messagebox.showinfo("Info", "No items in receipt!")
            return
        
        # Create selection dialog
        remove_dialog = tk.Toplevel(self.root)
        remove_dialog.title("Remove Item")
        remove_dialog.geometry("300x400")
        remove_dialog.configure(bg='#2d2d2d')
        remove_dialog.transient(self.root)
        remove_dialog.grab_set()
        
        tk.Label(remove_dialog, text="Select item to remove:", font=('Arial', 12, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(pady=10)
        
        items_listbox = tk.Listbox(remove_dialog, font=('Arial', 10), bg='#3d3d3d', fg='#ffffff')
        items_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        for item in self.current_receipt:
            items_listbox.insert(tk.END, f"{item['name']} (Qty: {item['quantity']})")
        
        def remove_selected():
            selection = items_listbox.curselection()
            if selection:
                index = selection[0]
                removed_item = self.current_receipt.pop(index)
                self.update_receipt_display()
                remove_dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Please select an item to remove!")
        
        tk.Button(remove_dialog, text="Remove", command=remove_selected,
                 font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
                 relief='flat', padx=20).pack(pady=10)
    
    def clear_receipt(self):
        """Clear current receipt"""
        if self.current_receipt:
            if messagebox.askyesno("Confirm", "Are you sure you want to clear the receipt?"):
                self.current_receipt = []
                self.update_receipt_display()
        else:
            messagebox.showinfo("Info", "Receipt is already empty!")
    
    def edit_price(self):
        """Edit price of selected item in receipt"""
        if not self.current_receipt:
            messagebox.showinfo("Info", "No items in receipt!")
            return
        
        # Create selection dialog
        edit_dialog = tk.Toplevel(self.root)
        edit_dialog.title("Edit Price")
        edit_dialog.geometry("400x500")
        edit_dialog.configure(bg='#2d2d2d')
        edit_dialog.transient(self.root)
        edit_dialog.grab_set()
        
        tk.Label(edit_dialog, text="Select item to edit price:", font=('Arial', 12, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(pady=10)
        
        # Items listbox
        items_listbox = tk.Listbox(edit_dialog, font=('Arial', 10), bg='#3d3d3d', fg='#ffffff')
        items_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        for item in self.current_receipt:
            items_listbox.insert(tk.END, f"{item['name']} (Current: {item['price']})")
        
        # Price entry frame
        price_frame = tk.Frame(edit_dialog, bg='#2d2d2d')
        price_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(price_frame, text="New Price:", font=('Arial', 10, 'bold'), 
                bg='#2d2d2d', fg='#ffffff').pack(side='left', padx=(0, 10))
        
        price_var = tk.StringVar()
        price_entry = tk.Entry(price_frame, textvariable=price_var, 
                              font=('Arial', 10), width=15, bg='#3d3d3d', fg='#ffffff',
                              insertbackground='#ffffff', relief='flat')
        price_entry.pack(side='left', padx=(0, 10))
        
        def edit_selected():
            selection = items_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select an item!")
                return
            
            try:
                new_price = float(price_var.get())
                if new_price < 0:
                    messagebox.showerror("Error", "Price cannot be negative!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid price!")
                return
            
            index = selection[0]
            item = self.current_receipt[index]
            
            # Get default price for this item
            default_price = 0
            for category, items in self.item_prices.items():
                if item['name'] in items:
                    default_price = items[item['name']]
                    break
            
            # Check if new price is lower than default
            if new_price < default_price:
                messagebox.showerror("Error", f"Price cannot be lower than the default price ({default_price})!")
                return
            
            # Update the price
            item['price'] = new_price
            item['total'] = item['price'] * item['quantity']
            
            self.update_receipt_display()
            edit_dialog.destroy()
            messagebox.showinfo("Success", f"Price updated for {item['name']} to {new_price}")
        
        # Buttons frame
        buttons_frame = tk.Frame(edit_dialog, bg='#2d2d2d')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Update Price", command=edit_selected,
                 font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                 relief='flat', padx=20, pady=5).pack(side='left', padx=5)
        
        tk.Button(buttons_frame, text="Cancel", command=edit_dialog.destroy,
                 font=('Arial', 10, 'bold'), bg='#95a5a6', fg='white',
                 relief='flat', padx=20, pady=5).pack(side='left', padx=5)
    
    def update_receipt_display(self):
        """Update the receipt display"""
        self.receipt_text.delete(1.0, tk.END)
        
        if not self.current_receipt:
            self.receipt_text.insert(tk.END, "No items in receipt")
            return
        
        # Header
        self.receipt_text.insert(tk.END, f"{'Item':<25} {'Qty':<5} {'Price':<8} {'Total':<8}\n")
        self.receipt_text.insert(tk.END, "-" * 50 + "\n")
        
        total = 0
        for item in self.current_receipt:
            self.receipt_text.insert(tk.END, 
                f"{item['name']:<25} {item['quantity']:<5} {item['price']:<8} {item['total']:<8}\n")
            total += item['total']
        
        self.receipt_text.insert(tk.END, "-" * 50 + "\n")
        # Show total on the left side for consistency
        self.receipt_text.insert(tk.END, f"{'TOTAL':<25} {'':<5} {'':<8} {total:<8}\n")
    
    def print_receipt(self):
        """Print receipt and store in database"""
        if not self.current_receipt:
            messagebox.showinfo("Info", "No items to print!")
            return

        # Generate unique receipt ID
        self.receipt_id = str(uuid.uuid4())[:8].upper()

        # Calculate total
        total = sum(item['total'] for item in self.current_receipt)

        # Receipt paper size (58mm ~ 384px, 80mm ~ 576px at 203dpi)
        receipt_width_px = 384  # for 58mm paper
        margin_px = 10

        # Create receipt display window
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title(f"Receipt Preview - {self.receipt_id}")
        receipt_window.geometry(f"{receipt_width_px+2*margin_px}x800")
        receipt_window.configure(bg='#ffffff')
        receipt_window.resizable(False, True)
        receipt_window.transient(self.root)
        receipt_window.grab_set()

        # Receipt content frame with small margins
        receipt_frame = tk.Frame(receipt_window, bg='#ffffff', width=receipt_width_px)
        receipt_frame.pack(fill='both', expand=True, padx=margin_px, pady=margin_px)

        # Header with logo and restaurant name
        header_frame = tk.Frame(receipt_frame, bg='#ffffff')
        header_frame.pack(fill='x', pady=(0, 10))

        # Load and resize logo
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        try:
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((60, 60), Image.ANTIALIAS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(header_frame, image=logo_photo, bg='#ffffff')
            logo_label.image = logo_photo  # Keep reference
            logo_label.pack(side='left', padx=(0, 10))
        except Exception as e:
            # If logo not found, skip
            logo_label = None

        # Restaurant name next to logo
        restaurant_label = tk.Label(header_frame, text="MERRY MARY RESTAURANT",
                                   font=('Arial', 14, 'bold'), bg='#ffffff', fg='#000000', anchor='w')
        restaurant_label.pack(side='left', fill='x', expand=True)

        # Receipt details
        details_frame = tk.Frame(receipt_frame, bg='#ffffff')
        details_frame.pack(fill='x', pady=5)
        
        tk.Label(details_frame, text=f"Receipt ID: {self.receipt_id}", 
                font=('Arial', 10), bg='#ffffff', fg='#000000').pack(anchor='w')
        tk.Label(details_frame, text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                font=('Arial', 10), bg='#ffffff', fg='#000000').pack(anchor='w')
        tk.Label(details_frame, text=f"Served by: {self.current_user['full_name']}", 
                font=('Arial', 10), bg='#ffffff', fg='#000000').pack(anchor='w')
        
        # Separator line
        separator1 = tk.Frame(receipt_frame, height=2, bg='#000000')
        separator1.pack(fill='x', pady=10)
        
        # Items header
        items_header_frame = tk.Frame(receipt_frame, bg='#ffffff')
        items_header_frame.pack(fill='x', pady=5)
        
        # Create a frame for the items table
        items_frame = tk.Frame(receipt_frame, bg='#ffffff')
        items_frame.pack(fill='both', expand=True, pady=5)
        
        # Items header row
        header_row = tk.Frame(items_frame, bg='#f0f0f0')
        header_row.pack(fill='x', pady=2)
        
        tk.Label(header_row, text="Item", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0', fg='#000000', width=25, anchor='w').pack(side='left', padx=5)
        tk.Label(header_row, text="Qty", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0', fg='#000000', width=5, anchor='w').pack(side='left', padx=5)
        tk.Label(header_row, text="Price", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0', fg='#000000', width=8, anchor='w').pack(side='left', padx=5)
        tk.Label(header_row, text="Total", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0', fg='#000000', width=8, anchor='w').pack(side='left', padx=5)
        
        # Items rows
        for item in self.current_receipt:
            item_row = tk.Frame(items_frame, bg='#ffffff')
            item_row.pack(fill='x', pady=1)
            
            tk.Label(item_row, text=item['name'], font=('Arial', 9), 
                    bg='#ffffff', fg='#000000', width=25, anchor='w').pack(side='left', padx=5)
            tk.Label(item_row, text=str(item['quantity']), font=('Arial', 9), 
                    bg='#ffffff', fg='#000000', width=5, anchor='w').pack(side='left', padx=5)
            tk.Label(item_row, text=f"{item['price']:,.0f}", font=('Arial', 9), 
                    bg='#ffffff', fg='#000000', width=8, anchor='w').pack(side='left', padx=5)
            tk.Label(item_row, text=f"{item['total']:,.0f}", font=('Arial', 9), 
                    bg='#ffffff', fg='#000000', width=8, anchor='w').pack(side='left', padx=5)
        
        # Separator line
        separator2 = tk.Frame(receipt_frame, height=2, bg='#000000')
        separator2.pack(fill='x', pady=10)
        
        # Total - moved to left side
        total_frame = tk.Frame(receipt_frame, bg='#ffffff')
        total_frame.pack(fill='x', pady=5)
        
        # Configure the frame to expand
        total_frame.columnconfigure(1, weight=1)
        
        tk.Label(total_frame, text="TOTAL:", font=('Arial', 12, 'bold'), 
                bg='#ffffff', fg='#000000').grid(row=0, column=0, sticky='w')
        tk.Label(total_frame, text=f"{total:,.0f} KES", font=('Arial', 12, 'bold'), 
                bg='#ffffff', fg='#000000').grid(row=0, column=1, sticky='e')
        
        # Separator line
        separator3 = tk.Frame(receipt_frame, height=2, bg='#000000')
        separator3.pack(fill='x', pady=10)
        
        # Payment details
        payment_frame = tk.Frame(receipt_frame, bg='#ffffff')
        payment_frame.pack(fill='x', pady=5)
        
        tk.Label(payment_frame, text="PAYMENT DETAILS:", font=('Arial', 10, 'bold'), 
                bg='#ffffff', fg='#000000').pack(anchor='w')
        tk.Label(payment_frame, text="Paybill: 247247", font=('Arial', 9), 
                bg='#ffffff', fg='#000000').pack(anchor='w')
        tk.Label(payment_frame, text="Account: 0764646464", font=('Arial', 9), 
                bg='#ffffff', fg='#000000').pack(anchor='w')
        
        # Thank you message
        thank_you_frame = tk.Frame(receipt_frame, bg='#ffffff')
        thank_you_frame.pack(fill='x', pady=10)
        
        tk.Label(thank_you_frame, text="Thank you for dining with us!", 
                font=('Arial', 10, 'bold'), bg='#ffffff', fg='#000000').pack()
        
        # Separator line
        separator4 = tk.Frame(receipt_frame, height=2, bg='#000000')
        separator4.pack(fill='x', pady=10)
        
        # Buttons frame - emphasize printing
        buttons_frame = tk.Frame(receipt_window, bg='#ffffff')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        # Print to thermal printer button - made more prominent
        def print_to_thermal():
            # Show confirmation dialog
            if messagebox.askyesno("Confirm Print", "Do you want to print this receipt to the thermal printer?"):
                messagebox.showinfo("Print", "Receipt sent to Bluetooth thermal printer!")
                receipt_window.destroy()
                # Store in database after printing
                self.store_receipt(total)
                # Clear current receipt
                self.current_receipt = []
                self.update_receipt_display()
        
        # Make print button more prominent
        print_button = tk.Button(buttons_frame, text="🖨️ PRINT RECEIPT", command=print_to_thermal,
                                font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                                relief='raised', padx=40, pady=15, cursor='hand2')
        print_button.pack(side='left', padx=5, expand=True, fill='x')
        
        # Save as PDF button (simulated)
        def save_as_pdf():
            messagebox.showinfo("Save", "Receipt saved as PDF!")
        
        tk.Button(buttons_frame, text="Save as PDF", command=save_as_pdf,
                 font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                 relief='flat', padx=30, pady=10).pack(side='left', padx=5)
        
        # Close button
        def close_preview():
            # Ask user if they want to print before closing
            if messagebox.askyesno("Print Receipt", "Do you want to print this receipt before closing?"):
                print_to_thermal()
            else:
                receipt_window.destroy()
        
        tk.Button(buttons_frame, text="Close", command=close_preview,
                 font=('Arial', 12, 'bold'), bg='#95a5a6', fg='white',
                 relief='flat', padx=30, pady=10).pack(side='right', padx=5)
        
        # Focus on print button to emphasize printing
        print_button.focus_set()
        
        # Bind Enter key to print
        receipt_window.bind('<Return>', lambda e: print_to_thermal())
        
        # Show a message emphasizing printing
        messagebox.showinfo("Receipt Ready", "Receipt preview is ready!\n\nPlease click 'PRINT RECEIPT' to print to the thermal printer.\n\nPress Enter key for quick printing.")
    
    def store_receipt(self, total_amount):
        """Store receipt data in the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Convert items to JSON-like string for storage
        items_str = str(self.current_receipt)
        
        cursor.execute('''
            INSERT INTO receipts (receipt_id, staff_name, staff_id, total_amount, created_date, items)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.receipt_id, self.current_user['full_name'], self.current_user['id'], 
              total_amount, datetime.now().isoformat(), items_str))
        
        conn.commit()
        conn.close()
    
    def manage_staff(self):
        """Manage staff interface"""
        StaffManagement(self.root, self.db_name)
    
    def manage_items(self):
        """Manage items interface"""
        ItemManagement(self.root, self.db_name)
        # Reload items after management
        self.load_items_from_database()
    
    def sales_analytics(self):
        """Sales analytics interface"""
        # Create analytics window
        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("Sales Analytics - Merry Mary Restaurant")
        analytics_window.geometry("1000x700")
        analytics_window.configure(bg='#1a1a1a')
        
        # Header
        header_frame = tk.Frame(analytics_window, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Sales Analytics", font=('Arial', 18, 'bold'), 
                bg='#2c3e50', fg='white').pack(expand=True)
        
        # Main content
        main_frame = tk.Frame(analytics_window, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Get today's sales
        today = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as total_receipts, 
                   SUM(total_amount) as total_sales,
                   COUNT(DISTINCT staff_name) as staff_count
            FROM receipts 
            WHERE DATE(created_date) = ?
        ''', (today,))
        
        today_stats = cursor.fetchone()
        
        # Get top selling items
        cursor.execute('''
            SELECT items FROM receipts WHERE DATE(created_date) = ?
        ''', (today,))
        
        all_items = cursor.fetchall()
        item_counts = {}
        
        for row in all_items:
            items_str = row[0]
            # Parse items (simplified)
            items_str = items_str.replace('[', '').replace(']', '').replace("'", '')
            items_list = items_str.split('}, {')
            
            for item in items_list:
                if item.strip():
                    item_parts = item.split(', ')
                    if len(item_parts) >= 2:
                        name = item_parts[0].split(': ')[1] if ': ' in item_parts[0] else item_parts[0]
                        quantity = int(item_parts[2].split(': ')[1]) if ': ' in item_parts[2] else 1
                        item_counts[name] = item_counts.get(name, 0) + quantity
        
        conn.close()
        
        # Display statistics
        stats_frame = tk.LabelFrame(main_frame, text="Today's Statistics", font=('Arial', 12, 'bold'), 
                                   bg='#2d2d2d', fg='#ffffff')
        stats_frame.pack(fill='x', pady=10)
        
        if today_stats[0] > 0:
            tk.Label(stats_frame, text=f"Total Receipts: {today_stats[0]}", 
                    font=('Arial', 12), bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
            tk.Label(stats_frame, text=f"Total Sales: {today_stats[1]:,.2f} KES", 
                    font=('Arial', 12), bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
            tk.Label(stats_frame, text=f"Staff on Duty: {today_stats[2]}", 
                    font=('Arial', 12), bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        else:
            tk.Label(stats_frame, text="No sales recorded today", 
                    font=('Arial', 12), bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=5)
        
        # Top selling items
        if item_counts:
            items_frame = tk.LabelFrame(main_frame, text="Top Selling Items Today", font=('Arial', 12, 'bold'), 
                                       bg='#2d2d2d', fg='#ffffff')
            items_frame.pack(fill='both', expand=True, pady=10)
            
            # Sort items by quantity
            sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
            
            for item_name, quantity in sorted_items[:10]:  # Top 10
                tk.Label(items_frame, text=f"{item_name}: {quantity} units", 
                        font=('Arial', 10), bg='#2d2d2d', fg='#ffffff').pack(anchor='w', padx=10, pady=2)
    
    def view_receipts(self):
        """View receipts interface"""
        # Create receipts viewer window
        receipts_window = tk.Toplevel(self.root)
        receipts_window.title("View Receipts - Merry Mary Restaurant")
        receipts_window.geometry("1200x700")
        receipts_window.configure(bg='#1a1a1a')
        
        # Header
        header_frame = tk.Frame(receipts_window, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="View Receipts", font=('Arial', 18, 'bold'), 
                bg='#2c3e50', fg='white').pack(expand=True)
        
        # Main content
        main_frame = tk.Frame(receipts_window, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Receipts treeview
        columns = ('Receipt ID', 'Staff', 'Amount', 'Date')
        receipts_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            receipts_tree.heading(col, text=col)
            receipts_tree.column(col, width=200)
        
        receipts_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load receipts
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT receipt_id, staff_name, total_amount, created_date 
            FROM receipts 
            ORDER BY created_date DESC
        ''')
        
        receipts = cursor.fetchall()
        conn.close()
        
        for receipt in receipts:
            receipt_id, staff_name, amount, date = receipt
            formatted_date = datetime.fromisoformat(date).strftime('%Y-%m-%d %H:%M')
            receipts_tree.insert('', 'end', values=(receipt_id, staff_name, f"{amount:,.2f} KES", formatted_date))
    
    def logout(self):
        """Logout and return to login screen"""
        self.current_user = None
        self.current_user_type = None
        self.current_receipt = []
        self.create_login_screen()

def main():
    root = tk.Tk()
    app = EnhancedReceiptApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
