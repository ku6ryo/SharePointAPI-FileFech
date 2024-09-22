import os
import msal
from flask import Flask, session, redirect, url_for, request, render_template
from msgraph_core import GraphClientFactory
import os
from dotenv import load_dotenv
load_dotenv()

AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')

# Configurations from Azure AD App Registration
AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
REDIRECT_PATH = "/azure_callback"
SCOPES = ["User.Read Sites.Read.All offline_access"]
LOGOUT_URL = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/logout"

# Flask app
app = Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(24)  # Secret key for Flask session

# MSAL ConfidentialClientApplication to acquire token
def _build_msal_app():
    return msal.ConfidentialClientApplication(
        AZURE_CLIENT_ID, authority=AUTHORITY, client_credential=AZURE_CLIENT_SECRET
    )

def _get_token_from_cache():
    accounts = _build_msal_app().get_accounts()
    if accounts:
        result = _build_msal_app().acquire_token_silent(SCOPES, account=accounts[0])
        return result

@app.route('/')
async def index():
    token = session.get('token')

    if token is not None:
        # Initialize Graph client
        client = GraphClientFactory().get_default_client()
        headers = {'Authorization': f'Bearer {token}'}
        user_response = await client.get("https://graph.microsoft.com/v1.0/me", headers=headers)
        profile = user_response.json()

    return render_template(
        'index.html',
        logged_in=token is not None,
        profile=profile if token is not None else None,
        token=token,
        refresh_token=session.get('refresh_token'),
    )

@app.route('/login')
def login():
    # Start the OAuth 2.0 Authorization flow
    auth_url = _build_msal_app().get_authorization_request_url(
        SCOPES,
        redirect_uri=url_for('authorized', _external=True)
    )
    return redirect(auth_url)

@app.route(REDIRECT_PATH)
def authorized():
    # Extract authorization code from the query string
    code = request.args.get('code')
    if code:
        result = _build_msal_app().acquire_token_by_authorization_code(
            code,
            scopes=SCOPES,
            redirect_uri=url_for('authorized', _external=True)
        )
        session['token'] = result.get('access_token')
        session['refresh_token'] = result.get('refresh_token')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(f"{LOGOUT_URL}?post_logout_redirect_uri={url_for('index', _external=True)}")


@app.route('/sites')
async def sites():
    token = session.get('token')
    if not token:
        return redirect(url_for('login'))

    client = GraphClientFactory().get_default_client()
    headers = {'Authorization': f'Bearer {token}'}
    res = await client.get("https://graph.microsoft.com/v1.0/sites?search=", headers=headers)
    sites = res.json()
    return render_template('sites.html', sites=sites)

@app.route('/sites/<site_id>/drives')
async def drives(site_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('login'))

    client = GraphClientFactory().get_default_client()
    headers = {'Authorization': f'Bearer {token}'}
    res = await client.get(f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives", headers=headers)
    drives = res.json()
    return render_template('drives.html', drives=drives)

@app.route('/sites/<site_id>/drives/<drive_id>')
async def files(site_id, drive_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('login'))

    client = GraphClientFactory().get_default_client()
    headers = {'Authorization': f'Bearer {token}'}
    res = await client.get(f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root/children", headers=headers)
    files = res.json()
    return render_template('files.html', files=files)


if __name__ == '__main__':
    app.run(debug=True, port=5000)