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

class ReceiptApp:
    def __init__(self):
        self.db_name = "receipt_database.db"
        self.current_receipt = []
        self.staff_name = ""
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create receipts table
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
    
    def set_staff_name(self, name):
        """Set the staff name for the current receipt"""
        self.staff_name = name
    
    def add_item(self, item_name, quantity=1, custom_price=None):
        """Add an item to the receipt preview"""
        # Find the item and its default price
        item_found = False
        default_price = 0
        
        for category, items in ITEM_PRICES.items():
            if item_name in items:
                default_price = items[item_name]
                item_found = True
                break
        
        if not item_found:
            print(f"Item '{item_name}' not found in the menu!")
            return False
        
        # Check if custom price is not less than default price
        if custom_price is not None and custom_price < default_price:
            print(f"Price cannot be less than the default price of {default_price} KES!")
            return False
        
        price = custom_price if custom_price is not None else default_price
        
        # Check if item already exists in receipt
        for item in self.current_receipt:
            if item['name'] == item_name:
                item['quantity'] += quantity
                item['total'] = item['quantity'] * item['price']
                print(f"Updated quantity for {item_name} to {item['quantity']}")
                return True
        
        # Add new item
        self.current_receipt.append({
            'name': item_name,
            'price': price,
            'quantity': quantity,
            'total': price * quantity
        })
        
        print(f"Added {quantity}x {item_name} at {price} KES each")
        return True
    
    def remove_item(self, item_name):
        """Remove an item from the receipt preview"""
        for i, item in enumerate(self.current_receipt):
            if item['name'] == item_name:
                removed_item = self.current_receipt.pop(i)
                print(f"Removed {removed_item['quantity']}x {item_name}")
                return True
        
        print(f"Item '{item_name}' not found in receipt!")
        return False
    
    def adjust_price(self, item_name, new_price):
        """Adjust the price of an item (not less than default price)"""
        # Find default price
        default_price = 0
        for category, items in ITEM_PRICES.items():
            if item_name in items:
                default_price = items[item_name]
                break
        
        if new_price < default_price:
            print(f"Price cannot be less than the default price of {default_price} KES!")
            return False
        
        # Update price in current receipt
        for item in self.current_receipt:
            if item['name'] == item_name:
                old_price = item['price']
                item['price'] = new_price
                item['total'] = item['quantity'] * new_price
                print(f"Adjusted price for {item_name} from {old_price} to {new_price} KES")
                return True
        
        print(f"Item '{item_name}' not found in receipt!")
        return False
    
    def display_receipt_preview(self):
        """Display the current receipt preview"""
        if not self.current_receipt:
            print("\n=== RECEIPT PREVIEW ===")
            print("No items in receipt")
            return
        
        print("\n=== RECEIPT PREVIEW ===")
        print(f"Staff: {self.staff_name}")
        print("-" * 50)
        print(f"{'Item':<25} {'Qty':<5} {'Price':<8} {'Total':<8}")
        print("-" * 50)
        
        total = 0
        for item in self.current_receipt:
            print(f"{item['name']:<25} {item['quantity']:<5} {item['price']:<8} {item['total']:<8}")
            total += item['total']
        
        print("-" * 50)
        print(f"{'TOTAL':<35} {total:<8}")
        print("=" * 50)
    
    def print_receipt(self):
        """Print the receipt and store in database"""
        if not self.current_receipt:
            print("No items to print!")
            return
        
        # Generate unique receipt ID
        receipt_id = str(uuid.uuid4())[:8].upper()
        
        # Calculate total
        total = sum(item['total'] for item in self.current_receipt)
        
        # Print receipt
        print("\n" + "=" * 50)
        print("           RECEIPT")
        print("=" * 50)
        print(f"Receipt ID: {receipt_id}")
        print(f"Staff: {self.staff_name}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        print(f"{'Item':<25} {'Qty':<5} {'Price':<8} {'Total':<8}")
        print("-" * 50)
        
        for item in self.current_receipt:
            print(f"{item['name']:<25} {item['quantity']:<5} {item['price']:<8} {item['total']:<8}")
        
        print("-" * 50)
        print(f"{'TOTAL':<35} {total:<8}")
        print("=" * 50)
        print("        Thank you!")
        print("=" * 50)
        
        # Store in database
        self.store_receipt(receipt_id, total)
        
        # Clear current receipt
        self.current_receipt = []
        print(f"\nReceipt {receipt_id} has been printed and stored in database!")
    
    def store_receipt(self, receipt_id, total_amount):
        """Store receipt data in the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Convert items to JSON-like string for storage
        items_str = str(self.current_receipt)
        
        cursor.execute('''
            INSERT INTO receipts (receipt_id, staff_name, total_amount, created_date, items)
            VALUES (?, ?, ?, ?, ?)
        ''', (receipt_id, self.staff_name, total_amount, datetime.now().isoformat(), items_str))
        
        conn.commit()
        conn.close()
    
    def display_menu(self):
        """Display the available menu items"""
        print("\n=== MENU ===")
        for category, items in ITEM_PRICES.items():
            print(f"\n{category}:")
            for item, price in items.items():
                print(f"  {item:<25} {price} KES")
    
    def run(self):
        """Main application loop"""
        print("Welcome to the Receipt App!")
        
        # Set staff name
        self.staff_name = input("Enter staff name: ").strip()
        if not self.staff_name:
            self.staff_name = "Unknown"
        
        while True:
            print("\n" + "=" * 50)
            print("RECEIPT APP MENU")
            print("=" * 50)
            print("1. Display Menu")
            print("2. Add Item to Receipt")
            print("3. Remove Item from Receipt")
            print("4. Adjust Item Price")
            print("5. Display Receipt Preview")
            print("6. Print Receipt")
            print("7. Exit")
            print("=" * 50)
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == "1":
                self.display_menu()
            
            elif choice == "2":
                self.display_menu()
                item_name = input("Enter item name: ").strip()
                try:
                    quantity = int(input("Enter quantity (default 1): ") or "1")
                    custom_price_input = input("Enter custom price (press Enter for default): ").strip()
                    custom_price = float(custom_price_input) if custom_price_input else None
                    self.add_item(item_name, quantity, custom_price)
                except ValueError:
                    print("Invalid input! Please enter valid numbers.")
            
            elif choice == "3":
                if self.current_receipt:
                    print("Current items in receipt:")
                    for i, item in enumerate(self.current_receipt, 1):
                        print(f"{i}. {item['name']} (Qty: {item['quantity']})")
                    item_name = input("Enter item name to remove: ").strip()
                    self.remove_item(item_name)
                else:
                    print("No items in receipt!")
            
            elif choice == "4":
                if self.current_receipt:
                    print("Current items in receipt:")
                    for i, item in enumerate(self.current_receipt, 1):
                        print(f"{i}. {item['name']} (Current price: {item['price']} KES)")
                    item_name = input("Enter item name: ").strip()
                    try:
                        new_price = float(input("Enter new price: "))
                        self.adjust_price(item_name, new_price)
                    except ValueError:
                        print("Invalid price! Please enter a valid number.")
                else:
                    print("No items in receipt!")
            
            elif choice == "5":
                self.display_receipt_preview()
            
            elif choice == "6":
                self.print_receipt()
            
            elif choice == "7":
                print("Thank you for using the Receipt App!")
                break
            
            else:
                print("Invalid choice! Please enter a number between 1-7.")

if __name__ == "__main__":
    app = ReceiptApp()
    app.run()
