import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

#function to create connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection

    except mysql.connector.Error as error:
        print("database connection error:", error)
        return None


# function to find daily sales
def daily_sales():
    connection=create_connection()
    cursor=connection.cursor()
    date=input("enter the date(YYYY-MM-DD):")
    query="""select s.sale_date,p.product_name,si.quantity,si.price,(si.quantity*si.price)as total
    from sales s
    join sale_items si 
    on s.sale_id=si.sale_id
    join products p 
    on si.product_id=p.product_id
    where s.sale_date=%s"""
    cursor.execute(query,(date,))
    records=cursor.fetchall()
    print("\n---------- DAILY SALES ---------")
    if records:
        for row in records:
            print("date:",row[0],
                  "|product:",row[1],
                  "|quantity:",row[2],
                  "|price:",row[3],
                  "|total:",row[4])
    else:
        print("no sales found for this date.")
    cursor.close()
    connection.close()            


#function to monthly sales
def monthly_sales():
    connection=create_connection()
    cursor=connection.cursor()
    month=input("enter month(YYYY-MM):")
    query="""select p.product_name,sum(si.quantity)as total_quantity,
    si.price,sum(si.quantity*si.price)as total
    from sales s
    join sale_items si
    on s.sale_id=si.sale_id
    join products p
    on si.product_id=p.product_id
    where date_format(s.sale_date,'%Y-%m')=%s
    group by p.product_id,
    p.product_name,si.price;"""
    cursor.execute(query,(month,))
    records=cursor.fetchall()
    print("\n------- MONTHLY SALES --------")
    if records:
        for row in records:
             print(
                    "product:",row[0],
                    "|quantity:",row[1],
                    "|price:",row[2],
                    "|total:",row[3])
    else:
        print("no sales found for this month.")
    cursor.close()
    connection.close()            


#function to find top 10 products
def top_products():
    connection=create_connection()
    cursor=connection.cursor()
    print("\n1.all time")
    print("2.specific month")
    print("3.specific year")
    choice=input("enter your choice:")
    if choice=="1":
        query="""select p.product_name,sum(si.quantity)as total_quantity,
        sum(si.quantity*si.price)as total
        from sale_items si
        join products p
        on si.product_id=p.product_id
        group by p.product_id,p.product_name
        order by total_quantity desc
        limit 10;"""
        cursor.execute(query) 
    elif choice=="2":
        month=input("enter month(YYYY-MM):")
        query="""select p.product_name,sum(si.quantity)as total_quantity,
        sum(si.quantity*si.price)as total
        from sales s
        join sale_items si
        on s.sale_id=si.sale_id
        join products p 
        on si.product_id=p.product_id
        where date_format(s.sale_date,'%Y-%m')=%s
        group by p.product_id,p.product_name
        order by total_quantity desc
        limit 10;"""
        cursor.execute(query,(month,))
    elif choice=="3":
        year=input("enter the year:")
        query="""select p.product_name,sum(si.quantity)as total_quantity,
        sum(si.quantity*si.price)as total
        from sales s
        join sale_items si 
        on s.sale_id=si.sale_id
        join products p
        on si.product_id=p.product_id
        where year(s.sale_date)=%s
        group by p.product_id,p.product_name
        order by total_quantity desc
        limit 10;"""
        cursor.execute(query,(year,))
    else:
        print("invalid choice")
        cursor.close()
        connection.close()
        return
    records=cursor.fetchall()
    print("\n--------TOP 10 PRODUCTS -------") 
    if records:
        for row in records:
            print("product:",row[0],
                  "quantity sold:",row[1],
                  "total:",row[2])                              
    else:
        print("no sales date found.")
    cursor.close()
    connection.close()   



#function to find top customers
def top_customers():
    connection = create_connection()
    cursor = connection.cursor()
    print("\n1. All Time")
    print("2. Specific Month")
    print("3. Specific Year")
    choice = input("Enter your choice: ")
    if choice == "1":
        query = """SELECT c.customer_name,
        SUM(si.quantity * si.price) AS total_spent
        FROM customers c
        JOIN sales s ON c.customer_id = s.customer_id
        JOIN sale_items si ON s.sale_id = si.sale_id
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_spent DESC;"""
        cursor.execute(query)
    elif choice == "2":
        month = input("Enter month (YYYY-MM): ")
        query = """SELECT c.customer_name,
        SUM(si.quantity * si.price) AS total_spent
        FROM customers c
        JOIN sales s ON c.customer_id = s.customer_id
        JOIN sale_items si ON s.sale_id = si.sale_id
        WHERE DATE_FORMAT(s.sale_date, '%Y-%m') = %s
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_spent DESC;"""
        cursor.execute(query, (month,))
    elif choice == "3":
        year = input("Enter year (YYYY): ")
        query = """SELECT c.customer_name,
        SUM(si.quantity * si.price) AS total_spent
        FROM customers c
        JOIN sales s ON c.customer_id = s.customer_id
        JOIN sale_items si ON s.sale_id = si.sale_id
        WHERE YEAR(s.sale_date) = %s
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_spent DESC;"""
        cursor.execute(query, (year,))
    else:
        print("Invalid choice")
        cursor.close()
        connection.close()
        return
    records = cursor.fetchall()
    print("\n------- TOP CUSTOMERS --------")
    if records:
        for row in records:
            print(
                "Customer:", row[0],
                "| Total Spent:", row[1]
            )
    else:
        print("No sales data found.")
    cursor.close()
    connection.close()  


#function to find product revenue              
def product_revenue():
    connection = create_connection()
    cursor = connection.cursor()
    print("\n1. All Time")
    print("2. Specific Month")
    print("3. Specific Year")
    choice = input("Enter your choice: ")
    if choice == "1":
        query = """SELECT p.product_name,
        SUM(si.quantity * si.price) AS revenue
        FROM products p
        JOIN sale_items si ON p.product_id = si.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC;"""
        cursor.execute(query)
    elif choice == "2":
        month = input("Enter month (YYYY-MM): ")
        query = """SELECT p.product_name,
        SUM(si.quantity * si.price) AS revenue
        FROM products p
        JOIN sale_items si ON p.product_id = si.product_id
        JOIN sales s ON si.sale_id = s.sale_id
        WHERE DATE_FORMAT(s.sale_date, '%Y-%m') = %s
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC;"""
        cursor.execute(query, (month,))
    elif choice == "3":
        year = input("Enter year (YYYY): ")
        query = """SELECT p.product_name,
        SUM(si.quantity * si.price) AS revenue
        FROM products p
        JOIN sale_items si ON p.product_id = si.product_id
        JOIN sales s ON si.sale_id = s.sale_id
        WHERE YEAR(s.sale_date) = %s
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC;"""
        cursor.execute(query, (year,))
    else:
        print("Invalid choice")
        cursor.close()
        connection.close()
        return
    records = cursor.fetchall()
    print("\n------- PRODUCT REVENUE -------")
    if records:
        for row in records:
            print(
                "Product:", row[0],
                "| Revenue:", row[1]
            )
    else:
        print("No sales data found.")
    cursor.close()
    connection.close()


#function to find average order value
def average_order_value():
    connection = create_connection()
    cursor = connection.cursor()
    print("\n1. All Time")
    print("2. Specific Month")
    print("3. Specific Year")
    choice = input("Enter your choice: ")
    if choice == "1":
        query = """SELECT AVG(order_total) AS average_order_value
        FROM (SELECT s.sale_id,
            SUM(si.quantity * si.price) AS order_total
            FROM sales s
            JOIN sale_items si ON s.sale_id = si.sale_id
            GROUP BY s.sale_id
            ) AS orders;"""
        cursor.execute(query)
    elif choice == "2":
        month = input("Enter month (YYYY-MM): ")
        query = """SELECT AVG(order_total) AS average_order_value
        FROM (SELECT s.sale_id,
            SUM(si.quantity * si.price) AS order_total
            FROM sales s
            JOIN sale_items si ON s.sale_id = si.sale_id
            WHERE DATE_FORMAT(s.sale_date, '%Y-%m') = %s
            GROUP BY s.sale_id
            ) AS orders;"""
        cursor.execute(query, (month,))
    elif choice == "3":
        year = input("Enter year (YYYY): ")
        query = """SELECT AVG(order_total) AS average_order_value
        FROM (SELECT s.sale_id,
            SUM(si.quantity * si.price) AS order_total
            FROM sales s
            JOIN sale_items si ON s.sale_id = si.sale_id
            WHERE YEAR(s.sale_date) = %s
            GROUP BY s.sale_id
            ) AS orders;"""
        cursor.execute(query, (year,))
    else:
        print("Invalid choice")
        cursor.close()
        connection.close()
        return
    result = cursor.fetchone()
    print("\n===== AVERAGE ORDER VALUE =====")
    if result and result[0] is not None:
        print("Average Order Value:", result[0])
    else:
        print("No sales data found.")
    cursor.close()
    connection.close() 


# Main menu
while True:
    print("\n======= SALES ANALYSIS SYSTEM =======")
    print("1. Daily Sales")
    print("2. Monthly Sales")
    print("3. Top 10 Products")
    print("4. Top Customers")
    print("5. Product Revenue")
    print("6. Average Order Value")
    print("7. Exit")
    print("==================================")
    choice = input("Enter your choice: ")
    if choice == "1":
        daily_sales()
    elif choice == "2":
        monthly_sales()
    elif choice == "3":
        top_products()
    elif choice == "4":
        top_customers()
    elif choice == "5":
        product_revenue()
    elif choice == "6":
        average_order_value()
    elif choice == "7":
        print("Exiting...")
        break
    else:
        print("Invalid choice")
       