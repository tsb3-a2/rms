from prettytable import PrettyTable
from datetime import datetime
import os
import sys
import time

shopping_cart = {}
inventory_database = {}
customer_database = {}
sales_database = {}

def add_to_shopping_cart():
    inventory_id = str(input("Enter inventory ID: "))
    shopping_cart_quantity = int(input("Enter quantity: "))
    if inventory_id in inventory_database:
        available_quantity = inventory_database[inventory_id]["inventory_quantity"]
        if available_quantity >= shopping_cart_quantity:
            if available_quantity - shopping_cart_quantity <= inventory_database[inventory_id]["reorder_level"]:
                print("Reorder level is reached or exceeded!")
                time.sleep(2)
            if inventory_id in shopping_cart:
                shopping_cart[inventory_id]["shopping_cart_quantity"] += shopping_cart_quantity
            else:
                shopping_cart[inventory_id] = {
                    "inventory_id": inventory_database[inventory_id]["inventory_id"],
                    "inventory_name": inventory_database[inventory_id]["inventory_name"],
                    "selling_price": inventory_database[inventory_id]["selling_price"],
                    "shopping_cart_quantity": shopping_cart_quantity
                }
            inventory_database[inventory_id]["inventory_quantity"] -= shopping_cart_quantity
            print(f"{inventory_id} : {inventory_database[inventory_id]['inventory_name']} : {shopping_cart_quantity} added to shopping cart!")
            time.sleep(2)
            return
        else:
            print("Invalid input, insufficient quantity!")
            time.sleep(2)
            return
    else:
        print("Invalid input, inventory not found!")
        time.sleep(2)
        return

def remove_from_shopping_cart():
    if not shopping_cart:
        print("Shopping cart is empty!")
        time.sleep(2)
        return
    inventory_id = str(input("Enter inventory ID: "))
    shopping_cart_quantity = int(input("Enter quantity: "))
    if inventory_id in inventory_database and inventory_id in shopping_cart:
        current_quantity = shopping_cart[inventory_id]["shopping_cart_quantity"]
        if current_quantity >= shopping_cart_quantity:
            shopping_cart[inventory_id]["shopping_cart_quantity"] -= shopping_cart_quantity
            inventory_database[inventory_id]["inventory_quantity"] += shopping_cart_quantity
            print(f"{inventory_id} : {inventory_database[inventory_id]['inventory_name']} : {shopping_cart_quantity} remove from shopping cart!")
            time.sleep(2)
            if shopping_cart[inventory_id]["shopping_cart_quantity"] == 0:
                del shopping_cart[inventory_id]
            return
        else:
            print(f"Invalid input, there is only {current_quantity} {shopping_cart[inventory_id]['inventory_name']} in the shopping cart!")
            time.sleep(2)
            return
    else:
        print("Invalid input, inventory not found or insufficient quantity!")
        time.sleep(2)
        return

def display_shopping_cart():
    if not shopping_cart:
        print("Shopping cart is empty!")
        time.sleep(2)
        return
    table = PrettyTable()
    table.field_names = ["Inventory ID", "Inventory Name", "Selling Price", "Quantity", "Total"]
    for inventory_id, shopping_cart_item in shopping_cart.items():
        table.add_row([inventory_id, shopping_cart_item["inventory_name"], f"{shopping_cart_item['selling_price']:.2f}", shopping_cart_item["shopping_cart_quantity"], round(shopping_cart_item["selling_price"] * shopping_cart_item["shopping_cart_quantity"], 2)])
    print()
    print(table)
    print()
    input("Press ENTER to continue!")
    return

def customer_membership_validation():
    while True:
        customer_id = str(input("Enter customer ID: "))
        if customer_id in customer_database:
            return customer_id
        else:
            print("Invalid input, customer not found!")
            time.sleep(2)
            while True:
                retype_customer_id = str(input("Would you like to retype the customer ID? [y/n]: "))
                if retype_customer_id.upper() == "Y":
                    break
                elif retype_customer_id.upper() == "N":
                    return
                else:
                    print("Invalid input, please select 'Y' or 'N'!")
                    time.sleep(2)
                    continue

def proceed_to_payment():
    if not shopping_cart:
        print("Shopping cart is empty!")
        time.sleep(2)
        return
    table = PrettyTable()
    table.field_names = ["Inventory ID", "Inventory Name", "Selling Price", "Quantity", "Total"]
    for inventory_id, shopping_cart_item in shopping_cart.items():
        table.add_row([inventory_id, shopping_cart_item["inventory_name"], f"{shopping_cart_item['selling_price']:.2f}", shopping_cart_item["shopping_cart_quantity"], round(shopping_cart_item["selling_price"] * shopping_cart_item["shopping_cart_quantity"], 2)])
    print()
    print(table)
    print()
    while True:
        confirm_payment = str(input("Would you like to confirm the payment? [y/n]: "))
        if confirm_payment.upper() == "Y":
            while True:
                customer_membership = str(input("Do you currently hold a membership? [y/n]: "))
                if customer_membership.upper() == "Y":
                    customer_id = customer_membership_validation()
                    if customer_id is not None:
                        subtotal = sum(shopping_cart_item["selling_price"] * shopping_cart_item["shopping_cart_quantity"] for shopping_cart_item in shopping_cart.values())
                        total = subtotal * (1 - 5 / 100)
                        for inventory_id, shopping_cart_item in shopping_cart.items():
                            if inventory_id in sales_database:
                                sales_database[inventory_id] += shopping_cart_item["selling_price"] * shopping_cart_item["shopping_cart_quantity"]
                            else:
                                sales_database[inventory_id] = shopping_cart_item["selling_price"] * shopping_cart_item["shopping_cart_quantity"]
                        break
                    else:
                        print("Membership validation is skipped!")
                        time.sleep(2)
                        subtotal = 0
                        total = sum(shopping_cart_item["selling_price"] * shopping_cart_item["shopping_cart_quantity"] for shopping_cart_item in shopping_cart.values())
                        for inventory_id, shopping_cart_item in shopping_cart.items():
                            if inventory_id in sales_database:
                                sales_database[inventory_id] += shopping_cart_item["selling_price"] * shopping_cart_item["shopping_cart_quantity"]
                            else:
                                sales_database[inventory_id] = shopping_cart_item["selling_price"] * shopping_cart_item["shopping_cart_quantity"]
                        break
                elif customer_membership.upper() == "N":
                    subtotal = 0
                    total = sum(shopping_cart_item["selling_price"] * shopping_cart_item["shopping_cart_quantity"] for shopping_cart_item in shopping_cart.values())
                    for inventory_id, shopping_cart_item in shopping_cart.items():
                        if inventory_id in sales_database:
                            sales_database[inventory_id] += shopping_cart_item["selling_price"] * shopping_cart_item["shopping_cart_quantity"]
                        else:
                            sales_database[inventory_id] = shopping_cart_item["selling_price"] * shopping_cart_item["shopping_cart_quantity"]
                    break
                else:
                    print("Invalid input, please select 'Y' or 'N'!")
                    time.sleep(2)
                    continue
        elif confirm_payment.upper() == "N":
            return
        else:
            print("Invalid input, please select 'Y' or 'N'!")
            time.sleep(2)
            continue
        date_today = datetime.now()
        time_today = datetime.now()
        current_date = date_today.strftime("%d/%m/%Y")
        current_time = time_today.strftime("%H:%M:%S %p")
        os.system("clear")
        print(":::::::::::::::::::::::")
        print("::: [+] Receipt [+] :::")
        print(":::::::::::::::::::::::")
        print()
        print("Date: " + current_date)
        print("Time: " + current_time)
        print()
        print(table)
        print()
        print(f"Subtotal: $ {subtotal:.2f}")
        print(f"Total: $ {total:.2f}")
        print()
        while True:
            print_receipt = str(input("Would you prefer a printed copy of the receipt? [y/n]: "))
            if print_receipt.upper() == "Y":
                dot = [".", "..", "..."]
                for display_dot in dot:
                    print("\rPrinting receipt" + display_dot, end = "", flush = True)
                    time.sleep(0.5)
                print()
                print("Receipt printed successfully!")
                time.sleep(2)
                print()
                input("Press ENTER to continue!")
                shopping_cart.clear()
                return
            elif print_receipt.upper() == "N":
                shopping_cart.clear()
                return
            else:
                print("Invalid input, please select 'Y' or 'N'!")
                time.sleep(2)
                continue

def transaction():
    while True:
        os.system("clear")
        print(":::::::::::::::::::::::::::")
        print("::: [+] Transaction [+] :::")
        print(":::::::::::::::::::::::::::")
        print()
        print("[1] Add product to shopping cart")
        print("[2] Remove product from shopping cart")
        print("[3] Display products in shopping cart")
        print("[4] Proceed to payment")
        print("[0] Back")
        print()
        user_input = str(input("Enter number >>> "))
        if user_input == "1":
            add_to_shopping_cart()
        elif user_input == "2":
            remove_from_shopping_cart()
        elif user_input == "3":
            display_shopping_cart()
        elif user_input == "4":
            proceed_to_payment()
        elif user_input == "0":
            while True:
                if shopping_cart:
                    clear_shopping_cart = str(input("Would you like to clear the shopping cart? [y/n]: "))
                    if clear_shopping_cart.upper() == "Y":
                        for inventory_id, inventory_record in shopping_cart.items():
                            shopping_cart_quantity = inventory_record["shopping_cart_quantity"]
                            if inventory_id in inventory_database:
                                inventory_database[inventory_id]["inventory_quantity"] += shopping_cart_quantity
                        shopping_cart.clear()
                        print("Shopping cart is cleared!")
                        time.sleep(2)
                        return
                    elif clear_shopping_cart.upper() == "N":
                        return
                    else:
                        print("Invalid input, please select 'Y' or 'N'!")
                        time.sleep(2)
                        continue
                else:
                    return
        else:
            print("Invalid input, function not found!")
            time.sleep(2)
            continue

def get_user_input(prompt_message, input_type, error_message = "Invalid input, please check your input!"):
    while True:
        try:
            user_input = input_type(input(prompt_message))
            return user_input
        except ValueError:
            print(error_message)
            time.sleep(2)

def add_inventory():
    os.system("clear")
    print(":::::::::::::::::::::::::::::")
    print("::: [+] Add Inventory [+] :::")
    print(":::::::::::::::::::::::::::::")
    print()
    while True:
        inventory_id = get_user_input("Enter inventory ID [Ex. A1]: ", str)
        if inventory_id in inventory_database:
            print("Invalid input, inventory ID already in use!")
            time.sleep(2)
        elif not inventory_id:
            print("Invalid input, inventory ID cannot be blank!")
            time.sleep(2)
        else:
            break
    inventory_name = get_user_input("Enter inventory name [Ex. Pineapple]: ", str)
    unit_cost = get_user_input("Enter unit cost [Ex. 1.00]: ", float)
    selling_price = get_user_input("Enter selling price [Ex. 5.00]: ", float)
    inventory_quantity = get_user_input("Enter inventory quantity [Ex. 100]: ", int)
    reorder_level = get_user_input("Enter reorder level [Ex. 50]: ", int)
    supplier_name = get_user_input("Enter supplier name [Ex. Nickolas Barry]: ", str)
    supplier_company = get_user_input("Enter supplier company [Ex. TropicalTaste Trading]: ", str)
    os.system("clear")
    print("::::::::::::::::::::::::::::::")
    print("::: [+] Inventory Data [+] :::")
    print("::::::::::::::::::::::::::::::")
    print()
    print("ID: " + str(inventory_id))
    print("Name: " + str(inventory_name))
    print(f"Unit cost: $ {unit_cost:.2f}")
    print(f"Selling price: $ {selling_price:.2f}")
    print("Inventory quantity: " + str(inventory_quantity))
    print("Reorder level: " + str(reorder_level))
    print("Supplier name: " + str(supplier_name))
    print("Supplier company: " + str(supplier_company))
    print()
    while True:
        confirm_add_inventory = str(input("Would you like to add this inventory data? [y/n]: "))
        if confirm_add_inventory.upper() == "Y":
            inventory_database[inventory_id] = {
                "inventory_id": inventory_id,
                "inventory_name": inventory_name,
                "unit_cost": unit_cost,
                "selling_price": selling_price,
                "inventory_quantity": inventory_quantity,
                "reorder_level": reorder_level,
                "supplier_name": supplier_name,
                "supplier_company": supplier_company
            }
            print("Inventory data added successfully!")
            time.sleep(2)
            return
        elif confirm_add_inventory.upper() == "N":
            print("Cancel, inventory data didn't add!")
            time.sleep(2)
            return
        else:
            print("Invalid input, please select 'Y' or 'N'!")
            time.sleep(2)
            continue

def update_inventory():
    os.system("clear")
    print("::::::::::::::::::::::::::::::::")
    print("::: [+] Update Inventory [+] :::")
    print("::::::::::::::::::::::::::::::::")
    print()
    inventory_id = str(input("Enter inventory ID: "))
    if inventory_id not in inventory_database:
        print("Invalid input, inventory not found!")
        time.sleep(2)
        return
    os.system("clear")
    print("::::::::::::::::::::::::::::::")
    print("::: [+] Inventory Data [+] :::")
    print("::::::::::::::::::::::::::::::")
    print()
    inventory_record = inventory_database[inventory_id]
    print("ID: " + str(inventory_record["inventory_id"]))
    print("Name: " + str(inventory_record["inventory_name"]))
    print(f"Unit cost: $ {inventory_record['unit_cost']:.2f}")
    print(f"Selling price: $ {inventory_record['selling_price']:.2f}")
    print("Inventory quantity: " + str(inventory_record["inventory_quantity"]))
    print("Reorder level: " + str(inventory_record["reorder_level"]))
    print("Supplier name: " + str(inventory_record["supplier_name"]))
    print("Supplier company: " + str(inventory_record["supplier_company"]))
    print()
    while True:
        confirm_inventory = str(input("Would you like to update this inventory data? [y/n]: "))
        if confirm_inventory.upper() == "Y":
            os.system("clear")
            print("::::::::::::::::::::::::::::::::")
            print("::: [+] Update Inventory [+] :::")
            print("::::::::::::::::::::::::::::::::")
            print()
            while True:
                new_inventory_id = get_user_input("Enter new inventory ID [Ex. A1]: ", str)
                if new_inventory_id in inventory_database:
                    print("Invalid input, inventory ID already in use!")
                    time.sleep(2)
                elif not new_inventory_id:
                    print("Invalid input, inventory ID cannot be blank!")
                    time.sleep(2)
                else:
                    break
            new_inventory_name = get_user_input("Enter new inventory name [Ex. Pineapple]: ", str)
            new_unit_cost = get_user_input("Enter new unit cost [Ex. 1.00]: ", float)
            new_selling_price = get_user_input("Enter new selling price [Ex. 5.00]: ", float)
            new_inventory_quantity = get_user_input("Enter new inventory quantity [Ex. 100]: ", int)
            new_reorder_level = get_user_input("Enter new reorder level [Ex. 50]: ", int)
            new_supplier_name = get_user_input("Enter new supplier name [Ex. Nickolas Barry]: ",str)
            new_supplier_company = get_user_input("Enter new supplier company [Ex. TropicalTaste Trading]: ", str)
            os.system("clear")
            print("::::::::::::::::::::::::::::::")
            print("::: [+] Inventory Data [+] :::")
            print("::::::::::::::::::::::::::::::")
            print()
            print("ID: " + str(new_inventory_id))
            print("Name: " + str(new_inventory_name))
            print(f"Unit cost: $ {new_unit_cost:.2f}")
            print(f"Selling price: $ {new_selling_price:.2f}")
            print("Inventory quantity: " + str(new_inventory_quantity))
            print("Reorder level: " + str(new_reorder_level))
            print("Supplier name: " + str(new_supplier_name))
            print("Supplier company: " + str(new_supplier_company))
            print()
            while True:
                confirm_update_inventory = str(input("Would you like to update this inventory data? [y/n]: "))
                if confirm_update_inventory.upper() == "Y":
                    inventory_database[new_inventory_id] = {
                        "inventory_name": new_inventory_name,
                        "unit_cost": new_unit_cost,
                        "selling_price": new_selling_price,
                        "inventory_quantity": new_inventory_quantity,
                        "reorder_level": new_reorder_level,
                        "supplier_name": new_supplier_name,
                        "supplier_company": new_supplier_company
                    }
                    if new_inventory_id != inventory_id:
                        del inventory_database[inventory_id]
                    print("Inventory data updated successfully!")
                    time.sleep(2)
                    return
                elif confirm_update_inventory.upper() == "N":
                    print("Cancel, inventory data didn't update!")
                    time.sleep(2)
                    return
                else:
                    print("Invalid input, please select 'Y' or 'N'!") 
                    time.sleep(2)
                    continue
        elif confirm_inventory.upper() == "N":
            print("Cancel, inventory data didn't update!")
            time.sleep(2)
            return
        else:
            print("Invalid input, please select 'Y' or 'N'!")
            time.sleep(2)
            continue

def display_inventory():
    os.system("clear")
    if not inventory_database:
        print("Inventory database is empty, no results found!")
        time.sleep(2)
        return
    table = PrettyTable()
    table.field_names = ["Inventory ID", "Inventory Name", "Unit Cost", "Selling Price", "Inventory Quantity", "Reorder Level", "Supplier Name", "Supplier Company"]
    for inventory_id, inventory_record in inventory_database.items():
        table.add_row([inventory_id, inventory_record["inventory_name"], f"{inventory_record['unit_cost']:.2f}", f"{inventory_record['selling_price']:.2f}", inventory_record["inventory_quantity"], inventory_record["reorder_level"], inventory_record["supplier_name"], inventory_record["supplier_company"]])
    print()
    print(table)
    print()
    input("Press ENTER to continue!")
    return

def search_inventory():
    os.system("clear")
    print("::::::::::::::::::::::::::::::::")
    print("::: [+] Search Inventory [+] :::")
    print("::::::::::::::::::::::::::::::::")
    print()
    inventory_id = str(input("Enter inventory ID: "))
    if inventory_id in inventory_database:
        os.system("clear")
        print("::::::::::::::::::::::::::::::")
        print("::: [+] Inventory Data [+] :::")
        print("::::::::::::::::::::::::::::::")
        print()
        inventory_record = inventory_database[inventory_id]
        print("ID: " + str(inventory_record["inventory_id"]))
        print("Name: " + str(inventory_record["inventory_name"]))
        print(f"Unit cost: $ {inventory_record['unit_cost']:.2f}")
        print(f"Selling price: $ {inventory_record['selling_price']:.2f}")
        print("Inventory quantity: " + str(inventory_record["inventory_quantity"]))
        print("Reorder level: " + str(inventory_record["reorder_level"]))
        print("Supplier name: " + str(inventory_record["supplier_name"]))
        print("Supplier company: " + str(inventory_record["supplier_company"]))
        print()
        input("Press ENTER to continue!")
        return
    else:
        print("Invalid input, inventory not found!")
        time.sleep(2)
        return

def delete_inventory():
    os.system("clear")
    print("::::::::::::::::::::::::::::::::")
    print("::: [+] Delete Inventory [+] :::")
    print("::::::::::::::::::::::::::::::::")
    print()
    inventory_id = str(input("Enter inventory ID: "))
    if inventory_id in inventory_database:
        os.system("clear")
        print("::::::::::::::::::::::::::::::")
        print("::: [+] Inventory Data [+] :::")
        print("::::::::::::::::::::::::::::::")
        print()
        inventory_record = inventory_database[inventory_id]
        print("ID: " + str(inventory_record["inventory_id"]))
        print("Name: " + str(inventory_record["inventory_name"]))
        print(f"Unit cost: $ {inventory_record['unit_cost']:.2f}")
        print(f"Selling price: $ {inventory_record['selling_price']:.2f}")
        print("Inventory quantity: " + str(inventory_record["inventory_quantity"]))
        print("Reorder level: " + str(inventory_record["reorder_level"]))
        print("Supplier name: " + str(inventory_record["supplier_name"]))
        print("Supplier company: " + str(inventory_record["supplier_company"]))
        print()
        while True:
            confirm_delete_inventory = str(input("Would you like to delete this employee data? [y/n]: "))
            if confirm_delete_inventory.upper() == "Y":
                del inventory_database[inventory_id]
                print("Inventory data deleted successfully!")
                time.sleep(2)
                return
            elif confirm_delete_inventory.upper() == "N":
                print("Cancel, inventory data didn't delete!")
                time.sleep(2)
                return
            else:
                print("Invalid input, please select 'Y' or 'N'!")
                time.sleep(2)
                continue
    else:
        print("Invalid input, inventory not found!")
        time.sleep(2)
        return

def inventory():
    while True:
        os.system("clear")
        print(":::::::::::::::::::::::::")
        print("::: [+] Inventory [+] :::")
        print(":::::::::::::::::::::::::")
        print()
        print("[1] Add inventory")
        print("[2] Update inventory")
        print("[3] Display inventory")
        print("[4] Search inventory")
        print("[5] Delete inventory")
        print("[0] Back")
        print()
        user_input = str(input("Enter number >>> "))
        if user_input == "1":
            add_inventory()
        elif user_input == "2":
            update_inventory()
        elif user_input == "3":
            display_inventory()
        elif user_input == "4":
            search_inventory()
        elif user_input == "5":
            delete_inventory()
        elif user_input == "0":
            main()
        else:
            print("Invalid input, function not found!")
            time.sleep(2)
            continue

def add_customer():
    while True:
        os.system("clear")
        print("::::::::::::::::::::::::::::")
        print("::: [+] Add Customer [+] :::")
        print("::::::::::::::::::::::::::::")
        print()
        customer_id = get_user_input("Enter customer ID [Ex. B1]: ", str)
        if customer_id in customer_database:
            print("Invalid input, customer ID already in use!")
            time.sleep(2)
        elif not customer_id:
            print("Invalid input, customer ID cannot be blank!")
            time.sleep(2)
        else:
            break
    customer_name = get_user_input("Enter customer name [Ex. Kieran Burke]: ", str)
    customer_age = get_user_input("Enter customer age [Ex. 30]: ", int)
    customer_gender = get_user_input("Enter customer gender [Ex. Male]: ", str)
    customer_email = get_user_input("Enter customer email [Ex. name@domain.com]: ", str)
    customer_phone_number = get_user_input("Enter customer phone number [Ex. 0123456789]: ", str)
    customer_home_address = get_user_input("Enter customer home address [Ex. 374 Park Road, East Central London, EC49 8UC]: ", str)
    os.system("clear")
    print(":::::::::::::::::::::::::::::")
    print("::: [+] Customer Data [+] :::")
    print(":::::::::::::::::::::::::::::")
    print()
    print("ID: " + str(customer_id))
    print("Name: " + str(customer_name))
    print("Age: " + str(customer_age))
    print("Gender: " + str(customer_gender))
    print("Email: " + str(customer_email))
    print("Phone number: " + str(customer_phone_number))
    print("Home address: " + str(customer_home_address))
    print()
    while True:
        confirm_add_customer = str(input("Would you like to add this customer data? [y/n]: "))
        if confirm_add_customer.upper() == "Y":
            customer_database[customer_id] = {
                "customer_id": customer_id,
                "customer_name": customer_name,
                "customer_age": customer_age,
                "customer_gender": customer_gender,
                "customer_email": customer_email,
                "customer_phone_number": customer_phone_number,
                "customer_home_address": customer_home_address
            }
            print("Customer data added successfully!")
            time.sleep(2)
            return
        elif confirm_add_customer.upper() == "N":
            print("Cancel, customer data didn't add!")
            time.sleep(2)
            return
        else:
            print("Invalid input, please select 'Y' or 'N'!")
            time.sleep(2)
            continue

def update_customer():
    os.system("clear")
    print(":::::::::::::::::::::::::::::::")
    print("::: [+] Update Customer [+] :::")
    print(":::::::::::::::::::::::::::::::")
    print()
    customer_id = str(input("Enter customer ID: "))
    if customer_id not in customer_database:
        print("Invalid input, customer not found!")
        time.sleep(2)
        return
    os.system("clear")
    print(":::::::::::::::::::::::::::::")
    print("::: [+] Customer Data [+] :::")
    print(":::::::::::::::::::::::::::::")
    print()
    customer_record = customer_database[customer_id]
    print("ID: " + str(customer_record["customer_id"]))
    print("Name: " + str(customer_record["customer_name"]))
    print("Age: " + str(customer_record["customer_age"]))
    print("Gender: " + str(customer_record["customer_gender"]))
    print("Email: " + str(customer_record["customer_email"]))
    print("Phone number: " + str(customer_record["customer_phone_number"]))
    print("Home address: " + str(customer_record["customer_home_address"]))
    print()
    while True:
        confirm_customer = str(input("Would you like to update this customer data? [y/n]: "))
        if confirm_customer.upper() == "Y":
            os.system("clear")
            print(":::::::::::::::::::::::::::::::")
            print("::: [+] Update Customer [+] :::")
            print(":::::::::::::::::::::::::::::::")
            print()
            while True:
                new_customer_id = get_user_input("Enter new customer ID [Ex. B1]: ", str)
                if new_customer_id in customer_database:
                    print("Invalid input, customer ID already in use!")
                    time.sleep(2)
                elif not new_customer_id:
                    print("Invalid input, customer ID cannot be blank!")
                    time.sleep(2)
                else:
                    break
            new_customer_name = get_user_input("Enter new customer name [Ex. Kieran Burke]: ", str)
            new_customer_age = get_user_input("Enter new customer age [Ex. 30]: ", int)
            new_customer_gender = get_user_input("Enter new customer gender [Ex. Male]: ", str)
            new_customer_email = get_user_input("Enter new customer email [Ex. name@domain.com]: ", str)
            new_customer_phone_number = get_user_input("Enter new customer phone number [Ex. 0123456789]: ", str)
            new_customer_home_address = get_user_input("Enter new customer home address [Ex. 374 Park Road, East Central London, EC49 8UC]: ", str)
            os.system("clear")
            print(":::::::::::::::::::::::::::::")
            print("::: [+] Customer Data [+] :::")
            print(":::::::::::::::::::::::::::::")
            print()
            print("ID: " + str(new_customer_id))
            print("Name: " + str(new_customer_name))
            print("Age: " + str(new_customer_age))
            print("Gender: " + str(new_customer_gender))
            print("Email: " + str(new_customer_email))
            print("Phone number: " + str(new_customer_phone_number))
            print("Home address: " + str(new_customer_home_address))
            print()
            while True:
                confirm_update_customer = str(input("Would you like to update this customer data? [y/n]: "))
                if confirm_update_customer.upper() == "Y":
                    customer_database[new_customer_id] = {
                        "customer_name": new_customer_name,
                        "customer_age": new_customer_age,
                        "customer_gender": new_customer_gender,
                        "customer_email": new_customer_email,
                        "customer_phone_number": new_customer_phone_number,
                        "customer_home_address": new_customer_home_address
                    }
                    if new_customer_id != customer_id:
                        del customer_database[customer_id]
                    print("Customer data updated successfully!")
                    time.sleep(2)
                    return
                elif confirm_update_customer.upper() == "N":
                    print("Cancel, customer data didn't update!")
                    time.sleep(2)
                    return
                else:
                    print("Invalid input, please select 'Y' or 'N'!")
                    time.sleep(2)
                    continue
        elif confirm_customer.upper() == "N":
            print("Cancel, customer data didn't update!")
            time.sleep(2)
            return
        else:
            print("Invalid input, please select 'Y' or 'N'!")
            time.sleep(2)
            continue

def display_customer():
    os.system("clear")
    if not customer_database:
        print("Customer database is empty, no results found!")
        time.sleep(2)
        return
    table = PrettyTable()
    table.field_names = ["Customer ID", "Customer Name", "Customer Age", "Customer Gender", "Customer Email", "Customer Phone Number", "Customer Home Address"]
    for customer_id, customer_record in customer_database.items():
        table.add_row([customer_id, customer_record["customer_name"], customer_record["customer_age"], customer_record["customer_gender"], customer_record["customer_email"], customer_record["customer_phone_number"], customer_record["customer_home_address"]])
    print()
    print(table)
    print()
    input("Press ENTER to continue!")
    return

def search_customer():
    os.system("clear")
    print(":::::::::::::::::::::::::::::::")
    print("::: [+] Search Customer [+] :::")
    print(":::::::::::::::::::::::::::::::")
    print()
    customer_id = str(input("Enter customer ID: "))
    if customer_id in customer_database:
        os.system("clear")
        print(":::::::::::::::::::::::::::::")
        print("::: [+] Customer Data [+] :::")
        print(":::::::::::::::::::::::::::::")
        print()
        customer_record = customer_database[customer_id]
        print("ID: " + str(customer_record["customer_id"]))
        print("Name: " + str(customer_record["customer_name"]))
        print("Age: " + str(customer_record["customer_age"]))
        print("Gender: " + str(customer_record["customer_gender"]))
        print("Email: " + str(customer_record["customer_email"]))
        print("Phone number: " + str(customer_record["customer_phone_number"]))
        print("Home address: " + str(customer_record["customer_home_address"]))
        print()
        input("Press ENTER to continue!")
        return
    else:
        print("Invalid input, customer not found!")
        time.sleep(2)
        return

def delete_customer():
    os.system("clear")
    print(":::::::::::::::::::::::::::::::")
    print("::: [+] Delete Customer [+] :::")
    print(":::::::::::::::::::::::::::::::")
    print()
    customer_id = str(input("Enter customer ID: "))
    if customer_id in customer_database:
        os.system("clear")
        print(":::::::::::::::::::::::::::::")
        print("::: [+] Customer Data [+] :::")
        print(":::::::::::::::::::::::::::::")
        print()
        customer_record = customer_database[customer_id]
        print("ID: " + str(customer_record["customer_id"]))
        print("Name: " + str(customer_record["customer_name"]))
        print("Age: " + str(customer_record["customer_age"]))
        print("Gender: " + str(customer_record["customer_gender"]))
        print("Email: " + str(customer_record["customer_email"]))
        print("Phone number: " + str(customer_record["customer_phone_number"]))
        print("Home address: " + str(customer_record["customer_home_address"]))
        print()
        while True:
            confirm_delete_customer = str(input("Would you like to delete this customer data? [y/n]: "))
            if confirm_delete_customer.upper() == "Y":
                del customer_database[customer_id]
                print("Customer data deleted successfully!")
                time.sleep(2)
                return
            elif confirm_delete_customer.upper() == "N":
                print("Cancel, customer data didn't delete!")
                time.sleep(2)
                return
            else:
                print("Invalid input, please select 'Y' or 'N'!")
                time.sleep(2)
                continue
    else:
        print("Invalid input, customer not found!")
        time.sleep(2)
        return

def customer():
    while True:
        os.system("clear")
        print("::::::::::::::::::::::::")
        print("::: [+] Customer [+] :::")
        print("::::::::::::::::::::::::")
        print()
        print("[1] Add customer")
        print("[2] Update customer")
        print("[3] Display customer")
        print("[4] Search customer")
        print("[5] Delete customer")
        print("[0] Back")
        print()
        user_input = str(input("Enter number >>> "))
        if user_input == "1":
            add_customer()
        elif user_input == "2":
            update_customer()
        elif user_input == "3":
            display_customer()
        elif user_input == "4":
            search_customer()
        elif user_input == "5":
            delete_customer()
        elif user_input == "0":
            main()
        else:
            print("Invalid input, function not found!")
            time.sleep(2)
            continue

def sales_report():
    os.system("clear")
    print("::::::::::::::::::::::::::::")
    print("::: [+] Sales Report [+] :::")
    print("::::::::::::::::::::::::::::")
    print()
    if not sales_database:
        print("Sales database is empty, no results found!")
        time.sleep(2)
        return
    sort_product = sorted(sales_database.items(), key = lambda x: x[1], reverse = True)
    table = PrettyTable()
    table.field_names = ["Rank", "Inventory ID", "Inventory Name", "Total Sales"]
    for rank, (inventory_id, total_sales) in enumerate(sort_product[:10], start = 1):
        inventory_name = inventory_database[inventory_id]["inventory_name"]
        table.add_row([rank, inventory_id, inventory_name, f"$ {total_sales:.2f}"])
    print()
    print(table)
    print()
    while True:
        print_report = str(input("Would you prefer a printed copy of the sales report? [y/n]: "))
        if print_report.upper() == "Y":
            dot = [".", "..", "..."]
            for display_dot in dot:
                print("\rPrinting sales report" + display_dot, end = "", flush = True)
                time.sleep(0.5)
            print()
            print("Sales report printed successfully!")
            time.sleep(2)
            print()
            input("Press ENTER to continue!")
            return
        elif print_report.upper() == "N":
            return
        else:
            print("Invalid input, please select 'Y' or 'N'!")
            time.sleep(2)
            continue

def inventory_reorder_report():
    os.system("clear")
    print("::::::::::::::::::::::::::::::::::::::::")
    print("::: [+] Inventory Reorder Report [+] :::")
    print("::::::::::::::::::::::::::::::::::::::::")
    print()
    reorder_inventory_item = []
    for inventory_id, inventory_record in inventory_database.items():
        if inventory_record['inventory_quantity'] <= inventory_record['reorder_level']:
            reorder_inventory_item.append({
                'inventory_id': inventory_record['inventory_id'],
                'inventory_name': inventory_record['inventory_name'],
                'inventory_quantity': inventory_record['inventory_quantity'],
                'reorder_level': inventory_record['reorder_level'],
                'supplier_name': inventory_record['supplier_name'],
                'supplier_company': inventory_record['supplier_company']
            })
    if not reorder_inventory_item:
        print("All inventory items are currently above the reorder level!")
        time.sleep(2)
        return
    table = PrettyTable()
    table.field_names = ["Inventory ID", "Inventory Name", "Inventory Quantity", "Reorder Level", "Supplier Name", "Supplier Company"]
    for reorder_item in reorder_inventory_item:
        table.add_row([reorder_item["inventory_id"], reorder_item["inventory_name"], reorder_item["inventory_quantity"], reorder_item["reorder_level"], reorder_item["supplier_name"], reorder_item["supplier_company"]])
    print()
    print(table)
    print()
    while True:
        print_report = str(input("Would you prefer a printed copy of the inventory reorder report? [y/n]: "))
        if print_report.upper() == "Y":
            dot = [".", "..", "..."]
            for display_dot in dot:
                print("\rPrinting inventory reorder report" + display_dot, end = "", flush = True)
                time.sleep(0.5)
            print()
            print("Inventory reorder report printed successfully!")
            time.sleep(2)
            print()
            input("Press ENTER to continue!")
            return
        elif print_report.upper() == "N":
            return
        else:
            print("Invalid input, please select 'Y' or 'N'!")
            time.sleep(2)
            continue

def report():
    while True:
        os.system("clear")
        print("::::::::::::::::::::::")
        print("::: [+] Report [+] :::")
        print("::::::::::::::::::::::")
        print()
        print("[1] Sales report")
        print("[2] Inventory reorder report")
        print("[0] Back")
        print()
        user_input = str(input("Enter number >>> "))
        if user_input == "1":
            sales_report()
        elif user_input == "2":
            inventory_reorder_report()
        elif user_input == "0":
            main()
        else:
            print("Invalid input, function not found!")
            time.sleep(2)
            continue

def exit_program():
    os.system("clear")
    print("Goodbye!")
    sys.exit(0)

def main():
    while True:
        os.system("clear")
        print("::::::::::::::::::::::::::::::::::::::::")
        print("::: [+] Retail Management System [+] :::")
        print("::::::::::::::::::::::::::::::::::::::::")
        print()
        print("[1] Transaction")
        print("[2] Inventory")
        print("[3] Customer")
        print("[4] Report")
        print("[0] Exit")
        print()
        user_input = str(input("Enter number >>> "))
        if user_input == "1":
            transaction()
        elif user_input == "2":
            inventory()
        elif user_input == "3":
            customer()
        elif user_input == "4":
            report()
        elif user_input == "0":
            exit_program()
        else:
            print("Invalid input, function not found!")
            time.sleep(2)
            continue

if __name__ == "__main__":
    main()