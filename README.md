# Pricing Calculator Platform

A flexible pricing calculator platform that allows companies to create and manage custom pricing tools.

## Features

- Company registration and authentication
- Custom pricing tool creation and management
- Tool versioning with draft/live states
- Price calculation based on components

## Setup

### Prerequisites

- Python 3.11
- pip (Python package manager)

### Installation

1. Clone the repository

2. Create and activate virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate   # On Unix/macOS
   # or
   .\venv\Scripts\activate    # On Windows
   pip install -r requirements.txt
   ```
3. Set environment variables (optional):
   ```bash
   export SECRET_KEY="your-secret-key"
   export JWT_SECRET_KEY="your-jwt-secret"
   export DATABASE_URL="your-database-url"  # Defaults to SQLite
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## API Documentation

### Authentication

#### Register Company

```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Company",
    "email": "company@gmail.com",
    "password": "secure_password"
  }'
```

Success Response (201 Created):
```json
{
  "message": "Company registered successfully",
  "company_id": 1
}
```

#### Login

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "company@gmail.com",
    "password": "secure_password"
  }'
```

Success Response (200 OK):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "company_id": 1
}
```

#### Delete Company

```bash
curl -X DELETE http://localhost:5000/company \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Success Response (200 OK):
```json
{
  "message": "Company deleted successfully"
}
```

### Tools Management

#### Create Tool

```bash
curl -X POST http://localhost:5000/tools \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Custom Price Calculator",
    "version": "1.0"
  }'
```

Success Response (201 Created):
```json
{
  "tool_id": 1,
  "name": "Custom Price Calculator",
  "version": "1.0",
  "status": "draft",
  "created_at": "2024-01-20T10:30:00Z"
}
```


#### List Tools

```bash
curl -X GET http://localhost:5000/tools \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Success Response (200 OK):
```json
{
  "tools": [
    {
      "tool_id": 1,
      "name": "Custom Price Calculator",
      "version": "1.0",
      "status": "draft",
      "created_at": "2024-01-20T10:30:00Z",
      "updated_at": "2024-01-20T10:30:00Z"
    }
  ],
  "total_count": 1,
  "page": 1,
  "per_page": 10
}
```

#### Update Tool

```bash
curl -X PUT http://localhost:5000/tools/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Calculator",
    "version": "1.1",
    "status": "live"
  }'
```

Success Response (200 OK):
```json
{
  "tool_id": 1,
  "name": "Updated Calculator",
  "version": "1.1",
  "status": "live",
  "updated_at": "2024-01-20T11:15:00Z"
}
```



#### Delete Tool

```bash
curl -X DELETE http://localhost:5000/tools/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Success Response (200 OK):
```json
{
  "message": "Tool deleted successfully"
}
```

### Component Management

Components support multiple pricing structures:

#### 1. Fixed Price Component
```bash
curl -X POST http://localhost:5000/sections/1/components \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "subscription",
    "variant": "basic",
    "pricing": {
        "type": "fixed",
        "amount": 29.99,
        "currency": "USD"
    }
  }'
```

#### 2. Tiered Price Component
```bash
curl -X POST http://localhost:5000/sections/1/components \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "usage",
    "variant": "api_calls",
    "pricing": {
        "type": "tiered",
        "tiers": [
            {"up_to": 1000, "price": 49.99},
            {"up_to": 5000, "price": 199.99},
            {"up_to": 10000, "price": 399.99}
        ]
    }
  }'
```

#### 3. Quantity-Based Component
```bash
curl -X POST http://localhost:5000/sections/1/components \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "license",
    "variant": "user_seats",
    "pricing": {
        "type": "quantity",
        "unit_price": 10.00,
        "currency": "USD",
        "minimum": 5,
        "maximum": 100
    }
  }'
```

#### 4. Feature-Based Component
```bash
curl -X POST http://localhost:5000/sections/1/components \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "feature_pack",
    "variant": "premium",
    "pricing": {
        "type": "feature",
        "base_price": 99.99,
        "features": [
            {"name": "advanced_analytics", "price": 49.99},
            {"name": "custom_reports", "price": 29.99},
            {"name": "api_access", "price": 79.99}
        ]
    }
  }'
```

Success Response (201 Created):
```json
{
  "component_id": 1,
  "type": "feature_pack",
  "variant": "premium",
  "pricing": {
    "type": "feature",
    "base_price": 99.99,
    "features": [
      {"name": "advanced_analytics", "price": 49.99},
      {"name": "custom_reports", "price": 29.99},
      {"name": "api_access", "price": 79.99}
    ]
  }
}
```

#### List Components

```bash
curl -X GET http://localhost:5000/tools/1/components \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Success Response (200 OK):
```json
{
  "components": [
    {
      "component_id": 1,
      "type": "subscription",
      "variant": "monthly",
      "cost": 29.99,
      "description": "Basic Monthly Subscription",
      "created_at": "2024-01-20T10:30:00Z"
    }
  ],
  "total_count": 1,
  "page": 1,
  "per_page": 10
}
```

#### Update Component

```bash
curl -X PUT http://localhost:5000/tools/1/components/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "subscription",
    "variant": "annual",
    "cost": 299.99,
    "description": "Annual Subscription"
  }'
```

Success Response (200 OK):
```json
{
  "component_id": 1,
  "type": "subscription",
  "variant": "annual",
  "cost": 299.99,
  "description": "Annual Subscription",
  "updated_at": "2024-01-20T11:15:00Z"
}
```

#### Delete Component

```bash
curl -X DELETE http://localhost:5000/tools/1/components/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Success Response (200 OK):
```json
{
  "message": "Component deleted successfully"
}
```

### Price Calculation

#### Calculate Total Cost

```bash
curl -X POST http://localhost:5000/tools/1/calculate \
  -H "Content-Type: application/json" \
ate  -d '{
    "components": [
      {
        "id": 1,
        "quantity": 1
      },
      {
        "id": 2,
        "quantity": 5000
      },
      {
        "id": 3,
        "quantity": 10,
        "features": ["advanced_analytics", "api_access"]
      }
    ]
  }'
```

Success Response (200 OK):
```json
{
  "total_cost": 429.97,
  "currency": "USD",
  "components": [
    {
      "id": 1,
      "type": "subscription",
      "variant": "basic",
      "cost": 29.99,
      "pricing": {
        "type": "fixed",
        "amount": 29.99,
        "currency": "USD"
      }
    },
    {
      "id": 2,
      "type": "usage",
      "variant": "api_calls",
      "cost": 199.99,
      "pricing": {
        "type": "tiered",
        "tiers": [
          {"up_to": 1000, "price": 49.99},
          {"up_to": 5000, "price": 199.99},
          {"up_to": 10000, "price": 399.99}
        ]
      }
    },
    {
      "id": 3,
      "type": "feature_pack",
      "variant": "premium",
      "cost": 199.99,
      "pricing": {
        "type": "feature",
        "base_price": 99.99,
        "features": [
          {"name": "advanced_analytics", "price": 49.99},
          {"name": "api_access", "price": 79.99}
        ]
      }
    }
  ]
}
```


## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found

Error Response Format:
```json
{
  "error": "Error message description"
}
```

### Email Validation

The API enforces strict email validation rules:

- Only valid email domains are accepted (e.g., gmail.com, outlook.com, yahoo.com)

Example of valid emails:
- user@gmail.com
- contact@outlook.com
- support@yahoo.com

Example of invalid emails:
- user@company.com
- contact@invalid.domain
- invalid.email@nonexistent.com

## Security

- JWT-based authentication
- Password hashing using PBKDF2-SHA256
- Email validation
- Company-specific data isolation

## Postman Integration

### Environment Setup

Import the following environment configuration into Postman:

```json
{
  "name": "Pricing Calculator",
  "values": [
    {
      "key": "base_url",
      "value": "http://localhost:5001",
      "type": "default",
      "enabled": true
    },
    {
      "key": "company_name",
      "value": "My Company",
      "type": "default",
      "enabled": true
    },
    {
      "key": "email",
      "value": "mycompany@gmail.com",
      "type": "default",
      "enabled": true
    },
    {
      "key": "password",
      "value": "secure_password",
      "type": "secret",
      "enabled": true
    },
    {
      "key": "access_token",
      "value": "",
      "type": "secret",
      "enabled": true
    },
    {
      "key": "company_id",
      "value": "",
      "type": "default",
      "enabled": true
    },
    {
      "key": "tool_id",
      "value": "",
      "type": "default",
      "enabled": true
    },
    {
      "key": "section_id",
      "value": "",
      "type": "default",
      "enabled": true
    },
    {
      "key": "fixed_component_id",
      "value": "",
      "type": "default",
      "enabled": true
    },
    {
      "key": "tiered_component_id",
      "value": "",
      "type": "default",
      "enabled": true
    },
    {
      "key": "quantity_component_id",
      "value": "",
      "type": "default",
      "enabled": true
    },
    {
      "key": "feature_component_id",
      "value": "",
      "type": "default",
      "enabled": true
    }
  ]
}
```

### Collection

Import the following Postman collection to test the API endpoints:

```json
{
  "info": {
    "name": "Pricing Calculator API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Tools",
      "item": [
        {
          "name": "Create Tool",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n    \"name\": \"Enterprise Calculator\",\n    \"version\": \"1.0\"\n}"
            },
            "url": "{{base_url}}/tools"
          }
        }
      ]
    },
    {
      "name": "Sections",
      "item": [
        {
          "name": "Create Section",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n    \"name\": \"Core Services\"\n}"
            },
            "url": "{{base_url}}/tools/1/sections"
          }
        }
      ]
    },
    {
      "name": "Components",
      "item": [
        {
          "name": "Add Fixed Price Component",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n    \"type\": \"subscription\",\n    \"variant\": \"basic\",\n    \"pricing\": {\n        \"type\": \"fixed\",\n        \"amount\": 29.99,\n        \"currency\": \"USD\",\n        \"billing_cycle\": \"monthly\"\n    }\n}"
            },
            "url": "{{base_url}}/sections/1/components"
          }
        },
        {
          "name": "Add Tiered Component",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n    \"type\": \"storage\",\n    \"variant\": \"cloud\",\n    \"pricing\": {\n        \"type\": \"tiered\",\n        \"currency\": \"USD\",\n        \"tiers\": [\n            {\"up_to\": 10, \"price\": 5.00},\n            {\"up_to\": 50, \"price\": 20.00},\n            {\"up_to\": 100, \"price\": 35.00}\n        ]\n    }\n}"
            },
            "url": "{{base_url}}/sections/1/components"
          }
        }
      ]
    },
    {
      "name": "Calculate",
      "item": [
        {
          "name": "Calculate Price",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n    \"components\": [\n        {\"id\": 1, \"quantity\": 1},\n        {\"id\": 2, \"quantity\": 25},\n        {\"id\": 3, \"features\": [\"API Access\", \"Advanced Analytics\"]}\n    ]\n}"
            },
            "url": "{{base_url}}/tools/1/calculate"
          }
        }
      ]
    }
  ]
}
```

### Usage Instructions

1. Import both the environment and collection files into Postman
2. Select the "Pricing Calculator" environment
3. Execute the requests in the following order:
   - Register a company (Authentication > Register Company)
   - Login to get the access token (Authentication > Login)
   - Create a tool (Tools > Create Tool)
   - Create sections and components as needed
   - Test the price calculation endpoint