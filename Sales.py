from database import conn


class Sales:
    def __init__(self):
        pass
    @staticmethod
    
    def create_table():
        cur=conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS sales(
                id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                data DATE NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                CONSTRAINT fk_sales_customer
                    FOREIGN KEY (customer_id)
                    REFERENCES customers(id)
                    on delete cascade
            )"""
        )
        conn.commit()
        cur.close()
    @staticmethod
    
    def insert_sales(customer_id,date,total_amount):
        cur=conn.cursor()
        cur.execute(
            """INSERT INTO sales(customer_id,date,total_amount)
            values(%s,%s,%s)""" ,
            (customer_id,date,total_amount),
        )
        
        print(">>>>>>> Sales Created!")
        conn.commit()
        cur.close()
    @staticmethod
    
    
    def update_sale(sale_id, customer_id=None, date=None, total_amount=None):
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM sales WHERE id = %s", (sale_id,))
            sale = cur.fetchone()
            if not sale:
                print(">>>>> Sale Not Found!")
                cur.close()
                return

            update_fields = []
            if customer_id is not None:
                update_fields.append(f"customer_id = {customer_id}")
            if date is not None:
                update_fields.append(f"date = '{date}'")
            if total_amount is not None:
                update_fields.append(f"total_amount = {total_amount}")

            if update_fields:
                update_query = f"UPDATE sales SET {','.join(update_fields)} WHERE id = %s"
                cur.execute(update_query, (sale_id,))
                conn.commit()
        except Exception as e:
            conn.rollback() # Transaction abort hone se bachane ke liye
            raise e
        finally:
            cur.close()
    @staticmethod
    
    def delete_sale(sale_id):
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM sales WHERE id = %s",
            (sale_id,)
        )
        conn.commit()
        cur.close()
    @staticmethod 
    
    def view_sales():
        cur=conn.cursor()
        cur.execute("SELECT * FROM sales")
        sales=cur.fetchall()
        cur.close()
        return sales  
    @staticmethod  
      
    def view_sale_id(sale_id):
        cur=conn.cursor()
        cur.execute("SELECT * FROM sales where id = %s",(sale_id,))
        sales=cur.fetchall()
        cur.close()
        return sales
    @staticmethod  
    
    def generate_bill(sale_id):
        cur=conn.cursor()
        cur.execute("SELECT * FROM Sales where id = %s",(sale_id,))
        sale_items=cur.fetchall()
        total_amount=0
        for item in sale_items:
            total_amount += item[4]* item[3]
        cur.close()
        return total_amount
    @staticmethod      
    #Analytical Queries    
    def total_sale_by_date(start_date,end_date):
        cur=conn.cursor()
        cur.execute(
           """SELECT product_id sum(quantity) as total_quantity 
            FROM sale_items
            group by product_id
            order by total_quantity desc
            limit 5,""")
        total_products=cur.fetchall()
        cur.close()
        return total_products
    @staticmethod
    def get_top_selling_products():
        cur=conn.cursor()
        cur.execute("SELECT * FROM sales where date between %s and %s",(start_date,end_date))
        total_sales=cur.fetchone()
        cur.close()
        return total_sales
    
    @staticmethod     
    def get_sales_by_customer(customer_id):
        cur = conn.cursor()
        # Single element tuple ke liye comma (customer_id,) zaroori hai
        cur.execute("SELECT * FROM sales WHERE customer_id = %s", (customer_id,))
        sales = cur.fetchall()
        cur.close()
        return sales
    
    @staticmethod
    def sales_menu():
        while True:
            print("1.Create Table")
            print("2.Insert Sale")
            print("3.Update Sale")
            print("4.Delete Sale")
            print("5.view Sale")
            print("6.view Sale by ID")
            print("7.Generate Bill")
            print("8.Total Sale by Date")
            print("9.Top 5 salling Products")
            print("10.Sales By Customer")
            print("0. Exit sales")
            
            choice=input("Enter choice")
            
            if choice =="1":
                Sales().create_table()  
                print(">>>>>> Sales table created!")
            elif choice=="2":
                
                customer_id=input("Enter the Customer ID")
                date=input("Enter the sales Date")
                total_amount=input("Enter the Enter sales Amount")
                
                Sales().insert_sales(customer_id,date,total_amount)
                print(">>>>>> Sales inserted!")
               
                
            elif choice=="3":
                customer_id=input("Enter the Customer ID")
                date=input("Enter the sales Date")
                total_amount=input("Enter the Enter sales Amount")
                Sales().update_sale(customer_id,date,total_amount)
                print(">>>>>> sales updated!")
                
            elif choice=="4":
                sale_id=input("Enter the sale id")
                Sales().delete_sale(sale_id)
                print(">>>>>> sale deleted!")
                            
                            
            elif choice=="5":
                sales = Sales().view_Sales()
                print(sales)
                print(">>>>>> sales fetched")
                
            elif choice=="6":
                sale_id=input("Enter the product id")
                sale = Sales().view_sale_id(sale_id)
                print(sale)
                print(">>>>>> sales fetched")
                
            elif choice=="7":
                sales_id=input("Enter sales id")
                sales = Sales().generate_bill(sale_id)
                print(sales)
                print(">>>>>> sales fetched")
                
            elif choice=="8":
                start_date=input("Enter Start Date")
                end_date=input("Enter end Date")
                bill = Sales().total_sale_by_date(start_date,end_date)
                print(bill)
                print(">>>>>> sales fetched")
                
            elif choice=="9":
                products = Sales().get_top_selling_products(start_date,end_date)
                print(products)
                print(">>>>>> products fetched")
                
            elif choice=="10":
                customer_id=input("Enter customer_id")
                sales = Sales().get_sales_by_customer(customer_id)
                print(sales)
                print(">>>>>> sales fetched")
                
            elif choice=="0":
                print("Exiting..")
                break
            
            else:
                print("Invalid choice. Please try again..")
                                        
# Sales().sales_menu()