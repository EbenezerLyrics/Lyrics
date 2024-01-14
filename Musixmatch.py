import requests
import base64
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# URL da sua página
url_do_site = input("Digite a URL: ")
url = url_do_site

# Adicionar cabeçalho user-agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Analisar a URL para obter o último segmento
last_segment = urlparse(url).path.split('/')[-1]

# Remover hifens do último segmento para criar o nome do arquivo
file_name = f'{last_segment.replace("-", " ")}.txt'

# Enviar uma solicitação para obter o conteúdo da página
response = requests.get(url, headers=headers)

# Verificando se a solicitação foi bem-sucedida (código 200)
if response.status_code == 200:
    html_content = response.content

    # Parseando o HTML com BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Encontrar todas as tags span com a classe 'lyrics__content__ok'
    lyrics_spans = soup.find_all('span', class_='lyrics__content__ok')

    # Verificar se as tags foram encontradas antes de tentar acessar o conteúdo
    if lyrics_spans:
        # Criar o conteúdo do arquivo
        file_content = '\n'.join([lyrics_span.get_text(strip=True) for lyrics_span in lyrics_spans])

        # Configurações para a API do GitHub
        github_api_url = 'https://api.github.com/repos/EbenezerLyrics/Lyrics/contents/Hinos/' + file_name
        github_token = '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'  # Substitua pelo seu token de acesso

        # Criar ou atualizar o arquivo no GitHub
        response_github = requests.put(
            github_api_url,
            headers={'Authorization': f'Bearer {github_token}'},
            json={
                'message': 'Atualizando arquivo',
                'content': base64.b64encode(file_content.encode()).decode(),
                'branch': 'main'
            }
        )

        if response_github.status_code == 200:
            print(f"Conteúdo salvo em {file_name} no GitHub.")
        else:
            print(f"Arquivo salvo com sucesso no Github. Código de status: {response_github.status_code}")
    else:
        print("Nenhuma tag encontrada.")
else:
    print(f"Falha na solicitação. Código de status: {response.status_code}")

