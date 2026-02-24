import hashlib
import json
import time
import uuid
from datetime import datetime
from cryptography.fernet import Fernet
import qrcode
from PIL import Image
import base64
import pyotp
import hmac
import os

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = {
            'index': 0,
            'timestamp': time.time(),
            'transactions': [],
            'previous_hash': '0',
            'nonce': 0
        }
        genesis_block['hash'] = self.hash_block(genesis_block)
        self.chain.append(genesis_block)
    
    def hash_block(self, block):
        """Create SHA-256 hash of a block"""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def add_transaction(self, qr_data, user_id, device_id):
        """Add a new transaction to the current transactions"""
        transaction = {
            'qr_id': qr_data['qr_id'],
            'user_id': user_id,
            'device_id': device_id,
            'timestamp': time.time(),
            'qr_metadata': qr_data,
            'transaction_id': str(uuid.uuid4())
        }
        self.current_transactions.append(transaction)
        return transaction['transaction_id']
    
    def mine_block(self):
        """Mine a new block with current transactions"""
        if not self.current_transactions:
            return None
        
        previous_block = self.chain[-1]
        new_block = {
            'index': len(self.chain),
            'timestamp': time.time(),
            'transactions': self.current_transactions.copy(),
            'previous_hash': previous_block['hash'],
            'nonce': 0
        }
        
        # Simple proof of work
        while not self.valid_proof(new_block):
            new_block['nonce'] += 1
        
        new_block['hash'] = self.hash_block(new_block)
        self.chain.append(new_block)
        self.current_transactions = []
        return new_block
    
    def valid_proof(self, block):
        """Simple proof of work validation"""
        guess = f"{block['previous_hash']}{block['nonce']}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
    def verify_qr_integrity(self, qr_id, qr_data):
        """Verify if QR code data matches blockchain records"""
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['qr_id'] == qr_id:
                    stored_data = transaction['qr_metadata']
                    return self.compare_qr_data(qr_data, stored_data)
        return False
    
    def compare_qr_data(self, data1, data2):
        """Compare two QR data objects for integrity"""
        return data1 == data2

class MultiFactorAuth:
    def __init__(self):
        self.secret_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.secret_key)
        self.device_registry = {}
        self.user_credentials = {}
    
    def register_device(self, user_id, device_id, device_info):
        """Register a device for a user"""
        if user_id not in self.device_registry:
            self.device_registry[user_id] = []
        
        device_data = {
            'device_id': device_id,
            'device_info': device_info,
            'registered_at': time.time(),
            'is_active': True
        }
        self.device_registry[user_id].append(device_data)
        return True
    
    def generate_otp(self, user_id):
        """Generate OTP for user"""
        if user_id not in self.user_credentials:
            self.user_credentials[user_id] = {
                'otp_secret': pyotp.random_base32(),
                'password_hash': None
            }
        
        totp = pyotp.TOTP(self.user_credentials[user_id]['otp_secret'])
        return totp.now()
    
    def verify_otp(self, user_id, otp):
        """Verify OTP for user"""
        if user_id not in self.user_credentials:
            return False
        
        totp = pyotp.TOTP(self.user_credentials[user_id]['otp_secret'])
        return totp.verify(otp)
    
    def set_password(self, user_id, password):
        """Set password for user"""
        if user_id not in self.user_credentials:
            self.user_credentials[user_id] = {
                'otp_secret': pyotp.random_base32(),
                'password_hash': None
            }
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.user_credentials[user_id]['password_hash'] = password_hash
        return True
    
    def verify_password(self, user_id, password):
        """Verify password for user"""
        if user_id not in self.user_credentials:
            return False
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.user_credentials[user_id]['password_hash'] == password_hash
    
    def verify_device(self, user_id, device_id):
        """Verify if device is registered for user"""
        if user_id not in self.device_registry:
            return False
        
        for device in self.device_registry[user_id]:
            if device['device_id'] == device_id and device['is_active']:
                return True
        return False
    
    def authenticate(self, user_id, password, otp, device_id):
        """Complete multi-factor authentication"""
        password_valid = self.verify_password(user_id, password)
        otp_valid = self.verify_otp(user_id, otp)
        device_valid = self.verify_device(user_id, device_id)
        
        return password_valid and otp_valid and device_valid

class SecureQRGenerator:
    def __init__(self, blockchain, auth_system):
        self.blockchain = blockchain
        self.auth_system = auth_system
    
    def generate_qr_data(self, content, user_id, device_id):
        """Generate secure QR code data with blockchain integration"""
        qr_id = str(uuid.uuid4())
        timestamp = time.time()
        
        # Create hash of content for integrity verification
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        qr_data = {
            'qr_id': qr_id,
            'content': content,
            'timestamp': timestamp,
            'hash': content_hash,
            'user_id': user_id,
            'device_id': device_id,
            'created_at': datetime.now().isoformat()
        }
        
        # Add to blockchain
        transaction_id = self.blockchain.add_transaction(qr_data, user_id, device_id)
        self.blockchain.mine_block()
        
        return qr_data
    
    def create_qr_code(self, qr_data):
        """Create QR code image with embedded security data"""
        # Create QR code with embedded metadata
        qr_content = json.dumps(qr_data)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to static folder
        output_dir = os.path.join('static', 'qr_codes')
        os.makedirs(output_dir, exist_ok=True)
        filename = f"qr_{qr_data['qr_id']}.png"
        output_path = os.path.join(output_dir, filename)
        img.save(output_path)
        
        return filename, qr_content
    
    def verify_qr_code(self, qr_content, user_id, device_id):
        """Verify QR code integrity and authenticity"""
        try:
            qr_data = json.loads(qr_content)
            
            # Verify blockchain integrity
            blockchain_valid = self.blockchain.verify_qr_integrity(
                qr_data['qr_id'], qr_data
            )
            
            # Verify hash integrity
            content_hash = hashlib.sha256(qr_data['content'].encode()).hexdigest()
            hash_valid = content_hash == qr_data['hash']
            
            # Verify user and device
            user_device_valid = (qr_data['user_id'] == user_id and 
                               qr_data['device_id'] == device_id)
            
            return {
                'valid': blockchain_valid and hash_valid and user_device_valid,
                'blockchain_valid': blockchain_valid,
                'hash_valid': hash_valid,
                'user_device_valid': user_device_valid,
                'qr_data': qr_data
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'blockchain_valid': False,
                'hash_valid': False,
                'user_device_valid': False
            }

# Initialize the system
blockchain = Blockchain()
auth_system = MultiFactorAuth()
qr_generator = SecureQRGenerator(blockchain, auth_system)

# Example usage
if __name__ == "__main__":
    # Register a user and device
    user_id = "user123"
    device_id = "device456"
    device_info = "Windows 10 Chrome Browser"
    
    # Set up authentication
    auth_system.register_device(user_id, device_id, device_info)
    auth_system.set_password(user_id, "securepassword123")
    
    # Generate OTP
    otp = auth_system.generate_otp(user_id)
    print(f"Generated OTP: {otp}")
    
    # Authenticate user
    auth_result = auth_system.authenticate(user_id, "securepassword123", otp, device_id)
    print(f"Authentication result: {auth_result}")
    
    if auth_result:
        # Generate secure QR code
        content = "This is a secure QR code with blockchain verification"
        qr_data = qr_generator.generate_qr_data(content, user_id, device_id)
        
        # Create QR code image
        filename, qr_content = qr_generator.create_qr_code(qr_data)
        print(f"QR code saved as: {filename}")
        
        # Verify QR code
        verification_result = qr_generator.verify_qr_code(qr_content, user_id, device_id)
        print(f"Verification result: {verification_result}")
