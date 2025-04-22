import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.markdown(
    '<style>'
    'body {background-color: #fce6fb;}'
    '.main {background-color: #fce6fb; text-align: center;}'
    'h1, .stApp h1 {color: #8a2be2 !important; text-align: center;}'
    'h2, h3, .stApp h2 {color: #8a2be2 !important; text-align: center;}'
    '.stButton>button {background-color: #8a2be2; color: white; border: none; border-radius: 8px; padding: 0.5em 1em; font-weight: bold;}'
    '.stTextArea textarea, .stSelectbox div[data-baseweb="select"] {color: #ffb3ec !important;}'
    '.custom-text {color: #ffb3ec; text-align: center; font-size: 16px;}'
    '</style>',
    unsafe_allow_html=True
)

st.title("Conversión de Texto a Audio")

image = Image.open('cuervito.png')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Esrcibe y/o pega un texto para poder escucharlo.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Sobre cuervos...")

st.markdown(
    '<p style="color:#a974d1; text-align:center; font-size:16px;">'
    'El cuervo voló durante días buscando el árbol más alto del mundo. Quería ver el fin del cielo. '
    'Al encontrarlo, se posó en la rama más alta y miró hacia arriba, pero todo seguía igual: azul, infinito, sin final. '
    'Entonces pensó que tal vez el cielo era él mismo, y en su orgullo, soltó un graznido tan fuerte que se cayó del susto.'
    '</p>'
    '<p style="color:#a974d1; text-align:center; font-size:16px;">'
    '¿Quieres escucharlo? Copia el texto'
    '</p>',
    unsafe_allow_html=True
)

text = st.text_area("Ingrese El texto a escuchar.")

tld = 'com'
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English"))
lg = 'es' if option_lang == "Español" else 'en'

def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("convertir a Audio"):
    result, output_text = text_to_speech(text, 'com', lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## Tú audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href
    st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio File"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
