# Certificate Generator Web App

A lightweight web application to generate self-signed certificates quickly.

- Supports RSA and ECDSA keys
- Custom Common Name (CN), SANs (DNS/IP)
- Validity period configuration
- Secure login page
- Auto-cleans generated certs after 1 hour
- Full Docker support for easy deployment

---
## 📦 Project Structure

cert_web/ ├── app.py # Flask backend ├── ca/ # Place your ca.crt and ca.key here │ ├── ca.crt │ └── ca.key ├── certs/ # Generated certs and keys (auto cleaned) ├── templates/ # HTML templates (Bootstrap styled) │ ├── index.html │ └── login.html ├── Dockerfile # Docker build file ├── docker-compose.yml # Docker Compose for easy deployment └── .gitignore # Git ignore rules


---

## 🚀 Features

- 🔐 **User Login** to access the generator
- 🛠 **RSA or ECDSA Key** generation
- 📜 **Certificate Signing Request** and **Certificate Signing**
- 📦 **ZIP** download containing Private Key, Signed Certificate, and CA Certificate
- 🧹 **Auto-delete** old files after 1 hour
- 🖌 **Modern Bootstrap UI**

---

## 🔥 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/cert-generator-app.git
cd cert-generator-app

### 2. Prepare your CA Files
Inside the ca/ directory, add:

ca.crt — Your CA public certificate

ca.key — Your CA private key

⚠️ Important: Never upload your ca.key to public repositories!

3. Build and Run using Docker Compose

docker-compose up --build

The app will be available at:
👉 http://your-server-ip:5000

Login with the configured password.
