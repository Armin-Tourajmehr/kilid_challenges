import mysql.connector

# Database configuration
DB_HOST = 'localhost'
DB_USER = '****'
DB_PASS = '****'
DB_NAME = 'bayut_db'

def analyze_listings():
    try:
        # Establish the connection
        print("Connecting to the database...")
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        print("Database connection successful.")

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Query: Count of listings for each region
        print("Executing query: Count of listings for each region...")
        cursor.execute("""
            SELECT region, COUNT(*) AS listing_count
            FROM properties
            GROUP BY region;
        """)
        listings_by_region = cursor.fetchall()

        if listings_by_region:
            print("\nCount of listings for each region:")
            for row in listings_by_region:
                print(f"Region: {row[0]}, Count: {row[1]}")
        else:
            print("\nNo listings found in the database.")

        # Query: Count of TruCheck listings for each region
        print("\nExecuting query: Count of TruCheck listings for each region...")
        cursor.execute("""
            SELECT region, COUNT(*) AS total_count,
                   SUM(CASE WHEN trucheck = 1 THEN 1 ELSE 0 END) AS trucheck_true,
                   SUM(CASE WHEN trucheck = 0 THEN 1 ELSE 0 END) AS trucheck_false
            FROM properties
            GROUP BY region;
        """)
        trucheck_by_region = cursor.fetchall()

        if trucheck_by_region:
            print("\nCount of TruCheck listings for each region:")
            for row in trucheck_by_region:
                print(f"Region: {row[0]}, Total: {row[1]}, TruCheck True: {row[2]}, TruCheck False: {row[3]}")
        else:
            print("\nNo TruCheck data found in the database.")

    except mysql.connector.Error as e:
        # Catch MySQL-specific errors
        print(f"MySQL error: {e}")
    except Exception as e:
        # Catch general errors
        print(f"Error: {e}")
    finally:
        # Ensure resources are closed properly
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    analyze_listings()
