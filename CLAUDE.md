# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CPA (Certified Public Accountant) learning platform with a cyberpunk-themed glassmorphism design. The application demonstrates modern web development techniques including form handling, file uploads, database operations, AJAX interactions, user session management, and an interactive flashcard learning system. The platform serves as both a learning tool for CPA students and a showcase of advanced Flask development techniques.

## Development Commands

### Setup and Installation
```bash
# Create and activate virtual environment (if not exists)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask flask-sqlalchemy flask-wtf wtforms email_validator werkzeug

# The project uses venv/ for dependency isolation
```

### Running the Application
```bash
# Navigate to project directory and run with virtual environment
cd /path/to/cpa
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

### Template System Architecture
The project uses a dual-template system:

**Cyberpunk Templates (Primary - Current Active):**
- **`templates/home_cyber.html`**: Main landing page with cyberpunk design
- **`templates/login_cyber.html`**: Modern login interface with glassmorphism
- **`templates/contact_cyber.html`**: Professional contact page with FAQ
- **`templates/about_cyber.html`**: Company/product introduction page
- **`templates/cpa_learning.html`**: CPA subject dashboard with progress tracking
- **`templates/flashcards.html`**: Interactive 3D flip card learning system

**Legacy Templates (Secondary - Original Tutorial Content):**
- **`templates/index.html`**, **`templates/login.html`**, etc. - Original tutorial templates

### Core Application Structure
- **`app.py`**: Main Flask application with all routes, database models, and core logic
- **`forms.py`**: Flask-WTF form definitions for contact form handling
- **`static/css/cyberpunk.css`**: Comprehensive cyberpunk design system
- **`static/css/style.css`**: Original basic CSS styling
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
- **`base.html`**: Legacy master template with navigation and flash message system
- **Cyberpunk templates**: Self-contained templates with inline cyberpunk styling
- **Flash messages**: Implemented with categories (success, error, info) - works across both template systems
- **Template inheritance**: Legacy templates use base.html, cyberpunk templates are standalone

### Route Structure
The application implements a comprehensive set of routes:

**Primary CPA Learning Routes (Cyberpunk Templates):**
- `/` - Home page (uses `home_cyber.html`)
- `/about` - About page (uses `about_cyber.html`)
- `/contact` - Contact form (uses `contact_cyber.html`)
- `/login` - User login (uses `login_cyber.html`)
- `/cpa-learning` - CPA subject dashboard (uses `cpa_learning.html`)
- `/flashcards` - Interactive flashcard system (uses `flashcards.html`)

**Legacy Demo Routes:**
- `/messages` - Message list display (original functionality)
- `/upload` - File upload functionality
- `/ajax-demo` - AJAX demonstration page
- `/logout` - User logout
- `/user/<username>` - User profile demo
- `/admin` - Admin dashboard demo
- `/guest/<guest>` - Guest welcome demo

**AJAX Endpoints:**
- `/ajax/say-hello` - POST endpoint for AJAX hello functionality
- `/ajax/say-goodbye` - POST endpoint for AJAX goodbye functionality

### Key Technical Features

#### Cyberpunk Design System
- **CSS Custom Properties**: Comprehensive color system with neon gradients
- **Glassmorphism Effects**: backdrop-filter blur and transparency
- **Neon Animations**: Pulsing borders and glowing text effects
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox

#### Flashcard Learning System
- **3D Card Flips**: CSS transform-based card rotations
- **Touch Gesture Support**: Swipe navigation for mobile devices
- **Keyboard Navigation**: Arrow keys and spacebar controls
- **Progress Tracking**: Visual progress bars and completion metrics
- **Difficulty Filtering**: Dynamic content filtering by difficulty level

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

### Development Patterns

#### Adding New Cyberpunk Pages
1. Create new template in `templates/` with `_cyber.html` suffix
2. Include cyberpunk CSS: `<link rel="stylesheet" href="{{ url_for('static', filename='css/cyberpunk.css') }}">`
3. Define route function in `app.py` pointing to the new template
4. Use glass-container class for main content areas
5. Apply neon-border class for interactive elements

#### Extending Flashcard System
1. Add new flashcard data to JavaScript arrays in `templates/flashcards.html`
2. Update category filtering logic
3. Add new progress tracking metrics
4. Implement new animation effects using CSS transforms

#### Database Model Extensions
1. Define new model class in `app.py`
2. Run database initialization (automatic on app restart)
3. Update forms and templates accordingly
4. Implement CRUD operations as needed

#### AJAX Endpoints
1. Create POST route in `app.py`
2. Return JSON responses using `jsonify()`
3. Implement JavaScript client-side logic
4. Add error handling and user feedback

#### Customizing Cyberpunk Theme
1. Modify CSS custom properties in `static/css/cyberpunk.css`
2. Update neon color variables for different themes
3. Adjust glassmorphism parameters for visual effects
4. Add new animation keyframes for interactive elements

This project provides a solid foundation for modern Flask development with advanced UI design and comprehensive feature coverage.