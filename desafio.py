# ====================================================================================================================================================
# PROJECT: Order Management System
# DESCRIPTION: A Python-based terminal application to manage customer orders.
# AUTHOR: [AXIOM]
# ====================================================================================================================================================

#_____________________________________________________________________________________________________________________________________________________
# 1. DATA STRUCTURES INITIALIZATION (The Database)
# Each variable is a DICTIONARY.
#_____________________________________________________________________________________________________________________________________________________
# Stores: customer_id -> {"name": str, "email": str}
database_customers = {}

# Stores: product_id -> (product_name, unit_price) -- Tuple used for product info
database_products = {}

# Stores: order_id -> {"customer_id": str, "product_id": str, "quantity": int, "unit_price": float, "total": float}
database_orders = {}

# Unique ID counter for orders
order_id_counter = 1

#=====================================================================================================================================================
# 2. MODULAR FUCCTIONS (Business Logic)
# RULE: All functions must RECEIVE parameters and RETURN data. 
#=====================================================================================================================================================

# --- MÓDULO 1: Customer Management ---
# Integrante Asignado: [Fernando Santos]

def validate_new_customer_id(customers_dict, customer_id):
    """Checks if a customer ID already exists.
Returns True if valid (unique)."""
# Using 'in' operator directly on the dictionary keys.
    if customer_id in customers_dict:
        return False
    return True

def create_customer_data(id_val, name_val, email_val):
    """Creates a dictionary representing customer data. RETURNS a dictionary."""
    return {"name": name_val, "email": email_val}

# --- MÓDULO 2: Product Management ---
# Integrante Asignado: [Jenrry Monsalve]

def validate_new_product_id(products_dict, product_id):
    """Checks if a product ID already exists. Returns True if valid (unique)."""
    # Using 'in' operator directly on the dictionary keys.
    if product_id in products_dict:
        return False
    return True

def create_product_data(id_val, name_val, price_val):
    """Creates a tuple representing product data. RETURNS a tuple."""
    # Product data (name, price) is stored as a tuple because it's immutable for this exercise.
    return (name_val, price_val)


#--- MÓDULO 3: Order Creation ---
 #Integrante Asignado: [Sebastian Mendoza]
def create_order_data(orders_dict, order_id_val, customer_id_val, product_id_val, quantity_val, unit_price_val):
    """Calculates the order total and creates a dictionary for the order. RETURNS a dictionary."""
    calculated_total = quantity_val * unit_price_val
    order_data = {
        "customer_id": customer_id_val,
        "product_id": product_id_val,
        "quantity": quantity_val,
        "unit_price": unit_price_val,
        "total": calculated_total
    }
    return order_data


# --- MÓDULO 4: Sales Reporting (View & Revenue) ---
# Integrante Asignado: [Fernando Santos]
def format_all_orders_view(orders_dict, customers_dict, products_dict):
    """Generates a formatted string of all registered orders. RETURNS a formatted string."""
    if not orders_dict:
        return "\nNo orders have been registered yet."

    formatted_output = "\n--- Registered Orders ---"
    # We iterate over dictionary keys (order_ids).
    for order_id in orders_dict:
        order_info = orders_dict[order_id]
        customer_id = order_info["customer_id"]
        product_id = order_info["product_id"]

        # Get names for display, defaulting to IDs if not found (just in case)
        customer_name = customers_dict.get(customer_id, {}).get("name", customer_id)
        # Remember product data is a tuple: (name, price)
        product_tuple = products_dict.get(product_id, (product_id, 0))
        product_name = product_tuple[0]

        formatted_output += f"\n  Order ID: {order_id}\n"
        formatted_output += f"    Customer: {customer_name} (ID: {customer_id})\n"
        formatted_output += f"    Product:  {product_name} (ID: {product_id})\n"
        formatted_output += f"    Quantity: {order_info['quantity']}\n"
        formatted_output += f"    Total:    {order_info['total']}\n"

    return formatted_output

def calculate_total_daily_revenue(orders_dict):
    """Sums the total field of all orders. RETURNS the sum."""
    revenue_sum = 0.0
    # We iterate over dictionary keys.
    for order_id in orders_dict:
        order_info = orders_dict[order_id]
        revenue_sum += order_info["total"]
    return revenue_sum


#--- MÓDULO 5: Final Consolidated Report ---
# Integrante Asignado: [Jenrry Monsalve - Sustentador]

def generate_final_report_string(orders_dict, customers_dict, products_dict):
    """Creates a consolidated daily sales report. RETURNS a formatted string."""
    if not orders_dict:
        return "\n--- Final Sales Report ---\nNo sales recorded today."

    total_orders = len(orders_dict)
    total_revenue = calculate_total_daily_revenue(orders_dict)

    # Dictionary to store revenue per customer
    # customer_id -> revenue_sum
    revenue_per_customer = {}

    # Dictionary to store product unit sales
    # product_id -> units_sum
    units_per_product = {}

    # Gather data for consolidation
    for order_id in orders_dict:
        order_info = orders_dict[order_id]
        c_id = order_info["customer_id"]
        p_id = order_info["product_id"]
        order_total = order_info["total"]
        order_quantity = order_info["quantity"]

        # Consolidate revenue per customer
        current_customer_revenue = revenue_per_customer.get(c_id, 0.0)
        revenue_per_customer[c_id] = current_customer_revenue + order_total

        # Consolidate units per product
        current_product_units = units_per_product.get(p_id, 0)
        units_per_product[p_id] = current_product_units + order_quantity

    # Find top selling product
    top_product_id = "None"
    max_units = 0
    # Iterating over units_per_product dictionary
    for prod_id in units_per_product:
        units_count = units_per_product[prod_id]
        if units_count > max_units:
            max_units = units_count
            top_product_id = prod_id

    # Remember products data is a tuple: (name, price)
    top_product_tuple = products_dict.get(top_product_id, (top_product_id, 0))
    top_product_name = top_product_tuple[0]

    # --- Formatting the Output ---
    report_string = "\n--- FINAL SALES REPORT ---"
    report_string += f"\nTotal Orders: {total_orders}"
    report_string += f"\nTotal Revenue: ${total_revenue:.2f}"
    report_string += "\n\n1. Revenue per Customer:"
# Iterating over revenue_per_customer dictionary
    for cust_id in revenue_per_customer:
        c_revenue = revenue_per_customer[cust_id]
        c_name = customers_dict.get(cust_id, {}).get("name", cust_id)
        report_string += f"\n  - {c_name}: ${c_revenue:.2f}"

    report_string += f"\n\n2. Best Selling Product: {top_product_name} ({max_units} units sold)"
    report_string += "\n"
    report_string += "\n End of Report \n"

    return report_string


# ==============================================================================

#    MAIN PROGRAM LOOP (Terminal Menu Interface)

# Integrante Asignado: [Fernando Santos - Líder]
# ==============================================================================
def display_menu():
    """Prints the main menu options to the terminal."""
    print("\n--- Riwi Order Management System ---")
    print("1. Register a Customer")
    print("2. Register a Product")
    print("3. Create a New Order")
    print("4. View All Registered Orders")
    print("5. Calculate Total Daily Revenue")
    print("6. Generate Final Consolidated Report")
    print("7. Exit")

def run_application():
    """Starts and runs the main program loop."""
    # Use global to modify order_id_counter from the global scope.
    global order_id_counter
while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ")

        # --- Choice 1: Register Customer ---
        if choice == '1':
            print("\n--- Registering Customer ---")
            cust_id = input("Enter Customer ID: ")

            # VALIDATION FUNCTION
            if not validate_new_customer_id(database_customers, cust_id):
                print(f"\nERROR: Customer ID '{cust_id}' already exists.")
            else:
                cust_name = input("Enter Customer Name: ")
                cust_email = input("Enter Customer Email: ")
                # CREATE DATA FUNCTION (RETURNS dictionary)
                new_customer_data = create_customer_data(cust_id, cust_name, cust_email)
                # ADDING TO DICTIONARY (key -> value)
                database_customers[cust_id] = new_customer_data
                print(f"\nSUCCESS: Customer '{cust_name}' registered.")
# --- Choice 2: Register Product ---
        elif choice == '2':
            print("\n--- Registering Product ---")
            prod_id = input("Enter Product ID: ")

            # VALIDATION FUNCTION
            if not validate_new_product_id(database_products, prod_id):
                print(f"\nERROR: Product ID '{prod_id}' already exists.")
            else:
                prod_name = input("Enter Product Name: ")
                prod_price_str = input("Enter Product Unit Price: ")
                try:
                    prod_price = float(prod_price_str)
                    # CREATE DATA FUNCTION (RETURNS tuple)
                    new_product_tuple = create_product_data(prod_id, prod_name, prod_price)
                    # ADDING TO DICTIONARY (key -> value)
                    database_products[prod_id] = new_product_tuple
                    print(f"\nSUCCESS: Product '{prod_name}' registered.")
                except ValueError:
                    print("\nERROR: Invalid price format. Must be a number.")
# --- Choice 3: Create Order ---
        elif choice == '3':
            print("\n--- Creating New Order ---")
            cust_id = input("Enter Customer ID: ")
            prod_id = input("Enter Product ID: ")

            # Check if both customer and product exist using dictionary keys
            if cust_id not in database_customers or prod_id not in database_products:
                print(f"\nERROR: Could not create order. Customer ID '{cust_id}' or Product ID '{prod_id}' does not exist.")
            else:
                qty_str = input("Enter Quantity: ")
                try:
                    qty = int(qty_str)
                    if qty <= 0:
                        print("\nERROR: Quantity must be a positive integer.")
                    else:
                        # Get unit price from product tuple: (name, price)
                        product_data_tuple = database_products[prod_id]
                        unit_price = product_data_tuple[1]

                        # CREATE DATA FUNCTION (RETURNS dictionary, calculates total)
                        new_order_data_dict = create_order_data(database_orders, order_id_counter, cust_id, prod_id, qty, unit_price)

# ADDING TO DICTIONARY (key -> value, using order_id_counter)
                        database_orders[order_id_counter] = new_order_data_dict
                        print(f"\nSUCCESS: Order ID {order_id_counter} created for {qty} {product_data_tuple[0]}(s).")
                        order_id_counter += 1
                except ValueError:
                    print("\nERROR: Invalid quantity format. Must be an integer.")

        # --- Choice 4: View Orders ---
        elif choice == '4':
            # REPORTING FUNCTION (RETURNS formatted string)
            formatted_view = format_all_orders_view(database_orders, database_customers, database_products)
            print(formatted_view)

# --- Choice 5: Calculate Revenue ---
        elif choice == '5':
            # REVENUE FUNCTION (RETURNS sum)
            revenue_total = calculate_total_daily_revenue(database_orders)
            print(f"\nTotal daily revenue so far: ${revenue_total:.2f}")

        # --- Choice 6: Generate Final Report ---
        elif choice == '6':
            # REPORTING FUNCTION (RETURNS consolidated report string)
            final_report_content = generate_final_report_string(database_orders, database_customers, database_products)
            print(final_report_content)

        # --- Choice 7: Exit ---
        elif choice == '7':
            print("\nExiting the Riwi Order Management System. Have a great day!")
            break

        # --- Invalid Choice Handling ---
        else:
            print("\nERROR: Invalid choice. Please enter a number between 1 and 7.")
# ==============================================================================

#    PROGRAM EXECUTION

# ==============================================================================
if __name__ == "__main__":
    run_application()
