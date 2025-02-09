import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# Display CLI Banner
def display_cli_banner():
    banner = """
    ██████╗ ██████╗ ██╗      █████╗ ███████╗    ██╗    ██╗██╗  ██╗██╗  ██████╗██╗  ██╗███████╗
    ██╔══██╗██╔══██╗██║     ██╔══██╗██╔════╝    ██║    ██║██║  ██║██║ ██╔══██╗██║  ██║██╔════╝
    ██████╔╝██████╔╝██║     ███████║███████╗    ██║ █╗ ██║███████║██║ ██████╔╝███████║███████╗
    ██╔══██╗██╔══██╗██║     ██╔══██║╚════██║    ██║███╗██║██╔══██║██║ ██╔══██╗██╔══██║╚════██║
    ██████╔╝██║  ██║███████╗██║  ██║███████║    ╚███╔███╔╝██║  ██║██║ ██████╔╝██║  ██║███████║
    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
    """

    print("\033[1;35m" + banner)  # Display the banner in purple (ANSI color code)

# Main Application Class for CVJ Alpha Networks
class CVJAlphaNetworksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CVJ Alpha Networks")
        self.root.geometry("700x500")
        self.root.config(bg="#4B0082")  # Purple background for the main window

        # Connect to SQLite database (creates file if it doesn't exist)
        self.conn = sqlite3.connect('cvj_alpha_networks.db')
        self.cursor = self.conn.cursor()

        # Create subscriptions table if not exists
        self.create_table()

        self.create_widgets()

    def create_table(self):
        """Creates the subscriptions table in the database."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                subscription_type TEXT,
                payment_status TEXT
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="CVJ Alpha Networks", font=("Helvetica", 24, "bold"), fg="yellow", bg="#4B0082")
        title_label.pack(pady=20)

        # Subscription Management
        sub_frame = tk.Frame(self.root, bg="#4B0082")
        sub_frame.pack(pady=20)

        # User Info
        self.user_name_label = tk.Label(sub_frame, text="Enter User Name:", font=("Helvetica", 12), fg="white", bg="#4B0082")
        self.user_name_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.user_name_entry = tk.Entry(sub_frame, font=("Helvetica", 12))
        self.user_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.subscription_label = tk.Label(sub_frame, text="Subscription Type:", font=("Helvetica", 12), fg="white", bg="#4B0082")
        self.subscription_label.grid(row=1, column=0, padx=10, pady=5)

        self.subscription_type = tk.StringVar(value="Basic")
        subscription_options = ["Basic", "Premium", "VIP"]
        self.subscription_menu = tk.OptionMenu(sub_frame, self.subscription_type, *subscription_options)
        self.subscription_menu.grid(row=1, column=1, padx=10, pady=5)

        # Payment Status
        self.payment_status = tk.StringVar(value="Unpaid")
        self.payment_menu = tk.OptionMenu(sub_frame, self.payment_status, "Unpaid", "Paid")
        self.payment_menu.grid(row=2, column=1, padx=10, pady=5)

        # Add User Button
        self.add_user_button = tk.Button(self.root, text="Add Subscription", font=("Helvetica", 12), bg="green", fg="white", command=self.add_user)
        self.add_user_button.pack(pady=20)

        # Active Subscriptions
        self.active_subscriptions_label = tk.Label(self.root, text="Active Subscriptions", font=("Helvetica", 16, "bold"), fg="yellow", bg="#4B0082")
        self.active_subscriptions_label.pack(pady=10)

        # Listbox for active subscriptions
        self.subscription_listbox = tk.Listbox(self.root, width=60, height=10, font=("Helvetica", 12), bg="lightgray")
        self.subscription_listbox.pack(pady=10)

        # Renew Subscription Button
        self.renew_button = tk.Button(self.root, text="Renew Subscription", font=("Helvetica", 12), bg="blue", fg="white", command=self.renew_subscription)
        self.renew_button.pack(pady=10)

        # Load existing subscriptions
        self.load_subscriptions()

    def load_subscriptions(self):
        """Load all subscriptions from the database and display them in the listbox."""
        self.subscription_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT user_name, subscription_type, payment_status FROM subscriptions")
        rows = self.cursor.fetchall()
        for row in rows:
            self.subscription_listbox.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]}")

    def add_user(self):
        # Get user data
        user_name = self.user_name_entry.get()
        subscription_type = self.subscription_type.get()
        payment_status = self.payment_status.get()

        if user_name:
            # Insert into database
            self.cursor.execute("INSERT INTO subscriptions (user_name, subscription_type, payment_status) VALUES (?, ?, ?)", 
                                (user_name, subscription_type, payment_status))
            self.conn.commit()
            
            # Update the listbox
            self.load_subscriptions()
            
            messagebox.showinfo("Subscription Added", f"Subscription added for {user_name} ({subscription_type}) with status: {payment_status}")
        else:
            messagebox.showwarning("Input Error", "Please enter a user name.")

    def renew_subscription(self):
        # Get selected subscription
        selected_user = self.subscription_listbox.curselection()
        
        if selected_user:
            # Get the details of the selected user
            user_details = self.subscription_listbox.get(selected_user)
            user_name = user_details.split(" - ")[0]
            
            # Update the payment status to "Paid" in the database
            self.cursor.execute("UPDATE subscriptions SET payment_status = ? WHERE user_name = ?", ("Paid", user_name))
            self.conn.commit()
            
            # Update the listbox
            self.load_subscriptions()
            
            messagebox.showinfo("Subscription Renewed", "Subscription has been successfully renewed!")
        else:
            messagebox.showwarning("Selection Error", "Please select a subscription to renew.")

# Main Execution
if __name__ == "__main__":
    # Display CLI Banner
    os.system("clear")  # Clear the terminal screen (use "cls" for Windows)
    display_cli_banner()  # Display the colorful CLI banner

    # Start the GUI
    root = tk.Tk()
    app = CVJAlphaNetworksApp(root)
    root.mainloop()

