

# %%
import os
import requests
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()  # Load environment variables


# %%
app = Flask(__name__)
app.secret_key = "560aab60-11fc-455d-9b12-d642c68f5f25"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Microsoft Graph API Credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = "http://localhost:5000/callback"

AUTH_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
UPLOAD_URL = "https://graph.microsoft.com/v1.0/me/drive/root:/Uploads/"

# Function to get access token
def get_access_token():
    data = {
        "client_id": CLIENT_ID,
        "scope": "Files.ReadWrite",
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    response = requests.post(AUTH_URL, data=data)
    return response.json().get("access_token")

# Upload File to OneDrive
def upload_to_onedrive(file_path, filename):
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/octet-stream"}
    with open(file_path, "rb") as file_data:
        response = requests.put(UPLOAD_URL + filename + ":/content", headers=headers, data=file_data)
    return response.json()

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            # Upload to OneDrive
            response = upload_to_onedrive(file_path, filename)
            flash(f"File uploaded to OneDrive: {response.get('@microsoft.graph.downloadUrl', 'Unknown')}")
            return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
