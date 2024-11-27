## To starts server type (`python app.py`) in console

## 1. Home Page (`/`)
**URL (method):** `/` (GET)  
**Description:**  
The main page of the site displaying featured cars.

- **Data shown on the page:**  
  - A list of featured cars with images, names, and prices.  

- **Actions the user can take:**  
  - Browse the list of featured cars.  

- **What’s on the page:**  
  - Car cards displaying images, names, and prices.

---

## 2. Car Details (`/car/<id>`)
**URL (method):** `/car/<id>` (GET)  
**Description:**  
The page displaying detailed information about a specific car. The page is accessed by the car's unique `id`.

- **Data shown on the page:**  
  - Car details: name, brand, price.

- **Actions the user can take:**  
  - Add the car to the wishlist (via POST request).  

- **What’s on the page:**  
  - car description.  
  - An "Add to Wishlist" button.  

**URL (method):** `/car/<id>/add_to_wishlist` (POST)  
**Description:**  
Adds the car to the user's wishlist.

- **Actions the user can take:**  
  - Submit the POST request to add the car to the wishlist.

---

## 3. Wishlist Page (`/wishlist`)
**URL (method):** `/wishlist` (GET)  
**Description:**  
The page displaying all cars that the user has added to their wishlist.

- **Data shown on the page:**  
  - List of cars in the wishlist (with images, names, and prices).

- **Actions the user can take:**  
  - Remove cars from the wishlist (via POST request).  

- **What’s on the page:**  
  - A list of cars with "Remove" buttons.  

---

## 4. Remove from Wishlist (`/wishlist/remove`)
**URL (method):** `/wishlist/remove` (POST)  
**Description:**  
Allows the user to remove a car from their wishlist.

- **Actions the user can take:**  
  - Submit the POST request to remove a car from the wishlist.
