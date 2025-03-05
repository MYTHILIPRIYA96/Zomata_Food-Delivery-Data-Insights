import streamlit as st
import mysql.connector
import pandas as pd
from faker import Faker
import plotly.express as px

# Initialize Faker
fake = Faker("en_IN")

# Database Class
class Database:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
    
    def create_user_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(15),
            address TEXT
        )'''
        self.cursor.execute(query)
        self.conn.commit()
    
    def add_user(self, name, email, phone, address):
        query = "INSERT INTO users (name, email, phone, address) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (name, email, phone, address))
        self.conn.commit()
    
    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()
    
    def update_user(self, user_id, name, email, phone, address):
        query = "UPDATE users SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
        self.cursor.execute(query, (name, email, phone, address, user_id))
        self.conn.commit()
    
    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id=%s"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()

# Database Connection Configuration
def db_config():
    return mysql.connector.connect(
        user='3obbBvALArqQPqW.root',
        password='MtV1PAc27naJolYM',
        host='gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
        database='zomato'
    )

db = Database(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com", user="3obbBvALArqQPqW.root", password="MtV1PAc27naJolYM", database="zomato")
conn = db.conn

# Sidebar Navigation
st.sidebar.title("Zomato Data Management")
page = st.sidebar.radio("Go to", ["CRUD Operations", "SQL Queries", "Visualizations"])

def main():
    if page == "CRUD Operations":
        st.title("Manage Database Records")
        table_name = "users"
        menu = ["Create", "Read", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Create":
            st.subheader("Add User")
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_area("Address")
            if st.button("Add User"):
                db.add_user(name, email, phone, address)
                st.success("User Added Successfully")
                # Show updated table data
            st.subheader(f"Updated Data in `{table_name}`")
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            st.dataframe(df)

        elif choice == "Read":
            st.subheader("Read Users")
            users = db.get_users()
            df = pd.DataFrame(users, columns=["ID", "Name", "Email", "Phone", "Address"])
            st.dataframe(df.head())

        elif choice == "Update":
            st.subheader("Update User")
            user_id = st.number_input("User ID", min_value=1, step=1)
            name = st.text_input("New Name")
            email = st.text_input("New Email")
            phone = st.text_input("New Phone")
            address = st.text_area("New Address")
            if st.button("Update User"):
                db.update_user(user_id, name, email, phone, address)
                st.success("User Updated Successfully")
                 # Fetch and display the updated user table
            st.subheader("Updated User")
            users = db.get_users()
            df = pd.DataFrame(users, columns=["ID", "Name", "Email", "Phone", "Address"])
            st.dataframe(df) 
    

        elif choice == "Delete":
            st.subheader("Delete User")
            user_id = st.number_input("User ID", min_value=1, step=1)
            if st.button("Delete User"):
                db.delete_user(user_id)
                st.success("User Deleted Successfully")
                 # Show updated table data
            st.subheader(f"Updated Data in `{table_name}`")
            df = pd.read_sql(f"SELECT * FROM {table_name} ", conn)
            st.dataframe(df)



    elif page == "SQL Queries":
        st.title("SQL Query Execution")
        
# Database connection
conn = db_config()
cursor = conn.cursor()

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
    if conn:
        st.write(f"Running: {selected_query_option}")
        df = pd.read_sql(queries[selected_query_option],conn )
        st.write(df)


    def fetch_data(query):
     conn = db_config()
     df = pd.read_sql(query, conn)
     conn.close()
     return df

elif page == "Visualizations":
        st.title("Data Visualizations")
        queries = {
            "Peak Ordering Times": "SELECT HOUR(order_date) AS order_hour, COUNT(*) AS order_count FROM orders GROUP BY order_hour ORDER BY order_count DESC;",
            "Orders with Delivery Delays": "SELECT order_id, TIMESTAMPDIFF(MINUTE, order_date, delivery_time) AS delay_minutes FROM orders WHERE TIMESTAMPDIFF(MINUTE, order_date, delivery_time) > 30;",
            "Top Customers by Order Frequency": "SELECT c.name AS customer_name, COUNT(o.order_id) AS total_orders FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.name ORDER BY total_orders DESC LIMIT 10;"
        }
        
        selected_query = st.sidebar.selectbox("Select Visualization Query", list(queries.keys()))

        if st.button("Generate Chart"):
            conn = db_config()
            df = pd.read_sql(queries[selected_query], conn)
            conn.close()


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

            elif selected_query == "Preferred Cuisines":
                fig = px.pie(df, names="preferred_cuisine", values="cuisine_count", 
                title="Preferred Cuisines Among Customers", hole=0.4)
                st.plotly_chart(fig)

            elif selected_query == "Most Popular Restaurants by Order Frequency":
                fig = px.bar(df, x="restaurant_name", y="order_frequency", 
                title="Most Popular Restaurants", color="order_frequency", 
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
