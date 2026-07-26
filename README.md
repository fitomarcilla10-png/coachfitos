# 🏀 Asistente Táctico Automático

## 🚀 Instrucciones para resolver el error "st.secrets has no key"

El error ocurre porque la aplicación necesita el archivo `secrets.toml` con las credenciales de Google Drive. He preparado toda la estructura para que funcione.

### Si trabajas en tu computadora (Local)
1. Descomprime este archivo ZIP.
2. Verás que hay una carpeta oculta llamada `.streamlit`. Adentro está el archivo `secrets.toml`.
3. Abre `secrets.toml` y **pega tus verdaderas credenciales** allí.
4. Ejecuta `streamlit run app.py`.

### Si estás en Streamlit Cloud
1. Sube `app.py` y `requirements.txt` a GitHub.
2. Abre el archivo `secrets.toml` que viene en este ZIP.
3. Copia todo su contenido y pégalo en la sección **"Secrets"** de la configuración de tu app en Streamlit Cloud (Settings > Secrets).
4. Modifica los valores con tus credenciales reales y dale a Save.