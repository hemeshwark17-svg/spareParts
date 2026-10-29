# Vehicle Spare Parts Inventory Management System

College DBMS starter website built with HTML, CSS, Python Flask, and MySQL.

## What's included
- Public catalogue with search and category filter
- Product details and stock availability
- Admin login and inventory add/edit/hide actions
- MySQL database schema and sample data
- Responsive styling for mobile and desktop

## Run on Windows
1. Install Python 3 and MySQL Server. MySQL Workbench is a database management tool.
2. In MySQL Workbench, connect to your local server, open `schema.sql`, and execute it.
3. Open Command Prompt in this project folder and run:
   `py -m venv .venv`
   `.venv\\Scripts\\activate`
   `pip install -r requirements.txt`
4. Set the database connection values in the same terminal:
   `set DB_HOST=localhost`
   `set DB_PORT=3306`
   `set DB_USER=root`
   `set DB_PASSWORD=YOUR_MYSQL_PASSWORD`
   `set DB_NAME=vehicle_spares`
   `set FLASK_SECRET_KEY=replace-with-a-long-random-secret`
   `set ADMIN_PASSWORD=choose-a-strong-password`
5. Start it with `python app.py`.
6. Open `http://127.0.0.1:5000`.
7. Admin page: `http://127.0.0.1:5000/admin/login`.

## Public deployment
This project is not online yet. To publish it, deploy the Flask app to a hosting provider and connect it to a managed MySQL database. Set all DB_* values, FLASK_SECRET_KEY, and ADMIN_PASSWORD as private environment variables in the provider dashboard. Do not publish credentials or expose MySQL directly to the public internet.

This is a learning starter, not a production-ready store. Before real public use, add CSRF protection, robust admin authentication, rate limiting, backups, HTTPS, and validation. The catalogue currently uses demo data and does not accept purchases.
