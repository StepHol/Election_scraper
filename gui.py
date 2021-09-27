import tkinter as tk
import os
from election_scraper import main as scraper_main

def run_scrape(url, filename):
    dir = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(dir, filename)
    print(f"Scraping {url} to {file}.")
    scraper_main(url, file)

def main():
    master = tk.Tk()

    # row URL
    label_url = tk.Label(master, text="URL to scrape: ")
    label_url.grid(row=0, column=0)
    entry_url = tk.Entry(master)
    entry_url.grid(row=0, column=1)
    entry_url.insert(tk.END, 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103')

    # row filename
    label_filename = tk.Label(master, text="Filename to output: ")
    label_filename.grid(row=1, column=0)
    entry_filename = tk.Entry(master)
    entry_filename.grid(row=1, column=1)
    entry_filename.insert(tk.END, "results_prostejov.csv")

    #button scrape
    button_scrape = tk.Button(master, text='Scrape', command=lambda: run_scrape(entry_url.get(), entry_filename.get()))
    button_scrape.grid(row=3, column=1, sticky=tk.W, pady=4)
    print(button_scrape.cget("command"))

    tk.mainloop()

if __name__ == "__main__":
    main()