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
    

# Sales Management (UI Based)
elif menu_option == "Sales Management":
    st.header("💰 Sales Management")
    
    # Radio button saare actions ko select karne ke liye
    action = st.radio(
        "Select Action:",
        [
            "View All Sales", 
            "Create New Sale", 
            "Update Sale", 
            "Delete Sale", 
            "View Sale by ID", 
            "Generate Bill",
            "Sales by Customer"
        ],
        horizontal=False
    )

    # 1. VIEW ALL SALES: Saari sales ki list table format me dikhane ke liye
    if action == "View All Sales":
        st.subheader("All Sales List")
        try:
            sales_data = Sales.view_sales()
            if sales_data:
                col1, col2, col3, col4 = st.columns([1, 2, 3, 2])
                col1.write("**Sale ID**")
                col2.write("**Customer ID**")
                col3.write("**Date**")
                col4.write("**Total Amount (₹)**")
                st.divider()

                for sale in sales_data:
                    c1, c2, c3, c4 = st.columns([1, 2, 3, 2])
                    c1.write(f"{sale[0]}")
                    c2.write(f"{sale[1]}")
                    c3.write(f"{sale[2]}")
                    c4.write(f"₹{sale[3]}")
                    st.divider()
            else:
                st.info("No sales records found.")
        except Exception as e:
            st.error(f"Error fetching sales: {e}")

    # 2. CREATE NEW SALE: Dropdown se customer select karke nayi sale insert karne ke liye
    elif action == "Create New Sale":
        st.subheader("Create New Sale")
        try:
            customers_list = Customers.get_all_customers()
        except Exception as e:
            customers_list = []
            st.error(f"Error loading customers: {e}")

        if not customers_list:
            st.warning("⚠️ Pehle Customers Management me jaakar customer add karein!")
        else:
            customer_options = {f"{cust[1]} (ID: {cust[0]})": cust[0] for cust in customers_list}
            
            with st.form("create_sale_form"):
                selected_cust_str = st.selectbox("Select Customer", options=list(customer_options.keys()))
                sale_date = st.date_input("Sale Date", value=date.today())
                total_amt = st.number_input("Total Amount (₹)", min_value=0.0, step=0.1)
                submitted = st.form_submit_button("Create Sale")

                if submitted:
                    try:
                        cust_id = customer_options[selected_cust_str]
                        Sales.insert_sales(int(cust_id), sale_date, float(total_amt))
                        st.success("🎉 Sale created successfully!")
                        st.toast("Sale Created!", icon="✅")
                    except Exception as e:
                        st.error(f"Error creating sale: {e}")

    # 3. UPDATE SALE: Existing sale ki details update karne ke liye
    elif action == "Update Sale":
        st.subheader("Update Sale Details")
        with st.form("update_sale_form"):
            s_id = st.number_input("Enter Sale ID to Update", min_value=1, step=1)
            cust_id_input = st.text_input("New Customer ID (Leave blank if no change)")
            sale_date_input = st.date_input("New Sale Date", value=None)
            total_amt_input = st.text_input("New Total Amount (Leave blank if no change)")
            update_submitted = st.form_submit_button("Update Sale")

            if update_submitted:
                cust_val = int(cust_id_input.strip()) if cust_id_input.strip() else None
                date_val = sale_date_input if sale_date_input else None
                amt_val = float(total_amt_input.strip()) if total_amt_input.strip() else None

                try:
                    Sales.update_sale(int(s_id), customer_id=cust_val, date=date_val, total_amount=amt_val)
                    st.success(f"✏️ Sale ID {s_id} updated successfully!")
                    st.toast("Sale Updated!", icon="✅")
                except Exception as e:
                    st.error(f"Error updating sale: {e}")

    # 4. DELETE SALE: Sale ID ke zariye record delete karne ke liye
    elif action == "Delete Sale":
        st.subheader("Delete a Sale Record")
        with st.form("delete_sale_form"):
            del_id = st.number_input("Enter Sale ID to Delete", min_value=1, step=1)
            delete_submitted = st.form_submit_button("Delete Sale", type="primary")

            if delete_submitted:
                try:
                    Sales.delete_sale(int(del_id))
                    st.success(f"🗑️ Sale ID {del_id} deleted successfully!")
                    st.toast("Sale Deleted!", icon="✅")
                except Exception as e:
                    st.error(f"Error deleting sale: {e}")

    # 5. VIEW SALE BY ID: Specific Sale ID ki details search karne ke liye
    elif action == "View Sale by ID":
        st.subheader("Search Sale by ID")
        with st.form("view_sale_id_form"):
            search_id = st.number_input("Enter Sale ID", min_value=1, step=1)
            search_submitted = st.form_submit_button("Search")

            if search_submitted:
                try:
                    sale_data = Sales.view_sale_id(int(search_id))
                    if sale_data:
                        st.success("Sale Record Found!")
                        for sale in sale_data:
                            col1, col2, col3, col4 = st.columns([1, 2, 3, 2])
                            col1.write(f"**ID:** {sale[0]}")
                            col2.write(f"**Customer ID:** {sale[1]}")
                            col3.write(f"**Date:** {sale[2]}")
                            col4.write(f"**Amount:** ₹{sale[3]}")
                    else:
                        st.warning(f"No sale found with ID: {search_id}")
                except Exception as e:
                    st.error(f"Error: {e}")

    # 6. GENERATE BILL: Sale ID select karke poora bill aur items display karne ke liye
    elif action == "Generate Bill":
        st.subheader("Generate Bill")
        try:
            sales_data = Sales.view_sales()
        except:
            sales_data = []

        if not sales_data:
            st.warning("⚠️ Koi sales record available nahi hai!")
        else:
            sale_options = {f"{sale[0]}": sale[0] for sale in sales_data}
            
            with st.form("generate_bill_form"):
                selected_sale_id = st.selectbox("Select Sale ID", options=list(sale_options.keys()))
                bill_submitted = st.form_submit_button("Generate Bill")

                if bill_submitted:
                    sale_id = int(selected_sale_id)
                    st.markdown("---")
                    st.subheader("BILL")
                    
                    sale_info = Sales.view_sale_id(sale_id)
                    if sale_info:
                        s = sale_info[0]
                        st.write(f"**Sale ID:** {s[0]}")
                        
                        try:
                            cur = conn.cursor()
                            cur.execute("SELECT name FROM customers WHERE id = %s", (s[1],))
                            cust_res = cur.fetchone()
                            cust_name = cust_res[0] if cust_res else f"Customer ID {s[1]}"
                            cur.close()
                        except:
                            cust_name = f"Customer ID {s[1]}"
                        
                        st.write(f"**Customer:** {cust_name}")
                        st.write(f"**Date:** {s[2]}")
                        
                        try:
                            cur = conn.cursor()
                            cur.execute("SELECT * FROM sale_items WHERE sale_id = %s", (sale_id,))
                            items = cur.fetchall()
                            cur.close()
                            
                            if items:
                                st.markdown("### Items")
                                for itm in items:
                                    st.write(f"- Product ID: {itm[2]} | Qty: {itm[3]} | Price: ₹{itm[4]}")
                                st.write(f"**Total Amount: ₹{s[3]}**")
                            else:
                                st.info("No items found for this sale.")
                        except Exception:
                            st.info("No items found for this sale.")

    # 7. SALES BY CUSTOMER: Kisi specific customer ki saari sales dekhne ke liye
    elif action == "Sales by Customer":
        st.subheader("View Sales by Customer ID")
        with st.form("sales_by_customer_form"):
            c_id = st.number_input("Enter Customer ID", min_value=1, step=1)
            cust_sales_submitted = st.form_submit_button("Fetch Sales")

            if cust_sales_submitted:
                try:
                    cust_sales = Sales.get_sales_by_customer(int(c_id))
                    if cust_sales:
                        st.success(f"Sales for Customer ID {c_id}:")
                        for sale in cust_sales:
                            col1, col2, col3, col4 = st.columns([1, 2, 3, 2])
                            col1.write(f"**Sale ID:** {sale[0]}")
                            col2.write(f"**Customer ID:** {sale[1]}")
                            col3.write(f"**Date:** {sale[2]}")
                            col4.write(f"**Amount:** ₹{sale[3]}")
                            st.divider()
                    else:
                        st.info(f"No sales found for Customer ID {c_id}")
                except Exception as e:
                    st.error(f"Error: {e}")
                    
                    
                    
elif menu_option == "Analytics & Reports":
    st.header("📈 Analytics & Reports")
    
    # Image ke mutabiq saare reports ke sub-options
    report_type = st.radio(
        "Select Report:",
        [
            "Sales Summary", 
            "Sales by Date Range", 
            "Top Selling Products", 
            "Customer Purchase History"
        ],
        horizontal=False
    )

    # 1. SALES SUMMARY: Total Revenue, Total Sales aur Total Customers dikhane ke liye
    if report_type == "Sales Summary":
        st.subheader("📊 Sales Summary Dashboard")
        try:
            cur = conn.cursor()
            cur.execute("SELECT SUM(total_amount), COUNT(id) FROM sales")
            rev_res = cur.fetchone()
            total_rev = rev_res[0] if rev_res and rev_res[0] is not None else 0.0
            total_sales = rev_res[1] if rev_res and rev_res[1] is not None else 0
            
            cur.execute("SELECT COUNT(id) FROM customers")
            cust_res = cur.fetchone()
            total_cust = cust_res[0] if cust_res and cust_res[0] is not None else 0
            cur.close()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Revenue", f"₹{total_rev:,.2f}")
            col2.metric("Total Sales", total_sales)
            col3.metric("Total Customers", total_cust)
            
            st.divider()
            st.subheader("Sales Trend Overview")
            sales_data = Sales.view_sales()
            if sales_data:
                import pandas as pd
                df = pd.DataFrame(sales_data, columns=["Sale ID", "Customer ID", "Date", "Total Amount"])
                df['Date'] = pd.to_datetime(df['Date'])
                chart_data = df.groupby('Date')['Total Amount'].sum().reset_index()
                st.line_chart(chart_data.set_index('Date')['Total Amount'])
            else:
                st.info("No sales data available for chart.")
        except Exception as e:
            st.error(f"Error loading summary: {e}")

    # 2. SALES BY DATE RANGE: Start date aur End date ke beech ki sales filter karne ke liye
    elif report_type == "Sales by Date Range":
        st.subheader("📅 Sales by Date Range")
        with st.form("date_range_form"):
            col1, col2 = st.columns(2)
            start_date = col1.date_input("Start Date")
            end_date = col2.date_input("End Date")
            submitted = st.form_submit_button("Fetch Report")

            if submitted:
                try:
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM sales WHERE date BETWEEN %s AND %s", (start_date, end_date))
                    filtered_sales = cur.fetchall()
                    cur.close()

                    if filtered_sales:
                        st.success(f"Found {len(filtered_sales)} sales between {start_date} and {end_date}:")
                        for sale in filtered_sales:
                            st.write(f"- Sale ID: {sale[0]} | Customer ID: {sale[1]} | Date: {sale[2]} | Amount: ₹{sale[3]}")
                    else:
                        st.info("No sales found in this date range.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # 3. TOP SELLING PRODUCTS: Sabse zyada bikne wale products ki list
    elif report_type == "Top Selling Products":
        st.subheader("🏆 Top Selling Products")
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT product_id, SUM(quantity) as total_qty 
                FROM sale_items 
                GROUP BY product_id 
                ORDER BY total_qty DESC LIMIT 5
            """)
            top_products = cur.fetchall()
            cur.close()

            if top_products:
                for idx, prod in enumerate(top_products, 1):
                    st.write(f"**{idx}. Product ID:** {prod[0]} | **Total Quantity Sold:** {prod[1]}")
            else:
                st.info("No product sales data found.")
        except Exception as e:
            st.error(f"Error loading top products: {e}")

    

    # 4. CUSTOMER PURCHASE HISTORY: Kisi specific customer ka purchase record
    elif report_type == "Customer Purchase History":
        st.subheader("👤 Customer Purchase History")
        with st.form("cust_history_form"):
            cust_id_input = st.number_input("Enter Customer ID", min_value=1, step=1)
            history_submitted = st.form_submit_button("View History")

            if history_submitted:
                try:
                    cur = conn.cursor()
                    # SELECT * use kiya taaki missing column ka error na aaye
                    cur.execute("SELECT * FROM customers WHERE id = %s", (int(cust_id_input),))
                    cust_info = cur.fetchone()
                    
                    if cust_info:
                        # cust_info[1] me customer ka naam hoga
                        st.write(f"**Customer Name:** {cust_info[1]}")
                        st.divider()
                        
                        sales_history = Sales.get_sales_by_customer(int(cust_id_input))
                        if sales_history:
                            st.markdown("### Purchase Records:")
                            for s in sales_history:
                                st.write(f"- Sale ID: {s[0]} | Date: {s[2]} | Amount: ₹{s[3]}")
                        else:
                            st.info("No purchase history found for this customer.")
                    else:
                        st.warning(f"No customer found with ID {cust_id_input}")
                    cur.close()
                except Exception as e:
                    conn.rollback() # Transaction reset karne ke liye
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
