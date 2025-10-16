# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Flask web application demonstrating modern web development techniques including form handling, file uploads, database operations, AJAX interactions, and user session management. The project serves as both a learning resource and a solid foundation for building production web applications.

## Development Commands

### Setup and Installation
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask flask-sqlalchemy flask-wtf wtforms email_validator werkzeug

# For development, the above packages are sufficient
# The project currently doesn't have a requirements.txt file
```

### Running the Application
```bash
# Navigate to project directory and run with virtual environment
cd my_website
source venv/bin/activate
python app.py

# The application runs on:
# Local: http://127.0.0.1:9250
# Network: http://0.0.0.0:9250 (allows remote access)
```

### Database Operations
```bash
# Initialize database (automatically done on first run)
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized')
"
```

### Testing
```bash
# Test basic functionality
curl http://127.0.0.1:9250/
curl -X POST http://127.0.0.1:9250/ajax/say-hello \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "lastname": "User"}'
```

## Architecture and Code Structure

### Core Application Structure
- **`app.py`**: Main Flask application with all routes, database models, and core logic
- **`forms.py`**: Flask-WTF form definitions for contact form handling
- **`templates/`**: Jinja2 templates with inheritance structure
- **`static/css/`**: Custom CSS styling
- **`uploads/`**: File upload storage directory
- **`messages.db`**: SQLite database file (auto-generated)

### Database Architecture
The application uses SQLAlchemy ORM with a single `Contact` model:
```python
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
```

### Template Architecture
- **`base.html`**: Master template with navigation and flash message system
- **Child templates**: Extend base.html for specific pages
- **Flash messages**: Implemented with categories (success, error, info)
- **Template inheritance**: Consistent layout across all pages

### Route Structure
The application implements a comprehensive set of routes:

**Public Routes:**
- `/` - Home page with session-based content
- `/about` - About page
- `/contact` - Contact form (GET/POST)
- `/messages` - Message list display
- `/upload` - File upload functionality
- `/ajax-demo` - AJAX demonstration page
- `/login` - User login (GET/POST)
- `/logout` - User logout

**AJAX Endpoints:**
- `/ajax/say-hello` - POST endpoint for AJAX hello functionality
- `/ajax/say-goodbye` - POST endpoint for AJAX goodbye functionality

### Key Technical Features

#### Form Handling
- Flask-WTF integration with CSRF protection
- Custom validation with WTForms validators
- Server-side validation with user-friendly error messages
- Form data persistence on validation failures

#### Session Management
- Flask sessions for user authentication state
- Multi-role system (admin, guest, logged-out)
- Session-based content personalization

#### File Upload System
- Secure file upload with filename sanitization
- File type validation (whitelist approach)
- Configurable upload directory
- Error handling for invalid uploads

#### Database Operations
- SQLAlchemy ORM integration
- Automatic table creation on startup
- CRUD operations with proper error handling
- Timestamp management for record creation

#### AJAX Implementation
- Modern fetch API usage
- JSON request/response handling
- Dynamic DOM manipulation without page refresh
- Real-time status updates and user feedback

### Security Implementation
- CSRF protection on all forms
- File upload validation with secure_filename
- Session-based authentication
- Input validation and sanitization
- SQL injection protection via ORM

### Development Notes

#### Virtual Environment
The project uses Python virtual environment (`venv/`) for dependency isolation. Always activate before running the application.

#### Database Configuration
- Uses SQLite for simplicity and portability
- Database file: `messages.db` in project root
- Automatic table creation on application startup
- Configurable via SQLAlchemy settings

#### Port Configuration
- Default port: 9250
- Host configuration: `0.0.0.0` for network access
- Debug mode enabled for development

#### File Structure Best Practices
- Separation of concerns (forms, routes, templates)
- Consistent naming conventions
- Modular template design with inheritance
- Static asset organization

### Common Development Patterns

#### Adding New Routes
1. Define route function in `app.py`
2. Create corresponding template in `templates/`
3. Add navigation link in `base.html`
4. Implement form handling if needed

#### Database Model Extensions
1. Define new model class in `app.py`
2. Run database initialization
3. Update forms and templates accordingly
4. Implement CRUD operations as needed

#### AJAX Endpoints
1. Create POST route in `app.py`
2. Return JSON responses using `jsonify()`
3. Implement JavaScript client-side logic
4. Add error handling and user feedback

This project provides a solid foundation for Flask development with modern best practices and comprehensive feature coverage.