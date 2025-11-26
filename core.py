import yt_dlp
import os

def download_video(url, tipo='video'):
    # Define a pasta de downloads
    output_path = 'downloads'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Configurações do yt-dlp
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s', # Nome do arquivo
        'progress_hooks': [hook_progresso], # Função para mostrar progresso
    }

    if tipo == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("\n✅ Download concluído com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro ao baixar: {e}")

# Função auxiliar para mostrar a barra de porcentagem
def hook_progresso(d):
    if d['status'] == 'downloading':
        porcentagem = d.get('_percent_str', '0%')
        print(f"Baixando: {porcentagem}", end='\r')

# --- TESTE MANUAL (Só roda se executar esse arquivo direto) ---
if __name__ == "__main__":
    link = input("Cole o link do YouTube: ")
    opcao = input("Digite 'v' para vídeo ou 'a' para áudio: ")
    
    if opcao.lower() == 'a':
        download_video(link, 'audio')
    else:
        download_video(link, 'video')