# flask_application
This repository contains the source code for a secure file-sharing system built using Flask, a Python web framework, and MySQL, a relational database management system. 

Set Up Flask and MySQL:

First, install Flask and Flask-MySQL:
pip install Flask Flask-MySQL

Create Flask Application:
Create a Python file (app.py) to define the Flask application.

Define Models:
Define models for User and File in app.py. Make sure to use SQLAlchemy for database interactions.


Ops User Endpoints:
/ops-login: Allows Ops Users to log in by providing their username and password.
/upload-file: Allows Ops Users to upload files. It checks if the uploaded file type is allowed (pptx, docx, xlsx) and saves the file in the server's filesystem.


Client User Endpoints:
/signup: Allows Client Users to sign up by providing a username, email, and password. Generates an encrypted URL for verification.
/verify-email/<encrypted_url>: Verifies the user's email using the provided encrypted URL (not fully implemented in this code).
/client-login: Allows Client Users to log in by providing their username and password.
/download-file/<int:file_id>: Allows Client Users to download files by providing the file ID. Generates a secure encrypted URL for downloading the file.
/list-files: Allows Client Users to list all uploaded files. Only Ops Users are authorized to access this endpoint.
