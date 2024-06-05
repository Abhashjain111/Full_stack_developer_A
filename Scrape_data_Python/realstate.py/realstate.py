import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import csv

class RealEstateScraper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Real Estate Scraper")
        self.search_label = tk.Label(self.root, text="Search for a suburb:")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.root, width=30)
        self.search_entry.pack(pady=5)
        self.scrape_button = tk.Button(self.root, text="Scrape Properties", command=self.scrape_and_save)
        self.scrape_button.pack(pady=20)

    def scrape_data(self, search_query):
        search_url = f"https://www.realestate.com.au/buy/{search_query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        listings = soup.find_all('article', class_='property-info')
        properties = []
        for listing in listings:
            # Extract the data from each listing
            title = listing.find('h2', class_ = 'property-info__header').text.strip()
            address = listing.find('span', class_='residential-card__address-text').text.strip()
            price = listing.find('span', class_='property-price').text.strip()
            bedrooms = listing.find('span', class_='general-features__icon general-features__beds').find_next_sibling('span').text.strip()
            bathrooms = listing.find('span', class_='general-features__icon general-features__baths').find_next_sibling('span').text.strip()
            car_spaces = listing.find('span', class_='general-features__icon general-features__cars').find_next_sibling('span').text.strip()
            agent = listing.find('div', class_='listing-card__agent').text.strip()
            properties.append({
                'Title': title,
                'Address': address,
                'Price': price,
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms,
                'Car Spaces': car_spaces,
                'Agent': agent
            })
        return properties

    def save_to_csv(self, properties):
        with open('properties.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Title', 'Address', 'Price', 'Bedrooms', 'Bathrooms', 'Car Spaces', 'Agent'])
            writer.writeheader()
            writer.writerows(properties)
        messagebox.showinfo("Success", "Data successfully saved to CSV file!")

    def scrape_and_save(self):
        search_query = self.search_entry.get()
        if not search_query:
            messagebox.showerror("Error", "Please enter a search query!")
            return
        properties = self.scrape_data(search_query)
        self.save_to_csv(properties)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    scraper = RealEstateScraper()
    scraper.run()

  ##  """""
##Implementation Process:

#Created a RealEstateScraper class to encapsulate the script's functionality.
#Defined the scrape_data method to send a GET request to the Real Estate website, parse the HTML response, and extract the property details.
#Defined the save_to_csv method to save the scraped data to a CSV file.
#Defined the scrape_and_save method to call the scrape_data and save_to_csv methods when the button is clicked.
#Created a GUI using tkinter with a search bar and a button to scrape properties.
#Ran the script using the if __name__ == "__main__": block.
