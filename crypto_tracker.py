import requests
import sys

def fetch_prices(crypto_ids=None):
    """Fetches cryptocurrency prices from CoinGecko API."""
    if crypto_ids is None:
        crypto_ids = ["bitcoin", "ethereum"]
    
    ids_string = ",".join(crypto_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_string}&vs_currencies=usd,inr"
    
    try:
        print(f"Fetching prices for: {', '.join(crypto_ids)}...")
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful
        response.raise_for_status() 
        
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def display_prices(data):
    """Displays prices in a user-friendly format."""
    if not data:
        print("No data to display or invalid cryptocurrency ID.")
        return

    print("\n--- Cryptocurrency Prices ---")
    for crypto, details in data.items():
        try:
            price_usd = details.get('usd')
            price_inr = details.get('inr')
            
            if price_usd is not None and price_inr is not None:
                print(f"{crypto.capitalize()}: ${price_usd:,.2f} / ₹{price_inr:,.2f}")
            else:
                 print(f"{crypto.capitalize()}: Price data incomplete")

        except KeyError:
            print(f"Could not find price for {crypto}")
    print("-----------------------------")

if __name__ == "__main__":
    while True:
        print("\nOptions:")
        print("1. Get general prices (Bitcoin, Ethereum)")
        print("2. Get price of a specific cryptocurrency")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            prices = fetch_prices()
            display_prices(prices)
        elif choice == '2':
            crypto_input = input("Enter the cryptocurrency ID (e.g., 'dogecoin', 'solana'): ").strip().lower()
            if crypto_input:
                prices = fetch_prices([crypto_input])
                display_prices(prices)
            else:
                print("Invalid input.")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
