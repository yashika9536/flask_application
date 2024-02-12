from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/file_sharing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)  # New field for email verification

# Define File model
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('files', lazy=True))

# Endpoint for Ops User login
@app.route('/ops-login', methods=['POST'])
def ops_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password, role='ops').first()
    if user:
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Endpoint for Ops User upload file
@app.route('/upload-file', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename

    # Check if the file extension is allowed
    allowed_extensions = {'pptx', 'docx', 'xlsx'}
    if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({"message": "Invalid file type"}), 400

    # Save the file
    file.save(filename)

    # Get user_id from headers
    user_id = request.headers.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID not provided"}), 400

    # Store the file in the database
    new_file = File(filename=filename, user_id=user_id)
    db.session.add(new_file)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully"}), 200

# Endpoint for Client User signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if the user already exists
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 409

    # Create a new User
    new_user = User(username=username, email=email, password=password, role='client')
    db.session.add(new_user)
    db.session.commit()

    # Generate encrypted URL for email verification
    token = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    verification_url = f"http://example.com/verify-email/{token}"  # Change example.com to your domain
    # Send verification email (not implemented in this example)

    return jsonify({"message": "User registered successfully", "verification_url": verification_url}), 201

# Endpoint for email verification
@app.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    # Decrypt token and retrieve user's email
    # For simplicity, I'm assuming the token is the same as the hashed email
    email = token

    # Find the user by email
    user = User.query.filter_by(email=email).first()
    if user:
        # Mark the user's email as verified
        user.email_verified = True
        db.session.commit()
        return redirect("http://example.com/email-verified")  # Redirect to a page indicating successful email verification
    else:
        return jsonify({"message": "User not found"}), 404

# Endpoint for Client User login
@app.route('/client-login', methods=['POST'])
def client_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password, role='client', email_verified=True).first()
    if user:
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    else:
        return jsonify({"message": "Invalid credentials or email not verified"}), 401

# Endpoint for Client User download file
@app.route('/download-file/<int:file_id>', methods=['GET'])
def download_file(file_id):
    # Check if the user is authorized
    user_id = request.headers.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID not provided"}), 400

    file = File.query.filter_by(id=file_id).first()
    if not file:
        return jsonify({"message": "File not found"}), 404

    # Generate encrypted URL (using UUID and hashing)
    url = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    
    return jsonify({"download-link": url}), 200

# Endpoint for listing all uploaded files
@app.route('/list-files', methods=['GET'])
def list_files():
    # Get user_id from headers
    user_id = request.headers.get('user_id')
    if not user_id:
        return jsonify({"message": "not found"})




if __name__ == '__main__':
    app.run(debug=True)
