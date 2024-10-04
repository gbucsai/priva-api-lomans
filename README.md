# priva-api-lomans
Priva API Python client example for Lomans.

## Synopsis
The `priva.py` file contains a reusable class that can be used to get historical Priva data from any site/meter combo.

## Usage
1. Create a Python virtual environment, activate it, and install the dependencies:
```bash
python.exe -m venv .\venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
2. Create a file called .env in the project root and set the following contents (this file is ignored by git):
```env
TENANT_ID=replace_this_with_actual_id
CLIENT_ID=replace_this_with_actual_id
CLIENT_SECRET=replace_this_with_actual_secret
```
3. Run the script which will return partial responses for examination:
```bash
python.exe .\priva.py
```

## What's next
You can parameterize and modify the script as needed, put it in scheduled tasks or behind API endpoints, and add functions to process and write the data to databases and similar.