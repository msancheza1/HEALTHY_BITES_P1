# Healthy Bites - Django Meal Planner & Recipe Application

A modern, responsive Django web application for managing healthy recipes, meal planning, and BMI tracking.

## 🌟 Features

- **User Authentication**: Secure registration and login system
- **Recipe Management**: Browse, search, and manage recipes
- **Favorites System**: Save and manage favorite recipes
- **User Profiles**: Complete profile management with health information (weight, height, allergies, dietary restrictions)
- **BMI Tracking**: Monitor BMI changes over time with historical records
- **Progress History**: Visual charts showing BMI and weight progression
- **Step-by-Step Recipes**: Detailed step-by-step recipe instructions with progress tracking
- **Smart Filtering**: Filter recipes based on user dietary preferences and health goals

## 📦 Project Structure

```
HEALTHY_BITES_P1/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
├── .gitignore
│
├── healthybites/          # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/              # User authentication and profiles
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       ├── accounts/
│       │   ├── register.html
│       │   └── profile.html
│       └── registration/
│           └── login.html
│
├── recipes/               # Recipe management
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── recipes/
│           ├── recipe_detail.html
│           ├── recipe_steps.html
│           ├── search_results.html
│           └── my_favorites.html
│
├── planner/               # Meal planning and progress tracking
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── planner/
│           ├── home.html
│           └── progress_history.html
│
├── templates/             # Global templates
│   └── base/
│       └── base.html
│
├── static/                # Static files (CSS, JS, Images)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   ├── img/
│   └── planner/
│       └── images/
│
└── media/                 # User-uploaded files
    └── uploads/
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd HEALTHY_BITES_P1
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create a superuser**
```bash
python manage.py createsuperuser
```

6. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

7. **Run the development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## 🏗️ Architecture

### Apps

#### **accounts**
- User registration and authentication
- User profile management
- BMI records and progress tracking
- Health metrics (weight, height, allergies, dietary restrictions)

#### **recipes**
- Recipe creation and management
- Recipe searching and filtering
- Favorites management
- Step-by-step recipe instructions
- Recipe details display

#### **planner**
- Home page with personalized recipe recommendations
- Progress history visualization with charts
- Integration of recipes and user health data
- BMI trend analysis

### Database Models

**UserProfile** (accounts.models)
- Linked to Django User model
- Stores health metrics and dietary preferences

**Recipe** (recipes.models)
- Stores recipe information
- Tracks dietary attributes (vegetarian, diabetic-friendly, lactose-free, gluten-free)

**RecipeStep** (recipes.models)
- Detailed instructions for recipes
- Sequential step management

**Favorite** (recipes.models)
- Tracks user favorite recipes

**BMIRecord** (accounts.models)
- Historical BMI tracking
- Snapshots created on profile updates

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory (for sensitive data):
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database
By default, SQLite is used for development. For production, update `DATABASES` in `settings.py`.

## 📊 Technologies Used

- **Backend**: Django 5.2
- **Frontend**: Bootstrap 5.3, HTML5, CSS3
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Charts**: Chart.js for BMI progress visualization
- **Forms**: Django Forms with Form Validation

## 👥 User Roles

- **Anonymous Users**: Can view recipes and search
- **Authenticated Users**: Can create profiles, save favorites, track progress

## 🔒 Security Features

- CSRF protection
- Password validation
- Secure session management
- User authentication decorators
- Form validation

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop (1920px and above)
- Tablet (768px - 1024px)
- Mobile (320px - 767px)

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions or suggestions, please contact the development team.

---

**Happy Eating! 🥗**

Healthy Bites provides a personalized nutrition experience based on:

- Weight and height
- Health conditions (e.g., diabetes, cholesterol)
- Dietary restrictions (vegetarian, gluten-free, lactose-free, allergies, etc.)
- User goals (gain, maintain, or lose weight)

The system classifies the user’s physical condition and generates tailored recommendations, recipe suggestions, and weekly shopping lists.

---

## 🎯 Problem Statement

Many people struggle with meal planning and healthy eating because:

- They do not know what to cook.
- They waste time searching for recipes.
- They do not consider their physical condition or dietary restrictions.
- They lack structured planning tools.

Healthy Bites addresses this gap by integrating nutrition personalization and recipe planning into a single web application.

---

## 💡 Proposed Solution

Healthy Bites offers:

- User registration and authentication
- Personalized nutrition profile
- Physical status calculation and classification
- Adapted nutrition recommendations
- Recipe catalog with filtering and search
- Weekly meal planning
- Automatic shopping list generation
- Optional chatbot for ingredient-based recommendations

---

## 🏗️ System Architecture

Healthy Bites follows a **3-tier Web Application architecture**:

### 1️⃣ Client Layer
- Web Browser
- Responsive User Interface
- HTTPS communication with backend

### 2️⃣ Business Layer (Backend)
- REST API
- Authentication & Authorization
- Business Logic Services:
  - User Management
  - Nutrition Classification
  - Recipe Management
  - Meal Planning
  - Shopping List Generation

### 3️⃣ Data Layer
- Relational Database
- Persistent storage for:
  - Users
  - Profiles
  - Recipes
  - Meal Plans
  - Ingredients

---

## 📋 Functional Scope

The system includes:

- 24 Functional Requirements (FR)
- 5 Usability Requirements (UR)
- 5 Database Requirements (DR)
- 4 System Constraints (CR)

Requirements are prioritized using the **MoSCoW method** (MUST, SHOULD, COULD).

---

## 🎥 Project Video

🔗 Add video link here

Video includes:
- Project introduction
- Problem statement
- Proposed solution
- Top 12 prioritized requirements
- Team participation

---

## 👥 Team Members

- Jeronimo Rodriguez  
- Jose Luis Restrepo  
- Mariana Sanchez  
- Fabiola Valencia  
- Yilmar Murillo  

Instructor: Mario Jaramillo Vargas  
University: EAFIT University  
Semester: 2026-1  

---

## 📂 Repository Structure


