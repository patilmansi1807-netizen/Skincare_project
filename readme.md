🌸 GlowCare – Smart Skincare Management Website
GlowCare is a skincare management web application built with Python and Flask. It helps users explore skincare products, receive personalized skincare recommendations based on selected skin type and concerns, manage daily routines, set reminders, track expenses, and schedule appointments.
✨ Features
- Personalized skincare recommendations: Rule-based guidance based on the selected skin type and primary concern.
- Skincare product catalog: Browse 30 curated products with brand, category, price, description, stock, skin-type suitability, concern, rating, and image information.
- Product matching: View products selected using skin type, concern, and general-suitability fields.
- Routine management: Add and remove morning or night skincare steps.
- Skincare reminders: Create, view, and delete reminders.
- Expense tracking: Record skincare spending, view total expenses, and see category-wise totals.
- Appointment management: Schedule and cancel skincare or dermatologist appointments.
- User profile: Save and update name, age, skin type, and primary concern.
- Product purchase logging: Record a product purchase in the expense tracker and order tables.
- Product JSON endpoint: Retrieve the catalog through /api/products.
- SQLite database: Store profiles, products, routines, reminders, expenses, appointments, and order information.
Note: Recommendations in the current code are generated using predefined Python rules. The application does not currently implement a trained AI/ML model or image-based skin diagnosis. Recommendations are for general informational purposes and are not a substitute for professional medical advice.

🛠️ Tech Stack
- Backend: Python, Flask
- Database: SQLite (sqlite3)
- Frontend: HTML templates rendered with Jinja2, plus CSS and JavaScript (if included in the project)
- Deployment server: Gunicorn
- Other dependencies: Werkzeug
📁 Project Structure
GlowCare/
├── app.py
├── requirements.txt
├── Procfile
├── .gitignore
├── run_app.bat
├── DEPLOY_INSTRUCTIONS.md
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── products.html
│   ├── profile.html
│   ├── routine.html
│   ├── reminder.html
│   ├── expenses.html
│   └── appointment.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── skincare.db  (created when the application runs)
This is an example of the expected structure. Keep only the files and folders that actually exist in your repository. The database is initialized by the application and may be created at runtime.
🚀 Getting Started
Prerequisites
- Python 3.10 or later
- pip
1. Clone the repository
Replace YOUR_GITHUB_REPOSITORY_URL with your repository's URL:
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
2. Create and activate a virtual environment
Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
macOS / Linux:
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Run the application
python app.py
On Windows, you can also use run_app.bat if it is configured for your environment.
5. Open GlowCare
Open this URL in your browser:
http://127.0.0.1:5000
The application initializes the SQLite tables and populates the default product catalog when needed.
🧭 Main Pages
Route	Purpose
/	Home page
/analyze	Generate recommendations and show matching products
/products	Browse the product catalog
/profile	Create or update the skincare profile
/routine	Manage daily routine steps
/reminder	Manage reminders
/expenses	Track expenses and category totals
/appointment	Manage appointments
/api/products	Return the product catalog as JSON


☁️ Deployment
The repository includes a Procfile for running the Flask application with Gunicorn.
Build command:
pip install -r requirements.txt
Start command:
gunicorn app:app
See [`DEPLOY_INSTRUCTIONS.md`](DEPLOY_INSTRUCTIONS.md) for the project's deployment instructions.
Deployment considerations:
- Set a secure SECRET_KEY environment variable in the hosting service.
- The current code uses a local SQLite database file. On hosts with ephemeral filesystems, data may be lost when the service restarts or redeploys unless persistent storage is configured.
- For a production deployment, turn off Flask debug mode and review security, authentication, data validation, and database configuration.
🎯 Project Objectives
- Make everyday skincare routine management easier.
- Organize product information and skin-concern-based suggestions in one place.
- Help users maintain reminders and appointments.
- Provide a simple way to record and review skincare expenses.
- Practice full-stack web development with Flask and SQLite.
🔮 Future Improvements
- Secure user registration and login.
- Improved product search and filtering.
- Email or push notifications for reminders.
- Interactive expense charts and analytics.
- Integration with a dermatologist consultation service.
- Optional image-based analysis, if implemented with appropriate validation and medical safeguards.
- More robust order management and payment integration.
👩‍💻 Author
Mansi Patil
Computer Science Engineering Student
📄 License
This project is currently presented for educational purposes. Add a LICENSE file if you want to specify terms for reuse and distribution.🌸 GlowCare – Smart Skincare Management Website
GlowCare is a skincare management web application built with Python and Flask. It helps users explore skincare products, receive personalized skincare recommendations based on selected skin type and concerns, manage daily routines, set reminders, track expenses, and schedule appointments.
✨ Features
- Personalized skincare recommendations: Rule-based guidance based on the selected skin type and primary concern.
- Skincare product catalog: Browse 30 curated products with brand, category, price, description, stock, skin-type suitability, concern, rating, and image information.
- Product matching: View products selected using skin type, concern, and general-suitability fields.
- Routine management: Add and remove morning or night skincare steps.
- Skincare reminders: Create, view, and delete reminders.
- Expense tracking: Record skincare spending, view total expenses, and see category-wise totals.
- Appointment management: Schedule and cancel skincare or dermatologist appointments.
- User profile: Save and update name, age, skin type, and primary concern.
- Product purchase logging: Record a product purchase in the expense tracker and order tables.
- Product JSON endpoint: Retrieve the catalog through /api/products.
- SQLite database: Store profiles, products, routines, reminders, expenses, appointments, and order information.
Note: Recommendations in the current code are generated using predefined Python rules. The application does not currently implement a trained AI/ML model or image-based skin diagnosis. Recommendations are for general informational purposes and are not a substitute for professional medical advice.

🛠️ Tech Stack
- Backend: Python, Flask
- Database: SQLite (sqlite3)
- Frontend: HTML templates rendered with Jinja2, plus CSS and JavaScript (if included in the project)
- Deployment server: Gunicorn
- Other dependencies: Werkzeug
📁 Project Structure
GlowCare/
├── app.py
├── requirements.txt
├── Procfile
├── .gitignore
├── run_app.bat
├── DEPLOY_INSTRUCTIONS.md
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── products.html
│   ├── profile.html
│   ├── routine.html
│   ├── reminder.html
│   ├── expenses.html
│   └── appointment.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── skincare.db  (created when the application runs)
This is an example of the expected structure. Keep only the files and folders that actually exist in your repository. The database is initialized by the application and may be created at runtime.
🚀 Getting Started
Prerequisites
- Python 3.10 or later
- pip
1. Clone the repository
Replace YOUR_GITHUB_REPOSITORY_URL with your repository's URL:
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
2. Create and activate a virtual environment
Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
macOS / Linux:
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Run the application
python app.py
On Windows, you can also use run_app.bat if it is configured for your environment.
5. Open GlowCare
Open this URL in your browser:
http://127.0.0.1:5000
The application initializes the SQLite tables and populates the default product catalog when needed.
🧭 Main Pages
Route	Purpose
/	Home page
/analyze	Generate recommendations and show matching products
/products	Browse the product catalog
/profile	Create or update the skincare profile
/routine	Manage daily routine steps
/reminder	Manage reminders
/expenses	Track expenses and category totals
/appointment	Manage appointments
/api/products	Return the product catalog as JSON


☁️ Deployment
The repository includes a Procfile for running the Flask application with Gunicorn.
Build command:
pip install -r requirements.txt
Start command:
gunicorn app:app
See [`DEPLOY_INSTRUCTIONS.md`](DEPLOY_INSTRUCTIONS.md) for the project's deployment instructions.
Deployment considerations:
- Set a secure SECRET_KEY environment variable in the hosting service.
- The current code uses a local SQLite database file. On hosts with ephemeral filesystems, data may be lost when the service restarts or redeploys unless persistent storage is configured.
- For a production deployment, turn off Flask debug mode and review security, authentication, data validation, and database configuration.
🎯 Project Objectives
- Make everyday skincare routine management easier.
- Organize product information and skin-concern-based suggestions in one place.
- Help users maintain reminders and appointments.
- Provide a simple way to record and review skincare expenses.
- Practice full-stack web development with Flask and SQLite.
🔮 Future Improvements
- Secure user registration and login.
- Improved product search and filtering.
- Email or push notifications for reminders.
- Interactive expense charts and analytics.
- Integration with a dermatologist consultation service.
- Optional image-based analysis, if implemented with appropriate validation and medical safeguards.
- More robust order management and payment integration.
👩‍💻 Author
Mansi Patil
Computer Science Engineering Student
📄 License
This project is currently presented for educational purposes. Add a LICENSE file if you want to specify terms for reuse and distribution.
