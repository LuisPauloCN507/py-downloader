import yt_dlp
import os

def download(url, mode):
    # Pasta de destino
    output_folder = os.path.expanduser('~/Downloads/Luis_Downloader')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Configurações base
    ydl_opts = {
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'quiet': False,
        'noplaylist': True,
    }

    if mode == '1':
        # MODO MP3 (Áudio + Capa + Metadados)
        print("\n🎵 Configurando para ÁUDIO (MP3)...")
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                {'key': 'FFmpegMetadata', 'add_metadata': True},
                {'key': 'EmbedThumbnail'},
            ],
            'writethumbnail': True,
        })
    else:
        # MODO MP4 (Vídeo de alta qualidade)
        print("\n🎬 Configurando para VÍDEO (MP4)...")
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n✅ Concluído! O ficheiro está em: {output_folder}")
    except Exception as e:
        print(f"❌ Erro ao descarregar: {e}")

if __name__ == "__main__":
    print("="*30)
    print("      LUIS DOWNLOADER v2.5")
    print("="*30)
    
    link = input("🔗 Cola o link do YouTube: ")
    
    print("\nEscolha o formato:")
    print("1 - Apenas Áudio (MP3 + Capa)")
    print("2 - Vídeo Completo (MP4)")
    
    opcao = input("\nDigite 1 ou 2: ")

    if opcao in ['1', '2']:
        download(link, opcao)
    else:
        print("❌ Opção inválida. Tente novamente.")