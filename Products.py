from database import conn
class Products:
    def __init__(self):
        pass
        
    @staticmethod
    def create_table():
        cur=conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS products(
                id SERIAL PRIMARY KEY,
                name varchar(50) not null,
                discription text not null,
                price decimal(10,2) not null,
                quantity integer not null   
            )"""
        )
        conn.commit()
        cur.close()
    @staticmethod
    def insert_product(name,discription,price,quantity):
        cur=conn.cursor()
        cur.execute(
            """INSERT INTO products(name,discription,price,quantity)
            values(%s,%s,%s,%s)""" ,
            (name,discription,price,quantity),
            
        )
        
        print(">>>>>>> Products Inserted!")
        conn.commit()
        cur.close()
        
    @staticmethod
    
    def update_product(product_id, name=None, discription=None, price=None, quantity=None):
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cur.fetchone()
        if not product:
            print(">>>>> Product Not Found!")
            cur.close()
            return

        update_fields = []
        if name:
            update_fields.append(f"name = '{name}'")
        if discription:
            update_fields.append(f"discription = '{discription}'")
        if price is not None:
            update_fields.append(f"price = {price}")
        if quantity is not None:
            update_fields.append(f"quantity = {quantity}")

        if update_fields:
            update_query = f"UPDATE products SET {','.join(update_fields)} WHERE id = %s"
            cur.execute(update_query, (product_id,))
            conn.commit()
        cur.close()
    @staticmethod
    def delete_product(product_id):
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM products WHERE id = %s",
            (product_id,)
        )
        conn.commit()
        cur.close()
            
    @staticmethod    
    def view_products():
        cur=conn.cursor()
        cur.execute("SELECT * FROM products")
        products=cur.fetchall()
        cur.close()
        return products
    
    @staticmethod
    def view_product_id(product_id):
        cur=conn.cursor()
        cur.execute("SELECT * FROM products where id = %s",(product_id,))
        products=cur.fetchone()
        cur.close()
        return products
  
    @staticmethod      
    def product_menu():
        while True:
            print("1.Create Table")
            print("2.Insert product")
            print("3.Update product")
            print("4.Delete product")
            print("5.view product")
            print("6.view_product by ID")
            print("0,Exit Product")
            
            choice=input("Enter choice")
            if choice =="1":
                Products().create_table()  
                print(">>>>>> product table created!")
            elif choice=="2":
                name=input("Enter product name")
                discription=input("Enter product discription")
                price=input("Enter product price")
                quantity=input("Enter product quantityt")
                Products().insert_product(name,discription,price,quantity)
               
                
            elif choice=="3":
                product_id=input("Enter the product id")
                name=input("Enter product name")
                discription=input("Enter product discription")
                price=input("Enter product price")
                quantity=input("Enter product quantity")
                Products().update_product(product_id,name,discription,price,quantity)
                print(">>>>>> product updated!")
                
            elif choice=="4":
                product_id=input("Enter the product id")
                Products().delete_product(product_id)
                print(">>>>>> product deleted!")
                            
                            
            elif choice=="5":
                products = Products().view_products()
                print(products)
                print(">>>>>> product fetched")
                
            elif choice=="6":
                product_id=input("Enter the product id")
                product = Products().view_product_id(product_id)
                print(product)
                print(">>>>>> product fetched")
                
            elif choice=="0":
                print("Exiting..")
                break
            
            else:
                print("Invalid choice. Please try again..")
                                        
# Products().product_menu()