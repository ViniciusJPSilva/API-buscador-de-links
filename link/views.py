import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse, HttpRequest

def get_links(request: HttpRequest): #
    # Obtém a URL fornecida pelo usuário nos parâmetros da requisição
    url = request.GET.get('url')  

    # Realiza o web scraping da página
    response = create_request(url)

    # Extrai os links da página
    links = create_links_list(BeautifulSoup(response.content, 'html.parser'))
    
    if not links: 
        return JsonResponse({'error' : 'Nenhum link encontrado'}, status=404)
    
    return JsonResponse(links, safe=False, status=200)
# get_links()


# Cria uma requisição e retorna a resposta.
# Tenta criar uma requisição efetuando a verificação dos certificados SSL, caso não consiga cria ignorando a verificação.
def create_request(url, ssl_cert=True): #
    try:
        return requests.get(url)
    except (requests.exceptions.SSLError):
        return requests.get(url, verify=False)
#


# Extrai os links da página.
def create_links_list(soup: BeautifulSoup): #
    links = []
    for link_tag in soup.find_all('a'):
        link_href = link_tag.get('href')
        
        if link_href:
            links.append({
                'nome': link_tag.text,
                'url': link_href
            })

    return links
#