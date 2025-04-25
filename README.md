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
```
cert_web/
├── app.py                  # Flask backend
├── ca/                      # Place your ca.crt and ca.key here
│   ├── ca.crt
│   └── ca.key
├── certs/                   # Generated certs and keys (auto cleaned)
├── templates/               # HTML templates (Bootstrap styled)
│   ├── index.html
│   └── login.html
├── Dockerfile               # Docker build file
├── docker-compose.yml       # Docker Compose for easy deployment
└── .gitignore               # Git ignore rules
```

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

1. Clone the repository
```bash
git clone https://github.com/abemin/cert-generator-app.git
cd cert-generator-app
```
2. Prepare your CA Files
Inside the ca/ directory, add:

ca.crt — Your CA public certificate

ca.key — Your CA private key

⚠️ Important: Never upload your ca.key to public repositories!

3. Build and Run using Docker Compose
```bash
docker compose up --build
```
or to run as daemon
```bash
docker compose up -d --build
```
The app will be available at:
👉 http://your-server-ip:5000

Login with the configured password.

### ⚙️ Environment Settings
Default Login Password is hardcoded in app.py

Default CA Password is hardcoded in app.py

(Coming soon: Docker secrets support!)

### 📄 Notes
🛡 Install the ca.crt on your client machines to trust the certificates generated here.

📜 Files generated will auto-delete after 1 hour for security.

🐳 Designed for Docker deployment but can also run locally with Python3 + Flask.

### 📋 To Do (Future Ideas)
Use Docker Secrets to pass CA password

Admin panel to list active certs

HTTPS support for the app itself

Let user choose Subject fields (O, OU, L, ST, C)

### 🧑‍💻 Author
Muhaimi Fatihi 🚀

### 📜 License
This project is for educational and internal/private use.
Not recommended for production public CA without enhancements.
