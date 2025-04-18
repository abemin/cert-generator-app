from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
import subprocess
import os
import datetime
import glob
import threading
import time
import zipfile

app = Flask(__name__)
app.secret_key = '5f2e55aa053f2d0f73af9a6a58616ac6'  # Change this secret!

# Hardcoded CA details
CA_CERT = 'ca/ca.crt'
CA_KEY = 'ca/ca.key'
CA_PASSWORD = 'P@ssw0rd' # Your CA pass

# Password to access
ACCESS_PASSWORD = 'Secr3t' # Your Login pass

# Where to store generated files
CERT_FOLDER = 'certs'

if not os.path.exists(CERT_FOLDER):
    os.makedirs(CERT_FOLDER)

# Cleanup thread to delete files older than 1 hour
def cleanup_certs_folder():
    while True:
        now = time.time()
        files = glob.glob(os.path.join(CERT_FOLDER, '*'))
        for f in files:
            if os.stat(f).st_mtime < now - 3600:  # 1 hour = 3600 seconds
                os.remove(f)
        time.sleep(600)  # Check every 10 minutes

# Start cleanup thread
threading.Thread(target=cleanup_certs_folder, daemon=True).start()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ACCESS_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid password")
    return render_template('login.html')

@app.route('/generate', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        common_name = request.form['common_name']
        dns_alt = request.form.get('dns_alt', '')
        ip_alt = request.form.get('ip_alt', '')
        key_algo = request.form.get('key_algo', 'RSA')
        key_size = request.form.get('key_size', '2048')
        validity_days = request.form.get('validity_days', '365')

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename_base = f"{common_name}_{timestamp}"

        key_file = os.path.join(CERT_FOLDER, f"{filename_base}.key")
        csr_file = os.path.join(CERT_FOLDER, f"{filename_base}.csr")
        crt_file = os.path.join(CERT_FOLDER, f"{filename_base}.crt")
        ext_file = os.path.join(CERT_FOLDER, f"{filename_base}.ext")
        zip_file = os.path.join(CERT_FOLDER, f"{filename_base}.zip")

        # 1. Generate private key based on selected algorithm
        if key_algo == 'RSA':
            subprocess.run([
                'openssl', 'genrsa', '-out', key_file, key_size
            ], check=True)
        elif key_algo == 'ECDSA':
            subprocess.run([
                'openssl', 'ecparam', '-genkey', '-name', 'prime256v1', '-out', key_file
            ], check=True)

        # 2. Generate CSR
        subprocess.run([
            'openssl', 'req', '-new', '-key', key_file, '-out', csr_file,
            '-subj', f"/CN={common_name}"
        ], check=True)

        # 3. Create .ext file
        with open(ext_file, 'w') as f:
            f.write("authorityKeyIdentifier=keyid,issuer\n")
            f.write("basicConstraints=CA:FALSE\n")
            f.write("keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment\n")
            f.write("subjectAltName = @alt_names\n\n")
            f.write("[alt_names]\n")
            f.write(f"DNS.1 = {common_name}\n")
            if dns_alt:
                dns_list = dns_alt.split(',')
                for idx, dns in enumerate(dns_list, start=2):
                    f.write(f"DNS.{idx} = {dns.strip()}\n")
            if ip_alt:
                ip_list = ip_alt.split(',')
                for idx, ip in enumerate(ip_list, start=1):
                    f.write(f"IP.{idx} = {ip.strip()}\n")

        # 4. Sign the CSR
        subprocess.run([
            'openssl', 'x509', '-req', '-in', csr_file, '-CA', CA_CERT, '-CAkey', CA_KEY,
            '-CAcreateserial', '-out', crt_file, '-days', validity_days, '-sha256',
            '-extfile', ext_file,
            '-passin', f'pass:{CA_PASSWORD}'
        ], check=True)

        # 5. Create ZIP file including: private key, cert, and CA cert
        with zipfile.ZipFile(zip_file, 'w') as zf:
            zf.write(key_file, arcname=os.path.basename(key_file))
            zf.write(crt_file, arcname=os.path.basename(crt_file))
            zf.write(CA_CERT, arcname='ca.crt')

        return render_template('index.html', zip_file=os.path.basename(zip_file))

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if not filename.endswith('.zip'):
        return "Not allowed", 403
    
    return send_from_directory(CERT_FOLDER, filename, as_attachment=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

