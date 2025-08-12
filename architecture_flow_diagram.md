# Django REST Framework Architecture Flow Diagram

## System Architecture Overview

```mermaid
graph TB
    %% Client Layer
    subgraph "Client Layer"
        A[Web Browser]
        B[Mobile App]
        C[API Consumer]
    end

    %% Load Balancer/Proxy Layer
    subgraph "Network Layer"
        D[Load Balancer/Proxy]
    end

    %% Django REST Framework Layer
    subgraph "Django REST Framework"
        E[URL Router]
        F[Middleware Stack]
        G[Authentication]
        H[Permissions]
        I[Views]
        J[Serializers]
        K[Filters]
    end

    %% Business Logic Layer
    subgraph "Business Logic"
        L[Services]
        M[Models]
        N[Background Tasks]
    end

    %% Data Layer
    subgraph "Data Layer"
        O[(SQLite Database)]
        P[Redis Cache]
    end

    %% Redis Usage Details
    subgraph "Redis Operations"
        Q[Cache Page Results]
        R[Session Storage]
        S[Rate Limiting]
        T[Query Results Cache]
    end

    %% Flow Connections
    A --> D
    B --> D
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    I --> K
    J --> L
    L --> M
    M --> O
    M --> P
    
    %% Redis specific flows
    P --> Q
    P --> R
    P --> S
    P --> T
    
    %% Cache flows
    I -.->|"cache_page decorator"| Q
    Q -.->|"15 min cache"| P
    P -.->|"Return cached data"| I
    
    %% Database flows
    M -->|"ORM Queries"| O
    O -->|"Query Results"| M
    
    %% Styling
    classDef clientLayer fill:#e1f5fe
    classDef drfLayer fill:#f3e5f5
    classDef businessLayer fill:#e8f5e8
    classDef dataLayer fill:#fff3e0
    classDef redisLayer fill:#ffebee
    
    class A,B,C clientLayer
    class E,F,G,H,I,J,K drfLayer
    class L,M,N businessLayer
    class O dataLayer
    class P,Q,R,S,T redisLayer
```

## Detailed Request Flow

```mermaid
sequenceDiagram
    participant Client as Client
    participant Router as URL Router
    participant Middleware as Middleware Stack
    participant Auth as Authentication
    participant Perms as Permissions
    participant View as View
    participant Serializer as Serializer
    participant Cache as Redis Cache
    participant DB as SQLite DB
    participant Model as Model

    Client->>Router: HTTP Request
    Router->>Middleware: Route to View
    
    Note over Middleware: Security, Sessions, CSRF
    
    Middleware->>Auth: Check Authentication
    Auth->>Perms: Verify Permissions
    
    alt Cache Hit
        Perms->>View: Request
        View->>Cache: Check Cache
        Cache-->>View: Return Cached Data
        View-->>Client: JSON Response
    else Cache Miss
        Perms->>View: Request
        View->>Serializer: Validate/Transform
        Serializer->>Model: Query Data
        Model->>DB: SQL Query
        DB-->>Model: Query Results
        Model-->>Serializer: Model Instances
        Serializer-->>View: Serialized Data
        View->>Cache: Store in Cache
        View-->>Client: JSON Response
    end
```

## API Endpoints Flow

```mermaid
graph LR
    subgraph "API Endpoints"
        A1[GET /products/]
        A2[POST /products/]
        A3[GET /products/<id>]
        A4[PUT /products/<id>]
        A5[DELETE /products/<id>]
        
        B1[GET /categories/]
        B2[POST /categories/]
        B3[GET /categories/<id>]
        B4[PUT /categories/<id>]
        B5[DELETE /categories/<id>]
        
        C1[GET /orders/]
        C2[POST /orders/]
        C3[GET /orders/<id>]
        C4[PUT /orders/<id>]
        C5[DELETE /orders/<id>]
        
        D1[GET /users/]
        D2[POST /users/]
        D3[GET /users/<id>]
        D4[PUT /users/<id>]
        D5[DELETE /users/<id>]
    end
    
    subgraph "View Classes"
        V1[ProductListCreateApiView]
        V2[ProductDetailApiView]
        V3[ProductInfoApiView]
        V4[OrderViewSet]
        V5[UserViewSet]
        V6[Category Views]
    end
    
    subgraph "Models"
        M1[Product]
        M2[Order]
        M3[User]
        M4[ProductCategory]
        M5[OrderItem]
    end
    
    A1 --> V1
    A2 --> V1
    A3 --> V2
    A4 --> V2
    A5 --> V2
    
    B1 --> V6
    B2 --> V6
    B3 --> V6
    B4 --> V6
    B5 --> V6
    
    C1 --> V4
    C2 --> V4
    C3 --> V4
    C4 --> V4
    C5 --> V4
    
    D1 --> V5
    D2 --> V5
    D3 --> V5
    D4 --> V5
    D5 --> V5
    
    V1 --> M1
    V2 --> M1
    V3 --> M1
    V4 --> M2
    V5 --> M3
    V6 --> M4
    
    classDef endpoint fill:#e3f2fd
    classDef view fill:#f1f8e9
    classDef model fill:#fff8e1
    
    class A1,A2,A3,A4,A5,B1,B2,B3,B4,B5,C1,C2,C3,C4,C5,D1,D2,D3,D4,D5 endpoint
    class V1,V2,V3,V4,V5,V6 view
    class M1,M2,M3,M4,M5 model
```

## Redis Caching Strategy

```mermaid
graph TD
    subgraph "Redis Cache Configuration"
        R1[Redis Server<br/>127.0.0.1:6379/1]
        R2[django_redis.cache.RedisCache]
        R3[DefaultClient]
    end
    
    subgraph "Caching Patterns"
        C1[Page-level Caching<br/>@cache_page(60*15)]
        C2[Query Result Caching]
        C3[Session Storage]
        C4[Rate Limiting]
    end
    
    subgraph "Cached Endpoints"
        E1[GET /products/<br/>15 min cache]
        E2[Product List Views]
        E3[Category Views]
    end
    
    subgraph "Cache Invalidation"
        I1[Manual Invalidation]
        I2[TTL Expiration]
        I3[Key-based Invalidation]
    end
    
    R1 --> R2
    R2 --> R3
    R3 --> C1
    R3 --> C2
    R3 --> C3
    R3 --> C4
    
    C1 --> E1
    C1 --> E2
    C1 --> E3
    
    C1 --> I1
    C1 --> I2
    C1 --> I3
    
    classDef redis fill:#ffcdd2
    classDef cache fill:#c8e6c9
    classDef endpoint fill:#bbdefb
    classDef invalidation fill:#ffe0b2
    
    class R1,R2,R3 redis
    class C1,C2,C3,C4 cache
    class E1,E2,E3 endpoint
    class I1,I2,I3 invalidation
```

## Authentication & Authorization Flow

```mermaid
graph TB
    subgraph "Authentication Methods"
        A1[JWT Authentication]
        A2[Session Authentication]
    end
    
    subgraph "Permission Classes"
        P1[AllowAny]
        P2[IsAuthenticated]
        P3[IsAdminUser]
    end
    
    subgraph "Protected Endpoints"
        E1[GET /products/ - AllowAny]
        E2[POST /products/ - IsAdminUser]
        E3[GET /orders/ - AllowAny]
        E4[POST /orders/ - IsAuthenticated]
        E5[GET /users/ - AllowAny]
        E6[POST /users/ - AllowAny]
    end
    
    subgraph "User Model"
        U1[Custom User Model]
        U2[api.User]
    end
    
    A1 --> P1
    A1 --> P2
    A1 --> P3
    A2 --> P1
    A2 --> P2
    A2 --> P3
    
    P1 --> E1
    P2 --> E4
    P3 --> E2
    
    U1 --> A1
    U1 --> A2
    
    classDef auth fill:#e1bee7
    classDef permission fill:#c5cae9
    classDef endpoint fill:#dcedc8
    classDef user fill:#ffccbc
    
    class A1,A2 auth
    class P1,P2,P3 permission
    class E1,E2,E3,E4,E5,E6 endpoint
    class U1,U2 user
```

## Database Schema Overview

```mermaid
erDiagram
    User {
        int id PK
        string username
        string email
        string password
        datetime created_at
        datetime updated_at
    }
    
    ProductCategory {
        int id PK
        string name
        string description
        int super_category_id FK
    }
    
    Product {
        int id PK
        string name
        text description
        decimal price
        int stock
        string image
        int category_id FK
    }
    
    Order {
        int id PK
        int user_id FK
        string status
        decimal total_amount
        datetime created_at
        datetime updated_at
    }
    
    OrderItem {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal price
    }
    
    User ||--o{ Order : places
    ProductCategory ||--o{ Product : contains
    Order ||--o{ OrderItem : contains
    Product ||--o{ OrderItem : included_in
```

## Key Features Summary

### Redis Usage
- **Primary Purpose**: Page-level caching for product listings
- **Configuration**: django-redis with Redis server on localhost:6379/1
- **Cache Duration**: 15 minutes for product list views
- **Cache Key**: `product_list` prefix for product endpoints

### Authentication
- **JWT Authentication**: Primary method for API access
- **Session Authentication**: Fallback for web interface
- **Custom User Model**: `api.User` instead of Django's default

### API Structure
- **Products**: CRUD operations with filtering and pagination
- **Categories**: Hierarchical category management
- **Orders**: Order management with user association
- **Users**: User management endpoints

### Performance Optimizations
- **Database**: SQLite for development (configurable for production)
- **Caching**: Redis-based page caching
- **Filtering**: Django-filter integration
- **Pagination**: PageNumberPagination with configurable page sizes
- **Query Optimization**: prefetch_related for related data

### Security Features
- **CSRF Protection**: Enabled for web interface
- **Permission Classes**: Role-based access control
- **Input Validation**: Serializer-based validation
- **SQL Injection Protection**: Django ORM protection 