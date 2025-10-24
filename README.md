# ELD Backend API (Django + DRF)

An Electronic Logging Device (ELD) backend built with Django and Django REST Framework.
It manages daily driver logs, tracks duty status changes (ON/OFF/DUTY/DRIVING/SLEEP BERTH), and records key trip metrics such as location data.

## Setup Instructions:

1. Clone and install dependencies

<pre>bash git clone https://github.com/&lt;your-username&gt;/eld-backend.git cd eld-backend python3 -m venv venv source venv/bin/activate pip install -r requirements.txt</pre>

2. Apply Migrations

<pre>python manage.py makemigrations eld python manage.py migrate</pre>

3. Run server

<pre>python manage.py runserver</pre>

API will be available at:

<pre>http://127.0.0.1:8000/api/</pre>

Endpoints (trailing slash is required as per current setup but you may modify settings.py to disable):

|  Method  | Endpoint                   | Description                                                 |
| :------: | -------------------------- | ----------------------------------------------------------- |
| **POST** | `/api/profile/`            | Add a new driver account                                    |
| **POST** | `/api/profile/login`       | Login driver account                                        |
| **GET**  | `/api/logs/`               | List all driver logs                                        |
| **GET**  | `/api/logs/{id}/`          | Retrieve a single daily log by ID                           |
| **POST** | `/api/logs/`               | Create a new daily log (not fully tested at this point)     |
| **POST** | `/api/logs/update-status/` | Add a new status change entry for the current driver & date |

Due to time constraints, I have not been able to complete the functionalities (while I added others like driver signup and login for session tracking)
