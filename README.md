# 🏀 Asistente Táctico Automático (Básquetbol Formativas)

Aplicación construida con **Streamlit** y **LangChain RAG** para procesar automáticamente una carpeta de Google Drive llena de PDFs de ejercicios y generar planificaciones estructuradas utilizando la inteligencia artificial de Google Gemini.

## 🚀 Despliegue en Streamlit Cloud

1. Sube estos archivos (`app.py`, `requirements.txt` y este `README.md`) a tu repositorio de GitHub.
2. Ingresa a [share.streamlit.io](https://share.streamlit.io/) y crea una nueva aplicación enlazándola a tu repositorio.
3. Para conectar con Google Drive de manera segura, debes crear una **Cuenta de Servicio de Google Cloud (Service Account)**.
4. Genera una nueva clave en formato JSON para tu cuenta de servicio.
5. Copia el correo electrónico de la cuenta de servicio (ej: `app-basquet@tu-proyecto.iam.gserviceaccount.com`) y **compártele tu carpeta de Google Drive** (dándole permisos de Lector).
6. En el panel de configuración de tu app en Streamlit Cloud, ve a la sección **Secrets** e ingresa el contenido de tu archivo JSON de la siguiente forma:

```toml
[gcp_service_account]
type = "service_account"
project_id = "tu-proyecto-id"
private_key_id = "xxxxx"
private_key = "-----BEGIN PRIVATE KEY-----\n..."
client_email = "cuenta@tu-proyecto.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

## 🛠 Uso de la Aplicación
- Ingresa a la URL generada por Streamlit Cloud.
- En el menú lateral, coloca tu API Key de Google Gemini.
- Presiona "Sincronizar con Google Drive" para que la IA descargue y procese tus PDFs.
- Una vez cargados en la base de datos (ChromaDB), realiza tu consulta en la pantalla principal (Ej. *"Genera 3 ejercicios de balance defensivo para U15"*).
