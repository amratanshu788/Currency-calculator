import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup as bs
from tkinter import *

class CurrencyConverter:
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

def fetch_conversion_rate(source_currency, target_currency):
    try:
        response = requests.get(f"https://www.x-rates.com/calculator/?from={source_currency}&to={target_currency}&amount=1")
        soup = bs(response.text, "html.parser")
        text1 = soup.find(class_="ccOutputTrail").previous_sibling
        text2 = soup.find(class_="ccOutputTrail").get_text(strip=True)
        rate = "{}{}".format(text1, text2)
        return float(rate)
    except Exception as e:
        print("Error fetching conversion rate:", e)
        return None

def clear():
    source_currency_entry.delete(0, END)
    target_currency_entry.delete(0, END)
    amount_entry.delete(0, END)
    result_label.config(text="")

def convert():
    source_currency = source_currency_entry.get().upper()
    target_currency = target_currency_entry.get().upper()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        result_label.config(text="Invalid amount")
        return
    
    rate = fetch_conversion_rate(source_currency, target_currency)
    if rate:
        result = amount * rate
        result_label.config(text=f"{result:.2f}")
    else:
        result_label.config(text="Conversion failed")

m = tk.Tk()
m.title('Currency Converter')
m.geometry("300x200")
m.eval('tk::PlaceWindow . center')

Label(m, text='Source Currency  :').grid(row=0, column=0, padx=10, pady=5)
Label(m, text='Target Currency  :').grid(row=1, column=0, padx=10, pady=5)
Label(m, text='Amount  :').grid(row=2, column=0, padx=10, pady=5)
Label(m, text='Result  :').grid(row=3, column=0, padx=10, pady=5)

source_currency_entry = Entry(m)
target_currency_entry = Entry(m)
amount_entry = Entry(m)

source_currency_entry.grid(row=0, column=1, padx=10, pady=5)
target_currency_entry.grid(row=1, column=1, padx=10, pady=5)
amount_entry.grid(row=2, column=1, padx=10, pady=5)

result_label = Label(m, text="", font='Helvetica 10 bold')
result_label.grid(row=3, column=1, padx=10, pady=5)

button = tk.Button(m, text='Convert', command=convert)
button.grid(row=4, column=0, padx=10, pady=5)

button2 = tk.Button(m, text='Clear', command=clear)
button2.grid(row=4, column=1, padx=10, pady=5)

m.mainloop()

print("done")