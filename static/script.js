// Global utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 3000;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// QR Code generation utilities
function generateQRCodeData(content, userInfo) {
    return {
        content: content,
        timestamp: Date.now(),
        user: userInfo,
        hash: generateHash(content + Date.now())
    };
}

function generateHash(data) {
    // Simple hash function for demo purposes
    let hash = 0;
    for (let i = 0; i < data.length; i++) {
        const char = data.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash).toString(16);
}

// Form validation utilities
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            field.style.borderColor = '#e1e5e9';
        }
    });
    
    return isValid;
}

// API utilities
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'API call failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// QR Code display utilities
function displayQRCode(qrData, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = `
        <div class="qr-display">
            <div class="qr-image">
                <i class="fas fa-qrcode"></i>
                <p>QR Code Generated</p>
            </div>
            <div class="qr-details">
                <h4>QR Code Details</h4>
                <p><strong>ID:</strong> ${qrData.qr_id || 'N/A'}</p>
                <p><strong>Content:</strong> ${qrData.content || 'N/A'}</p>
                <p><strong>Generated:</strong> ${new Date(qrData.timestamp * 1000).toLocaleString()}</p>
                <p><strong>Status:</strong> <span class="status-success">Secure & Verified</span></p>
            </div>
        </div>
    `;
}

// Verification display utilities
function displayVerificationResult(verification, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const statusClass = verification.valid ? 'success' : 'error';
    const statusText = verification.valid ? 'VALID' : 'INVALID';
    
    container.innerHTML = `
        <div class="verification-display">
            <div class="verification-status ${statusClass}">
                <i class="fas fa-${verification.valid ? 'check-circle' : 'times-circle'}"></i>
                <h3>${statusText}</h3>
            </div>
            <div class="verification-details">
                <div class="detail-item ${verification.blockchain_valid ? 'valid' : 'invalid'}">
                    <i class="fas fa-${verification.blockchain_valid ? 'check' : 'times'}"></i>
                    <span>Blockchain Verification: ${verification.blockchain_valid ? 'PASSED' : 'FAILED'}</span>
                </div>
                <div class="detail-item ${verification.hash_valid ? 'valid' : 'invalid'}">
                    <i class="fas fa-${verification.hash_valid ? 'check' : 'times'}"></i>
                    <span>Hash Integrity: ${verification.hash_valid ? 'PASSED' : 'FAILED'}</span>
                </div>
                <div class="detail-item ${verification.user_device_valid ? 'valid' : 'invalid'}">
                    <i class="fas fa-${verification.user_device_valid ? 'check' : 'times'}"></i>
                    <span>User/Device Binding: ${verification.user_device_valid ? 'PASSED' : 'FAILED'}</span>
                </div>
            </div>
            ${verification.qr_data ? `
                <div class="qr-data-display">
                    <h4>QR Code Data</h4>
                    <p><strong>Content:</strong> ${verification.qr_data.content}</p>
                    <p><strong>Created:</strong> ${new Date(verification.qr_data.timestamp * 1000).toLocaleString()}</p>
                    <p><strong>QR ID:</strong> ${verification.qr_data.qr_id}</p>
                </div>
            ` : ''}
        </div>
    `;
}

// Blockchain status utilities
function displayBlockchainStatus(status, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = `
        <div class="blockchain-status">
            <div class="status-item">
                <i class="fas fa-cubes"></i>
                <div>
                    <strong>Total Blocks:</strong>
                    <span>${status.total_blocks}</span>
                </div>
            </div>
            <div class="status-item">
                <i class="fas fa-clock"></i>
                <div>
                    <strong>Pending Transactions:</strong>
                    <span>${status.pending_transactions}</span>
                </div>
            </div>
            <div class="status-item">
                <i class="fas fa-link"></i>
                <div>
                    <strong>Latest Block Hash:</strong>
                    <code>${status.latest_block_hash ? status.latest_block_hash.substring(0, 20) + '...' : 'N/A'}</code>
                </div>
            </div>
        </div>
    `;
}

// Device detection utilities
function getDeviceInfo() {
    const userAgent = navigator.userAgent;
    const platform = navigator.platform;
    const language = navigator.language;
    
    let deviceType = 'Unknown';
    if (/Mobile|Android|iPhone|iPad/.test(userAgent)) {
        deviceType = 'Mobile';
    } else if (/Windows/.test(userAgent)) {
        deviceType = 'Windows Desktop';
    } else if (/Mac/.test(userAgent)) {
        deviceType = 'Mac Desktop';
    } else if (/Linux/.test(userAgent)) {
        deviceType = 'Linux Desktop';
    }
    
    return {
        type: deviceType,
        platform: platform,
        language: language,
        userAgent: userAgent.substring(0, 100) + '...'
    };
}

// Auto-fill device info on registration
document.addEventListener('DOMContentLoaded', function() {
    const deviceInfoInput = document.getElementById('device_info');
    if (deviceInfoInput && !deviceInfoInput.value) {
        const deviceInfo = getDeviceInfo();
        deviceInfoInput.value = `${deviceInfo.type} - ${deviceInfo.platform}`;
    }
});

// Form enhancement utilities
function enhanceForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    // Add real-time validation
    const inputs = form.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#e1e5e9';
            }
        });
        
        input.addEventListener('input', function() {
            if (this.style.borderColor === 'rgb(220, 53, 69)') {
                this.style.borderColor = '#e1e5e9';
            }
        });
    });
}

// Initialize form enhancements
document.addEventListener('DOMContentLoaded', function() {
    enhanceForm('registerForm');
    enhanceForm('loginForm');
    enhanceForm('generateQrForm');
    enhanceForm('verifyQrForm');
});

// Export utilities for use in other scripts
window.QRUtils = {
    showNotification,
    validateForm,
    apiCall,
    displayQRCode,
    displayVerificationResult,
    displayBlockchainStatus,
    getDeviceInfo,
    generateHash
};
