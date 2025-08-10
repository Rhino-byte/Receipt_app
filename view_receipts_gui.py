import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from datetime import datetime

class ReceiptViewerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Receipt Database Viewer")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        self.db_name = "receipt_database.db"
        self.create_widgets()
        self.load_receipts()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="RECEIPT DATABASE VIEWER", font=('Arial', 20, 'bold'), 
                bg='#2c3e50', fg='white').pack(expand=True)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Receipts list
        left_panel = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Receipts list section
        list_frame = tk.LabelFrame(left_panel, text="Stored Receipts", font=('Arial', 12, 'bold'), 
                                  bg='#ffffff', fg='#2c3e50')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Search frame
        search_frame = tk.Frame(list_frame, bg='#ffffff')
        search_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(search_frame, text="Search by Receipt ID:", font=('Arial', 10, 'bold'), 
                bg='#ffffff').pack(side='left', padx=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 10), width=15)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_receipts)
        
        # Receipts listbox
        self.receipts_listbox = tk.Listbox(list_frame, font=('Arial', 10), selectmode='single')
        self.receipts_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.receipts_listbox.bind('<<ListboxSelect>>', self.show_receipt_details)
        
        # Buttons frame
        buttons_frame = tk.Frame(left_panel, bg='#ffffff')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Refresh", command=self.load_receipts, 
                 font=('Arial', 10, 'bold'), bg='#3498db', fg='white', 
                 relief='flat', padx=20).pack(side='left', padx=5)
        
        tk.Button(buttons_frame, text="Clear Search", command=self.clear_search, 
                 font=('Arial', 10, 'bold'), bg='#95a5a6', fg='white', 
                 relief='flat', padx=20).pack(side='left', padx=5)
        
        # Right panel - Receipt details
        right_panel = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Receipt details section
        details_frame = tk.LabelFrame(right_panel, text="Receipt Details", font=('Arial', 12, 'bold'), 
                                     bg='#ffffff', fg='#2c3e50')
        details_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Receipt details display
        self.details_text = scrolledtext.ScrolledText(details_frame, font=('Courier', 10), 
                                                     bg='#f8f9fa', fg='#2c3e50')
        self.details_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief='sunken', 
                             anchor='w', bg='#bdc3c7', fg='#2c3e50')
        status_bar.pack(side='bottom', fill='x')
    
    def load_receipts(self):
        """Load all receipts from database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT receipt_id, staff_name, total_amount, created_date
                FROM receipts
                ORDER BY created_date DESC
            ''')
            
            receipts = cursor.fetchall()
            conn.close()
            
            self.receipts_listbox.delete(0, tk.END)
            
            if not receipts:
                self.receipts_listbox.insert(tk.END, "No receipts found in database")
                self.status_var.set("No receipts found")
                return
            
            self.all_receipts = receipts  # Store for filtering
            
            for receipt in receipts:
                receipt_id, staff_name, total_amount, created_date = receipt
                
                # Parse the date
                try:
                    date_obj = datetime.fromisoformat(created_date)
                    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
                except:
                    formatted_date = created_date[:16] if len(created_date) > 16 else created_date
                
                display_text = f"{receipt_id} | {staff_name} | {total_amount} KES | {formatted_date}"
                self.receipts_listbox.insert(tk.END, display_text)
            
            self.status_var.set(f"Loaded {len(receipts)} receipts")
            
        except sqlite3.OperationalError:
            self.receipts_listbox.delete(0, tk.END)
            self.receipts_listbox.insert(tk.END, "Database not found! Please run the receipt app first.")
            self.status_var.set("Database not found")
        except Exception as e:
            self.receipts_listbox.delete(0, tk.END)
            self.receipts_listbox.insert(tk.END, f"Error loading receipts: {e}")
            self.status_var.set("Error loading receipts")
    
    def filter_receipts(self, event=None):
        """Filter receipts based on search term"""
        search_term = self.search_var.get().strip().upper()
        
        if not hasattr(self, 'all_receipts'):
            return
        
        self.receipts_listbox.delete(0, tk.END)
        
        if not search_term:
            # Show all receipts
            for receipt in self.all_receipts:
                receipt_id, staff_name, total_amount, created_date = receipt
                try:
                    date_obj = datetime.fromisoformat(created_date)
                    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
                except:
                    formatted_date = created_date[:16] if len(created_date) > 16 else created_date
                
                display_text = f"{receipt_id} | {staff_name} | {total_amount} KES | {formatted_date}"
                self.receipts_listbox.insert(tk.END, display_text)
        else:
            # Filter receipts
            filtered_count = 0
            for receipt in self.all_receipts:
                receipt_id, staff_name, total_amount, created_date = receipt
                
                if search_term in receipt_id.upper() or search_term in staff_name.upper():
                    try:
                        date_obj = datetime.fromisoformat(created_date)
                        formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
                    except:
                        formatted_date = created_date[:16] if len(created_date) > 16 else created_date
                    
                    display_text = f"{receipt_id} | {staff_name} | {total_amount} KES | {formatted_date}"
                    self.receipts_listbox.insert(tk.END, display_text)
                    filtered_count += 1
            
            self.status_var.set(f"Found {filtered_count} receipts matching '{search_term}'")
    
    def clear_search(self):
        """Clear search and show all receipts"""
        self.search_var.set("")
        self.load_receipts()
    
    def show_receipt_details(self, event=None):
        """Show details of selected receipt"""
        selection = self.receipts_listbox.curselection()
        if not selection:
            return
        
        try:
            # Get the selected receipt
            selected_text = self.receipts_listbox.get(selection[0])
            receipt_id = selected_text.split(" | ")[0]
            
            # Load receipt details from database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT receipt_id, staff_name, total_amount, created_date, items
                FROM receipts
                WHERE receipt_id = ?
            ''', (receipt_id,))
            
            receipt = cursor.fetchone()
            conn.close()
            
            if not receipt:
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, "Receipt not found!")
                return
            
            receipt_id, staff_name, total_amount, created_date, items = receipt
            
            # Parse the date
            try:
                date_obj = datetime.fromisoformat(created_date)
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            except:
                formatted_date = created_date
            
            # Format receipt details
            details_content = f"""
{'='*60}
RECEIPT DETAILS
{'='*60}
Receipt ID: {receipt_id}
Staff: {staff_name}
Date: {formatted_date}
Total Amount: {total_amount} KES
{'='*60}

ITEMS:
{'-'*60}
{'Item':<30} {'Qty':<8} {'Price':<10} {'Total':<10}
{'-'*60}
"""
            
            # Parse items (simplified parsing)
            items_str = items.replace('[', '').replace(']', '').replace("'", '')
            items_list = items_str.split('}, {')
            
            for item in items_list:
                if item.strip():
                    # Extract item details (simplified)
                    item_parts = item.split(', ')
                    if len(item_parts) >= 4:
                        name = item_parts[0].split(': ')[1] if ': ' in item_parts[0] else item_parts[0]
                        price = item_parts[1].split(': ')[1] if ': ' in item_parts[1] else item_parts[1]
                        quantity = item_parts[2].split(': ')[1] if ': ' in item_parts[2] else item_parts[2]
                        total = item_parts[3].split(': ')[1] if ': ' in item_parts[3] else item_parts[3]
                        
                        details_content += f"{name:<30} {quantity:<8} {price:<10} {total:<10}\n"
            
            details_content += f"""
{'-'*60}
TOTAL: {total_amount} KES
{'='*60}
"""
            
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, details_content)
            
            self.status_var.set(f"Showing details for receipt {receipt_id}")
            
        except Exception as e:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Error loading receipt details: {e}")
            self.status_var.set("Error loading receipt details")

def main():
    root = tk.Tk()
    app = ReceiptViewerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
