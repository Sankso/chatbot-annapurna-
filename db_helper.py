import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='pandeyji_eatery',
            user='root',
            password='Sa@261104'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

global cnx
# Establish a database connection
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sa@261104",
    database="pandeyji_eatery"
)

def get_total_order_price(order_id):
    cursor = cnx.cursor()

    #Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    #fetching the result
    result = cursor.fetchone()[0]

    #closing the cursor
    cursor.close()
    return result

def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        #calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        #Committing the changes
        cnx.commit()

        #closing the cursor
        cursor.close()

        print("Order item inserted successfully!")
        return 1
    
    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        #rollback changes if necessary
        cnx.rollback()
        return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        #rollback changes if necessary
        cnx.rollback()
        return -1

def get_next_order_id():
    cursor = cnx.cursor()

    #executing the SQL query to get the next available order-id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    #fetching the result
    result = cursor.fetchone()[0]

    #closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1  # if no orders exist, start from order_id 1
    else:
        return result + 1  # increment the max order_id by 1

def get_order_status(order_id: int):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()

    # Closing the cursor
    cursor.close()

    # Returning the order status
    if result:
        return result[0]
    else:
        return None

def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    #inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    #committing the changes
    cnx.commit()

    #Closing the cursor
    cursor.close()

# Optional: Close the connection when done
def close_connection():
    cnx.close()
def main():
    connection = create_connection()
    if connection:
        try:
            # Create a cursor and execute a test query
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")  # Query to fetch the current database
            current_database = cursor.fetchone()
            print(f"Connected to the database: {current_database[0]}")

            # Close the cursor and connection
            cursor.close()
        except Error as e:
            print(f"Error while fetching data: {e}")
        finally:
            if connection.is_connected():
                connection.close()
                print("Database connection closed.")



def fetch_order_by_id(connection, order_id):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT food_item, quantity FROM orders WHERE order_id = {order_id}")
        order_details = cursor.fetchall()

        if not order_details:
            return None

        food_dict = {item['food_item']: item['quantity'] for item in order_details}
        return ", ".join([f"{value} {key}" for key, value in food_dict.items()])
    except Error as e:
        print(f"Error fetching order details: {e}")
        return None

def calculate_total_bill(connection, order_id):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT SUM(price * quantity) as total_bill FROM orders WHERE order_id = {order_id}")
        total_bill = cursor.fetchone()[0]
        return total_bill
    except Error as e:
        print(f"Error calculating total bill: {e}")
        return None


if __name__ == "__main__":
    main()