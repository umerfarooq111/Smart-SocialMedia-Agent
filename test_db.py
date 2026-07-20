from app.tools.product import product_search_tool


result = product_search_tool.invoke({ "query":"iphone 15" })


print(result)