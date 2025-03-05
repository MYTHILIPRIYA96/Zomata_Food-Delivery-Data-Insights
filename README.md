# Zomata_Food-Delivery-Data-Insights
Analyze food delivery operations to enhance efficiency and  improve customer satisfaction.
# key Features
Synthetic Data Generation:
Faker customer,restaurant,order,delivery and delivery person data
Database Design:
Mysql schema
CURD Operations:
A streamlit app for managing user.
Data Insights:
SQL queries 
Data Insights & Visualization
# install libraries
pip install mysql-connector-python
pip install faker
# Tech Stack
Database:MySQL
Backend:python
Fontend:streamlit(CURD)
Data Generation:Faker(synthetic dataset)
Data Analysis:SQL queries,python
Connect :tidbcloud
# Database Schema
Customers - stores customer details.
Restaurants - contains restaurants data.
Orders - Tracks food order.
Deliveries - stores delivery details.
Delivery person - stores delivery person details.
# Business Use Cases for Zomato Food Delivery Data Analysis
Your SQL queries provide insights that can be directly mapped to critical business use cases. Below is how they align with operational efficiency, customer satisfaction, and business growth.

1. Order Management & Demand Analysis
Use Cases:
Peak Ordering Locations → Identify high-demand areas for better restaurant and delivery allocation.
Peak Ordering Times → Optimize staffing and food preparation for rush hours.
Identify Days with Most Orders → Plan restaurant operations and marketing campaigns around high-order days.
Peak Ordering Times for Each Restaurant → Help restaurants adjust working hours and staffing levels.
Relevant Queries:
Query 1: Peak Ordering Locations
Query 2: Peak Ordering Times
Query 14: Identify Days with Most Orders
Query 16: Peak Ordering Times for Each Restaurant
2. Customer Behavior & Retention
Use Cases:
Top Customers by Order Frequency & Total Order Value → Identify loyal customers and create targeted reward programs.
Most Popular Cuisines Among Customers → Personalize recommendations and marketing campaigns.
Preferred Cuisines by Customers → Optimize restaurant partnerships and menu offerings.
Top 10 High-Value & High-Rated Customers → Identify premium users for exclusive deals and priority support.
Relevant Queries:
Query 5: Top Customers by Order Frequency
Query 6: Top Customers by Total Order Value
Query 8: Preferred Cuisines
Query 18: Most Popular Cuisines Among Customers
Query 19: Top 10 High-Value & High-Rated Customers
3. Delivery Performance & Optimization
Use Cases:
Orders with Delivery Delays → Identify delays and improve logistics efficiency.
Average Delivery Time → Optimize delivery processes to reduce delays.
Deliveries per Delivery Person → Track performance and workload distribution.
Average Delivery Time by Delivery Person → Reward efficient delivery personnel and train underperformers.
Orders with Significant Delivery Delays → Reduce customer complaints by improving delivery speed.
Relevant Queries:
Query 3: Orders with Delivery Delays
Query 7: Average Delivery Time
Query 9: Deliveries per Delivery Person
Query 10: Average Delivery Time by Delivery Person
Query 20: Orders with Significant Delivery Delays
4. Restaurant Performance & Market Strategy
Use Cases:
Most Popular Restaurants by Order Frequency → Rank and highlight top-performing restaurants.
Restaurants with Highest Total Order Value → Identify high-revenue restaurants for premium listings.
Average Order Value by Restaurant → Help restaurants adjust pricing strategies.
Most Popular Cuisines → Recommend trending cuisines to restaurants.
Restaurants with High Cancelled Orders → Identify struggling restaurants and improve service quality.
Relevant Queries:
Query 11: Most Popular Cuisines
Query 12: Most Popular Restaurants by Order Frequency
Query 13: Average Order Value by Restaurant
Query 15: Restaurants with Highest Total Order Value
Query 17: Restaurants with High Cancelled Orders
5. Fraud Detection & Risk Management
Use Cases:
Cancelled Deliveries → Identify patterns of frequent cancellations to detect fraudulent orders.
Orders with Significant Delivery Delays → Investigate excessive delays for potential fraud or inefficiencies.
Restaurants with High Cancelled Orders → Flag restaurants with frequent cancellations for further review.
Relevant Queries:
Query 4: Cancelled Deliveries
Query 17: Restaurants with High Cancelled Orders
Query 20: Orders with Significant Delivery Delays

# Lincence 
MIT
