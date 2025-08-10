import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_erd_diagram():
    """Create ERD diagram for the enhanced receipt app database"""
    
    # Create figure and axis with much more space
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 16)
    ax.set_aspect('equal')
    
    # Remove axes
    ax.axis('off')
    
    # Title
    ax.text(10, 15.5, 'Merry Mary Restaurant - Database Schema ERD', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Colors
    entity_color = '#3498db'
    attribute_color = '#ecf0f1'
    primary_key_color = '#e74c3c'
    foreign_key_color = '#f39c12'
    
    # Entity 1: Users (positioned higher and with more space)
    users_box = FancyBboxPatch((1, 11), 4, 3, 
                              boxstyle="round,pad=0.1", 
                              facecolor=entity_color, 
                              edgecolor='black', 
                              linewidth=2)
    ax.add_patch(users_box)
    
    ax.text(3, 13.7, 'USERS', fontsize=14, fontweight='bold', ha='center')
    
    # Users attributes (more spacing)
    users_attrs = [
        ('id', 'INTEGER PRIMARY KEY'),
        ('username', 'TEXT UNIQUE'),
        ('pin', 'TEXT'),
        ('user_type', 'TEXT'),
        ('full_name', 'TEXT'),
        ('created_date', 'TEXT')
    ]
    
    for i, (attr, type_info) in enumerate(users_attrs):
        y_pos = 13.2 - i * 0.4
        color = primary_key_color if attr == 'id' else attribute_color
        ax.text(1.3, y_pos, f'• {attr}: {type_info}', fontsize=9, 
                bbox=dict(boxstyle="round,pad=0.1", facecolor=color, alpha=0.7))
    
    # Entity 2: Items (positioned higher and center)
    items_box = FancyBboxPatch((8, 11), 4, 3, 
                              boxstyle="round,pad=0.1", 
                              facecolor=entity_color, 
                              edgecolor='black', 
                              linewidth=2)
    ax.add_patch(items_box)
    
    ax.text(10, 13.7, 'ITEMS', fontsize=14, fontweight='bold', ha='center')
    
    # Items attributes (more spacing)
    items_attrs = [
        ('id', 'INTEGER PRIMARY KEY'),
        ('name', 'TEXT UNIQUE'),
        ('category', 'TEXT'),
        ('price', 'REAL'),
        ('created_date', 'TEXT')
    ]
    
    for i, (attr, type_info) in enumerate(items_attrs):
        y_pos = 13.2 - i * 0.4
        color = primary_key_color if attr == 'id' else attribute_color
        ax.text(8.3, y_pos, f'• {attr}: {type_info}', fontsize=9, 
                bbox=dict(boxstyle="round,pad=0.1", facecolor=color, alpha=0.7))
    
    # Entity 3: Receipts (positioned higher and right)
    receipts_box = FancyBboxPatch((15, 11), 4, 3, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor=entity_color, 
                                 edgecolor='black', 
                                 linewidth=2)
    ax.add_patch(receipts_box)
    
    ax.text(17, 13.7, 'RECEIPTS', fontsize=14, fontweight='bold', ha='center')
    
    # Receipts attributes (more spacing)
    receipts_attrs = [
        ('receipt_id', 'TEXT PRIMARY KEY'),
        ('staff_name', 'TEXT'),
        ('staff_id', 'TEXT'),
        ('total_amount', 'REAL'),
        ('created_date', 'TEXT'),
        ('items', 'TEXT')
    ]
    
    for i, (attr, type_info) in enumerate(receipts_attrs):
        y_pos = 13.2 - i * 0.4
        if attr in ['receipt_id']:
            color = primary_key_color
        elif attr in ['staff_id']:
            color = foreign_key_color
        else:
            color = attribute_color
        ax.text(15.3, y_pos, f'• {attr}: {type_info}', fontsize=9, 
                bbox=dict(boxstyle="round,pad=0.1", facecolor=color, alpha=0.7))
    
    # Relationships (adjusted positioning)
    # Users to Receipts (staff_id)
    ax.annotate('', xy=(5, 12.5), xytext=(15, 12.5),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    ax.text(10, 12.8, 'staff_id', fontsize=10, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # Cardinality (adjusted positioning)
    ax.text(4.7, 12.1, '1', fontsize=12, fontweight='bold', ha='center',
            bbox=dict(boxstyle="circle,pad=0.2", facecolor='white', alpha=0.8))
    ax.text(15.3, 12.1, 'N', fontsize=12, fontweight='bold', ha='center',
            bbox=dict(boxstyle="circle,pad=0.2", facecolor='white', alpha=0.8))
    
    # Legend (positioned at bottom left with more space)
    legend_y = 1.5
    ax.text(1, legend_y + 1.5, 'Legend:', fontsize=12, fontweight='bold')
    
    # Primary Key
    pk_box = patches.Rectangle((1, legend_y + 0.8), 0.3, 0.3, 
                              facecolor=primary_key_color, alpha=0.7)
    ax.add_patch(pk_box)
    ax.text(1.4, legend_y + 0.95, 'Primary Key', fontsize=10)
    
    # Foreign Key
    fk_box = patches.Rectangle((1, legend_y + 0.4), 0.3, 0.3, 
                              facecolor=foreign_key_color, alpha=0.7)
    ax.add_patch(fk_box)
    ax.text(1.4, legend_y + 0.55, 'Foreign Key', fontsize=10)
    
    # Regular Attribute
    attr_box = patches.Rectangle((1, legend_y), 0.3, 0.3, 
                                facecolor=attribute_color, alpha=0.7)
    ax.add_patch(attr_box)
    ax.text(1.4, legend_y + 0.15, 'Regular Attribute', fontsize=10)
    
    # Entity
    entity_box = patches.Rectangle((1, legend_y - 0.4), 0.3, 0.3, 
                                  facecolor=entity_color, alpha=0.7)
    ax.add_patch(entity_box)
    ax.text(1.4, legend_y - 0.25, 'Entity', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('database_schema_erd.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def create_simple_erd():
    """Create a simple text-based ERD"""
    erd_text = """
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
    """
    
    return erd_text

if __name__ == "__main__":
    print("Generating ERD diagram...")
    
    # Create simple text ERD
    simple_erd = create_simple_erd()
    print(simple_erd)
    
    # Try to create visual ERD if matplotlib is available
    try:
        print("\nGenerating visual ERD diagram...")
        fig = create_erd_diagram()
        print("Visual ERD saved as 'database_schema_erd.png'")
    except ImportError:
        print("Matplotlib not available. Only text ERD generated.")
    except Exception as e:
        print(f"Error generating visual ERD: {e}")
        print("Text ERD generated successfully.")
