Certainly! Here's the API documentation for the provided Flask application that retrieves records from Google Cloud Datastore based on a specified product ID:

## API Documentation

This API allows you to retrieve a record from the Datastore based on the specified product ID.

### Base URL
```
https://fetch-iqcjxj5v4a-el.a.run.app
```

### Endpoint: /get_record

#### Description
Fetches a single record from the Datastore based on the specified product ID.

#### HTTP Method
GET

#### URL Parameters
- **product_id** (string, required): The product ID to retrieve a record for.

#### Request Example
```
GET http://<your-server-ip>:5000/get_record?product_id=12345
```

#### Response Examples

##### Success (200 OK)
```json
{
    "property1": "value1",
    "property2": "value2",
    ...
}
```

##### Error (400 Bad Request)
```json
{
    "error": "Product ID not provided."
}
```

##### Error (404 Not Found)
```json
{
    "error": "No record found with Product ID: <specified_product_id>"
}
```

##### Error (500 Internal Server Error)
```json
{
    "error": "Error occurred: <error_message>"
}
```

