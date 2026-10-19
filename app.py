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
            "SELECT setval('customers_id_seq', (SELECT MAX(id) FROM Customers))"
        )
        cur.execute("SELECT setval('products_id_seq', (SELECT MAX(id) FROM Products))")
        cur.execute("SELECT setval('sales_id_seq', (SELECT MAX(id) FROM Sales))")
        cur.execute(
            "SELECT setval('sale_items_id_seq', (SELECT MAX(id) FROM Sale_Items))"
        )
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error initializing tables: {e}")


# App title and sidebar
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
        "Customer Management",
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
        # Count customers
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM customers")
        customer_count = cur.fetchone()[0]

        # Count products
        cur.execute("SELECT COUNT(*) FROM products")
        product_count = cur.fetchone()[0]

        # Count sales
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


# import streamlit as st
# from datetime import date
# from database import conn
# from Customers import Customers
# from Products import Products
# from Sales import Sales
# from SalesItem import SaleItems

# # ---------------------------------------------------------
# # 1. Initialize Tables & Fix Sequences Automatically
# # ---------------------------------------------------------
# def initialize_tables():
#     try:
#         Customers.create_table()
#         Products.create_table()
#         Sales.create_table()
#         SaleItems.create_table()

#         cur = conn.cursor()
#         cur.execute("SELECT setval('customers_id_seq', (SELECT COALESCE(MAX(id), 1) FROM customers))")
#         cur.execute("SELECT setval('products_id_seq', (SELECT COALESCE(MAX(id), 1) FROM products))")
#         cur.execute("SELECT setval('sales_id_seq', (SELECT COALESCE(MAX(id), 1) FROM sales))")
#         cur.execute("SELECT setval('sale_items_id_seq', (SELECT COALESCE(MAX(id), 1) FROM sale_items))")
#         conn.commit()
#         cur.close()
        
#         st.success("atabase table Initialized successfully!")
#     except Exception as e:
#         st.error(f"Error initializing tables: {e}")

# # App launch hone par tables create aur fix ho jayengi
# initialize_tables()

# # ---------------------------------------------------------
# # 2. Streamlit UI Layout
# # ---------------------------------------------------------
# st.set_page_config(page_title="Smart Billing System", layout="wide")
# st.title("🛍️ Smart Inventory & Billing System")

# # Sidebar Navigation Menu
# menu = st.sidebar.selectbox(
#     "Select Option / Domain",
#     ["Dashboard", "Customer Management", "Product Management", "Sales Management"]
# )

# # ---------------------------------------------------------
# # DASHBOARD
# # ---------------------------------------------------------
# if menu == "Dashboard":
#     st.header("📊 Business Overview")
#     col1, col2, col3 = st.columns(3)
    
#     customers_list = Customers.get_all_customers()
#     products_list = Products.view_products()
#     sales_list = Sales.view_sales()

#     col1.metric("Total Customers", len(customers_list))
#     col2.metric("Total Products", len(products_list))
#     col3.metric("Total Sales Records", len(sales_list))

# # ---------------------------------------------------------
# # CUSTOMER MANAGEMENT
# # ---------------------------------------------------------
# elif menu == "Customer Management":
#     st.header("👤 Customer Management")
#     tab1, tab2 = st.tabs(["View Customers", "Add Customer"])

#     with tab1:
#         st.subheader("All Customers")
#         data = Customers.get_all_customers()
#         if data:
#             st.dataframe(data, column_config={0: "ID", 1: "Name", 2: "Contact"}, use_container_width=True)
#         else:
#             st.info("No customers found.")

#     with tab2:
#         st.subheader("Add New Customer")
#         with st.form("add_customer_form"):
#             c_name = st.text_input("Customer Name")
#             c_contact = st.text_input("Customer Contact")
#             submitted = st.form_submit_button("Add Customer")

#             if submitted:
#                 if c_name and c_contact:
#                     Customers.insert_customer(c_name, c_contact)
#                     st.success(f"Customer '{c_name}' added successfully!")
#                     st.rerun()
#                 else:
#                     st.warning("Please fill all details!")

# # ---------------------------------------------------------
# # PRODUCT MANAGEMENT
# # ---------------------------------------------------------
# elif menu == "Product Management":
#     st.header("📦 Product Management")
#     tab1, tab2 = st.tabs(["View Products", "Add Product"])

#     with tab1:
#         st.subheader("All Products")
#         data = Products.view_products()
#         if data:
#             st.dataframe(data, column_config={0: "ID", 1: "Name", 2: "Description", 3: "Price", 4: "Quantity"}, use_container_width=True)
#         else:
#             st.info("No products found.")

#     with tab2:
#         st.subheader("Add New Product")
#         with st.form("add_product_form"):
#             p_name = st.text_input("Product Name")
#             p_desc = st.text_area("Product Description")
#             p_price = st.number_input("Price", min_value=0.0, step=0.5)
#             p_qty = st.number_input("Quantity", min_value=1, step=1)
#             submitted = st.form_submit_button("Add Product")

#             if submitted:
#                 if p_name and p_desc:
#                     Products.insert_product(p_name, p_desc, p_price, p_qty)
#                     st.success(f"Product '{p_name}' added successfully!")
#                     st.rerun()
#                 else:
#                     st.warning("Please enter all details!")

# # ---------------------------------------------------------
# # SALES MANAGEMENT
# # ---------------------------------------------------------
# elif menu == "Sales Management":
#     st.header("🧾 Sales Management")
#     tab1, tab2 = st.tabs(["Sales Records", "Create New Sale"])

#     with tab1:
#         st.subheader("All Sales History")
#         data = Sales.view_sales()
#         if data:
#             st.dataframe(data, column_config={0: "Sale ID", 1: "Customer ID", 2: "Date", 3: "Total Amount"}, use_container_width=True)
#         else:
#             st.info("No sales records found.")

#     with tab2:
#         st.subheader("Create New Sale")
#         with st.form("add_sale_form"):
#             s_cust_id = st.number_input("Customer ID", min_value=1, step=1)
#             s_date = st.date_input("Sale Date", value=date.today())
#             s_amount = st.number_input("Total Amount", min_value=0.0, step=1.0)
#             submitted = st.form_submit_button("Create Sale Entry")

#             if submitted:
#                 Sales.insert_sales(s_cust_id, s_date, s_amount)
#                 st.success("Sale recorded successfully!")
#                 st.rerun()