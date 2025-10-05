import tkinter as tk
import jinja2
from tkinter import ttk

jinja2.Environment(loader=jinja2.FileSystemLoader('.'))

root = tk.Tk()
tree = ttk.Treeview(root)
tree.pack(fill='both', expand=True)

# Top-level nodes
tree.insert('', 'end', iid='database', text='Database')

# Child nodes
tree.insert('database', 'end', iid='users', text='Users Table')
tree.insert('database', 'end', iid='orders', text='Orders Table')

# Sub-child nodes (simulate nested Treeview)
tree.insert('users', 'end', text='data1')
tree.insert('users', 'end', text='data2')
tree.insert('users', 'end', text='data3')

tree.insert('orders', 'end', text='data1')
tree.insert('orders', 'end', text='data2')
tree.insert('orders', 'end', text='data3')

root.mainloop()
