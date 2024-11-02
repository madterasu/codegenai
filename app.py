import streamlit as st
import ollama
import torch

# Konfigurasi halaman Streamlit (Harus di bagian paling atas setelah import)
st.set_page_config(page_title="CodeGen AI", page_icon="🤖", layout="centered")

# Cek status koneksi Ollama dan inisialisasi model
try:
    models = [model["name"] for model in ollama.list()["models"]]
    ollama_offline = False
except Exception:
    models = []
    ollama_offline = True

# CSS untuk gaya tambahan
st.markdown(
    """
    <style>
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .online {
        background-color: #28a745;
    }
    .offline {
        background-color: #dc3545;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Judul aplikasi
st.title("🤖 CodeGen AI")
st.markdown(":red-background[***AI Assistant*** untuk Pengkodean Tanpa Hambatan] | © INFORMATIKA UMSIDA 2024")

# Menampilkan indikator status koneksi
status_text = "Ollama Online" if not ollama_offline else "Ollama Offline"
status_class = "online" if not ollama_offline else "offline"
st.markdown(f'<div class="status-indicator {status_class}"></div><span>{status_text}</span>', unsafe_allow_html=True)

# Pilihan model (jika tersedia)
if not ollama_offline:
    model = st.selectbox("Pilih Model:", models)
else:
    st.warning("Model tidak tersedia. Periksa koneksi ke Ollama.")

# Area input teks untuk prompt
prompt_input = st.text_area("Masukkan prompt Anda di sini:", height=150, placeholder="Ketik prompt...")

# Tombol untuk mengirim prompt
if st.button("Generate") and not ollama_offline:
    if not prompt_input.strip():
        st.warning("Prompt tidak boleh kosong. Silakan masukkan prompt.")
    else:
        # Menampilkan spinner saat pemrosesan berlangsung
        with st.spinner("Model sedang memproses..."):
            try:
                # Panggilan ke Ollama untuk chat
                response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt_input}])
                
                # Pastikan response berupa dictionary, akses konten teks
                response_text = response.get("message", {}).get("content", "").strip()

                # Menampilkan respons sebagai kode
                if response_text:
                    st.subheader("Respons Kode:")
                    st.markdown(response_text)
                else:
                    st.warning("Tidak ada konten yang diterima dari model.")

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
