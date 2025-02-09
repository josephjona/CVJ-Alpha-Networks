import time
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import talib
import requests
import smtplib
import pyfiglet
from colorama import Fore, Style, init
import tkinter as tk
from tkinter import ttk

# Initialize Colorama
init()

# Display CLI Banner
def display_banner():
    banner_text = pyfiglet.figlet_format("CVJ Alpha", font="slant")
    print(Fore.MAGENTA + banner_text)  # Purple
    print(Fore.YELLOW + "🚀 AI-Powered Trading Bot for Pocket Option")
    print(Fore.GREEN + "✅ Automated Trading | ✅ Risk Management | ✅ AI Trade Timing")
    print(Fore.CYAN + "📊 Multi-Timeframe Analysis | 📢 Telegram & Email Alerts")
    print(Style.RESET_ALL)

display_banner()

# GUI Class for Trade Monitoring
class TradingBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CVJ Alpha - Trading Bot")
        self.root.geometry("600x400")
        self.root.configure(bg="#1e1e1e")

        self.balance_label = tk.Label(root, text="Balance: $0.00", font=("Arial", 14), fg="green", bg="#1e1e1e")
        self.balance_label.pack()

        self.trades_label = tk.Label(root, text="Active Trades: 0", font=("Arial", 14), fg="cyan", bg="#1e1e1e")
        self.trades_label.pack()

        self.start_button = ttk.Button(root, text="Start Bot", command=self.start_bot)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(root, text="Stop Bot", command=self.stop_bot)
        self.stop_button.pack(pady=5)

        self.log_box = tk.Text(root, height=10, width=60, bg="#333", fg="white")
        self.log_box.pack(pady=10)

    def update_balance(self, balance):
        self.balance_label.config(text=f"Balance: ${balance:.2f}")

    def update_trades(self, trades):
        self.trades_label.config(text=f"Active Trades: {trades}")

    def log_message(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def start_bot(self):
        self.log_message("🚀 Bot started...")

    def stop_bot(self):
        self.log_message("🛑 Bot stopped.")

# Initialize WebDriver
def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without opening a browser
    driver = webdriver.Chrome(options=options)
    driver.get("https://pocketoption.com")
    return driver

# Fetch Real Balance from Pocket Option
def get_account_balance(driver, gui):
    try:
        balance_element = driver.find_element(By.CLASS_NAME, "balance-class")  # Adjust selector
        balance = float(balance_element.text.replace("$", ""))
        gui.update_balance(balance)
        return balance
    except:
        return None

# AI-Based Trade Execution
def ai_trade_execution(df, balance, gui):
    trade_signal, trade_size = None, 0
    df["RSI"] = talib.RSI(df["Close"], timeperiod=14)
    macd, macdsignal, _ = talib.MACD(df["Close"], fastperiod=12, slowperiod=26, signalperiod=9)
    df["MACD_Trend"] = macd - macdsignal

    latest_data = df.iloc[-1]

    if latest_data["RSI"] < 30 and latest_data["MACD_Trend"] > 0:
        trade_signal = "BUY"
    elif latest_data["RSI"] > 70 and latest_data["MACD_Trend"] < 0:
        trade_signal = "SELL"

    if trade_signal:
        trade_size = balance * 0.02
        gui.log_message(f"Executing {trade_signal} | Size: ${trade_size:.2f}")
    
    return trade_signal, trade_size

# Automated Signal-Based Trading
def execute_trade(driver, trade_signal, trade_size):
    try:
        if trade_signal == "BUY":
            buy_button = driver.find_element(By.ID, "buy-button")  # Adjust ID
            buy_button.click()
        elif trade_signal == "SELL":
            sell_button = driver.find_element(By.ID, "sell-button")  # Adjust ID
            sell_button.click()
    except Exception as e:
        print(f"Error executing trade: {e}")

# Risk Management & Money Management
def calculate_trade_size(balance, risk_percentage=2):
    return balance * (risk_percentage / 100)

# Send Telegram Notification
def send_telegram_alert(message):
    bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

# Send Email Alert
def send_email_alert(subject, message):
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver_email@gmail.com"
    password = "your_password"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{message}")
    server.quit()

# Main Function
def main():
    driver = initialize_driver()
    gui.update_balance(1000)  # Dummy balance for testing
    gui.update_trades(0)

    while True:
        balance = get_account_balance(driver, gui)
        df = pd.DataFrame({"Close": np.random.randn(50) * 10 + 100})  # Dummy data for testing
        trade_signal, trade_size = ai_trade_execution(df, balance, gui)

        if trade_signal:
            execute_trade(driver, trade_signal, trade_size)
            gui.update_trades(1)
            send_telegram_alert(f"Trade Executed: {trade_signal}, Size: ${trade_size:.2f}")
            send_email_alert("Trade Alert", f"Trade Executed: {trade_signal}, Size: ${trade_size:.2f}")

        time.sleep(60)  # Wait 1 minute before checking again

# Start GUI
if __name__ == "__main__":
    root = tk.Tk()
    gui = TradingBotGUI(root)
    root.after(1000, main)
    root.mainloop()

