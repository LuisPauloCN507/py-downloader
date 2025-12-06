import yt_dlp
import os

def download_media(url, tipo='video'):
    # Define a pasta base (Tudo vai cair aqui dentro)
    base_folder = 'downloads'
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    print(f"\n🚀 Analisando link...")

    # --- CONFIGURAÇÕES GERAIS ---
    ydl_opts = {
        # LÓGICA DE NOMES SUPER SIMPLES:
        # Salva apenas como: downloads/Titulo do Video.ext
        # Removemos qualquer numeração ou pasta de playlist
        'outtmpl': f'{base_folder}/%(title)s.%(ext)s',
        
        'progress_hooks': [hook_progresso], 
        'writethumbnail': True,  # Baixa a capa
        'addmetadata': True,     # Escreve metadados
        'ignoreerrors': True,    # Pula erros
        'postprocessors': [],    # Lista vazia para preencher abaixo
    }

    if tipo == 'audio':
        # --- MODO ÁUDIO (MP3 320kbps + Capa + Tags) ---
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320', # Qualidade máxima
            },
            {
                'key': 'EmbedThumbnail', # Cola a capa
            },
            {
                'key': 'FFmpegMetadata', # Dados do arquivo
                'add_metadata': True,
            }
        ]
        # Tenta separar "Artista - Música" do título
        ydl_opts['parse_metadata'] = [{'title': '%(artist)s - %(title)s'}]
        
    else:
        # --- MODO VÍDEO (MP4 Alta Qualidade) ---
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        ydl_opts['postprocessors'].append({'key': 'FFmpegMetadata', 'add_metadata': True})
        ydl_opts['postprocessors'].append({'key': 'EmbedThumbnail'})

    # --- EXECUÇÃO ---
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extrai info antes
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                print(f"\n📄 Playlist: {info.get('title')}")
                print(f"📊 Total: {len(info['entries'])} arquivos")
            else:
                print(f"\n🎬 Vídeo: {info.get('title')}")

            confirmacao = input("\nConfirmar download? [S/n]: ").lower()
            if confirmacao == 'n':
                print("Cancelado.")
                return

            print("\n🏁 Iniciando Downloads...")
            ydl.download([url])
            
            print(f"\n✨ Finalizado! Arquivos salvos em '{base_folder}'")
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")

# --- BARRA DE PROGRESSO ---
def hook_progresso(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%','')
        filename = d.get('filename', '').split('/')[-1]
        filename = (filename[:40] + '..') if len(filename) > 40 else filename
        
        print(f"⬇️  {filename} | {p}%", end='\r')
    
    if d['status'] == 'finished':
        print(f"\n✅ Baixado. Convertendo...", end='\r')

# --- MENU PRINCIPAL ---
if __name__ == "__main__":
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*50)
        print("🎵 PyDownloader 3.2 - Clean Names")
        print("="*50)
        
        link = input("🔗 Cole o link aqui (ou 'sair'): ")
        
        if link.lower() == 'sair':
            break
            
        print("\n[a] Áudio (MP3 320kbps + Capa)")
        print("[v] Vídeo (MP4 Alta Qualidade)")
        opcao = input("Escolha o formato: ").lower()
        
        if opcao == 'a':
            download_media(link, 'audio')
        elif opcao == 'v':
            download_media(link, 'video')
        else:
            print("❌ Opção inválida!")
        
        input("\nPressione Enter para continuar...")