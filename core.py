import yt_dlp
import os

def baixar_musica_completa(url):
    # Pasta organizada
    output_folder = os.path.expanduser('~/Downloads/Musicas_Luis')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'postprocessors': [
            {
                # Extrai o áudio e convertelo para MP3
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                # Adiciona metadados (Artista, Título, Álbum se disponível)
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            },
            {
                # Embutir a imagem da capa no arquivo MP3
                'key': 'EmbedThumbnail',
            }
        ],
        'writethumbnail': True, # Baixa a imagem da capa
        'quiet': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"🚀 Buscando dados e baixando...")
            ydl.download([url])
            print(f"\n✅ Sucesso! Sua música está em: {output_folder}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("--- LUIS MUSIC DOWNLOADER v2.0 ---")
    link = input("🔗 Cole o link do YouTube (Musica Individual): ")
    baixar_musica_completa(link)