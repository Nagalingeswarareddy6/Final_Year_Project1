# Blockchain-Based Tamper-Proof QR Code System

A secure QR code generation and verification system that uses blockchain technology and multi-factor authentication to ensure data integrity and prevent tampering.

## 📋 Current Implementation Status

This section provides a detailed breakdown of what has been completed in the project:

### ✅ Built Core Infrastructure
- **Blockchain Class**: Fully implemented with genesis block creation, chain management, and block hashing using SHA-256
- **Proof-of-Work Consensus**: Developed simple mining algorithm requiring hash to start with "0000"
- **Transaction System**: Built transaction queue and block mining mechanism for QR metadata storage
- **Flask Web Server**: Constructed complete backend with RESTful API endpoints and session management
- **Frontend Interface**: Created 5 HTML templates (base, index, register, login, dashboard) with responsive CSS styling
- **Static Assets**: Designed custom CSS (`style.css`) and JavaScript utilities (`script.js`) for client-side interactions

### 🔐 Integrated Security Systems
- **Multi-Factor Authentication (MFA)**: Integrated three-layer authentication combining password, TOTP-based OTP, and device binding
- **Password Hashing**: Implemented SHA-256 password hashing for credential storage
- **TOTP Generation**: Integrated PyOTP library for time-based one-time password generation
- **Device Registry**: Built device fingerprinting and registration system linking users to trusted devices
- **Session Management**: Integrated Flask session handling for authenticated user tracking
- **Hash Verification**: Embedded content integrity checking using SHA-256 checksums

### 💻 Developed Application Features
- **User Registration Flow**: Developed complete registration endpoint with automatic device ID generation
- **Login Authentication**: Created multi-step login process with password, OTP, and device verification
- **QR Code Generation**: Developed secure QR creation pipeline that generates unique IDs, timestamps, content hashes, and blockchain transactions
- **QR Code Verification**: Built comprehensive verification system checking blockchain integrity, hash validity, and user/device authorization
- **Blockchain Status Dashboard**: Developed real-time monitoring displaying total blocks, pending transactions, and latest block hash
- **Logout Functionality**: Implemented secure session termination

### 🎨 Designed User Experience
- **Responsive Layout**: Designed mobile-friendly and desktop-optimized interface
- **Dashboard Interface**: Created centralized control panel for QR generation, verification, and blockchain monitoring
- **Form Validation**: Built client-side and server-side input validation
- **JSON API Responses**: Structured consistent API response format for frontend-backend communication
- **Error Handling**: Designed user-friendly error messages and exception handling

### 🧪 Implemented Technical Components
- **QRCode Library Integration**: Implemented QR image generation with configurable error correction and sizing
- **PIL Image Processing**: Integrated image creation and file saving for QR codes
- **UUID Generation**: Utilized UUID v4 for unique QR IDs, transaction IDs, and device IDs
- **Cryptography Module**: Incorporated Fernet encryption suite (though key generation is implemented, encryption is not fully utilized)
- **RESTful API Architecture**: Established 8 API endpoints following REST conventions
- **In-Memory Data Storage**: Configured runtime storage for blockchain, users, devices, and credentials

### 🔗 Architected System Components
- **Modular Design**: Separated core logic (`blockchain_qr_system.py`) from web application (`app.py`)
- **Class-Based Architecture**: Structured three primary classes (Blockchain, MultiFactorAuth, SecureQRGenerator)
- **Template Inheritance**: Utilized Jinja2 template inheritance with `base.html` for consistent UI
- **Static File Serving**: Configured Flask to serve CSS and JavaScript assets
- **Error Correction**: Implemented QR error correction at level L (7% recovery)

### 📝 Documented System
- **Comprehensive README**: Written detailed documentation covering installation, usage, architecture, and troubleshooting
- **Inline Code Comments**: Added explanatory comments throughout Python modules
- **API Documentation**: Documented all endpoints with methods and purposes
- **File Structure Map**: Provided complete project structure overview
- **Troubleshooting Guide**: Created common issues and solutions section

### 🧠 Brainstormed & Planned
- **Future Enhancements Section**: Identified potential improvements including real blockchain integration, AES encryption, mobile apps, batch operations, and analytics
- **Security Considerations**: Outlined current security measures and their theoretical effectiveness
- **Scalability Thoughts**: Acknowledged current in-memory limitations and need for persistent storage
- **Production Readiness Notes**: Flagged demo/educational nature and need for production hardening

### ⚠️ Known Limitations (Already Identified)
- **In-Memory Storage**: All data (blockchain, users, devices) is lost on application restart
- **Simplified Blockchain**: No persistence, no network distribution, no actual consensus beyond single-node PoW
- **Basic Security**: SHA-256 for passwords (industry standard is bcrypt/argon2), hardcoded secret key, no rate limiting
- **QR File Management**: QR images saved to project root instead of organized static folder
- **No Database**: No SQL/NoSQL backend for persistent data storage
- **Single Server**: No horizontal scaling or load balancing support
- **OTP Exposure**: OTP returned directly in API response instead of secure delivery channel

## Features

### 🔒 Security Features
- **Blockchain Integration**: QR metadata stored on decentralized ledger
- **Multi-Factor Authentication**: Password + OTP + Device binding
- **Tamper Detection**: Hash-based integrity verification
- **Device Binding**: QR codes tied to specific devices
- **Real-time Verification**: Instant blockchain validation

### 🚀 Technical Features
- **Flask Web Application**: Modern web interface
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live blockchain status monitoring
- **Secure Storage**: Encrypted data handling
- **User-friendly Interface**: Intuitive dashboard

## Installation

1. **Clone or download the project files**
   ```bash
   # Ensure you have Python 3.7+ installed
   python --version
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the system**
   - Open your browser and go to `http://localhost:5000`
   - Register a new account or login with existing credentials

## Usage

### 1. Registration
- Click "Register" on the homepage
- Enter your User ID and password
- Device information is auto-detected
- Save your Device ID for future logins

### 2. Login
- Enter your User ID, password, and Device ID
- Click "Generate OTP" to get a one-time password
- Enter the OTP and click "Login"

### 3. Generate QR Codes
- Go to the Dashboard after login
- Enter the content you want to encode
- Click "Generate QR Code"
- The system creates a secure QR code with blockchain verification

### 4. Verify QR Codes
- Paste the QR code content in the verification section
- Click "Verify QR Code"
- View detailed verification results including blockchain status

### 5. Monitor Blockchain
- View real-time blockchain status
- See total blocks, pending transactions, and latest block hash
- Refresh status to get updated information

## System Architecture

### Core Components

1. **Blockchain Class**
   - Manages the decentralized ledger
   - Handles transaction verification
   - Implements proof-of-work consensus

2. **Multi-Factor Authentication**
   - Password-based authentication
   - Time-based OTP generation
   - Device binding and verification

3. **Secure QR Generator**
   - Creates tamper-proof QR codes
   - Embeds security metadata
   - Integrates with blockchain storage

4. **Web Interface**
   - Flask-based backend
   - Responsive HTML/CSS frontend
   - Real-time JavaScript interactions

### Security Flow

1. **User Registration**
   ```
   User → Device Registration → Password Setup → OTP Secret Generation
   ```

2. **QR Generation**
   ```
   Content → Hash Generation → Blockchain Storage → QR Code Creation
   ```

3. **QR Verification**
   ```
   QR Content → Blockchain Lookup → Hash Verification → Device Validation
   ```

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - User login with MFA
- `POST /generate_otp` - Generate OTP for user
- `GET /logout` - User logout

### QR Operations
- `POST /generate_qr` - Generate secure QR code
- `POST /verify_qr` - Verify QR code integrity
- `GET /blockchain_status` - Get blockchain information

## Security Considerations

### Data Protection
- All passwords are hashed using SHA-256
- OTP secrets are generated using cryptographically secure methods
- Device information is encrypted before storage

### Blockchain Security
- Each block contains a cryptographic hash of the previous block
- Proof-of-work prevents easy tampering
- Transaction data is immutable once added to the blockchain

### Multi-Factor Authentication
- Requires password, OTP, and device binding
- OTP expires after a short time period
- Device binding prevents unauthorized access

## File Structure

```
project/
├── app.py                          # Flask web application
├── blockchain_qr_system.py         # Core blockchain and QR logic
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── templates/                      # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
└── static/                         # Static assets
    ├── style.css                   # CSS styles
    └── script.js                   # JavaScript utilities
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.7+ required)

2. **Port Already in Use**
   - Change the port in `app.py`: `app.run(port=5001)`
   - Or kill the process using port 5000

3. **QR Code Not Generating**
   - Check if the content is not empty
   - Ensure user is properly authenticated
   - Check browser console for JavaScript errors

4. **Verification Failing**
   - Ensure QR content is complete and unmodified
   - Check if user and device IDs match
   - Verify blockchain connectivity

### Debug Mode

To enable debug mode, modify `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Future Enhancements

- **Real Blockchain Integration**: Connect to actual blockchain networks
- **Advanced Encryption**: Implement AES encryption for sensitive data
- **Mobile App**: Native mobile applications
- **Batch Operations**: Generate multiple QR codes at once
- **Analytics Dashboard**: Usage statistics and monitoring
- **API Rate Limiting**: Prevent abuse and ensure fair usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and demonstration purposes. Please ensure compliance with local laws and regulations when using blockchain technology.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue with detailed error information

---

**Note**: This is a demonstration system. For production use, implement additional security measures, use real blockchain networks, and follow security best practices.
