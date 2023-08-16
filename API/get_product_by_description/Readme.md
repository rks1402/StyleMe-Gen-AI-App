Sure, here's the modern documentation for the given API code:

# Product Search API Documentation

The Product Search API allows you to search for products based on their descriptions. This API is built using Flask and Google Cloud Datastore. It takes a search query as input and returns a list of products that match the query.

## Base URL

```
https://get-product-by-description-hmvyexj3oa-el.a.run.app
```

## Endpoints

### Get Products by Description

Returns a list of products that match the provided description query.

**Endpoint:** `/get_product_by_description`

**HTTP Method:** GET

**Parameters:**

- `query` (string, required): The description query to search for products.

**Example Request:**

```http
GET /get_product_by_description?query=high%20quality%20shoes
```

**Example Response:**

```json
[
    {
        "product_id": 1,
        "product_name": "High-Quality Running Shoes",
        "description": "These shoes provide excellent comfort and support for runners.",
        "price": 99.99
    },
    {
        "product_id": 2,
        "product_name": "Premium Leather Shoes",
        "description": "Handcrafted leather shoes for a classy look.",
        "price": 149.99
    }
]
```

**Response Codes:**

- 200 OK: Products found and returned successfully.
- 400 Bad Request: Search query parameter not provided.
- 404 Not Found: No matching products found for the given query.
- 500 Internal Server Error: An error occurred while processing the request.

## Error Responses

In case of errors, the API returns JSON responses with an `error` field describing the issue.

**Example Error Response:**

```json
{
    "error": "Search query not provided."
}
```

## Running the API

To run the API, execute the following command in the terminal:

```bash
python your_app_file.py
```

Replace `your_app_file.py` with the name of the file containing the provided API code.

## Notes

- The API splits both the search query and the stored descriptions into words for a partial match.
- The Google Cloud Datastore is used to store product information.
- It's recommended to use appropriate authentication and authorization mechanisms when deploying this API in production.
