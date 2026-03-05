from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

# --- SETTINGS ---
NOPECHA_KEY = "sub_1StYahCRwBwvt6ptBncTYxOF"  # Apni NopeCHA API Key yahan dalein
IVASMS_LOGIN_URL = "https://www.ivasms.com/portal/login"
# IVASMS ki SiteKey source code se nikaal kar yahan likhein
SITE_KEY = "6Lxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 

@app.route('/')
def home():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/login', methods=['POST'])
def process_login():
    email = request.form.get('email')
    password = request.form.get('password')

    print(f"Login attempt for: {email}")
    print("Requesting NopeCHA to solve captcha...")

    # Step 1: Solve Captcha via NopeCHA
    solve_url = f"https://api.nopecha.com/?key={NOPECHA_KEY}&type=recaptcha2&sitekey={SITE_KEY}&url={IVASMS_LOGIN_URL}"
    
    try:
        response = requests.get(solve_url).json()
        if response.get('data'):
            token = response['data']
            print("Captcha Solved Successfully!")

            # Step 2: Send Login Data to IVASMS
            payload = {
                "email": email,
                "password": password,
                "g-recaptcha-response": token
            }
            # Note: Ivasms ke asli login parameters (name fields) check kar lena
            final_res = requests.post(IVASMS_LOGIN_URL, data=payload)
            
            return f"<h3>Processing Done!</h3><p>Captcha Token: {token[:30]}...</p><p>Check IVASMS Response.</p>"
        else:
            return "Captcha Solving Failed. Check your NopeCHA balance/Key."

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(port=8080)
