import tkinter as tk
from tkinter import ttk
from collections import defaultdict
import sqlite3


class SantasInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Santa's Enhanced Inventory Management System")
        self.database_setup()
        self.setup_ui()

    def database_setup(self):
        """Initialize the SQLite database."""
        self.conn = sqlite3.connect("santas_inventory.db")
        self.cursor = self.conn.cursor()

        # Create Tables
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT UNIQUE NOT NULL,
            stock INTEGER NOT NULL
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS elf_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            elf_name TEXT UNIQUE NOT NULL,
            score INTEGER NOT NULL
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sleigh_loading (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gift_name TEXT NOT NULL,
            child_name TEXT NOT NULL,
            status TEXT NOT NULL
        )""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS child_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT NOT NULL,
            feedback TEXT NOT NULL
        )""")
        self.conn.commit()

    def setup_ui(self):
        # Add festive colors
        self.root.configure(bg="white")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="white", foreground="green")
        style.configure("TNotebook.Tab", background="lightgreen", foreground="red")
        style.configure("TFrame", background="white")

        # Notebook for tabs
        notebook = ttk.Notebook(self.root, style="TNotebook")
        notebook.pack(expand=True, fill="both")

        # Tabs
        inventory_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(inventory_frame, text="Inventory")
        self.setup_inventory_tab(inventory_frame)

        elf_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(elf_frame, text="Elf Management")
        self.setup_elf_management_tab(elf_frame)

        sleigh_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(sleigh_frame, text="Sleigh Loading")
        self.setup_sleigh_loading_tab(sleigh_frame)

        feedback_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(feedback_frame, text="Child Feedback")
        self.setup_feedback_tab(feedback_frame)

    # Inventory Tab
    def setup_inventory_tab(self, frame):
        ttk.Label(frame, text="Item:", background="white", foreground="green").grid(row=0, column=0, padx=10, pady=10)
        self.item_entry = ttk.Entry(frame)
        self.item_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Stock:", background="white", foreground="green").grid(row=1, column=0, padx=10, pady=10)
        self.stock_entry = ttk.Entry(frame)
        self.stock_entry.grid(row=1, column=1, padx=10, pady=10)

        add_button = ttk.Button(frame, text="Add Stock", command=self.add_stock)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.inventory_listbox = tk.Listbox(frame, height=10, width=50, bg="lightgreen", fg="red")
        self.inventory_listbox.grid(row=3, column=0, columnspan=2, pady=10)

        self.refresh_inventory_list()

    def add_stock(self):
        """Add stock to the database."""
        item = self.item_entry.get()
        try:
            stock = int(self.stock_entry.get())
            self.cursor.execute("""
            INSERT INTO inventory (item, stock) VALUES (?, ?) 
            ON CONFLICT(item) DO UPDATE SET stock = stock + ?""", 
            (item, stock, stock))
            self.conn.commit()
            self.refresh_inventory_list()
        except ValueError:
            print("Invalid stock value")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def refresh_inventory_list(self):
        """Refresh the inventory list from the database."""
        self.inventory_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT item, stock FROM inventory")
        for row in self.cursor.fetchall():
            self.inventory_listbox.insert(tk.END, f"{row[0]}: {row[1]} in stock")

    # Elf Management Tab
    def setup_elf_management_tab(self, frame):
        ttk.Label(frame, text="Elf Name:", background="white", foreground="green").grid(row=0, column=0, padx=10, pady=10)
        self.elf_name_entry = ttk.Entry(frame)
        self.elf_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(frame, text="SantaCoins:", background="white", foreground="green").grid(row=1, column=0, padx=10, pady=10)
        self.elf_score_entry = ttk.Entry(frame)
        self.elf_score_entry.grid(row=1, column=1, padx=10, pady=10)

        add_elf_button = ttk.Button(frame, text="Add Elf Score", command=self.add_elf_score)
        add_elf_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.elf_listbox = tk.Listbox(frame, height=10, width=50, bg="lightgreen", fg="red")
        self.elf_listbox.grid(row=3, column=0, columnspan=2, pady=10)

        self.refresh_elf_list()

    def add_elf_score(self):
        """Add elf score to the database."""
        elf_name = self.elf_name_entry.get()
        try:
            score = int(self.elf_score_entry.get())
            self.cursor.execute("""
            INSERT INTO elf_scores (elf_name, score) VALUES (?, ?) 
            ON CONFLICT(elf_name) DO UPDATE SET score = score + ?""", 
            (elf_name, score, score))
            self.conn.commit()
            self.refresh_elf_list()
        except ValueError:
            print("Invalid SantaCoins value")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def refresh_elf_list(self):
        """Refresh the elf list from the database."""
        self.elf_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT elf_name, score FROM elf_scores")
        for row in self.cursor.fetchall():
            self.elf_listbox.insert(tk.END, f"{row[0]}: {row[1]} SantaCoins")

    # Sleigh Loading Tab
    def setup_sleigh_loading_tab(self, frame):
        ttk.Label(frame, text="Gift Name:", background="white", foreground="green").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(frame, text="Child Name:", background="white", foreground="green").grid(row=1, column=0, padx=10, pady=10)
        # Add more as needed...

    # Feedback Tab
    def setup_feedback_tab(self, frame):
        ttk.Label(frame, text="Child Name:", background="white", foreground="green").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(frame, text="Feedback:", background="white", foreground="green").grid(row=1, column=0, padx=10, pady=10)
        # Add more as needed...

    def __del__(self):
        """Close the database connection on app exit."""
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = SantasInventoryApp(root)
    root.mainloop()

