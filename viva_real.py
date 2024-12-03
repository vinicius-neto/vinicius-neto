# [15:59, 02/12/2024] Jou:  - Pesquisa no site da viva real. Vai ter uma planilha de input, com o nome do bairro e da cidade, com o tipo de contrato(aluguel ou compra)  e você tem que capturar: Valor, Area, Cresci, Imobiliaria e telefone. Depois de pesquisar, tem que ir anuncio em anuncio e pegando as fotos e criar um PDF com as Fotos e tirar um print da pagina do anuncio. Precisa pegar a data e a hora que foi feita a pesquisa e o link de cada resultado que retornou

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from openpyxl import load_workbook
import undetected_chromedriver as uc

# Abrindo o navegador
navegador = uc.Chrome()
navegador.get("https://www.vivareal.com.br/")
navegador.maximize_window()


# Carregando a planilha
planilha = 'Viva_Real.xlsx'
abrir_planilha = load_workbook(planilha)
sheet = abrir_planilha['Planilha1']
sleep(1)


# Percorrendo as linhas
for linha in range(2, sheet.max_row +1):
    nome_bairro = sheet[f'A{linha}'].value
    nome_cidade = sheet[f'B{linha}'].value
    tipo_contrato = sheet[f'C{linha}'].value
    
    # Localizando elementos comprar ou alugar
    contrato_alugar = navegador.find_element(By.XPATH, './/button[@data-cy="home-rent-tb-tab"]').text
    contrato_comprar = navegador.find_element(By.XPATH, './/button[@data-cy="home-buy-tb-tab"]').text

    # Comparando contrato da planilha com o do site
    if tipo_contrato == contrato_alugar:
        contrato_alugar = navegador.find_element(By.XPATH, './/button[@data-cy="home-rent-tb-tab"]').click()
        sleep(1)
    else:
        contrato_comprar = navegador.find_element(By.XPATH, './/button[@data-cy="home-buy-tb-tab"]').click()
        sleep(1)

    
    preencher = navegador.find_element(By.XPATH, './/input[@type="text"]')
    preencher.clear()
    preencher.send_keys(f"{nome_bairro} {nome_cidade}")
    sleep(5)
      
    checkbox = WebDriverWait(navegador, 5).until(
        EC.visibility_of_element_located((By.XPATH, './/input[@id="l-checkbox-4"]')))
    
    checkbox.click()
    sleep(1)
        
    botao_buscar = navegador.find_element(By.XPATH, './/button[@type="submit"]').click()
    sleep(1)
        
        



input('Enter para encerrar...')
    