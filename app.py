import streamlit as st
import pandas as pd
import gspread
import os
import os
import json
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.service_account import ServiceAccountCredentials

# # Google Sheets authentication
# def authenticate_google_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     # creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/credentials.json", scope)
#     # creds = ServiceAccountCredentials.from_json_keyfile_name("/opt/render/secrets/credentials.json", scope)
#     client = gspread.authorize(creds)
#     return client

def authenticate_google_sheets():
    creds_b64 = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
    if not creds_b64:
        raise ValueError("Google Sheets credentials not found. Set GOOGLE_SHEETS_CREDENTIALS env variable.")

    # Decode the Base64 string
    creds_json = base64.b64decode(creds_b64).decode("utf-8")
    creds_dict = json.loads(creds_json)

    # Authenticate with Google Sheets
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    return gspread.authorize(creds)

client = authenticate_google_sheets()

# Save data to Google Sheets
def save_to_google_sheets(df):
    client = authenticate_google_sheets()
    sheet_url = "https://docs.google.com/spreadsheets/d/1rWwyLn_LQ3-nZiIkmg8Iw8141Zt8S1F_nrx4Durxt6E/edit"
    sheet = client.open_by_url(sheet_url).sheet1  # Select first sheet
    data = df.values.tolist()  # Convert DataFrame to list
    sheet.append_rows(data)
    st.success("✅ Data successfully saved to Google Sheets!")

# Load the Excel file
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Reference sheet (1).xlsx")  # Ensure this file exists in the working directory
        return df
    except FileNotFoundError:
        st.error("File 'Reference sheet (1).xlsx' not found! Please check the file path.")
        return None

def main():
    st.title("Excel Data Auto-Populate Form")

    df = load_data()
    if df is None:
        return  # Exit if file not found

    required_columns = ["Site ID", "Maximo Asset ID"]
    if not all(col in df.columns for col in required_columns):
        st.error(f"Excel file must contain columns: {', '.join(required_columns)}")
        return

    with st.form("data_form"):
        col1, col2 = st.columns(2)
        site_id = col1.selectbox("Select Site ID", df["Site ID"].dropna().unique())
        asset_id = col2.selectbox("Select Maximo Asset ID", df["Maximo Asset ID"].dropna().unique())

        # Filter data
        filtered_data = df[(df["Site ID"] == site_id) & (df["Maximo Asset ID"] == asset_id)].copy()

        if filtered_data.empty:
            st.warning("No matching data found.")
        else:
            st.write("Auto-populated Data:")
            st.dataframe(filtered_data)

            # User input for name
            name = st.text_input("Enter your Name")

            # Submit button
            submitted = st.form_submit_button("Submit")
            if submitted:
                if name.strip() == "":
                    st.error("Please enter a valid name.")
                else:
                    filtered_data.loc[:, "Entered Name"] = name  # Ensure modification doesn't trigger warnings
                    save_to_google_sheets(filtered_data)

if __name__ == "__main__":
    main()




# import streamlit as st
# import pandas as pd
# import datetime

# # Load the Excel file
# @st.cache_data
# def load_data():
#     try:
#         df = pd.read_excel("Reference sheet (1).xlsx")  # Ensure this file exists in the working directory
#         return df
#     except FileNotFoundError:
#         st.error("File 'Reference sheet (1).xlsx' not found! Please check the file path.")
#         return None

# # Save to Excel with timestamped filename
# def save_data(df):
#     filename = f"filtered_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
#     df.to_excel(filename, index=False)
#     st.success(f"Data saved as {filename}")

# def main():
#     st.title("Excel Data Auto-Populate Form")

#     df = load_data()
#     if df is None:
#         return  # Exit if file not found

#     required_columns = ["Site ID", "Maximo Asset ID"]
#     if not all(col in df.columns for col in required_columns):
#         st.error(f"Excel file must contain columns: {', '.join(required_columns)}")
#         return

#     with st.form("data_form"):
#         col1, col2 = st.columns(2)
#         site_id = col1.selectbox("Select Site ID", df["Site ID"].dropna().unique())
#         asset_id = col2.selectbox("Select Maximo Asset ID", df["Maximo Asset ID"].dropna().unique())

#         # Filter data
#         filtered_data = df[(df["Site ID"] == site_id) & (df["Maximo Asset ID"] == asset_id)].copy()

#         if filtered_data.empty:
#             st.warning("No matching data found.")
#         else:
#             st.write("Auto-populated Data:")
#             st.dataframe(filtered_data)

#             # User input for name
#             name = st.text_input("Enter your Name")

#             # Submit button
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 if name.strip() == "":
#                     st.error("Please enter a valid name.")
#                 else:
#                     filtered_data.loc[:, "Entered Name"] = name  # Ensure modification doesn't trigger warnings
#                     save_data(filtered_data)

# if __name__ == "__main__":
#     main()


### target

# from authlib.integrations.requests_client import OAuth2Session

# import streamlit as st
# import pandas as pd
# from authlib.integrations.requests_client import OAuth2Session

# # OAuth settings
# CLIENT_ID = "your-client-id"
# CLIENT_SECRET = "your-client-secret"
# AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"
# TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
# REDIRECT_URI = "https://your-app.onrender.com/callback"

# @st.cache_data
# def load_data():
#     try:
#         df = pd.read_excel("Reference sheet (1).xlsx")
#         return df
#     except FileNotFoundError:
#         st.error("File not found! Please check the file path.")
#         return None

# def save_data(df, filename="filtered_data.xlsx"):
#     df.to_excel(filename, index=False)
#     st.success(f"Data saved to {filename}")

# def login():
#     session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
#     auth_url, _ = session.create_authorization_url(AUTHORIZATION_URL, prompt="select_account")
#     st.markdown(f"[Login with Google]({auth_url})")

# def main():
#     st.title("Excel Data Auto-Populate Form")

#     # Authentication
#     if "email" not in st.session_state:
#         login()
#         return
    
#     user_email = st.session_state["email"]
#     if "@target.com" not in user_email:
#         st.error("Access Denied: Only employees with @target.com email can access this form.")
#         return

#     df = load_data()
#     if df is None:
#         return

#     required_columns = ["Site ID", "Maximo Asset ID"]
#     if not all(col in df.columns for col in required_columns):
#         st.error(f"Excel file must contain columns: {', '.join(required_columns)}")
#         return

#     with st.form("data_form"):
#         col1, col2 = st.columns(2)
#         site_id = col1.selectbox("Select Site ID", df["Site ID"].dropna().unique())
#         asset_id = col2.selectbox("Select Maximo Asset ID", df["Maximo Asset ID"].dropna().unique())

#         filtered_data = df[(df["Site ID"] == site_id) & (df["Maximo Asset ID"] == asset_id)]

#         if filtered_data.empty:
#             st.warning("No matching data found.")
#         else:
#             st.write("Auto-populated Data:")
#             st.dataframe(filtered_data)

#             name = st.text_input("Enter your Name")
#             submitted = st.form_submit_button("Submit")

#             if submitted:
#                 if name.strip() == "":
#                     st.error("Please enter a valid name.")
#                 else:
#                     filtered_data["Entered Name"] = name
#                     save_data(filtered_data)

# if __name__ == "__main__":
#     main()


# microsoft





# import streamlit as st
# import pandas as pd
# from authlib.integrations.requests_client import OAuth2Session

# # Microsoft OAuth Settings
# CLIENT_ID = "your-client-id"
# CLIENT_SECRET = "your-client-secret"
# TENANT_ID = "your-tenant-id"

# AUTHORIZATION_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
# TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
# REDIRECT_URI = "https://your-app.onrender.com/callback"

# @st.cache_data
# def load_data():
#     try:
#         df = pd.read_excel("Reference sheet (1).xlsx")
#         return df
#     except FileNotFoundError:
#         st.error("File not found! Please check the file path.")
#         return None

# def save_data(df, filename="filtered_data.xlsx"):
#     df.to_excel(filename, index=False)
#     st.success(f"Data saved to {filename}")

# def login():
#     session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
#     auth_url, _ = session.create_authorization_url(AUTHORIZATION_URL, scope="openid email profile")
#     st.markdown(f"[Login with Microsoft]({auth_url})")

# def main():
#     st.title("Excel Data Auto-Populate Form")

#     # Authentication
#     if "email" not in st.session_state:
#         login()
#         return
    
#     user_email = st.session_state["email"]
#     if "@target.com" not in user_email:
#         st.error("Access Denied: Only employees with @target.com email can access this form.")
#         return

#     df = load_data()
#     if df is None:
#         return

#     required_columns = ["Site ID", "Maximo Asset ID"]
#     if not all(col in df.columns for col in required_columns):
#         st.error(f"Excel file must contain columns: {', '.join(required_columns)}")
#         return

#     with st.form("data_form"):
#         col1, col2 = st.columns(2)
#         site_id = col1.selectbox("Select Site ID", df["Site ID"].dropna().unique())
#         asset_id = col2.selectbox("Select Maximo Asset ID", df["Maximo Asset ID"].dropna().unique())

#         filtered_data = df[(df["Site ID"] == site_id) & (df["Maximo Asset ID"] == asset_id)]

#         if filtered_data.empty:
#             st.warning("No matching data found.")
#         else:
#             st.write("Auto-populated Data:")
#             st.dataframe(filtered_data)

#             name = st.text_input("Enter your Name")
#             submitted = st.form_submit_button("Submit")

#             if submitted:
#                 if name.strip() == "":
#                     st.error("Please enter a valid name.")
#                 else:
#                     filtered_data["Entered Name"] = name
#                     save_data(filtered_data)

# if __name__ == "__main__":
#     main()




#### gmail




# import streamlit as st
# import pandas as pd
# from authlib.integrations.requests_client import OAuth2Session

# # OAuth settings
# CLIENT_ID = "your-client-id"
# CLIENT_SECRET = "your-client-secret"
# AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"
# TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
# REDIRECT_URI = "https://your-app.onrender.com/callback"

# @st.cache_data
# def load_data():
#     try:
#         df = pd.read_excel("Reference sheet (1).xlsx")
#         return df
#     except FileNotFoundError:
#         st.error("File not found! Please check the file path.")
#         return None

# def save_data(df, filename="filtered_data.xlsx"):
#     df.to_excel(filename, index=False)
#     st.success(f"Data saved to {filename}")

# def login():
#     session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
#     auth_url, _ = session.create_authorization_url(AUTHORIZATION_URL, prompt="select_account")
#     st.markdown(f"[Login with Google]({auth_url})")

# def main():
#     st.title("Excel Data Auto-Populate Form")

#     # Authentication
#     if "email" not in st.session_state:
#         login()
#         return
    
#     user_email = st.session_state["email"]
#     if "@gmail.com" not in user_email:
#         st.error("Access Denied: Only users with @gmail.com email can access this form.")
#         return

#     df = load_data()
#     if df is None:
#         return

#     required_columns = ["Site ID", "Maximo Asset ID"]
#     if not all(col in df.columns for col in required_columns):
#         st.error(f"Excel file must contain columns: {', '.join(required_columns)}")
#         return

#     with st.form("data_form"):
#         col1, col2 = st.columns(2)
#         site_id = col1.selectbox("Select Site ID", df["Site ID"].dropna().unique())
#         asset_id = col2.selectbox("Select Maximo Asset ID", df["Maximo Asset ID"].dropna().unique())

#         filtered_data = df[(df["Site ID"] == site_id) & (df["Maximo Asset ID"] == asset_id)]

#         if filtered_data.empty:
#             st.warning("No matching data found.")
#         else:
#             st.write("Auto-populated Data:")
#             st.dataframe(filtered_data)

#             name = st.text_input("Enter your Name")
#             submitted = st.form_submit_button("Submit")

#             if submitted:
#                 if name.strip() == "":
#                     st.error("Please enter a valid name.")
#                 else:
#                     filtered_data["Entered Name"] = name
#                     save_data(filtered_data)

# if __name__ == "__main__":
#     main()
