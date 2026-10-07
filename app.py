import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- Database Tier ---
conn = sqlite3.connect('customer.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT
)
''')
conn.commit()

# --- Logic Tier ---
def add_customer():
    if not entry_name.get() or not entry_phone.get():
        messagebox.showwarning("Warning", "Name aur Phone jaruri hai!")
        return
    cursor.execute("INSERT INTO customers (name, phone, email, address) VALUES (?,?,?,?)",
                   (entry_name.get(), entry_phone.get(), entry_email.get(), entry_address.get()))
    conn.commit()
    messagebox.showinfo("Success", "Customer Add ho gaya")
    view_customers()
    clear_entries()

def view_customers():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM customers")
    for r in cursor.fetchall():
        tree.insert("", tk.END, values=r)

def search_customer():
    for row in tree.get_children():
        tree.delete(row)
    query = search_entry.get()
    cursor.execute("SELECT * FROM customers WHERE name LIKE? OR phone LIKE?",
                   ('%'+query+'%', '%'+query+'%'))
    for r in cursor.fetchall():
        tree.insert("", tk.END, values=r)

def delete_customer():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Pehle list se customer select karo")
        return
    customer_id = tree.item(selected[0])['values'][0]
    cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    conn.commit()
    view_customers()

def fill_entries(event):
    selected = tree.selection()
    if not selected: return
    values = tree.item(selected[0])['values']
    clear_entries()
    entry_name.insert(0, values[1])
    entry_phone.insert(0, values[2])
    entry_email.insert(0, values[3])
    entry_address.insert(0, values[4])

def update_customer():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Update ke liye customer select karo")
        return
    customer_id = tree.item(selected[0])['values'][0]
    cursor.execute("UPDATE customers SET name=?, phone=?, email=?, address=? WHERE id=?",
                   (entry_name.get(), entry_phone.get(), entry_email.get(), entry_address.get(), customer_id))
    conn.commit()
    view_customers()

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    search_entry.delete(0, tk.END)

# --- GUI Tier ---
root = tk.Tk()
root.title("Customer Contact Management System")
root.geometry("900x600")

# Form
form = tk.Frame(root)
form.pack(pady=10)

tk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(form, width=25)
entry_name.grid(row=0, column=1)

tk.Label(form, text="Phone:").grid(row=0, column=2, padx=5, pady=5)
entry_phone = tk.Entry(form, width=25)
entry_phone.grid(row=0, column=3)

tk.Label(form, text="Email:").grid(row=1, column=0, padx=5, pady=5)
entry_email = tk.Entry(form, width=25)
entry_email.grid(row=1, column=1)

tk.Label(form, text="Address:").grid(row=1, column=2, padx=5, pady=5)
entry_address = tk.Entry(form, width=25)
entry_address.grid(row=1, column=3)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", command=add_customer, bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", command=update_customer, bg="#2196F3", fg="white", width=12).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_customer, bg="#f44336", fg="white", width=12).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Clear", command=clear_entries, width=12).grid(row=0, column=3, padx=5)

# Search
search_frame = tk.Frame(root)
search_frame.pack(pady=10)
tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", command=search_customer).pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Show All", command=view_customers).pack(side=tk.LEFT, padx=5)

# Table with ttk
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tree = ttk.Treeview(tree_frame, columns=("ID","Name","Phone","Email","Address"), show="headings")
for col in ("ID","Name","Phone","Email","Address"):
    tree.heading(col, text=col)
tree.column("ID", width=50)
tree.pack(fill=tk.BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", fill_entries)

view_customers()
root.mainloop()