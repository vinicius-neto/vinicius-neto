# [15:59, 02/12/2024] Jou:  - Pesquisa no site da viva real. Vai ter uma planilha de input, com o nome do bairro e da cidade, com o tipo de contrato(aluguel ou compra) 
# e você tem que capturar: Valor, Area, Cresci, Imobiliaria e telefone.
# Depois de pesquisar, tem que ir anuncio em anuncio e pegando as fotos e criar um PDF com as Fotos e tirar um print da pagina do anuncio. 
# Precisa pegar a data e a hora que foi feita a pesquisa e o link de cada resultado que retornou

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

    #Localizando campo de pesquisa e preenchendo.
    preencher = navegador.find_element(By.XPATH, './/input[@type="text"]')
    preencher.clear()
    preencher.send_keys(f"{nome_bairro} {nome_cidade}")
    sleep(5)
    
    # Aguardando o elemento aparecer
    checkbox = WebDriverWait(navegador, 5).until(
        EC.visibility_of_element_located((By.XPATH, './/input[@id="l-checkbox-4"]')))
    
    # Clica no elemento
    checkbox.click()
    sleep(1)
    
    # Clica no botão de buscar
    botao_buscar = navegador.find_element(By.XPATH, './/button[@type="submit"]').click()
    sleep(5)
    
    # Criando variável que vai receber lista de imoveis
    lista_imoveis = []
    
    # Localizando elemento pai
    imoveis = navegador.find_elements(By.XPATH, './/div[@data-type="property"]')
    aba_original = navegador.current_window_handle
        
    for imovel in imoveis:
        acessar_anuncio = navegador.find_element(By.XPATH, './/div[@class="property-card__content"]').click()
        sleep(3)
        
        valor_imovel = navegador.find_element(By. XPATH, './/p[@data-testid="price-info-value"]').text
        area_imovel = navegador.find_element(By.XPATH, './/p[@itemprop="floorSize"]/span[@data-cy="ldp-propertyFeatures-txt"]').text
        cresci = navegador.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div/div/div[1]/div/div/div[2]/p').text
        imobiliaria = navegador.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div/div/div[1]/div/div/div[2]/div/p').text
        
        botao_ver_telefone = navegador.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/section/div[3]/button').click()
        telefone1 = WebDriverWait(navegador, 5).until(EC.visibility_of_element_located((By.XPATH, './/a[@data-cy="lead-modalPhone-phonesList-txt"][1]')))
        telefone2 = WebDriverWait(navegador, 5).until(EC.visibility_of_element_located((By.XPATH, './/a[@data-cy="lead-modalPhone-phonesList-txt"][2]')))
        
        url = navegador.current_url   
        
        lista_imoveis.append({'valor_imovel': valor_imovel, 'area_imovel': area_imovel, 'cresci': cresci, 'imobiliaria': imobiliaria, 'telefone1': telefone1, 'telefone2': telefone2, 'url': url})
        
        navegador.close()
        
        navegador.switch_to.window(aba_original)
    
    for imovel in lista_imoveis:
        print(f"{imovel['valor_imovel']:<10}{imovel['area_imovel']:<5}{imovel['cresci']:<10}{imovel['imobiliaria']:<20}{imovel['telefone1']:<10}{imovel['telefone2']:<10}{imovel['url']:<50}")
        print("-" * 70)
    
    
    
    
    
    
        
        



input('Enter para encerrar...')
    