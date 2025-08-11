# Merry Mary Restaurant - Enhanced Receipt System

A modern, multi-user Python-based offline receipt application with admin and staff accounts, designed for restaurant management. The app stores all receipt data in a SQLite database and features a beautiful, responsive GUI.

## 🎯 **Key Features**

### 👥 **Multi-User System**
- **Admin Account**: Full system management capabilities
- **Staff Account**: Receipt creation and management
- **Secure Login**: PIN-based authentication with SHA-256 hashing
- **User Management**: Add, edit, and remove staff members

### 🍽️ **Receipt Management**
- **Add food items** to receipt preview with prices and quantity
- **Remove items** from receipt preview
- **Adjust prices** (but not less than default prices)
- **Print receipts** with unique identity
- **Store data** in SQLite database
- **Offline functionality** - no internet required

### 🔍 **Enhanced User Experience**
- **Modern GUI**: Dark theme with professional design
- **Search functionality**: Find items quickly
- **Category filtering**: Organize items by category
- **Real-time preview**: Live receipt display
- **Responsive design**: Adapts to different screen sizes

### 📊 **Admin Features**
- **Staff Management**: Add, edit, and remove staff members
- **Item Management**: Add, edit, and remove menu items
- **Sales Analytics**: Daily sales summary and top-selling items
- **Receipt History**: View all receipts with filtering

### 🖨️ **Printing Features**
- **Bluetooth Thermal Printer Support**: Ready for thermal printing
- **Professional Receipt Format**: Clean, organized layout
- **Payment Details**: Includes paybill and account information
- **Staff Attribution**: Shows who served the customer

## 🏗️ **System Architecture**

### **Database Schema**
```
receipts:
- receipt_id (TEXT PRIMARY KEY)
- staff_name (TEXT)
- staff_id (TEXT)
- total_amount (REAL)
- created_date (TEXT)
- items (TEXT)

users:
- id (INTEGER PRIMARY KEY)
- username (TEXT UNIQUE)
- pin (TEXT)
- user_type (TEXT)
- full_name (TEXT)
- created_date (TEXT)

items:
- id (INTEGER PRIMARY KEY)
- name (TEXT UNIQUE)
- category (TEXT)
- price (REAL)
- created_date (TEXT)
```

### **File Structure**
```
Receipt_app/
├── receipt_app_enhanced.py    # Main application
├── admin_management.py        # Admin management interfaces
├── requirements.txt           # Dependencies
├── README.md                 # Documentation
└── enhanced_receipt_database.db  # SQLite database
```

## 🚀 **Installation & Setup**

### **Prerequisites**
- Python 3.7 or higher
- tkinter (usually included with Python)

### **Installation Steps**
1. **Clone or download** the project files
2. **Navigate** to the project directory:
   ```bash
   cd Receipt_app
   ```
3. **Run the application**:
   ```bash
   python receipt_app_enhanced.py
   ```

### **Default Login Credentials**
- **Admin Account**:
  - Username: `admin`
  - PIN: `pass@word1`

## 🎮 **Usage Guide**

### **Admin Dashboard**
1. **Login** with admin credentials
2. **Manage Staff**: Add, edit, or remove staff members
3. **Manage Items**: Add, edit, or remove menu items
4. **Sales Analytics**: View daily sales statistics
5. **Logout**: Return to login screen

### **Staff Dashboard**
1. **Login** with staff credentials
2. **New Receipt**: Create a new receipt
3. **View Receipts**: Browse receipt history
4. **Logout**: Return to login screen

### **Creating Receipts**
1. **Select Category**: Choose from Snacks, Food, Kuku, or Drinks
2. **Search Items**: Use the search bar to find items quickly
3. **Add Items**: Double-click items or use the "Add Item" button
4. **Adjust Quantity**: Set the desired quantity
5. **Review Receipt**: Check the receipt preview
6. **Print Receipt**: Generate and print the final receipt

## 🍽️ **Menu Categories & Items**

### **Snacks**
- chapo 
- Ndazi 
- Tm 
- cake 
- Hcake 
- Omelet 
- Sausage/Smokie 

### **Food**
- ChapoMix 
- Walimix 
- Ugalimix 
- PilauMix 
- ChapoMinji 
- Waliminji 
- Ugaliminji 
- PilauMinji 
- BeefChapo 
- BeefUgali 
- BeefRice 
- BeefPilau 
- And many more...

### **Kuku (Chicken)**
- KukuChapo 
- KukuUgali 
- KukuRice 
- KukuPilau 
- And more...

### **Drinks**
- Tea 
- BlackCoffee 
- WhiteCoffee 
- LemonTea 
- Concusion 
- Predator 
- Soda 
- And more...

## 🔧 **Technical Details**

### **Technologies Used**
- **Python 3.7+**: Core programming language
- **tkinter**: GUI framework
- **SQLite3**: Database management
- **hashlib**: Password hashing
- **uuid**: Unique ID generation
- **datetime**: Date and time handling

### **Security Features**
- **Password Hashing**: SHA-256 encryption for PINs
- **User Authentication**: Secure login system
- **Access Control**: Role-based permissions
- **Data Validation**: Input validation and sanitization

### **Database Features**
- **ACID Compliance**: Reliable data transactions
- **Automatic Backup**: Data persistence
- **Query Optimization**: Efficient data retrieval
- **Data Integrity**: Foreign key constraints

## 🎨 **UI/UX Design**

### **Color Scheme**
- **Primary**: Dark theme (#1a1a1a, #2d2d2d)
- **Accent**: Blue (#3498db), Green (#27ae60), Orange (#e67e22)
- **Text**: White (#ffffff), Light Gray (#cccccc)
- **Background**: Dark Gray (#1a1a1a), Medium Gray (#2d2d2d)

### **Design Principles**
- **Modern Interface**: Clean, professional appearance
- **Intuitive Navigation**: Easy-to-use menus and buttons
- **Responsive Layout**: Adapts to different screen sizes
- **Accessibility**: Clear fonts and high contrast

## 🖨️ **Printing Configuration**

### **Thermal Printer Setup**
- **Paybill Number**: 247247
- **Account Number**: 0764646464
- **Receipt Format**: Optimized for thermal printers
- **Print Size**: Standard receipt width

### **Receipt Format**
```
==================================================
        MERRY MARY RESTAURANT
==================================================
Receipt ID: [UNIQUE_ID]
Date: [DATE_TIME]
Served by: [STAFF_NAME]
==================================================
Item                    Qty   Price    Total
--------------------------------------------------
[Item Name]            [Qty]  [Price]  [Total]
...
--------------------------------------------------
TOTAL                              [TOTAL]
==================================================

PAYMENT DETAILS:
Paybill: 247247
Account: 0764646464

Thank you for dining with us!
==================================================
```

## 🔄 **Updates & Maintenance**

### **Adding New Items**
1. **Admin Login**: Access admin dashboard
2. **Manage Items**: Click "Manage Items"
3. **Add Item**: Fill in name, category, and price
4. **Save**: Item is immediately available

### **Adding New Staff**
1. **Admin Login**: Access admin dashboard
2. **Manage Staff**: Click "Manage Staff"
3. **Add Staff**: Fill in username, full name, PIN, and user type
4. **Save**: Staff can immediately login

### **Database Backup**
- **Automatic**: Database is automatically created and maintained
- **Manual Backup**: Copy `enhanced_receipt_database.db` file
- **Restore**: Replace database file to restore data

## 🐛 **Troubleshooting**

### **Common Issues**
1. **Login Failed**: Check username and PIN
2. **Items Not Loading**: Restart application
3. **Printing Issues**: Check thermal printer connection
4. **Database Errors**: Check file permissions

### **Support**
- **Documentation**: Refer to this README
- **Error Messages**: Check console output
- **Database Issues**: Verify SQLite installation

## 📈 **Future Enhancements**

### **Planned Features**
- **Inventory Management**: Track stock levels
- **Customer Database**: Store customer information
- **Advanced Analytics**: Detailed sales reports
- **Mobile App**: Companion mobile application
- **Cloud Sync**: Online backup and sync
- **Multi-Location**: Support for multiple restaurants

### **Technical Improvements**
- **Performance Optimization**: Faster loading times
- **Enhanced Security**: Additional security measures
- **API Integration**: Third-party service integration
- **Automated Backups**: Scheduled database backups

## 📄 **License**

This project is developed for Merry Mary Restaurant. All rights reserved.

## 👥 **Contributors**

- **Developer**: Savins
- **Restaurant**: Merry Mary Restaurant
- **Version**: 1.0 Enhanced

---

**Merry Mary Restaurant - Receipt Management System v1.0**
*Professional restaurant management made simple*
