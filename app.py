import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Configuración de credenciales
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "alumnasdanza",
    "private_key_id": "cf2cb4afae8957968edc2240a2558203df1e3694",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCzO9V5pt0L92iG\nCxacw6GtC84xbWmyw7cAfmfZ2+hlgGDSI+W625ruImnSuQ0ajFVsu9/AfafzNU/7\nq/1cYo5QjDJMRi4hH9YvX4QFHZw4D2GsKxIdQK91y74H9qgL0n3GTXEkj/QRvWEP\nw4hxisUB28FioEcctqhS61IM7GhCIXNvaXnxtXIOA0TPIH9oHvuf6VVs0reOuUII\n/qS+x8mcAUZexEaVujOHU5SpwHVfp0Lj28lhnHpNbXtjMU86GJpKn9GIzU6/WDR8\ntASQeskyPDWutfwAwZkYE3PzFVtfcfFN+JkIzJ3DrNRADi0IfV0LOXUMLQOKO3ZV\npErV/JgVAgMBAAECggEACs+UG8dd0+fzbQpkLcZ7DQYGROL1mivF8Qiu2Owzw1OQ\nA3zY0YGHgc+flG9HBA/s4ycd4u1xYPEZRvPjz1u+e8tJCWK+S48xCyB2xRw5HQSI\nfqsGZ69MJg3JA4/0KOpkXb60EWGBdkR3A01nAHo/UdJggsNqJqg51O6Ov2rPCxYB\ni2w/rztp/1qLWHaWvI8fevJUBWOKuPL44M9xUvy4jhL167ZYiNoXz77Sp1xICzDR\nTT2M9nJqoZueD3Q43y0Zzg3PB8LgWX1dzPGRTvckO3QZB7/h3qM/LCDppmpgjWY+\nkx8e10kqhAlHQXekEUvcpPEL+7pmgbDZbTGlaX2l4QKBgQDlBOC6/DznTcpOnvI+\nwHbnJBzixD0sCA8BGdCk+IzSs5f9xbm/EVTXGGffQlUXLZ23UUFP6Gbk3xRkQNf7\njYKGrvZTeWtdKrL72H4lVf5afNnsdc8BTpWtkKfo4dzZ21pB0st09VVsZfFRih+D\nEcAxrfYxf/3aTk6tYb9AT9vjjQKBgQDIWXNeLMU0PsuJADJy9u7cdfuH+7NkghY4\nqLLx0qlYxmDdcIxb65WQpBz3QQU2ubhuwBM9kdvR6osbd/HRWW9ZzIRQbnUrpcK7\nwyRvWg9tT100DiprimabElOpKOvlU7qwwK8/giQ/Nj3a/w3YE+LMobwtafcxQi8H\nHtOUx5jgqQKBgC8uyBX97ZZB4pI8EPB4uoZ4XDMj9u5hYqX5aZDzXB/0vDWeTNxe\nd7ow3wWSJvG1hi7EYM5TtQ8mHo9hBJ5g0yloVntwInx5VZKpUaPjiZme607aHqHI\nTPILQWyrS9LebEPvZ9dazBSfFA6WhFN+jrgtfPFJy0T0qSTzZHGdglHpAoGBAIGk\noGrIPbPZDovQfNS3xUkTb3hG/4aCRy7SuziQQNUZSYUBV1ID1/yItdWpVV5cP2Qr\nFkg5Ii1rwCg+LVRyswNAvD3vvBJKaQBm/iSv+luZh44vvHNqU4r1CP3lZQA4dg36\nIWzPIfVlfBFCCgtQkuonnkUk1LgjQ5sv72nO3rZBAoGBAJJM2CjpLVfhmgTDjOKI\nt5ro0sXHLlkjR0L65tICO4K2NGQlmXTJeydTfxPrQ3/61QQvk3gJ1pMZmAEk+1hp\nq91Nw/DCRv7vGWtOZH7QrBK2gs9780JztHthqhfhEgTqE/ECJ4cAuMIz14WY9B0h\n0P4cD9u4fS4QgJgMPHAwAb8e\n-----END PRIVATE KEY-----\n",
    "client_email": "streamlit-alumnas@alumnasdanza.iam.gserviceaccount.com",
    "client_id": "104985675305361994763",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/streamlit-alumnas%40alumnasdanza.iam.gserviceaccount.com"
}

# Conectar a Google Sheets
credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPE)
gc = gspread.authorize(credentials)

# Abrir Google Sheet por URL
spreadsheet_url = "https://docs.google.com/spreadsheets/d/154ueaF5pT7lDqk8ECO9I8r_6ZNOhXFWLodYaeZNjP00/edit#gid=0"
sh = gc.open_by_url(spreadsheet_url)

# Seleccionar primera hoja
worksheet = sh.get_worksheet(0)

# Cargar datos en DataFrame
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Mostrar en Streamlit
st.title("Datos de Alumnas")
st.dataframe(df)
