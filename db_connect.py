# print_schema.py
import mysql.connector
from mysql.connector import Error

def print_full_schema():
    try:
        # --- 1. Connect ---
        conn = mysql.connector.connect(
            host='localhost',
            database='hospital',
            user='root',
            password='',
            port=3306
        )

        if not conn.is_connected():
            print("Failed to connect.")
            return

        cursor = conn.cursor()
        print("Connected to 'hospital' database\n")
        print("="*60)
        print("FULL DATABASE SCHEMA")
        print("="*60)

        # --- 2. Get all tables ---
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        if not tables:
            print("No tables found in 'hospital' database.")
            return

        for (table_name,) in tables:
            print(f"\nTABLE: `{table_name}`")
            print("-" * 50)

            # --- 3. Get full column info ---
            cursor.execute(f"SHOW FULL COLUMNS FROM `{table_name}`")
            columns = cursor.fetchall()

            # Print header
            print(f"{'Column':<20} {'Type':<15} {'Null':<6} {'Key':<6} {'Default':<10} {'Extra'}")
            print("-" * 80)

            for col in columns:
                col_name = col[0]
                col_type = col[1]
                null = col[3]  # 'YES' or 'NO'
                key = col[4]   # PRI, UNI, MUL
                default = col[6] if col[6] is not None else "NULL"
                extra = col[8]

                print(f"{col_name:<20} {col_type:<15} {null:<6} {key:<6} {default:<10} {extra}")

            # --- 4. Show indexes ---
            print(f"\nIndexes for `{table_name}`:")
            cursor.execute(f"SHOW INDEX FROM `{table_name}`")
            indexes = cursor.fetchall()
            if indexes:
                seen = set()
                for idx in indexes:
                    idx_name = idx[2]
                    if idx_name not in seen:
                        seen.add(idx_name)
                        non_unique = "Non-unique" if idx[1] else "Unique"
                        cols = []
                        cursor.execute(f"SHOW INDEX FROM `{table_name}` WHERE Key_name = %s", (idx_name,))
                        for row in cursor.fetchall():
                            cols.append(row[4])
                        print(f"  • {non_unique} Index `{idx_name}` on ({', '.join(cols)})")
            else:
                print("  (No indexes)")

        print("\n" + "="*60)
        print("END OF SCHEMA")
        print("="*60)

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("\nConnection closed.")

# --- Run ---
if __name__ == "__main__":
    print_full_schema()