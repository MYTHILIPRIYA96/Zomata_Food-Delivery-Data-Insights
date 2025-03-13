import streamlit as st
import mysql.connector
import pandas as pd
from faker import Faker
from datetime import datetime
import uuid
import plotly.express as px

# Initialize Faker
fake = Faker("en_IN")

# Database Class
class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def fetch_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def add_customer(self, customer_id, name, email, phone):
        query = "INSERT INTO customers(customer_id, name, email, phone) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (customer_id, name, email, phone))
        self.connection.commit()

    def add_restaurant(self, restaurant_id, name, location, cuisine_type):
        query = "INSERT INTO restaurants (restaurant_id, name, location, cuisine_type) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (restaurant_id, name, location, cuisine_type))
        self.connection.commit()

    def add_order(self, order_id, customer_id, restaurant_id, order_date, total_amount, status,payment_mode):
        query = """
        INSERT INTO orders (order_id, customer_id, restaurant_id, order_date, total_amount, status,payment_mode)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (order_id, customer_id, restaurant_id, order_date, total_amount, status,payment_mode))
        self.connection.commit()

    def add_delivery(self, delivery_id, order_id, delivery_person_id, delivery_time, status):
        query = """
        INSERT INTO deliveries (delivery_id, order_id, delivery_person_id, delivery_time, status)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (delivery_id, order_id, delivery_person_id, delivery_time, status))
        self.connection.commit()

    def add_delivery_person(self, delivery_person_id, name,  contact_number):
        query = """
        INSERT INTO delivery_persons (delivery_person_id, name, contact_number)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (delivery_person_id, name,  contact_number))
        self.connection.commit()


    def update_customer(self, customer_id, name, email, phone):
        query = "UPDATE customers SET name=%s, email=%s, phone=%s WHERE customer_id=%s"
        self.cursor.execute(query, (name, email, phone, customer_id))
        self.connection.commit()

    def update_restaurant(self, restaurant_id, name, location, cuisine_type):
        query = "UPDATE restaurants SET name=%s, location=%s, cuisine_type=%s WHERE restaurant_id=%s"
        self.cursor.execute(query, (name, location, cuisine_type, restaurant_id))
        self.connection.commit()

    def update_order(self, order_id, customer_id, restaurant_id, order_date, total_amount, status):
        query = """
        UPDATE orders SET customer_id=%s, restaurant_id=%s, order_date=%s,
        total_amount=%s, status=%s WHERE order_id=%s
        """
        self.cursor.execute(query, (customer_id, restaurant_id, order_date, total_amount, status, order_id))
        self.connection.commit()

    def update_delivery(self, delivery_id, order_id, delivery_person, delivery_time, status):
        query = """
        UPDATE deliveries SET order_id=%s, delivery_person=%s, delivery_time=%s, status=%s
        WHERE delivery_id=%s
        """
        self.cursor.execute(query, (order_id, delivery_person, delivery_time, status, delivery_id))
        self.connection.commit()

    def update_delivery_person(self, delivery_person_id, name,  contact_number):
        query = """
        UPDATE delivery_persons
        SET  name=%s,  contact_number=%s
        WHERE delivery_person_id=%s
        """
        self.cursor.execute(query, (name, contact_number, delivery_person_id))
        self.connection.commit()

    def delete_customer(self, name):
        query = "DELETE FROM customers WHERE name=%s"
        self.cursor.execute(query, (name,))
        self.connection.commit()

    def delete_restaurant(self, name):
        query = "DELETE FROM restaurants WHERE name=%s"
        self.cursor.execute(query, (name,))
        self.connection.commit()

    def delete_order_by_id(self, order_id):
        query = "DELETE FROM orders WHERE order_id=%s"
        self.cursor.execute(query, (order_id,))
        self.connection.commit()

    def delete_delivery_by_id(self, delivery_id):
        query = "DELETE FROM deliveries WHERE delivery_id=%s"
        self.cursor.execute(query, (delivery_id,))
        self.connection.commit()

    def delete_delivery_person_by_id(self, delivery_person_id):
        query = "DELETE FROM delivery_persons WHERE delivery_person_id=%s"
        self.cursor.execute(query, (delivery_person_id,))
        self.connection.commit()

# Database Connection Configuration
def db_config():
    return mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="3obbBvALArqQPqW.root",
    password="MtV1PAc27naJolYM",
    database="zomato"
)
db = Database(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com", user="3obbBvALArqQPqW.root", password="MtV1PAc27naJolYM", database="zomato")
connection = db.connection

# Sidebar Navigation
st.sidebar.title("Zomato Data Management")
menu = st.sidebar.selectbox("Select Action", ["Home", "CRUD Operations", "SQL Queries", "Visualizations"])

# Main Content
def main():
    if menu == "Home":
        st.title("Zomato Data Management Dashboard")
        st.markdown("""
        Welcome to the Zomato Streamlit App  
        Use the left sidebar to perform CRUD Operations, run SQL queries, and view visualizations.
        """)

    elif menu == "CRUD Operations":
        st.title("CRUD Operations")

        table_name = st.sidebar.selectbox("Select Table", ["Customers", "Restaurants", "Orders", "Deliveries", "Delivery Persons"])
        operation = st.sidebar.radio("Select Operation", ["Create", "Read", "Update", "Delete"])

        # ---------- CREATE ----------
        if operation == "Create":
            st.subheader(f"Add New Record to {table_name}")

            if table_name == "Customers":
                name = st.text_input("Customer Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                if st.button("Add Customer"):
                    customer_id = str(uuid.uuid4())
                    db.add_customer(customer_id, name, email, phone)
                    st.success("Customer Added Successfully")

            elif table_name == "Restaurants":
                name = st.text_input("Restaurant Name")
                location = st.text_input("Location")
                cuisine_type = st.text_input("Cuisine Type")
                if st.button("Add Restaurant"):
                    restaurant_id = str(uuid.uuid4())
                    db.add_restaurant(restaurant_id, name, location, cuisine_type)
                    st.success("Restaurant Added Successfully")

            elif table_name == "Orders":
                # Fetch existing valid customer and restaurant IDs from DB
                customer_ids = [str(row[0]) for row in db.fetch_all("SELECT customer_id FROM customers")]
                restaurant_ids = [str(row[0]) for row in db.fetch_all("SELECT restaurant_id FROM restaurants")]
                selected_customer_id = st.selectbox("Select Customer ID", customer_ids)
                selected_restaurant_id = st.selectbox("Select Restaurant ID", restaurant_ids)
                order_date = st.date_input("Order Date")
                total_amount = st.number_input("Total Amount", min_value=0.0)
                status = st.selectbox("Status", ["Pending", "Delivered", "Cancelled"])
                payment_mode = st.selectbox("Payment Mode", ["credit card", "cash", "UPI", "debit card", "net banking"])
                if st.button("Add Order"):
                    order_id = str(uuid.uuid4())
                    db.add_order(order_id, selected_customer_id, selected_restaurant_id, order_date, total_amount, status,payment_mode)
                    st.success("Order Added Successfully")

            elif table_name == "Deliveries":
               order_ids = [str(row[0]) for row in db.fetch_all("SELECT order_id FROM orders")]
               order_id = st.selectbox("Select Order ID", order_ids)
               delivery_person_ids  = [str(row[0]) for row in db.fetch_all("SELECT delivery_person_id FROM delivery_persons")]
               delivery_person_id = st.selectbox("Select Delivery Person ID", delivery_person_ids)
               delivery_time = st.time_input("Delivery Time")
               status = st.selectbox("Delivery Status", ["In Transit", "Delivered", "Delayed"])
               if st.button("Add Delivery"):
                  delivery_id = str(uuid.uuid4())
                  db.add_delivery(delivery_id, order_id, delivery_person_id, str(delivery_time), status)
                  st.success("Delivery Added Successfully")


            elif table_name == "Delivery_Persons":
                name = st.text_input("Name")
                contact_number = st.text_input("Contact Number")
                if st.button("Add Delivery Person"):
                   delivery_person_id = str(uuid.uuid4())
                   db.add_delivery_person(delivery_person_id, name, contact_number)
                   st.success("Delivery Person Added Successfully")

            # Show updated data
            st.subheader(f"Updated Data in `{table_name}`")
            df = pd.read_sql(f"SELECT * FROM {table_name.lower()}", connection)
            st.dataframe(df)

        # ---------- READ ----------
        elif operation == "Read":
            st.subheader(f"Data from `{table_name}` Table")
            df = pd.read_sql(f"SELECT * FROM {table_name.lower()}", connection)
            st.dataframe(df)

        # ---------- UPDATE ----------
        elif operation == "Update":
            st.subheader(f"Update Record in `{table_name}`")

            if table_name == "Customers":
                customer_id = st.text_input("Customer ID (existing)")
                name = st.text_input("New Name")
                email = st.text_input("New Email")
                phone = st.text_input("New Phone")
                if st.button("Update Customer"):
                    db.update_customer(customer_id, name, email, phone)
                    st.success("Customer Updated Successfully")

            elif table_name == "Restaurants":
                restaurant_id = st.text_input("Restaurant ID (existing)")
                name = st.text_input("New Name")
                location = st.text_input("New Location")
                cuisine_type = st.text_input("New Cuisine Type")
                if st.button("Update Restaurant"):
                    db.update_restaurant(restaurant_id, name, location, cuisine_type)
                    st.success("Restaurant Updated Successfully")

            elif table_name == "Orders":
                order_ids = [str(row[0]) for row in db.fetch_all("SELECT order_id FROM orders")]
                customer_ids = [str(row[0]) for row in db.fetch_all("SELECT customer_id FROM customers")]
                restaurant_ids = [str(row[0]) for row in db.fetch_all("SELECT restaurant_id FROM restaurants")]
                selected_order_id = st.selectbox("Select Order ID to Update", order_ids)
                selected_customer_id = st.selectbox("New Customer ID", customer_ids)
                selected_restaurant_id = st.selectbox("New Restaurant ID", restaurant_ids)
                order_date = st.date_input("New Order Date")
                total_amount = st.number_input("New Total Amount", min_value=0.0)
                status = st.selectbox("New Status", ["Pending", "Delivered", "Cancelled"])
                if st.button("Update Order"):
                    db.update_order(selected_order_id, selected_customer_id, selected_restaurant_id, order_date, total_amount, status)
                    st.success("Order Updated Successfully")

            elif table_name == "Deliveries":
                delivery_ids = [str(row[0]) for row in db.fetch_all("SELECT delivery_id FROM deliveries")]
                order_ids = [str(row[0]) for row in db.fetch_all("SELECT order_id FROM orders")]
                selected_delivery_id = st.selectbox("Select Delivery ID to Update", delivery_ids)
                selected_order_id = st.selectbox("New Order ID", order_ids)
                delivery_person = st.text_input("New Delivery Person")
                delivery_time = st.time_input("New Delivery Time")
                status = st.selectbox("New Delivery Status", ["In Transit", "Delivered", "Delayed"])
                if st.button("Update Delivery"):
                    db.update_delivery(selected_delivery_id, selected_order_id, delivery_person, str(delivery_time), status)
                    st.success("Delivery Updated Successfully")

            elif table_name == "Delivery_Persons":
                delivery_person_id = st.text_input("Delivery Person ID (existing)")
                name = st.text_input("New Name")
                contact_number = st.text_input("New Contact Number")
                if st.button("Update Delivery Person"):
                   db.update_delivery_person(delivery_person_id, name, contact_number)
                   st.success("Delivery Person Updated Successfully")

            st.subheader(f"Updated Data in `{table_name}`")
            df = pd.read_sql(f"SELECT * FROM {table_name.lower()}", connection)
            st.dataframe(df)

        # ---------- DELETE ----------
        elif operation == "Delete":
            st.subheader(f" Delete Record from `{table_name}`")

            if table_name == "Customers":
                name = st.text_input("Customer Name to Delete")
                if st.button("Delete Customer"):
                    db.delete_customer(name)
                    st.success(" Customer Deleted Successfully")

            elif table_name == "Restaurants":
                name = st.text_input("Restaurant Name to Delete")
                if st.button("Delete Restaurant"):
                    db.delete_restaurant(name)
                    st.success("Restaurant Deleted Successfully")

            elif table_name == "Orders":
                order_id = st.text_input("Order ID to Delete")
                if st.button("Delete Order"):
                    db.delete_order_by_id(order_id)
                    st.success("Order Deleted Successfully")

            elif table_name == "Deliveries":
                delivery_id = st.text_input("Delivery ID to Delete")
                if st.button("Delete Delivery"):
                    db.delete_delivery_by_id(delivery_id)
                    st.success("Delivery Deleted Successfully")

            elif table_name == "Delivery_Persons":
                delivery_person_ids = [str(row[0]) for row in db.fetch_all("SELECT delivery_person_id FROM delivery_persons")]
                selected_id = st.selectbox("Select Delivery Person ID to Delete", delivery_person_ids)
                if st.button("Delete Delivery Person"):
                   db.delete_delivery_person_by_id(selected_id)
                   st.success("Delivery Person Deleted Successfully")
                   
            st.subheader(f"Updated Data in `{table_name}`")
            df = pd.read_sql(f"SELECT * FROM {table_name.lower()}", connection)
            st.dataframe(df)



    elif menu == "SQL Queries":
        st.title("SQL Queries for Business Insights ")
        
# Database connection
connection = db_config()
cursor = connection.cursor()

# Sidebar for SQL Queries
query_options = [
    "Query 1: Peak Ordering Locations",
    "Query 2: Peak Ordering Times",
    "Query 3: Orders with Delivery Delays",
    "Query 4: Cancelled Deliveries",
    "Query 5: Top Customers by Order Frequency",
    "Query 6: Top Customers by Total Order Value",
    "Query 7: Average Delivery Time",
    "Query 8: Preferred Cuisines",
    "Query 9: Deliveries per Delivery Person",
    "Query 10: Average Delivery Time by Delivery Person",
    "Query 11: Most Popular Cuisines",
    "Query 12: Most Popular Restaurants by Order Frequency",
    "Query 13: Average Order Value by Restaurant",
    "Query 14: Identify the Days with the Most Orders",
    "Query 15: Restaurants with Highest Total Order Value",
    "Query 16: Peak Ordering Times for Each Restaurant",
    "Query 17: Restaurants with High Cancelled Orders",
    "Query 18: Most Popular Cuisines Among Customers",
    "Query 19: Top 10 High-Value & High-Rated Customers",
    "Query 20: Orders with Significant Delivery Delays"
]
selected_query_option = st.sidebar.selectbox("Select SQL operation:", query_options)

queries = {
    "Query 1: Peak Ordering Locations": """
           SELECT location, COUNT(*) AS order_count
           FROM orders o
           JOIN restaurants r ON o.restaurant_id = r.restaurant_id
           GROUP BY location
           ORDER BY order_count DESC;""",
    
    "Query 2: Peak Ordering Times": """
           SELECT HOUR(order_date) AS order_hour, COUNT(*) AS order_count
           FROM orders
           GROUP BY order_hour
           ORDER BY order_count DESC;
    """,
     "Query 3: Orders with Delivery Delays":
        """SELECT order_id, order_date, delivery_time
           FROM orders
           WHERE TIMESTAMPDIFF(MINUTE, order_date, delivery_time) > 30;""",

    "Query 4: Cancelled Deliveries": """
        SELECT order_id, order_date, status
        FROM orders
        WHERE status = 'Cancelled';
    """,

    "Query 5: Top Customers by Order Frequency": """
        SELECT c.customer_id, c.name, COUNT(o.order_id) AS total_orders
        FROM customers c 
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        ORDER BY total_orders DESC
        LIMIT 10;
    """,

    "Query 6: Top Customers by Total Order Value": """
        SELECT c.customer_id, c.name, ROUND(SUM(o.total_amount)) AS total_order_value
        FROM customers c 
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        ORDER BY total_order_value DESC
        LIMIT 10;
    """,

    "Query 7: Average Delivery Time": """
        SELECT ROUND(AVG(TIMESTAMPDIFF(MINUTE, order_date, delivery_time))) AS average_delivery_time
        FROM orders;
    """,

    "Query 8: Preferred Cuisines": """
        SELECT preferred_cuisine, COUNT(*) AS cuisine_count
        FROM customers
        GROUP BY preferred_cuisine
        ORDER BY cuisine_count DESC
        LIMIT 6;
    """,

    "Query 9: Deliveries per Delivery Person": """
        SELECT dp.delivery_person_id, dp.name, COUNT(d.delivery_id) AS total_deliveries
        FROM delivery_persons dp
        JOIN deliveries d ON dp.delivery_person_id = d.delivery_person_id
        GROUP BY dp.delivery_person_id, dp.name
        ORDER BY total_deliveries DESC;
    """,

    "Query 10: Average Delivery Time by Delivery Person": """
        SELECT dp.delivery_person_id, dp.name, ROUND(AVG(TIMESTAMPDIFF(MINUTE, o.order_date, o.delivery_time))) AS avg_delivery_time
        FROM delivery_persons dp
        JOIN deliveries d ON dp.delivery_person_id = d.delivery_person_id
        JOIN orders o ON d.order_id = o.order_id
        GROUP BY dp.delivery_person_id, dp.name
        ORDER BY avg_delivery_time;
    """,

    "Query 11: Most Popular Cuisines": """
        SELECT r.cuisine_type, COUNT(o.order_id) AS cuisine_frequency
        FROM restaurants r
        JOIN orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.cuisine_type
        ORDER BY cuisine_frequency DESC;
    """,

    "Query 12: Most Popular Restaurants by Order Frequency": """
        SELECT r.restaurant_id, r.name, COUNT(o.order_id) AS order_frequency
        FROM restaurants r
        JOIN orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.restaurant_id, r.name
        ORDER BY order_frequency DESC;
    """,

    "Query 13: Average Order Value by Restaurant": """
        SELECT r.restaurant_id, r.name, ROUND(AVG(o.total_amount), 2) AS avg_order_value
        FROM restaurants r
        JOIN orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.restaurant_id, r.name
        ORDER BY avg_order_value DESC;
    """,

    "Query 14: Identify the Days with the Most Orders": """
        SELECT DAYOFWEEK(order_date) AS day_of_week, COUNT(*) AS order_count
        FROM orders
        GROUP BY day_of_week
        ORDER BY order_count DESC;
    """,

    "Query 15: Restaurants with Highest Total Order Value": """
        SELECT r.restaurant_id, r.name, ROUND(SUM(o.total_amount)) AS total_order_value
        FROM restaurants r
        JOIN orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.restaurant_id, r.name
        ORDER BY total_order_value DESC
        LIMIT 10;
    """,

    "Query 16: Peak Ordering Times for Each Restaurant": """
        SELECT r.restaurant_id, r.name, HOUR(o.order_date) AS order_hour, COUNT(o.order_id) AS hourly_order_frequency
        FROM restaurants r
        JOIN orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.restaurant_id, r.name, order_hour
        ORDER BY r.restaurant_id, hourly_order_frequency DESC;
    """,

    "Query 17: Restaurants with High Cancelled Orders": """
        SELECT r.restaurant_id, r.name, COUNT(o.order_id) AS cancelled_orders
        FROM restaurants r
        JOIN orders o ON r.restaurant_id = o.restaurant_id
        WHERE o.status = 'Cancelled'
        GROUP BY r.restaurant_id, r.name
        ORDER BY cancelled_orders DESC
        LIMIT 10;
    """,

    "Query 18: Most Popular Cuisines Among Customers": """
        SELECT c.preferred_cuisine, COUNT(*) AS cuisine_count, ROUND(AVG(o.total_amount)) AS avg_order_value
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.preferred_cuisine
        LIMIT 6;
    """,

    "Query 19: Top 10 High-Value & High-Rated Customers": """
        SELECT c.customer_id, c.name, SUM(o.total_amount) AS total_order_value, ROUND(AVG(o.feedback_rating)) AS avg_rating
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        HAVING avg_rating > 4
        ORDER BY total_order_value DESC
        LIMIT 10;
    """,

    "Query 20: Orders with Significant Delivery Delays": """
        SELECT order_id, order_date, delivery_time
        FROM orders
        WHERE TIMESTAMPDIFF(MINUTE, order_date, delivery_time) > 15;
    """}
# Run the selected query
if st.button("Run Query"):
    if connection:
        st.write(f"Running: {selected_query_option}")
        df = pd.read_sql(queries[selected_query_option],connection )
        st.write(df)


    def fetch_data(query):
     connection= db_config()
     df = pd.read_sql(query, connection)
     connection.close()
     return df

elif menu == "Visualizations":
        st.title("Data Visualizations")
    
        queries = {
    "Peak Ordering Times": """
        SELECT HOUR(order_date) AS order_hour, COUNT(*) AS order_count 
        FROM orders 
        GROUP BY order_hour 
        ORDER BY order_count DESC;
    """,
    
    "Orders with Delivery Delays": """
        SELECT order_id, TIMESTAMPDIFF(MINUTE, order_date, delivery_time) AS delay_minutes 
        FROM orders 
        WHERE TIMESTAMPDIFF(MINUTE, order_date, delivery_time) > 30;
    """,
    
    "Top Customers by Order Frequency": """
        SELECT c.name AS customer_name, COUNT(o.order_id) AS total_orders 
        FROM customers c 
        JOIN orders o ON c.customer_id = o.customer_id 
        GROUP BY c.customer_id, c.name 
        ORDER BY total_orders DESC 
        LIMIT 10;
    """,
    
    "Preferred Cuisines": """
        SELECT preferred_cuisine, COUNT(*) AS cuisine_count 
        FROM customers 
        GROUP BY preferred_cuisine 
        ORDER BY cuisine_count DESC 
        LIMIT 6;
    """,
    
    "Most Popular Restaurants by Order Frequency": """
        SELECT r.name AS restaurant_name, COUNT(o.order_id) AS order_frequency
        FROM restaurants r
        JOIN orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.restaurant_id, r.name
        ORDER BY order_frequency DESC;
    """,
    
    "Orders with Significant Delivery Delays": """
        SELECT order_id, TIMESTAMPDIFF(MINUTE, order_date, delivery_time) AS delay_minutes
        FROM orders
        WHERE TIMESTAMPDIFF(MINUTE, order_date, delivery_time) > 15;
    """,
    
    "Top Customers by Total Order Value": """
        SELECT c.name AS customer_name, ROUND(SUM(o.total_amount)) AS total_order_value
        FROM customers c 
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        ORDER BY total_order_value DESC
        LIMIT 10;
    """
}

        
        selected_query = st.sidebar.selectbox("Select Visualization Query", list(queries.keys()))

        if st.button("Generate Chart"):
            connection = db_config()
            df = pd.read_sql(queries[selected_query], connection)
            connection.close()


            if selected_query == "Peak Ordering Times":
                fig = px.bar(df, x="order_hour", y="order_count", title="Peak Ordering Times", labels={"order_hour": "Hour", "order_count": "Number of Orders"})
                st.plotly_chart(fig)

            elif selected_query == "Orders with Delivery Delays":
                fig = px.bar(df, x="delay_minutes", title="Orders with Delivery Delays", labels={"delay_minutes": "Delay in Minutes"})
                st.plotly_chart(fig)

            elif selected_query == "Top Customers by Order Frequency":
                fig = px.bar(df, x="customer_name", y="total_orders", title="Top Customers by Order Frequency", labels={"customer_name": "Customer Name", "total_orders": "Order Count"})
                st.plotly_chart(fig)

            elif selected_query == "Preferred Cuisines":
                fig = px.pie(df, names="preferred_cuisine", values="cuisine_count", 
                title=" Preferred Cuisines Among Customers", hole=0.4)
                st.plotly_chart(fig)

            elif selected_query == "Most Popular Restaurants by Order Frequency":
                fig = px.bar(df, x="restaurant_name", y="order_frequency", 
                title=" Most Popular Restaurants", color="order_frequency", 
                color_continuous_scale="Viridis")
                st.plotly_chart(fig)

            elif selected_query == "Orders with Significant Delivery Delays":
                fig = px.bar(df, x="order_id", y="delay_minutes",
                title="Orders with Significant Delivery Delays",
                labels={"order_id": "Order ID", "delay_minutes": "Delay (Minutes)"},
                color="delay_minutes", color_continuous_scale="Reds")
                st.plotly_chart(fig, use_container_width=True) 

            elif selected_query == "Top Customers by Total Order Value":
                fig = px.bar(df, x="customer_name", y="total_order_value", 
                title="Top Customers by Total Order Value", 
                labels={"customer_name": "Customer", "total_order_value": "Order Value"}, 
                color="total_order_value", color_continuous_scale="Blues")
                st.plotly_chart(fig, use_container_width=True)
                
if __name__ == "__main__":
    main()
