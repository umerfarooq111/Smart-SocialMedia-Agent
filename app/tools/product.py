from langchain_core.tools import tool
from app.database.connection import get_connection
import json
from decimal import Decimal


def json_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)

    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


@tool
def product_search_tool(query: str) -> str:
    """
    Search product database and return product details.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query_sql = """
    SELECT 
        name,
        price,
        currency,
        stock,
        product_url,
        description
    FROM products
    WHERE name ILIKE %s
    OR product_url ILIKE %s
    OR id::text = %s
    LIMIT 1;
    """

    search_param = f"%{query}%"
    cursor.execute(
        query_sql,
        (search_param, search_param, str(query))
    )

    product = cursor.fetchone()

    cursor.close()
    conn.close()


    if not product:
        return json.dumps({
            "status": "not_found",
            "message": "Product not found"
        })


    result = {

        "status": "success",

        "product": {
            "name": product[0],
            "price": product[1],
            "currency": product[2],
            "stock_quantity": product[3],
            "availability": "In Stock" if (product[3] is not None and product[3] > 0) else "Out of Stock",
            "product_url": product[4],
            "description": product[5]
        }
    }


    return json.dumps(result,default=json_serializer,indent=2)