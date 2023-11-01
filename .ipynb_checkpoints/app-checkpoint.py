import streamlit as st

import requests
import csv
from io import StringIO

def load_dictionary_from_csv(file_path):
    dictionary = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            lampung_word = row[0]
            indonesian_translations = row[1].split(',')
            dictionary[lampung_word] = indonesian_translations
    return dictionary

def load_dictionary_from_url(url):
    response = requests.get(url)
    data = response.text
    csvfile = StringIO(data)
    dictionary = {}
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        lampung_word = row[0]
        indonesian_translations = row[1].split(',')
        dictionary[lampung_word] = indonesian_translations
    return dictionary

def check_missing_words(text, dictionary):
    words = text.split()
    missing_words = []
    for word in words:
        if word not in dictionary:
            missing_words.append(word)
    return missing_words

# Fungsi untuk menerjemahkan teks dari bahasa Lampung ke bahasa Indonesia
def translate_indonesia_to_lampung(text, dictionary):
    words = text.split()
    translated_words = []
    for word in words:
        possible_translations = dictionary.get(word, [word])  # Gunakan kata asli jika tidak ditemukan di kamus
        best_translation = min(possible_translations, key=len)  # Pilih terjemahan terpendek
        translated_words.append(best_translation)
    translated_text = ' '.join(translated_words)
    return translated_text

# Fungsi untuk menerjemahkan teks dari bahasa Indonesia ke bahasa Lampung
def translate_lampung_to_indonesia(text, dictionary):
    words = text.split()
    translated_words = []
    for word in words:
        lampung_word = None
        for key, translations in dictionary.items():
            if word in translations:
                lampung_word = key
                break
        translated_words.append(lampung_word if lampung_word else word)
    translated_text = ' '.join(translated_words)
    return translated_text

# Memuat kamus dari URL berkas CSV
csv_url = 'https://huggingface.co/datasets/mabzak/kamus-daerah-indo/raw/main/KamusLampungIndonesia.csv'
dictionary = load_dictionary_from_url(csv_url)



# Konfigurasi tema kustom
st.markdown(
    """
    <style>
        body {
            background-color: #eeeeee;  /* Ganti dengan warna latar belakang yang Anda inginkan */
            color: #ccc;  /* Ganti dengan warna teks yang Anda inginkan */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Judul dan deskripsi
st.title("Penerjemah Indonesia - Lampung")
st.write("Penerjemahan belum sempurna, saya hanya menggunakan data kamus bahasa lampung untuk mengubah kata bahasa indonesia ke lampung, kata yang di terjemahkan mungkin belum lengkap'.")
st.write("Masukkan teks dalam bahasa Indonesia di bawah dan klik tombol 'Terjemahkan'.")

# Sidebar untuk tombol navigasi
menu_selection = st.sidebar.radio("Pilih Arah Terjemahan", ("Indonesia ke Lampung","Lampung ke Indonesia"))

# Widget untuk memasukkan teks
input_text = st.text_area("Masukkan Teks", "")

# Tombol untuk memicu penerjemahan
if st.button("Terjemahkan"):
    if input_text:
        if menu_selection == "Lampung ke Indonesia":
            translated_text = translate_lampung_to_indonesia(input_text, dictionary)
        elif menu_selection == "Indonesia ke Lampung":
            translated_text = translate_indonesia_to_lampung(input_text, dictionary)
        st.write("Hasil Terjemahan:")
        st.write(translated_text)
    else:
        st.write("Silakan masukkan teks terlebih dahulu.")