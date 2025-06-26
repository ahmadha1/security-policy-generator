#!/usr/bin/env python3
"""
SSL Certificate Generator for Security Policy Generator
Generates self-signed SSL certificates for HTTPS support
"""

import os
import sys
import ipaddress
from datetime import datetime, timedelta

def generate_ssl_certificates():
    """Generate self-signed SSL certificates for HTTPS"""
    
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
    except ImportError:
        print("Installing cryptography library...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "cryptography"])
        print("Please run this script again after installation.")
        return False
    
    # Create SSL directory
    ssl_dir = 'ssl'
    os.makedirs(ssl_dir, exist_ok=True)
    
    cert_file = os.path.join(ssl_dir, 'cert.pem')
    key_file = os.path.join(ssl_dir, 'key.pem')
    
    print("Generating self-signed SSL certificates...")
    
    try:
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Generate certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Security Policy Generator"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Write certificate and private key to files
        with open(cert_file, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open(key_file, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print(f"✅ SSL certificates generated successfully!")
        print(f"   Certificate: {cert_file}")
        print(f"   Private Key: {key_file}")
        print(f"   Valid until: {(datetime.utcnow() + timedelta(days=365)).strftime('%Y-%m-%d')}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating SSL certificates: {e}")
        return False

if __name__ == "__main__":
    success = generate_ssl_certificates()
    if success:
        print("\n🚀 You can now run the app with HTTPS!")
        print("   python app.py")
    else:
        print("\n❌ Failed to generate SSL certificates.")
        sys.exit(1) 