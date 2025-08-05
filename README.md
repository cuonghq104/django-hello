# Django REST Framework E-Commerce API

A robust e-commerce API built with Django REST Framework featuring product management, order processing, user authentication, and advanced filtering capabilities.

## 🚀 Features

- **Product Management**: CRUD operations for products with categories
- **Order Processing**: Complete order lifecycle with status tracking
- **User Authentication**: Secure user management with permissions
- **Advanced Filtering**: Django-filter integration for complex queries
- **Admin Interface**: Customizable Django admin with table views
- **API Documentation**: Auto-generated API documentation
- **Performance Monitoring**: Silk profiler integration

## 📋 Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-hello-django
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv-drf
   source venv-drf/bin/activate  # On Windows: venv-drf\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 🏗️ Project Structure

```
python-hello-django/
├── api/                    # Main API application
│   ├── models.py          # Database models
│   ├── views.py           # API views and endpoints
│   ├── serializers.py     # Data serialization
│   ├── admin.py          # Django admin configuration
│   ├── filters.py        # Custom filters
│   └── urls.py           # API URL patterns
├── drf_course/           # Django project settings
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## 📚 API Endpoints

### Products

| Method | Endpoint | Description | Permissions |
|--------|----------|-------------|-------------|
| GET | `/products/` | List all products | Public |
| POST | `/products/` | Create new product | Admin only |
| GET | `/products/<id>/` | Get product details | Public |
| PUT | `/products/<id>/` | Update product | Admin only |
| DELETE | `/products/<id>/` | Delete product | Admin only |
| GET | `/products/info` | Product statistics | Public |

### Categories

| Method | Endpoint | Description | Permissions |
|--------|----------|-------------|-------------|
| GET | `/categories/` | List all categories | Authenticated |
| POST | `/categories/` | Create new category | Admin only |
| GET | `/categories/<id>/` | Get category details | Authenticated |
| PUT | `/categories/<id>/` | Update category | Admin only |
| DELETE | `/categories/<id>/` | Delete category | Admin only |

### Products by Category

| Method | Endpoint | Description | Permissions |
|--------|----------|-------------|-------------|
| GET | `/categories/<id>/products` | Get products by category | Authenticated |

### Orders

| Method | Endpoint | Description | Permissions |
|--------|----------|-------------|-------------|
| GET | `/orders/` | List all orders | Admin only |
| GET | `/user-orders/` | List user's orders | Authenticated |

## 🔍 Filtering & Search

### Product Filtering
- **By name**: `GET /products/?name=coffee`
- **By category**: `GET /products/?category=1`
- **Combined filters**: `GET /products/?name=laptop&category=2`

### Products by Category with Filtering
- **Filtered by name**: `GET /categories/1/products/?name=coffee`

## 🔐 Authentication & Permissions

### Permission Levels
- **Public**: No authentication required
- **Authenticated**: User must be logged in
- **Admin**: User must have admin privileges

### Authentication Methods
- Session authentication (default)
- Token authentication (configurable)

## 🗄️ Database Models

### Product
- `name`: Product name
- `description`: Product description
- `price`: Product price (Decimal)
- `stock`: Available stock quantity
- `image`: Product image (optional)
- `category`: Foreign key to ProductCategory

### ProductCategory
- `name`: Category name
- `description`: Category description

### Order
- `order_id`: Unique UUID identifier
- `user`: Foreign key to User
- `created_at`: Order creation timestamp
- `status`: Order status (Pending/Confirmed/Cancelled)
- `products`: Many-to-many relationship with Product

### OrderItem
- `order`: Foreign key to Order
- `product`: Foreign key to Product
- `quantity`: Item quantity

## 🎛️ Admin Interface

### ProductAdmin Features
- **Table Display**: ID, Name, Price, Category, Stock, In Stock status
- **Filtering**: By category and stock
- **Search**: By name and description
- **Pagination**: 20 items per page

### ProductCategoryAdmin Features
- **Table Display**: ID, Name, Description
- **Search**: By name and description
- **Pagination**: 20 items per page

## 🛠️ Development

### Running Tests
```bash
python manage.py test
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Populate database with sample data
python manage.py populate_db
```

### Performance Monitoring
The project includes Silk profiler for performance monitoring:
- Access at `/silk/` when DEBUG=True
- Monitor database queries and performance

## 📦 Dependencies

### Core Dependencies
- **Django**: 5.1.1 - Web framework
- **Django REST Framework**: 3.15.2 - API framework
- **Pillow**: 10.4.0 - Image processing
- **django-extensions**: 3.2.3 - Development utilities

### Development Dependencies
- **Silk**: Performance profiling
- **drf-spectacular**: API documentation
- **django-filters**: Advanced filtering

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS`
3. Use environment variables for `SECRET_KEY`
4. Set up proper database (PostgreSQL recommended)
5. Configure static files
6. Set up HTTPS
7. Configure logging

### Environment Variables
```bash
export SECRET_KEY='your-secret-key'
export DEBUG=False
export ALLOWED_HOSTS='your-domain.com'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the Django REST Framework documentation
- Review the API documentation at `/api/schema/`

---

**Built with ❤️ using Django REST Framework** 