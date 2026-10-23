products = [
    {
        "id": 1,
        "name": "Laptop Pro",
        "price": 75000,
        "stock": 12
    },
    {
        "id": 2,
        "name": "Wireless Headphones",
        "price": 2999,
        "stock": 50
    },
    {
        "id": 3,
        "name": "Mechanical Keyboard",
        "price": 4999,
        "stock": 25
    },
    {
        "id": 4,
        "name": "Smart Watch",
        "price": 5999,
        "stock": 18
    }
]


def search_products(query: str):

    query = query.lower()

    results = []

    for product in products:

        if (
            product["name"].lower() in query
            or any(
                word in product["name"].lower()
                for word in query.split()
            )
        ):
            results.append(product)

    return results


def get_product(product_id: int):

    for product in products:

        if product["id"] == product_id:
            return product

    return None

if __name__ == "__main__":

    print(search_products("What is the price of Laptop Pro?"))

    print(get_product(1))