def print_erd_diagram():
    """Print the ERD diagram for the database schema"""
    
    erd = """
┌─────────────────────────────────────────────────────────────────┐
│                    MERRY MARY RESTAURANT                       │
│                      DATABASE SCHEMA ERD                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│      USERS      │         │      ITEMS      │         │     RECEIPTS    │
├─────────────────┤         ├─────────────────┤         ├─────────────────┤
│ PK: id          │         │ PK: id          │         │ PK: receipt_id  │
│     username    │         │     name        │         │     staff_name  │
│     pin         │         │     category    │         │ FK: staff_id    │
│     user_type   │         │     price       │         │     total_amount│
│     full_name   │         │     created_date│         │     created_date│
│     created_date│         └─────────────────┘         │     items       │
└─────────────────┘                                     └─────────────────┘
              │                                                       │
              │                                                       │
              │ 1:N relationship                                      │
              │ (One user can create                                  │
              │  many receipts)                                       │
              └───────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                           LEGEND                                │
├─────────────────────────────────────────────────────────────────┤
│ PK = Primary Key                                                │
│ FK = Foreign Key                                                │
│ 1:N = One-to-Many Relationship                                  │
│                                                                 │
│ RELATIONSHIPS:                                                  │
│ • Users (1) → Receipts (N): One user can create many receipts  │
│ • Items are referenced in receipts.items as JSON-like string   │
│                                                                 │
│ DATA TYPES:                                                     │
│ • INTEGER: Auto-incrementing IDs                                │
│ • TEXT: String data (usernames, names, dates, etc.)            │
│ • REAL: Decimal numbers (prices, amounts)                      │
│ • UNIQUE: Ensures no duplicate values                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        DETAILED SCHEMA                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ USERS TABLE:                                                    │
│ ┌─────────────┬─────────────┬─────────────────────────────────┐ │
│ │ Column      │ Type        │ Description                     │ │
│ ├─────────────┼─────────────┼─────────────────────────────────┤ │
│ │ id          │ INTEGER     │ Primary Key, Auto-increment     │ │
│ │ username    │ TEXT        │ Unique login identifier         │ │
│ │ pin         │ TEXT        │ SHA-256 hashed password         │ │
│ │ user_type   │ TEXT        │ 'admin' or 'staff'              │ │
│ │ full_name   │ TEXT        │ Display name                    │ │
│ │ created_date│ TEXT        │ Account creation timestamp      │ │
│ └─────────────┴─────────────┴─────────────────────────────────┘ │
│                                                                 │
│ ITEMS TABLE:                                                    │
│ ┌─────────────┬─────────────┬─────────────────────────────────┐ │
│ │ Column      │ Type        │ Description                     │ │
│ ├─────────────┼─────────────┼─────────────────────────────────┤ │
│ │ id          │ INTEGER     │ Primary Key, Auto-increment     │ │
│ │ name        │ TEXT        │ Unique item name                │ │
│ │ category    │ TEXT        │ Snacks, Food, Kuku, Drinks      │ │
│ │ price       │ REAL        │ Item price in KES               │ │
│ │ created_date│ TEXT        │ Item creation timestamp         │ │
│ └─────────────┴─────────────┴─────────────────────────────────┘ │
│                                                                 │
│ RECEIPTS TABLE:                                                 │
│ ┌─────────────┬─────────────┬─────────────────────────────────┐ │
│ │ Column      │ Type        │ Description                     │ │
│ ├─────────────┼─────────────┼─────────────────────────────────┤ │
│ │ receipt_id  │ TEXT        │ Primary Key, 8-char unique ID   │ │
│ │ staff_name  │ TEXT        │ Name of staff who created       │ │
│ │ staff_id    │ TEXT        │ Foreign Key to users.id         │ │
│ │ total_amount│ REAL        │ Total receipt amount            │ │
│ │ created_date│ TEXT        │ Receipt creation timestamp      │ │
│ │ items       │ TEXT        │ JSON-like string of items       │ │
│ └─────────────┴─────────────┴─────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        RELATIONSHIPS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. USERS → RECEIPTS (One-to-Many)                              │
│    • One user can create multiple receipts                     │
│    • Relationship: users.id → receipts.staff_id                │
│    • Cardinality: 1:N                                          │
│                                                                 │
│ 2. ITEMS → RECEIPTS (Many-to-Many via JSON)                    │
│    • Items are stored as JSON-like string in receipts.items   │
│    • This allows flexible item combinations per receipt        │
│    • No direct foreign key relationship                        │
│                                                                 │
│ 3. SELF-REFERENCING (Users)                                    │
│    • Users can be either 'admin' or 'staff'                    │
│    • Determined by user_type field                             │
│    • Admins have additional privileges                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        CONSTRAINTS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ PRIMARY KEYS:                                                   │
│ • users.id: Auto-incrementing integer                          │
│ • items.id: Auto-incrementing integer                          │
│ • receipts.receipt_id: Unique 8-character string               │
│                                                                 │
│ UNIQUE CONSTRAINTS:                                             │
│ • users.username: Must be unique for login                     │
│ • items.name: Must be unique for menu items                    │
│                                                                 │
│ FOREIGN KEY CONSTRAINTS:                                        │
│ • receipts.staff_id → users.id                                 │
│                                                                 │
│ DATA VALIDATION:                                                │
│ • user_type: Must be 'admin' or 'staff'                        │
│ • price: Must be non-negative                                  │
│ • total_amount: Must be non-negative                           │
│ • pin: Must be at least 4 characters                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
"""
    
    print(erd)

def print_schema_details():
    """Print detailed schema information"""
    
    schema_details = """
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEMA DETAILS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. USERS TABLE                                                  │
│    Purpose: Store user authentication and profile information  │
│    Key Features:                                                │
│    • Secure password hashing (SHA-256)                         │
│    • Role-based access control (admin/staff)                   │
│    • Unique username constraint                                │
│    • Audit trail with creation timestamps                      │
│                                                                 │
│ 2. ITEMS TABLE                                                  │
│    Purpose: Store menu items and pricing information           │
│    Key Features:                                                │
│    • Categorized items (Snacks, Food, Kuku, Drinks)            │
│    • Flexible pricing system                                   │
│    • Unique item names                                         │
│    • Audit trail with creation timestamps                      │
│                                                                 │
│ 3. RECEIPTS TABLE                                               │
│    Purpose: Store transaction records and receipt data         │
│    Key Features:                                                │
│    • Unique receipt identifiers (8-char)                       │
│    • Staff attribution and tracking                            │
│    • Flexible item storage (JSON-like)                         │
│    • Complete transaction history                               │
│                                                                 │
│ DESIGN DECISIONS:                                               │
│ • JSON-like storage for receipt items allows flexibility       │
│ • Separate staff_name and staff_id for redundancy              │
│ • Timestamps for audit and reporting purposes                  │
│ • Unique constraints prevent data duplication                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
"""
    
    print(schema_details)

if __name__ == "__main__":
    print("=" * 80)
    print("MERRY MARY RESTAURANT - DATABASE SCHEMA ERD")
    print("=" * 80)
    
    print_erd_diagram()
    print_schema_details()
    
    print("\n" + "=" * 80)
    print("ERD DIAGRAM GENERATED SUCCESSFULLY")
    print("=" * 80)
