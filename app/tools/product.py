from langchain_core.tools import tool
import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="customer-Support-Assistant",
        user="postgres",
        password="0123umer",
        port=5433
    )

@tool
def product_search_tool(query: str) -> str:
    """
    Search product information from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name, price, stock, url
        FROM products
        WHERE name ILIKE %s
        """,
        (f"%{query}%",)
    )

    product = cursor.fetchone()

    cursor.close()
    conn.close()


    if not product:
        return "Product not found."


    return f"""
Product Information:

Name: {product[0]}
Price: {product[1]} PKR
Stock: {product[2]}
URL: {product[3]}
"""