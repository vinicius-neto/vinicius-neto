from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import openpyxl
from time import sleep
import sys


# Configurando as opções do Chrome para abrir no modo anônimo
chrome_options = Options()
chrome_options.add_argument("--incognito")


# Abrindo o Chrome, maximizando a tela e entrando no site
navegador = webdriver.Chrome(options=chrome_options)
navegador.maximize_window()
navegador.get("https://www.amazon.com.br/")

# Solicita o usuário qual o produto que vai ser pesquisado
produto = input("Digite o produto: ")

# Solicita o usuário para colocar o nome do arquivo que será gerado no final, adicionando um if not para caso o usuário não tenha colocado extensão .xlsx, o programa coloque
nome_arquivo = input("Digite o nome do arquivo: ")
if not nome_arquivo.endswith(".xlsx"):
    nome_arquivo += ".xlsx"

# Localizando o botão de busca na página
botaoBusca = navegador.find_element(By.XPATH, './/input[@placeholder="Pesquisa Amazon.com.br"]')

# Limpando o campo caso tenha algo preenchido nele
botaoBusca.clear()

# Insere o produto que o usuário digitou
botaoBusca.send_keys(produto)

# Pressiona "Enter" após finalizar a inserção
botaoBusca.send_keys(Keys.ENTER)
sleep(3)

# Criando a lista que será alimentada pelos produtos
lista_produtos = []

# Localizando o elemento pai de cada produto
produtos = navegador.find_elements(By.XPATH, './/div[@data-component-type="s-search-result"]')

for produto in produtos:
    # Raspando o nome dos produtos utilizando .text para já vir como string
    nome = produto.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]').text
    
    try:
        #Raspando o preço dos produtos. Nesse caso os centavos ficam localizados numa tag separada, então peguei o preço e o decimal separados e concatenei.
        preco = produto.find_element(By.XPATH, './/span[@class="a-price-whole"]').text
       
        preco_decimal = produto.find_element(By.XPATH, './/span[@class="a-price-fraction"]').text
        preco_completo = f"{preco},{preco_decimal}" if preco_decimal else preco
    except:
        preco_completo = "Preço não disponível"
    
    # Raspando a URL do produto
    url = produto.find_element(By.XPATH, './/a').get_attribute('href')
    
    # Adicionado-os à lista
    lista_produtos.append({'nome': nome, 'preco': preco_completo, 'url': url})

#Para mostrar no terminal
#for produto in lista_produtos:
#    print(f"{produto['nome']:<20} {produto['preco']:<15} {produto['url']:<50}")
#   print("-" * 70)

# Criando a planilha
planilha = openpyxl.Workbook()

# Criando a sheet
sheet = planilha.active

# Entitulando a sheet
sheet.title = "Lista de Produtos"

#Criando cabeçalho
sheet.append(["Nome", "Preço", "URL"])

#Inserindo os produtos na planilha
for produto in lista_produtos:
    sheet.append([produto["nome"], produto["preco"], produto["url"]])

#salvando a planilha
planilha.save(nome_arquivo)
print(f"Planilha {nome_arquivo} criada com sucesso!")


input("Pressione Enter para encerrar")
navegador.quit()
sys.exit()