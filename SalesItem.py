from database import conn
class SaleItems:
    def create_table():
        
        @staticmethod
        def create_table():
            cur=conn.cursor()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS sale_items(
                    id SERIAL PRIMARY KEY,
                    sale_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    CONSTRAINT fk_sale_items_sale
                        FOREIGN KEY (sale_id)
                        REFERENCES sales(id)
                        on delete cascade,
                    CONSTRAINT fk_sale_items_product
                        FOREIGN KEY (product_id)
                        REFERENCES Products(id)
                        on delete cascade,
                )"""
            )
            conn.commit()
            cur.close()