# Iron Sight Armory

## Overview

Iron Sight Armory is a tactical optics e-commerce web application built with Flask. The system provides a product catalog for tactical equipment including red dot sights, scopes, iron sights, and mounts. It features order management capabilities with real-time tracking and status updates. The application is designed for tactical equipment retailers and enthusiasts looking for a streamlined ordering and inventory management system.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Flask for server-side rendering
- **Styling**: Custom CSS with responsive design principles
- **User Interface**: Clean, professional design with tactical/military aesthetic
- **JavaScript Integration**: Client-side product filtering and dynamic form updates

### Backend Architecture
- **Framework**: Flask (Python) with minimal dependencies for lightweight deployment
- **Data Storage**: In-memory storage using Python lists and dictionaries for rapid prototyping
- **Session Management**: Flask's built-in session handling with secret key encryption
- **Request Handling**: RESTful route structure for order management and product display

### Data Models
- **Product Catalog**: Hierarchical structure with categories (red_dot_sights, scopes, iron_sights, mounts)
- **Order Management**: Simple order tracking with status workflow (pending, confirmed, shipped)
- **Customer Data**: Basic customer information capture for order processing

### Application Structure
- **Static Assets**: CSS stylesheets served from static directory
- **Templates**: HTML templates with Jinja2 for dynamic content rendering
- **Route Organization**: Separation of concerns between product display and order management

## External Dependencies

### Core Dependencies
- **Flask 2.3.3**: Web framework for Python applications
- **Jinja2**: Template engine (included with Flask)
- **Werkzeug**: WSGI toolkit (included with Flask)

### Future Considerations
- **Database Integration**: Current in-memory storage should be replaced with persistent database (PostgreSQL recommended)
- **Payment Processing**: Integration with payment gateways for transaction handling
- **Authentication System**: User accounts and role-based access control
- **Inventory Management**: Real-time stock tracking and automated reordering
- **Shipping Integration**: API connections with shipping providers for logistics

### Development Dependencies
- **Python 3.x**: Runtime environment
- **pip**: Package management for Python dependencies

Note: The application currently uses in-memory storage which is suitable for development and testing but will require database integration for production deployment.