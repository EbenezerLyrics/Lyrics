import os
import requests
from bs4 import BeautifulSoup
import base64

# URL da página
url_do_site = input("Digite a URL: ")
url = url_do_site

# Baixar o conteúdo da página
response = requests.get(url)
html = response.text

# Analisar o HTML com BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Encontrar a tag 'article'
article_tag = soup.find('article')

# Encontrar a div com a classe 'lyric'
lyric_div = article_tag.find('div', class_='lyric')

# Encontrar a div com a classe 'lyric-original'
lyric_original_div = lyric_div.find('div', class_='lyric-original')

# Encontrar todas as tags 'p' dentro da div 'lyric-original'
p_tags = lyric_original_div.find_all('p')

# Criar uma lista para armazenar as linhas de texto
lines = []

# Extrair o texto das tags 'p' com quebras de linha para cada <br>
for p_tag in p_tags:
    lines.extend([line.strip() for line in p_tag.stripped_strings])

# Extrair o último parâmetro da URL como nome do arquivo, removendo hifens
file_name = url.split('/')[-2].replace('-', ' ') + '.txt'  # Usamos -2 para ignorar a barra final

# Caminho completo para o arquivo
file_path = os.path.join(os.getcwd(), file_name)

# Salvar o conteúdo no arquivo .txt
with open(file_path, 'w', encoding='utf-8') as file:
    file.write('\n'.join(lines))

print(f'Arquivo salvo com sucesso como {file_path}')

# Configurações para a API do GitHub
github_repo = 'EbenezerLyrics/Lyrics'
github_branch = 'main'
github_directory = 'Hinos'
github_token = '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'

# URL para upload do arquivo
upload_url = f'https://api.github.com/repos/{github_repo}/contents/{github_directory}/{file_name}'

# Cabeçalhos para autenticação
headers = {
    'Authorization': f'token {github_token}',
    'Content-Type': 'application/json',
}

# Ler o conteúdo do arquivo
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# Codificar o conteúdo em Base64
file_content_base64 = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')

# Dados para enviar para a API do GitHub
data = {
    'message': 'Adicionando novo arquivo',
    'content': file_content_base64,
    'branch': github_branch,
}

# Fazer a solicitação para a API do GitHub
response = requests.put(upload_url, headers=headers, json=data)

if response.status_code == 201:
    print('Arquivo enviado com sucesso para o GitHub!')
else:
    print(f'Erro ao enviar arquivo para o GitHub. Status Code: {response.status_code}, Mensagem: {response.text}')
