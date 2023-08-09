## API Documentation

This API provides a way to retrieve records from a Google Cloud Datastore based on the specified gender category.

### Base URL
```
https://gender-iqcjxj5v4a-el.a.run.app
```

### Endpoint:/get_by_gender

#### Description
Fetches records from the Datastore based on the specified gender category.

#### HTTP Method
GET

#### URL Parameters
- **gender** (string, required): The gender category to filter records by.

#### Request Example
```
GET https://gender-iqcjxj5v4a-el.a.run.app/get_by_gender?gender=MEN
```

#### Response Examples

##### Success (200 OK)
```json
[
    {
        "property1": "value1",
        "property2": "value2",
        ...
    },
    {
        "property1": "value3",
        "property2": "value4",
        ...
    }
]
```

##### Error (400 Bad Request)
```json
{
    "error": "gender category not provided."
}
```

##### Error (404 Not Found)
```json
{
    "error": "No record found with Product ID: <specified_gender>"
}
```

##### Error (500 Internal Server Error)
```json
{
    "error": "Error occurred: <error_message>"
}
```

