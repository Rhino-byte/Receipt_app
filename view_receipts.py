import sqlite3
from datetime import datetime

def view_receipts():
    """View all stored receipts from the database"""
    try:
        conn = sqlite3.connect("receipt_database.db")
        cursor = conn.cursor()
        
        # Get all receipts
        cursor.execute('''
            SELECT receipt_id, staff_name, total_amount, created_date, items
            FROM receipts
            ORDER BY created_date DESC
        ''')
        
        receipts = cursor.fetchall()
        
        if not receipts:
            print("No receipts found in database!")
            return
        
        print(f"\n=== STORED RECEIPTS ({len(receipts)} total) ===")
        print("=" * 80)
        
        for receipt in receipts:
            receipt_id, staff_name, total_amount, created_date, items = receipt
            
            # Parse the date
            try:
                date_obj = datetime.fromisoformat(created_date)
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            except:
                formatted_date = created_date
            
            print(f"\nReceipt ID: {receipt_id}")
            print(f"Staff: {staff_name}")
            print(f"Date: {formatted_date}")
            print(f"Total: {total_amount} KES")
            print("-" * 50)
            
            # Display items (simplified)
            print("Items:")
            items_str = items.replace('[', '').replace(']', '').replace("'", '')
            items_list = items_str.split('}, {')
            for item in items_list:
                if item.strip():
                    print(f"  {item.strip()}")
            
            print("=" * 80)
        
        conn.close()
        
    except sqlite3.OperationalError:
        print("Database not found! Please run the receipt app first to create the database.")
    except Exception as e:
        print(f"Error viewing receipts: {e}")

def view_receipt_by_id(receipt_id):
    """View a specific receipt by ID"""
    try:
        conn = sqlite3.connect("receipt_database.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT receipt_id, staff_name, total_amount, created_date, items
            FROM receipts
            WHERE receipt_id = ?
        ''', (receipt_id,))
        
        receipt = cursor.fetchone()
        
        if not receipt:
            print(f"Receipt with ID {receipt_id} not found!")
            return
        
        receipt_id, staff_name, total_amount, created_date, items = receipt
        
        # Parse the date
        try:
            date_obj = datetime.fromisoformat(created_date)
            formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except:
            formatted_date = created_date
        
        print(f"\n=== RECEIPT {receipt_id} ===")
        print("=" * 50)
        print(f"Staff: {staff_name}")
        print(f"Date: {formatted_date}")
        print(f"Total: {total_amount} KES")
        print("-" * 50)
        print("Items:")
        
        # Display items in a more readable format
        items_str = items.replace('[', '').replace(']', '').replace("'", '')
        items_list = items_str.split('}, {')
        for item in items_list:
            if item.strip():
                print(f"  {item.strip()}")
        
        print("=" * 50)
        
        conn.close()
        
    except sqlite3.OperationalError:
        print("Database not found! Please run the receipt app first to create the database.")
    except Exception as e:
        print(f"Error viewing receipt: {e}")

if __name__ == "__main__":
    print("Receipt Database Viewer")
    print("=" * 30)
    print("1. View all receipts")
    print("2. View specific receipt by ID")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            view_receipts()
        elif choice == "2":
            receipt_id = input("Enter receipt ID: ").strip().upper()
            if receipt_id:
                view_receipt_by_id(receipt_id)
            else:
                print("Please enter a valid receipt ID!")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")
