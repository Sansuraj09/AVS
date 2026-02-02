# Python Flask Server with MySQL - No PHP Required!
# Run: python app.py

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for frontend

# MySQL Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',              # Change this to your MySQL username
    'password': 'Suraj_jadhav2003',              # Change this to your MySQL password
    'database': 'users'  # Change this to your database name
}

# Function to get database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

# Test database connection on startup
def test_connection():
    conn = get_db_connection()
    if conn and conn.is_connected():
        print("✅ Successfully connected to MySQL database")
        print(f"📊 Database: {DB_CONFIG['database']}")
        conn.close()
        return True
    else:
        print("❌ Failed to connect to MySQL database")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database credentials are correct")
        print("3. Database exists")
        return False

# Serve the main HTML page
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve static files
@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return jsonify({'error': 'File not found'}), 404

# Health check endpoint
@app.route('/health')
def health():
    conn = get_db_connection()
    if conn and conn.is_connected():
        conn.close()
        return jsonify({
            'status': 'OK',
            'message': 'Server and database are running',
            'database': DB_CONFIG['database']
        })
    else:
        return jsonify({
            'status': 'ERROR',
            'message': 'Database connection lost'
        }), 500

# Test database connection endpoint
@app.route('/api/test-connection')
def test_db_connection():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT DATABASE() as db, VERSION() as version, USER() as user')
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'connection': result
        })
    except Error as e:
        return jsonify({'error': 'Database query failed', 'details': str(e)}), 500

# CREATE - Add new record
@app.route('/api/data', methods=['POST'])
def create_data():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        query = 'INSERT INTO users (name, email, created_at) VALUES (%s, %s, NOW())'
        cursor.execute(query, (name, email))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Record created successfully',
            'id': new_id
        }), 201
    except Error as e:
        error_msg = str(e)
        if 'Duplicate entry' in error_msg:
            return jsonify({'error': 'Email already exists'}), 400
        elif "doesn't exist" in error_msg:
            return jsonify({'error': 'Table does not exist. Please run setup_database.sql first'}), 500
        else:
            return jsonify({'error': 'Database error', 'details': error_msg}), 500

# READ - Get all records
@app.route('/api/data', methods=['GET'])
def get_all_data():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convert datetime to string for JSON serialization
        for row in results:
            if 'created_at' in row and row['created_at']:
                row['created_at'] = str(row['created_at'])
            if 'updated_at' in row and row['updated_at']:
                row['updated_at'] = str(row['updated_at'])
        
        return jsonify(results)
    except Error as e:
        error_msg = str(e)
        if "doesn't exist" in error_msg:
            return jsonify({'error': 'Table does not exist. Please run setup_database.sql first'}), 500
        else:
            return jsonify({'error': 'Database error', 'details': error_msg}), 500

# READ - Get single record by ID
@app.route('/api/data/<int:id>', methods=['GET'])
def get_data_by_id(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            # Convert datetime to string
            if 'created_at' in result and result['created_at']:
                result['created_at'] = str(result['created_at'])
            if 'updated_at' in result and result['updated_at']:
                result['updated_at'] = str(result['updated_at'])
            return jsonify(result)
        else:
            return jsonify({'error': 'Record not found'}), 404
    except Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

# UPDATE - Update existing record
@app.route('/api/data/<int:id>', methods=['PUT'])
def update_data(id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        query = 'UPDATE users SET name = %s, email = %s, updated_at = NOW() WHERE id = %s'
        cursor.execute(query, (name, email, id))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Record updated successfully'})
        else:
            return jsonify({'error': 'Record not found'}), 404
    except Error as e:
        error_msg = str(e)
        if 'Duplicate entry' in error_msg:
            return jsonify({'error': 'Email already exists'}), 400
        else:
            return jsonify({'error': 'Database error', 'details': error_msg}), 500

# DELETE - Delete record
@app.route('/api/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Record deleted successfully'})
        else:
            return jsonify({'error': 'Record not found'}), 404
    except Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

# Get all tables
@app.route('/api/tables', methods=['GET'])
def get_tables():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SHOW TABLES')
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

if __name__ == '__main__':
    print('\n' + '='*60)
    print('🚀 Starting Flask Server (No PHP Required!)')
    print('='*60 + '\n')
    
    # Test connection on startup
    if test_connection():
        print(f'\n📡 Server running on http://localhost:5000')
        print(f'🌐 Open http://localhost:5000 in your browser\n')
        print('💡 API Endpoints:')
        print('   GET    /health              - Check server status')
        print('   GET    /api/data            - Get all records')
        print('   GET    /api/data/<id>       - Get single record')
        print('   POST   /api/data            - Create new record')
        print('   PUT    /api/data/<id>       - Update record')
        print('   DELETE /api/data/<id>       - Delete record')
        print('\n⏹️  Press Ctrl+C to stop the server\n')
        
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print('\n❌ Cannot start server - database connection failed')
        print('Please check your MySQL configuration in the script\n')
