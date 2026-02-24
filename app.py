from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from blockchain_qr_system import blockchain, auth_system, qr_generator
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET' and 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        data = request.get_json() or {}
        user_id = (data.get('user_id') or '').strip()
        password = data.get('password') or ''
        device_info = data.get('device_info', 'Unknown Device')

        if not user_id or not password:
            return jsonify({
                'success': False,
                'message': 'User ID and password are required'
            }), 400

        if user_id in auth_system.user_credentials:
            return jsonify({
                'success': False,
                'message': 'User already exists. Please login instead.'
            }), 409
        
        # Generate device ID
        device_id = str(uuid.uuid4())
        
        # Register user and device
        auth_system.register_device(user_id, device_id, device_info)
        auth_system.set_password(user_id, password)
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'device_id': device_id,
            'redirect_url': url_for('login')
        })
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        data = request.get_json() or {}
        user_id = (data.get('user_id') or '').strip()
        password = data.get('password') or ''
        otp = (data.get('otp') or '').strip()
        device_id = (data.get('device_id') or '').strip()

        if not user_id or not password or not otp or not device_id:
            return jsonify({
                'success': False,
                'message': 'User ID, password, device ID and OTP are required'
            }), 400
        
        # Verify authentication
        auth_result = auth_system.authenticate(user_id, password, otp, device_id)
        
        if auth_result:
            session['user_id'] = user_id
            session['device_id'] = device_id
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'redirect_url': url_for('dashboard')
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Authentication failed'
            }), 401
    
    return render_template('login.html')

@app.route('/generate_otp', methods=['POST'])
def generate_otp():
    data = request.get_json() or {}
    user_id = (data.get('user_id') or '').strip()

    if not user_id:
        return jsonify({
            'success': False,
            'message': 'User ID is required'
        }), 400
    
    if user_id in auth_system.user_credentials:
        otp = auth_system.generate_otp(user_id)
        return jsonify({
            'success': True,
            'otp': otp,
            'message': 'OTP generated successfully'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', 
                         user_id=session['user_id'],
                         device_id=session['device_id'])

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Not authenticated',
            'redirect_url': url_for('login')
        }), 401
    
    data = request.get_json() or {}
    content = (data.get('content') or '').strip()
    
    if not content:
        return jsonify({'success': False, 'message': 'Content is required'}), 400
    
    try:
        # Generate QR data
        qr_data = qr_generator.generate_qr_data(
            content, 
            session['user_id'], 
            session['device_id']
        )
        
        # Create QR code
        filename, qr_content = qr_generator.create_qr_code(qr_data)
        
        return jsonify({
            'success': True,
            'qr_id': qr_data['qr_id'],
            'filename': filename,
            'image_url': url_for('static', filename=f'qr_codes/{filename}'),
            'qr_content': qr_content,
            'timestamp': qr_data['timestamp']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating QR code: {str(e)}'
        })

@app.route('/verify_qr', methods=['POST'])
def verify_qr():
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Not authenticated',
            'redirect_url': url_for('login')
        }), 401
    
    data = request.get_json() or {}
    qr_content = (data.get('qr_content') or '').strip()
    
    if not qr_content:
        return jsonify({'success': False, 'message': 'QR content is required'}), 400
    
    try:
        verification_result = qr_generator.verify_qr_code(
            qr_content,
            session['user_id'],
            session['device_id']
        )
        
        return jsonify({
            'success': True,
            'verification': verification_result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error verifying QR code: {str(e)}'
        })

@app.route('/blockchain_status')
def blockchain_status():
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Not authenticated',
            'redirect_url': url_for('login')
        }), 401
    
    # Get blockchain information
    chain_info = {
        'total_blocks': len(blockchain.chain),
        'pending_transactions': len(blockchain.current_transactions),
        'latest_block_hash': blockchain.chain[-1]['hash'] if blockchain.chain else None
    }
    
    return jsonify({
        'success': True,
        'blockchain': chain_info
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
