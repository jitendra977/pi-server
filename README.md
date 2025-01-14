# Home Automation Server Project

This is a Django-based server project for home automation, running on a Raspberry Pi (64-bit). The project is designed to manage and automate various home systems and devices, providing a web interface for control and monitoring.

## Project Structure

- `db.sqlite3`: SQLite database file storing the application's data.
- `manage.py`: Django's command-line utility for administrative tasks.
- `mysite/`: Main Django project directory containing settings, URLs, and WSGI configuration.
- `mytest.py`: Custom script or test file for the project.
- `server/`: Contains server-related configuration and files.
- `venv/`: Python virtual environment for the project.
- `views.py`: Contains Django views handling the application's logic.

## Setup Instructions

### Prerequisites

- Raspberry Pi (64-bit)
- Python 3.x
- Virtual Environment (`venv`)
- Django framework

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd Django