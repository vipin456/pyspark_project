from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, row_number
from pyspark.sql.window import Window

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Customer Transaction Analysis") \
    .getOrCreate()

# Sample data for Customers
customers_data = [
    (1, "Alice", "New York"),
    (2, "Bob", "San Francisco"),
    (3, "Charlie", "Los Angeles"),
    (4, "David", "Chicago"),
    (5, "Eve", "Boston")
]
customers_columns = ["customer_id", "name", "city"]

# Sample data for Transactions
transactions_data = [
    (101, 1, 150.0, "2023-10-01"),
    (102, 2, 200.0, "2023-10-02"),
    (103, 3, 300.0, "2023-10-03"),
    (104, 1, 500.0, "2023-10-04"),
    (105, 4, 100.0, "2023-10-05"),
    (106, 2, 700.0, "2023-10-06"),
    (107, 5, 250.0, "2023-10-07"),
    (108, 3, 450.0, "2023-10-08"),
    (109, 1, 50.0, "2023-10-09"),
    (110, 4, 800.0, "2023-10-10")
]
transactions_columns = ["transaction_id", "customer_id", "amount", "date"]

# Create DataFrames
customers_df = spark.createDataFrame(customers_data, customers_columns)
transactions_df = spark.createDataFrame(transactions_data, transactions_columns)

# Show the DataFrames
print("Customers DataFrame:")
customers_df.show()

print("Transactions DataFrame:")
transactions_df.show()

# Step 1: Filter transactions above a certain amount (e.g., $200)
filtered_transactions_df = transactions_df.filter(col("amount") > 200)
print("Filtered Transactions (Amount > $200):")
filtered_transactions_df.show()

# Step 2: Join transactions with customer data
joined_df = filtered_transactions_df.join(customers_df, on="customer_id", how="inner")
print("Joined DataFrame (Transactions + Customers):")
joined_df.show()

# Step 3: Calculate total spend per customer
total_spend_df = joined_df.groupBy("customer_id", "name") \
    .agg(sum("amount").alias("total_spend")) \
    .orderBy(col("total_spend").desc())
print("Total Spend per Customer:")
total_spend_df.show()

# Step 4: Rank customers based on their total spend
# Define window specification to partition by customer_id
window_spec = Window.partitionBy("customer_id").orderBy(col("total_spend").desc())
ranked_customers_df = total_spend_df.withColumn("rank", row_number().over(window_spec))
print("Ranked Customers by Total Spend:")
ranked_customers_df.show()

# Step 5: Identify the top 3 customers
top_customers_df = ranked_customers_df.filter(col("rank") <= 3)
print("Top 3 Customers by Total Spend:")
top_customers_df.show()

# Stop the Spark session
# spark.stop()
