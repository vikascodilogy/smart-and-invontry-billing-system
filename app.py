# import streamlit as st
# from datetime import date
# from database import conn
# from Customers import Customers
# from Products import Products
# from Sales import Sales

# from SalesItem import SaleItems


# # Initialize tables if they don't exist
# def initialize_tables():
#     try:
#         Customers.create_table()
#         Products.create_table()
#         Sales.create_table()
#         SaleItems.create_table()

#         # Fix sequences for all tables
#         cur = conn.cursor()
#         cur.execute(
#             "SELECT setval('customers_id_seq', (SELECT MAX(id) FROM Customers))"
#         )
#         cur.execute("SELECT setval('products_id_seq', (SELECT MAX(id) FROM Products))")
#         cur.execute("SELECT setval('sales_id_seq', (SELECT MAX(id) FROM Sales))")
#         cur.execute(
#             "SELECT setval('sale_items_id_seq', (SELECT MAX(id) FROM Sale_Items))"
#         )
#         conn.commit()
#         cur.close()
#     except Exception as e:
#         print(f"Error initializing tables: {e}")


# # App title and sidebar
# st.set_page_config(page_title="Smart Inventory and Billing System", layout="wide")
# st.title("🤖 Smart Inventory and Billing System")

# # Initialize tables on first run
# if "tables_initialized" not in st.session_state:
#     initialize_tables()
#     st.session_state.tables_initialized = True

# # Sidebar navigation
# st.sidebar.header("Navigation")
# menu_option = st.sidebar.selectbox(
#     "Choose an option:",
#     [
#         "Dashboard",
#         "Customer Management",
#         "Product Management",
#         "Sales Management",
#         "Analytics & Reports",
#     ]
# )



# # Dashboard
# if menu_option == "Dashboard":
#     st.header("📊 Dashboard")
#     st.write("Welcome to the Smart Inventory and Billing System!")
#     st.write("Use the navigation menu to manage customers, products, and sales.")

#     # Show some statistics
#     try:
#         # Count customers
#         cur = conn.cursor()
#         cur.execute("SELECT COUNT(*) FROM customers")
#         customer_count = cur.fetchone()[0]

#         # Count products
#         cur.execute("SELECT COUNT(*) FROM products")
#         product_count = cur.fetchone()[0]

#         # Count sales
#         cur.execute("SELECT COUNT(*) FROM sales")
#         sales_count = cur.fetchone()[0]

#         cur.close()
        
#         # Display metrics
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Total Customers", customer_count)
#         col2.metric("Total Products", product_count)
#         col3.metric("Total Sales", sales_count)
#     except Exception as e:
#         st.error(f"Error loading statistics: {e}")

import streamlit as st
from datetime import date
from database import conn
from Customers import Customers
from Products import Products
from Sales import Sales
from SalesItem import SaleItems

# Initialize tables if they don't exist
def initialize_tables():
    try:
        Customers.create_table()
        Products.create_table()
        Sales.create_table()
        SaleItems.create_table()

        # Fix sequences for all tables
        cur = conn.cursor()
        cur.execute(
            "SELECT setval('customers_id_seq', (SELECT COALESCE(MAX(id), 1) FROM customers))"
        )
        cur.execute("SELECT setval('products_id_seq', (SELECT COALESCE(MAX(id), 1) FROM products))")
        cur.execute("SELECT setval('sales_id_seq', (SELECT COALESCE(MAX(id), 1) FROM sales))")
        cur.execute("SELECT setval('sale_items_id_seq', (SELECT COALESCE(MAX(id), 1) FROM sale_items))")
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error initializing tables: {e}")

# App title and sidebar configuration
st.set_page_config(page_title="Smart Inventory and Billing System", layout="wide")
st.title("🤖 Smart Inventory and Billing System")

# Initialize tables on first run
if "tables_initialized" not in st.session_state:
    initialize_tables()
    st.session_state.tables_initialized = True

# Sidebar navigation
st.sidebar.header("Navigation")
menu_option = st.sidebar.selectbox(
    "Choose an option:",
    [
        "Dashboard",
        "Customers Management",
        "Product Management",
        "Sales Management",
        "Analytics & Reports",
    ]
)

# Dashboard
if menu_option == "Dashboard":
    st.header("📊 Dashboard")
    st.write("Welcome to the Smart Inventory and Billing System!")
    st.write("Use the navigation menu to manage customers, products, and sales.")

    # Show some statistics
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM customers")
        customer_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM products")
        product_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM sales")
        sales_count = cur.fetchone()[0]
        cur.close()
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Customers", customer_count)
        col2.metric("Total Products", product_count)
        col3.metric("Total Sales", sales_count)
    except Exception as e:
        st.error(f"Error loading statistics: {e}")

# Customers Management (UI Based)
elif menu_option == "Customers Management":
    st.header("👥 Customers Management")
    
    action = st.radio(
        "Select Action:",
        ["View All Customers", "Add New Customer", "Update Customer", "Delete Customer"],
        horizontal=False
    )

    # 1. View All Customers
    if action == "View All Customers":
        st.subheader("All Customers List")
        try:
            customers_data = Customers.get_all_customers()
            if customers_data:
                for cust in customers_data:
                    col1, col2, col3 = st.columns([1, 3, 3])
                    col1.write(f"**ID: {cust[0]}**")
                    col2.write(f"Name: {cust[1]}")
                    col3.write(f"Contact: {cust[2]}")
                    st.divider()
            else:
                st.info("No customers found in the database.")
        except Exception as e:
            st.error(f"Error fetching customers: {e}")

    # 2. Add New Customer
    elif action == "Add New Customer":
        st.subheader("Add New Customer")
        with st.form("add_customer_form"):
            c_name = st.text_input("Customer Name")
            c_contact = st.text_input("Contact Information")
            submitted = st.form_submit_button("Add Customer")

            if submitted:
                if c_name and c_contact:
                    try:
                        Customers.insert_customer(c_name, c_contact)
                        st.success(f"Customer '{c_name}' added successfully!")
                        st.toast("Customer Added!", icon="✅")
                        # st.rerun()
                    except Exception as e:
                        st.error(f"Error adding customer: {e}")
                else:
                    st.warning("Please fill in all details!")

    # 3. Update Customer
    elif action == "Update Customer":
        st.subheader("Update Customer Details")
        with st.form("update_customer_form"):
            c_id = st.number_input("Enter Customer ID to Update", min_value=1, step=1)
            new_name = st.text_input("New Customer Name (Leave blank if no change)")
            new_contact = st.text_input("New Contact Information (Leave blank if no change)")
            update_submitted = st.form_submit_button("Update Customer")

            if update_submitted:
                name_val = new_name.strip() if new_name.strip() else None
                contact_val = new_contact.strip() if new_contact.strip() else None

                if name_val or contact_val:
                    try:
                        Customers.update_customer(int(c_id), name=name_val, contact=contact_val)
                        st.success(f"Customer ID {c_id} updated successfully!")
                        st.toast("Customer Updated!", icon="✅")
                        # st.rerun()
                    except Exception as e:
                        st.error(f"Error updating customer: {e}")
                else:
                    st.warning("Please enter at least Name or Contact to update!")

    # 4. Delete Customer
    elif action == "Delete Customer":
        st.subheader("Delete a Customer")
        with st.form("delete_customer_form"):
            del_id = st.number_input("Enter Customer ID to Delete", min_value=1, step=1)
            delete_submitted = st.form_submit_button("Delete Customer", type="primary")

            if delete_submitted:
                try:
                    Customers.delete_customer(int(del_id))
                    st.success(f"Customer ID {del_id} deleted successfully!")
                    st.toast("Customer Deleted!", icon="✅")
                    # st.rerun()
                except Exception as e:
                    st.error(f"Error deleting customer: {e}")
                    
                    

# Product Management (UI Based)
elif menu_option == "Product Management":
    st.header("📦 Product Management")
    
    action = st.radio(
        "Select Action:",
        ["View All Products", "Add New Product", "Update Product", "Delete Product", "View Product by ID"],
        horizontal=False
    )

    # 1. View All Products
    if action == "View All Products":
        st.subheader("All Products List")
        try:
            products_data = Products.view_products()
            if products_data:
                # Table Headers / Headings
                col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 2, 2])
                col1.write("**ID**")
                col2.write("**Name**")
                col3.write("**Description**")
                col4.write("**Price (₹)**")
                col5.write("**Quantity**")
                st.divider()

                # Table Rows Data
                for prod in products_data:
                    c1, c2, c3, c4, c5 = st.columns([1, 2, 3, 2, 2])
                    c1.write(f"{prod[0]}")
                    c2.write(f"{prod[1]}")
                    c3.write(f"{prod[2]}")
                    c4.write(f"₹{prod[3]}")
                    c5.write(f"{prod[4]}")
                    st.divider()
            else:
                st.info("No products found in the database.")
        except Exception as e:
            st.error(f"Error fetching products: {e}")
    # 2. Add New Product
    elif action == "Add New Product":
        st.subheader("Add New Product")
        with st.form("add_product_form"):
            p_name = st.text_input("Product Name")
            p_desc = st.text_area("Product Description")
            p_price = st.number_input("Price (₹)", min_value=0.0, step=0.1)
            p_qty = st.number_input("Quantity", min_value=0, step=1)
            submitted = st.form_submit_button("Add Product")

            if submitted:
                if p_name and p_desc:
                    try:
                        Products.insert_product(p_name, p_desc, p_price, int(p_qty))
                        st.success(f"🎉 Product '{p_name}' added successfully!")
                        st.toast("Product Added!", icon="✅")
                    except Exception as e:
                        st.error(f"Error adding product: {e}")
                else:
                    st.warning("Please fill in all details!")

    # 3. Update Product
    elif action == "Update Product":
        st.subheader("Update Product Details")
        with st.form("update_product_form"):
            p_id = st.number_input("Enter Product ID to Update", min_value=1, step=1)
            p_name = st.text_input("New Name (Leave blank if no change)")
            p_desc = st.text_area("New Description (Leave blank if no change)")
            p_price_input = st.text_input("New Price (Leave blank if no change)")
            p_qty_input = st.text_input("New Quantity (Leave blank if no change)")
            update_submitted = st.form_submit_button("Update Product")

            if update_submitted:
                name_val = p_name.strip() if p_name.strip() else None
                desc_val = p_desc.strip() if p_desc.strip() else None
                price_val = float(p_price_input.strip()) if p_price_input.strip() else None
                qty_val = int(p_qty_input.strip()) if p_qty_input.strip() else None

                try:
                    Products.update_product(
                        int(p_id), 
                        name=name_val, 
                        discription=desc_val, 
                        price=price_val, 
                        quantity=qty_val
                    )
                    st.success(f"✏️ Product ID {p_id} updated successfully!")
                    st.toast("Product Updated!", icon="✅")
                except Exception as e:
                    st.error(f"Error updating product: {e}")

    # 4. Delete Product
    elif action == "Delete Product":
        st.subheader("Delete a Product")
        with st.form("delete_product_form"):
            del_id = st.number_input("Enter Product ID to Delete", min_value=1, step=1)
            delete_submitted = st.form_submit_button("Delete Product", type="primary")

            if delete_submitted:
                try:
                    Products.delete_product(int(del_id))
                    st.success(f"🗑️ Product ID {del_id} deleted successfully!")
                    st.toast("Product Deleted!", icon="✅")
                except Exception as e:
                    st.error(f"Error deleting product: {e}")

    # 5. View Product by ID
    elif action == "View Product by ID":
        st.subheader("Search Product by ID")
        with st.form("view_product_id_form"):
            search_id = st.number_input("Enter Product ID", min_value=1, step=1)
            search_submitted = st.form_submit_button("Search")

            if search_submitted:
                try:
                    prod_data = Products.view_product_id(int(search_id))
                    if prod_data:
                        for prod in prod_data:
                            st.success("Product Found!")
                            st.write(f"**ID:** {prod[0]}")
                            st.write(f"**Name:** {prod[1]}")
                            st.write(f"**Description:** {prod[2]}")
                            st.write(f"**Price:** ₹{prod[3]}")
                            st.write(f"**Quantity:** {prod[4]}")
                    else:
                        st.warning("No product found with this ID.")
                except Exception as e:
                    st.error(f"Error: {e}")
    
                    
                    
# Product Management Placeholder
elif menu_option == "Product Management":
    st.header("📦 Product Management")
    st.info("Product management UI is coming up next!")

# Sales Management Placeholder
elif menu_option == "Sales Management":
    st.header("💰 Sales Management")
    st.info("Sales management UI is coming up next!")

# Analytics & Reports Placeholder
elif menu_option == "Analytics & Reports":
    st.header("📈 Analytics & Reports")
    st.info("Analytics dashboard is coming up next!")
