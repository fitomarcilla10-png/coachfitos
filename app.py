import streamlit as st
import tempfile
import os
import io
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="Biblioteca Maestra de Básquet", layout="wide")
st.title("🏀 Asistente Táctico Automático")

# Configuración y credenciales
FOLDER_ID = "10I4H2BpLHM5msIDwWs21ZDE76JxLjHdM"
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    """Autentica y crea el servicio de Google Drive usando los Secrets de Streamlit."""
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def fetch_pdfs_from_drive(service, folder_id):
    """Obtiene la lista de PDFs y los descarga a archivos temporales."""
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/pdf'",
        pageSize=100, fields="nextPageToken, files(id, name)"
    ).execute()
    
    items = results.get('files', [])
    temp_files = []
    
    progress_text = "Descargando archivos desde Drive..."
    bar = st.progress(0, text=progress_text)
    
    for i, item in enumerate(items):
        request = service.files().get_media(fileId=item['id'])
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            
        # Guardar en temporal para que PyPDFLoader pueda leerlo
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file.write(fh.getvalue())
        temp_file.close()
        temp_files.append((item['name'], temp_file.name))
        
        bar.progress((i + 1) / len(items), text=f"Descargado: {item['name']}")
        
    bar.empty()
    return temp_files

with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("Ingresa tu Google Gemini API Key", type="password")
    sync_button = st.button("Sincronizar con Google Drive")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if sync_button and api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    
    try:
        drive_service = get_drive_service()
        st.info("Conectado a Google Drive. Buscando manuales...")
        
        pdf_files = fetch_pdfs_from_drive(drive_service, FOLDER_ID)
        
        if not pdf_files:
            st.warning("No se encontraron PDFs en la carpeta.")
        else:
            with st.spinner("Procesando e indexando tácticas..."):
                all_docs = []
                for name, path in pdf_files:
                    loader = PyPDFLoader(path)
                    all_docs.extend(loader.load())
                    os.remove(path) # Limpiamos el temporal
                
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                splits = text_splitter.split_documents(all_docs)
                
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                vector_store = Chroma.from_documents(documents=splits, embedding=embeddings)
                
                st.session_state.vector_store = vector_store
                st.success(f"¡{len(pdf_files)} manuales sincronizados y listos!")
                
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")

# Área principal de chat/consultas
st.markdown("### 📋 Generador de Planificaciones")
user_query = st.text_area("¿Qué necesitas planificar hoy? (Ej. Ejercicios de transición para U15)")

if st.button("Generar Respuesta"):
    if not api_key:
        st.error("Ingresa la API Key de Gemini.")
    elif st.session_state.vector_store is None:
        st.error("Primero debes sincronizar con Drive.")
    elif user_query:
        os.environ["GOOGLE_API_KEY"] = api_key
        
        with st.spinner("Analizando la biblioteca..."):
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
            
            system_prompt = (
                "Eres un Director Deportivo experto en formativas (U11 a U17). "
                "Usa SOLO el siguiente contexto para responder. "
                "Presenta siempre ejercicios con formato Ficha Técnica."
                "\n\n{context}"
            )
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])
            
            retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 5})
            rag_chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))
            
            response = rag_chain.invoke({"input": user_query})
            st.write(response["answer"])
