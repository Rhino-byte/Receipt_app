import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import uuid
from datetime import datetime
import os

# Item categories with prices (in Kenyan Shillings)
ITEM_PRICES = {
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

class ReceiptAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Receipt App - Food & Beverages")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize variables
        self.db_name = "receipt_database.db"
        self.current_receipt = []
        self.staff_name = ""
        self.receipt_id = ""
        
        # Initialize database
        self.init_database()
        
        # Create GUI
        self.create_widgets()
        
        # Set staff name
        self.get_staff_name()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipts (
                receipt_id TEXT PRIMARY KEY,
                staff_name TEXT,
                total_amount REAL,
                created_date TEXT,
                items TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_staff_name(self):
        """Get staff name from user"""
        staff_dialog = tk.Toplevel(self.root)
        staff_dialog.title("Staff Name")
        staff_dialog.geometry("300x150")
        staff_dialog.configure(bg='#f0f0f0')
        staff_dialog.transient(self.root)
        staff_dialog.grab_set()
        
        # Center the dialog
        staff_dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        tk.Label(staff_dialog, text="Enter Staff Name:", font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        staff_entry = tk.Entry(staff_dialog, font=('Arial', 12), width=20)
        staff_entry.pack(pady=10)
        staff_entry.focus()
        
        def submit_staff():
            self.staff_name = staff_entry.get().strip()
            if not self.staff_name:
                self.staff_name = "Unknown"
            staff_dialog.destroy()
            self.update_staff_label()
        
        tk.Button(staff_dialog, text="Submit", command=submit_staff, 
                 font=('Arial', 10, 'bold'), bg='#4CAF50', fg='white', 
                 relief='flat', padx=20).pack(pady=10)
        
        staff_entry.bind('<Return>', lambda e: submit_staff())
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="RECEIPT APP", font=('Arial', 24, 'bold'), 
                bg='#2c3e50', fg='white').pack(expand=True)
        
        # Staff info frame
        self.staff_frame = tk.Frame(self.root, bg='#ecf0f1', height=40)
        self.staff_frame.pack(fill='x', padx=10, pady=5)
        self.staff_frame.pack_propagate(False)
        
        self.staff_label = tk.Label(self.staff_frame, text="Staff: ", font=('Arial', 12, 'bold'), 
                                   bg='#ecf0f1', fg='#2c3e50')
        self.staff_label.pack(side='left', padx=10, pady=5)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Menu and Add Items
        left_panel = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Menu section
        menu_frame = tk.LabelFrame(left_panel, text="Menu Items", font=('Arial', 12, 'bold'), 
                                  bg='#ffffff', fg='#2c3e50')
        menu_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Category selection
        tk.Label(menu_frame, text="Category:", font=('Arial', 10, 'bold'), bg='#ffffff').pack(anchor='w', padx=5, pady=5)
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(menu_frame, textvariable=self.category_var, 
                                          values=list(ITEM_PRICES.keys()), state='readonly', font=('Arial', 10))
        self.category_combo.pack(fill='x', padx=5, pady=5)
        self.category_combo.bind('<<ComboboxSelected>>', self.update_items_list)
        
        # Items list
        tk.Label(menu_frame, text="Items:", font=('Arial', 10, 'bold'), bg='#ffffff').pack(anchor='w', padx=5, pady=5)
        
        self.items_listbox = tk.Listbox(menu_frame, height=8, font=('Arial', 10))
        self.items_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.items_listbox.bind('<Double-Button-1>', self.add_selected_item)
        
        # Add item section
        add_frame = tk.LabelFrame(left_panel, text="Add Item", font=('Arial', 12, 'bold'), 
                                 bg='#ffffff', fg='#2c3e50')
        add_frame.pack(fill='x', padx=10, pady=10)
        
        # Quantity
        tk.Label(add_frame, text="Quantity:", font=('Arial', 10, 'bold'), bg='#ffffff').pack(anchor='w', padx=5, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = tk.Entry(add_frame, textvariable=self.quantity_var, font=('Arial', 10), width=10)
        self.quantity_entry.pack(anchor='w', padx=5, pady=5)
        
        # Custom price
        tk.Label(add_frame, text="Custom Price (optional):", font=('Arial', 10, 'bold'), bg='#ffffff').pack(anchor='w', padx=5, pady=5)
        self.custom_price_var = tk.StringVar()
        self.custom_price_entry = tk.Entry(add_frame, textvariable=self.custom_price_var, font=('Arial', 10), width=10)
        self.custom_price_entry.pack(anchor='w', padx=5, pady=5)
        
        # Add button
        tk.Button(add_frame, text="Add Item", command=self.add_item, 
                 font=('Arial', 10, 'bold'), bg='#3498db', fg='white', 
                 relief='flat', padx=20, pady=5).pack(pady=10)
        
        # Right panel - Receipt
        right_panel = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Receipt section
        receipt_frame = tk.LabelFrame(right_panel, text="Current Receipt", font=('Arial', 12, 'bold'), 
                                     bg='#ffffff', fg='#2c3e50')
        receipt_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Receipt display
        self.receipt_text = scrolledtext.ScrolledText(receipt_frame, height=15, font=('Courier', 10), 
                                                     bg='#f8f9fa', fg='#2c3e50')
        self.receipt_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Receipt actions
        actions_frame = tk.Frame(receipt_frame, bg='#ffffff')
        actions_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(actions_frame, text="Remove Item", command=self.remove_item, 
                 font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white', 
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        tk.Button(actions_frame, text="Adjust Price", command=self.adjust_price, 
                 font=('Arial', 10, 'bold'), bg='#f39c12', fg='white', 
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        tk.Button(actions_frame, text="Clear Receipt", command=self.clear_receipt, 
                 font=('Arial', 10, 'bold'), bg='#95a5a6', fg='white', 
                 relief='flat', padx=15).pack(side='left', padx=5)
        
        # Print receipt button
        print_frame = tk.Frame(right_panel, bg='#ffffff')
        print_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(print_frame, text="PRINT RECEIPT", command=self.print_receipt, 
                 font=('Arial', 14, 'bold'), bg='#27ae60', fg='white', 
                 relief='flat', padx=30, pady=10).pack(fill='x')
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief='sunken', 
                             anchor='w', bg='#bdc3c7', fg='#2c3e50')
        status_bar.pack(side='bottom', fill='x')
    
    def update_staff_label(self):
        """Update staff label"""
        self.staff_label.config(text=f"Staff: {self.staff_name}")
    
    def update_items_list(self, event=None):
        """Update items list based on selected category"""
        self.items_listbox.delete(0, tk.END)
        category = self.category_var.get()
        if category in ITEM_PRICES:
            for item, price in ITEM_PRICES[category].items():
                self.items_listbox.insert(tk.END, f"{item} - {price} KES")
    
    def add_selected_item(self, event=None):
        """Add selected item from listbox"""
        selection = self.items_listbox.curselection()
        if selection:
            item_text = self.items_listbox.get(selection[0])
            item_name = item_text.split(" - ")[0]
            self.add_item_to_receipt(item_name)
    
    def add_item(self):
        """Add item manually"""
        selection = self.items_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item from the list!")
            return
        
        item_text = self.items_listbox.get(selection[0])
        item_name = item_text.split(" - ")[0]
        self.add_item_to_receipt(item_name)
    
    def add_item_to_receipt(self, item_name):
        """Add item to receipt with quantity and custom price"""
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity!")
            return
        
        # Get custom price if provided
        custom_price = None
        if self.custom_price_var.get().strip():
            try:
                custom_price = float(self.custom_price_var.get())
                if custom_price < 0:
                    messagebox.showerror("Error", "Price cannot be negative!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid price!")
                return
        
        # Find default price
        default_price = 0
        for category, items in ITEM_PRICES.items():
            if item_name in items:
                default_price = items[item_name]
                break
        
        if custom_price is not None and custom_price < default_price:
            messagebox.showerror("Error", f"Price cannot be less than the default price of {default_price} KES!")
            return
        
        price = custom_price if custom_price is not None else default_price
        
        # Check if item already exists
        for item in self.current_receipt:
            if item['name'] == item_name:
                item['quantity'] += quantity
                item['total'] = item['quantity'] * item['price']
                self.update_receipt_display()
                self.status_var.set(f"Updated quantity for {item_name} to {item['quantity']}")
                return
        
        # Add new item
        self.current_receipt.append({
            'name': item_name,
            'price': price,
            'quantity': quantity,
            'total': price * quantity
        })
        
        self.update_receipt_display()
        self.status_var.set(f"Added {quantity}x {item_name} at {price} KES each")
        
        # Clear inputs
        self.quantity_var.set("1")
        self.custom_price_var.set("")
    
    def remove_item(self):
        """Remove item from receipt"""
        if not self.current_receipt:
            messagebox.showinfo("Info", "No items in receipt!")
            return
        
        # Create selection dialog
        remove_dialog = tk.Toplevel(self.root)
        remove_dialog.title("Remove Item")
        remove_dialog.geometry("300x400")
        remove_dialog.configure(bg='#f0f0f0')
        remove_dialog.transient(self.root)
        remove_dialog.grab_set()
        
        tk.Label(remove_dialog, text="Select item to remove:", font=('Arial', 12, 'bold'), 
                bg='#f0f0f0').pack(pady=10)
        
        items_listbox = tk.Listbox(remove_dialog, font=('Arial', 10))
        items_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        for item in self.current_receipt:
            items_listbox.insert(tk.END, f"{item['name']} (Qty: {item['quantity']})")
        
        def remove_selected():
            selection = items_listbox.curselection()
            if selection:
                index = selection[0]
                removed_item = self.current_receipt.pop(index)
                self.update_receipt_display()
                self.status_var.set(f"Removed {removed_item['quantity']}x {removed_item['name']}")
                remove_dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Please select an item to remove!")
        
        tk.Button(remove_dialog, text="Remove", command=remove_selected, 
                 font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white', 
                 relief='flat', padx=20).pack(pady=10)
    
    def adjust_price(self):
        """Adjust item price"""
        if not self.current_receipt:
            messagebox.showinfo("Info", "No items in receipt!")
            return
        
        # Create selection dialog
        adjust_dialog = tk.Toplevel(self.root)
        adjust_dialog.title("Adjust Price")
        adjust_dialog.geometry("300x400")
        adjust_dialog.configure(bg='#f0f0f0')
        adjust_dialog.transient(self.root)
        adjust_dialog.grab_set()
        
        tk.Label(adjust_dialog, text="Select item to adjust:", font=('Arial', 12, 'bold'), 
                bg='#f0f0f0').pack(pady=10)
        
        items_listbox = tk.Listbox(adjust_dialog, font=('Arial', 10))
        items_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        for item in self.current_receipt:
            items_listbox.insert(tk.END, f"{item['name']} (Current: {item['price']} KES)")
        
        tk.Label(adjust_dialog, text="New price:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(pady=5)
        
        price_entry = tk.Entry(adjust_dialog, font=('Arial', 10))
        price_entry.pack(pady=5)
        
        def adjust_selected():
            selection = items_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select an item!")
                return
            
            try:
                new_price = float(price_entry.get())
                if new_price < 0:
                    messagebox.showerror("Error", "Price cannot be negative!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid price!")
                return
            
            index = selection[0]
            item = self.current_receipt[index]
            
            # Check default price
            default_price = 0
            for category, items in ITEM_PRICES.items():
                if item['name'] in items:
                    default_price = items[item['name']]
                    break
            
            if new_price < default_price:
                messagebox.showerror("Error", f"Price cannot be less than the default price of {default_price} KES!")
                return
            
            old_price = item['price']
            item['price'] = new_price
            item['total'] = item['quantity'] * new_price
            
            self.update_receipt_display()
            self.status_var.set(f"Adjusted price for {item['name']} from {old_price} to {new_price} KES")
            adjust_dialog.destroy()
        
        tk.Button(adjust_dialog, text="Adjust", command=adjust_selected, 
                 font=('Arial', 10, 'bold'), bg='#f39c12', fg='white', 
                 relief='flat', padx=20).pack(pady=10)
    
    def clear_receipt(self):
        """Clear current receipt"""
        if self.current_receipt:
            if messagebox.askyesno("Confirm", "Are you sure you want to clear the receipt?"):
                self.current_receipt = []
                self.update_receipt_display()
                self.status_var.set("Receipt cleared")
        else:
            messagebox.showinfo("Info", "Receipt is already empty!")
    
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
        self.receipt_text.insert(tk.END, f"{'TOTAL':<35} {total:<8}\n")
    
    def print_receipt(self):
        """Print receipt and store in database"""
        if not self.current_receipt:
            messagebox.showinfo("Info", "No items to print!")
            return
        
        # Generate unique receipt ID
        self.receipt_id = str(uuid.uuid4())[:8].upper()
        
        # Calculate total
        total = sum(item['total'] for item in self.current_receipt)
        
        # Create receipt display
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title(f"Receipt {self.receipt_id}")
        receipt_window.geometry("500x600")
        receipt_window.configure(bg='#ffffff')
        
        # Receipt content
        receipt_text = scrolledtext.ScrolledText(receipt_window, font=('Courier', 12), 
                                                bg='#ffffff', fg='#2c3e50')
        receipt_text.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Format receipt
        receipt_content = f"""
{'='*50}
           RECEIPT
{'='*50}
Receipt ID: {self.receipt_id}
Staff: {self.staff_name}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'-'*50}
{'Item':<25} {'Qty':<5} {'Price':<8} {'Total':<8}
{'-'*50}
"""
        
        for item in self.current_receipt:
            receipt_content += f"{item['name']:<25} {item['quantity']:<5} {item['price']:<8} {item['total']:<8}\n"
        
        receipt_content += f"""
{'-'*50}
{'TOTAL':<35} {total:<8}
{'='*50}
        Thank you!
{'='*50}
"""
        
        receipt_text.insert(tk.END, receipt_content)
        receipt_text.config(state='disabled')
        
        # Store in database
        self.store_receipt(total)
        
        # Clear current receipt
        self.current_receipt = []
        self.update_receipt_display()
        
        self.status_var.set(f"Receipt {self.receipt_id} has been printed and stored in database!")
        
        # Print button
        def print_receipt():
            # In a real application, this would send to printer
            messagebox.showinfo("Print", "Receipt sent to printer!")
        
        tk.Button(receipt_window, text="Print", command=print_receipt, 
                 font=('Arial', 12, 'bold'), bg='#3498db', fg='white', 
                 relief='flat', padx=30, pady=10).pack(pady=10)
    
    def store_receipt(self, total_amount):
        """Store receipt data in the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Convert items to JSON-like string for storage
        items_str = str(self.current_receipt)
        
        cursor.execute('''
            INSERT INTO receipts (receipt_id, staff_name, total_amount, created_date, items)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.receipt_id, self.staff_name, total_amount, datetime.now().isoformat(), items_str))
        
        conn.commit()
        conn.close()

def main():
    root = tk.Tk()
    app = ReceiptAppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
