# Pricing Calculator Platform - Architecture Overview

## System Architecture

The Pricing Calculator Platform is built using a modern, scalable architecture with the following key components:

### Backend Stack
- **Web Framework**: Flask (Python 3.11)
- **Database**: SQLite (can be configured for PostgreSQL)
- **Authentication**: JWT-based token system
- **API Style**: RESTful

## Component Diagram
```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Client App    │────▶│   REST API       │────▶│    Database     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  Price Engine    │
                        └──────────────────┘
```

## Core Components

### 1. Authentication System
- Company registration and login
- JWT token generation and validation
- Role-based access control
- Secure password hashing (PBKDF2-SHA256)

### 2. Pricing Tool Management
- Tool creation and versioning
- Draft/Live state management
- Component configuration
- Section organization

### 3. Price Engine
- Supports multiple pricing models:
  - Fixed pricing
  - Tiered pricing
  - Quantity-based pricing
  - Feature-based pricing
- Real-time calculation
- Currency handling

## Data Models

### Company
```
Company
├── id: Integer (PK)
├── name: String
├── email: String (Unique)
└── password_hash: String
```

### Tool
```
Tool
├── id: Integer (PK)
├── company_id: Integer (FK)
├── name: String
├── version: String
├── status: Enum(draft, live)
├── created_at: DateTime
└── updated_at: DateTime
```

### Section
```
Section
├── id: Integer (PK)
├── tool_id: Integer (FK)
├── name: String
└── order: Integer
```

### Component
```
Component
├── id: Integer (PK)
├── section_id: Integer (FK)
├── type: String
├── variant: String
└── pricing: JSON
```

## Security Measures

1. **Authentication**
   - JWT-based token system
   - Token expiration and refresh
   - Secure password storage

2. **Data Isolation**
   - Company-specific data separation
   - Tool version control
   - Access control checks

3. **Input Validation**
   - Request payload validation
   - Email format verification
   - Pricing rule validation

## API Flow

1. **Company Registration**
   ```
   Client → Register → Validate → Create Company → Return Token
   ```

2. **Tool Creation**
   ```
   Client → Authenticate → Create Tool → Configure Components → Save
   ```

3. **Price Calculation**
   ```
   Client → Submit Components → Calculate Price → Return Total
   ```

## Scalability Considerations

1. **Database**
   - Supports migration to PostgreSQL
   - Indexed queries for performance
   - Efficient JSON storage for pricing rules

2. **API**
   - Stateless design
   - Cacheable responses
   - Pagination for large datasets

3. **Computation**
   - Asynchronous price calculations
   - Bulk operation support
   - Rate limiting implementation