# 🤖 Smart Inventory and Billing System

A complete **Inventory Management & Billing System** built with **Python** and **PostgreSQL**. The system provides two interfaces:

- 🌐 A modern, interactive **Streamlit Web Application** (`app.py`)
- 💻 A simple **Command-Line Interface** (`main.py`)

It helps you manage **Customers**, **Products**, and **Sales**, generate **bills**, and view **analytical reports** such as top-selling products and sales summaries.

---

## ✨ Features

### 📊 Dashboard
- Quick statistics: Total Customers, Total Products, Total Sales

### 👥 Customer Management
- Create customers table
- Add / Update / Delete / View customers

### 📦 Product Management
- Create products table
- Add / Update / Delete / View products (with name, description, price, quantity)
- View a single product by ID

### 💰 Sales Management
- Create sales table
- Create / Update / Delete / View sales
- View a sale by ID
- **Generate a bill** for a sale (with customer name and item details)
- View all sales for a specific customer

### 📈 Analytics & Reports
- Sales Summary (total revenue, total sales, total customers)
- Sales by Date Range
- Top 5 Selling Products
- Customer Purchase History

---

## 🛠️ Tech Stack

| Technology  | Purpose                              |
|-------------|--------------------------------------|
| **Python 3** | Core programming language           |
| **psycopg2** | PostgreSQL database driver          |
| **PostgreSQL** | Relational database                |
| **Streamlit** | Web UI framework                   |

---

## 📁 Project Structure

```
smart-and-invontry-billing-system/
├── app.py            # Streamlit web application (main UI)
├── main.py           # Command-line interface (CLI entry point)
├── database.py       # PostgreSQL connection setup
├── Customers.py      # Customer CRUD + menu operations
├── Products.py       # Product CRUD + menu operations
├── Sales.py          # Sales CRUD, billing, and analytical queries
├── SalesItem.py      # sale_items table creation
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

---

## 🗄️ Database Schema

The application uses a database named **`ecommerce`** with the following tables:

### `customers`
| Column   | Type           | Constraints        |
|----------|----------------|--------------------|
| id       | SERIAL         | PRIMARY KEY        |
| name     | VARCHAR(100)   | NOT NULL           |
| contact  | VARCHAR(15)    | NOT NULL           |

### `products`
| Column      | Type           | Constraints        |
|-------------|----------------|--------------------|
| id          | SERIAL         | PRIMARY KEY        |
| name        | VARCHAR(50)    | NOT NULL           |
| discription | TEXT           | NOT NULL           |
| price       | DECIMAL(10,2)  | NOT NULL           |
| quantity    | INTEGER        | NOT NULL           |

### `sales`
| Column       | Type           | Constraints                          |
|--------------|----------------|--------------------------------------|
| id           | SERIAL         | PRIMARY KEY                          |
| customer_id  | INTEGER        | FK → `customers(id)` ON DELETE CASCADE |
| date         | DATE           | NOT NULL                             |
| total_amount | DECIMAL(10,2)  | NOT NULL                             |

### `sale_items`
| Column      | Type           | Constraints                          |
|-------------|----------------|--------------------------------------|
| id          | SERIAL         | PRIMARY KEY                          |
| sale_id     | INTEGER        | FK → `sales(id)` ON DELETE CASCADE   |
| product_id  | INTEGER        | FK → `products(id)` ON DELETE CASCADE |
| quantity    | INTEGER        | NOT NULL                             |
| price       | DECIMAL(10,2)  | NOT NULL                             |

> Tables are created automatically by the app when you run it (choose the *Create Table* option in the CLI, or on first launch in the web app).


---

## 📋 Prerequisites

Before you begin, make sure you have installed:

- **Python 3.8+** — [python.org](https://www.python.org/downloads/)
- **PostgreSQL** — [postgresql.org](https://www.postgresql.org/download/)
- **Git** (optional, for cloning)

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/vikascodilogy/smart-and-invontry-billing-system.git
cd smart-and-invontry-billing-system
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Open **pgAdmin** or the **psql** shell and create the database:

```sql
CREATE DATABASE ecommerce;
```

### 5. Configure the database connection

Open `database.py` and update the connection credentials to match **your** local PostgreSQL setup:

```python
con = psycopg2.connect(
    host="localhost",
    database="ecommerce",
    user="postgres",
    password="YOUR_PASSWORD",   # ← change this
    port="5432"
)
```

> ⚠️ **Note:** Currently the password is hardcoded in `database.py`. For better security, consider using environment variables instead.


---

## ▶️ Running the Application

### 🌐 Streamlit Web App (Recommended)

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

### 💻 Command-Line Interface

```bash
python main.py
```

From the main menu you can choose:

```
1. Customer Management
2. Product Management
3. Sales Management
4. Exit Application
```

Each sub-menu lets you create tables, insert, update, delete, and view records, and (in Sales) generate bills and run analytical queries.

---

## 🖥️ Usage Guide (Streamlit UI)

| Page                    | What you can do                                                     |
|-------------------------|---------------------------------------------------------------------|
| **Dashboard**           | View total customers, products, and sales                           |
| **Customers Management**| View, add, update, and delete customers                             |
| **Product Management**  | View, add, update, delete, and search products by ID                |
| **Sales Management**    | Create, view, update, delete sales; generate bills; sales by customer |
| **Analytics & Reports** | Sales summary, date-range sales, top 5 products, customer history   |

---

## 🔮 Roadmap / Future Scope

- [ ] Add sales items management UI in the web app
- [ ] Stock-level alerts (low-quantity notifications)
- [ ] Export bills to PDF
- [ ] Authentication / login system
- [ ] Move database credentials to environment variables

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an **issue** or submit a **pull request**.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a pull request

---

## 📄 License

This project is open-source and available for learning and personal use.

---

<div align="center">
  Made with ❤️ using Python & PostgreSQL
</div>

