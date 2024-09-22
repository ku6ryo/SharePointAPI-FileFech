This is a demo web app for getting files uploaded to SharePoint sites.

This app is using [flask](https://flask.palletsprojects.com/en/3.0.x/), [msal](https://github.com/AzureAD/microsoft-authentication-library-for-python), [msgraph-core](https://github.com/microsoftgraph/msgraph-sdk-python/blob/main/UPGRADING.md).

# How to run the server
Please make a copy of `.env.sample` and name it `.env`. Sets the environment variables in the file.

```
pip install -r requirements.txt
python -m server
```