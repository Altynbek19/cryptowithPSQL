import time
import requests
import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="adil011106",
    dbname="Info"
)
cursor = conn.cursor()

# Create a table to store the data
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS crypto_prices (
        crypto_name VARCHAR(255),
        price REAL,
        timestamp NUMERIC
    );
    """
)

# Get the name of the cryptocurrency from the user
crypto_name = input("Enter the name of the cryptocurrency: ")

while True:
    # Get the current price of the cryptocurrency
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    price = data[crypto_name]['usd']
    
    # Get the current time
    timestamp = time.time()
    
    # Insert the data into the database
    cursor.execute("INSERT INTO crypto_prices VALUES (%s, %s, %s)", (crypto_name, price, timestamp))
    conn.commit()
    
    # Print the price and time
    print(f"{crypto_name} price: {price} at {timestamp}")
    
    # Wait for 5 seconds
    time.sleep(5)

# Close the connection to the database
cursor.close()
conn.close()
