Golden Grove Colections - E-Commerce Website for Selling Clothes

Overview
This is an e-commerce website designed for selling clothing items.
It includes features like product browsing, adding to cart, checkout, and user authentication.

Features
* User Registration and Login
* Product Browsing
* Cart Management
* Secure Checkout with Payment Integration
* Admin Dashboard for Product Management

How to Run the Application
Prerequisites
1. Ensure Python 3.9+ is installed.
2. Install the necessary dependencies using pip install -r requirements.txt.
3. Ensure you have a database (e.g., SQLite or PostgreSQL) set up.
Steps
1. Clone this repository:bash Copy code   git clone https://github.com/Darline-Konadu/Golden-Grove-Collections
2. cd https://github.com/Darline-Konadu/Golden-Grove-Collections
3. Install dependencies:bash Copy code   pip install -r requirements.txt
4. Set up environment variables: Create a .env file in the root directory and add:plaintext Copy code   SECRET_KEY=your_secret_key
5. DEBUG=True
6.DATABASE_URL=Database not hosted, we used django's inbuilt database manager   
7. Apply migrations:bash Copy code   python manage.py migrate
8. Run the server:bash Copy code   python manage.py runserver
9. Open the application in your browser: Navigate to http://127.0.0.1:8000/

Screenshots
Home Page

![homepage](https://github.com/user-attachments/assets/78befef1-0bb5-4c47-b48e-bae585a91cfe)
Product Page

![productpage](https://github.com/user-attachments/assets/7574b578-35f5-41f6-97b1-82a315810b01)
Cart Page

![cart](https://github.com/user-attachments/assets/70b7bbdd-1568-4006-bce7-28343fe45ee5)


Checkout Page
![checkout](https://github.com/user-attachments/assets/2eed436a-44ad-40f2-845c-601c186f1773)





Contributors ;
Richard Asiedu Bentum
Darline Konadu Amoafo
