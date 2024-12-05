# [15:59, 02/12/2024] Jou:  - Pesquisa no site da viva real. Vai ter uma planilha de input, com o nome do bairro e da cidade, com o tipo de contrato(aluguel ou compra) 
# e você tem que capturar: Valor, Area, Cresci, Imobiliaria e telefone.
# Depois de pesquisar, tem que ir anuncio em anuncio e pegando as fotos e criar um PDF com as Fotos e tirar um print da pagina do anuncio. 
# Precisa pegar a data e a hora que foi feita a pesquisa e o link de cada resultado que retornou


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
sleep(5)

# Carregando a planilha
planilha = 'Viva_Real.xlsx'
abrir_planilha = load_workbook(planilha)
sheet = abrir_planilha['Planilha1']
sleep(1)


# Percorrendo as linhas
for linha in sheet.iter_rows(2, sheet.max_row +1, values_only=True):
    nome_bairro, nome_cidade, tipo_contrato = linha
    
    
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
    
    # Criando o loop que vai utilizar o elemento pai de base, onde vai passar anuncio por anuncio    
    for imovel in imoveis:
        
        # Setando a aba da pesquisa como principal
        aba_principal = navegador.current_window_handle
        
        #Clicando no anuncio que abrirá em outra aba
        imovel.find_element(By.XPATH, './/div[@class="property-card__content"]').click()
        sleep(4)
        
        # Setando a lista de abas do navegador para a variável abas
        abas = navegador.window_handles
        
        # Mudando o foco para a última aba aberta. (colocando -1 sempre vai buscar a ultima aba aberta)
        navegador.switch_to.window(abas[-1])
        sleep(1)
        
        #Capturando o valor do imóvel
        valor_imovel = navegador.find_element(By.XPATH, './/p[@data-testid="price-info-value"]').text
        sleep(1)
        
        # Capturando a área do imóvel
        area_imovel = navegador.find_element(By.XPATH, './/p[@itemprop="floorSize"]/span[@data-cy="ldp-propertyFeatures-txt"]').text
        sleep(1)
        #imobiliaria = navegador.find_element(By.XPATH, '(//div/a[@title="Loja Oficial do Anunciante"])[2]').text
        
        # Localizando e clicando o elemento do botão que expõe o(s) telefone(s)
        botao_ver_telefone = navegador.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/section/div[3]/button').click()
        sleep(20)
        
        # Captura o primeiro telefone
        telefone1 = WebDriverWait(navegador, 5).until(EC.visibility_of_element_located((By.XPATH, './/a[@data-cy="lead-modalPhone-phonesList-txt"][1]'))).text
        sleep(1)
        
        # Alguns anúncios tem dois telefones, então Vai aguardar 5 segundo e verificar se o elemento do segundo telefone está na tela,
        # se estiver ele captura, se não estiver a variável receberá "Sem Telefone"
        try:
            telefone2 = WebDriverWait(navegador, 5).until(EC.visibility_of_element_located((By.XPATH, '(.//a[@data-cy="lead-modalPhone-phonesList-txt"])[2]'))).text
        except:
            telefone2 = "Sem telefone"
        sleep(1)
        
        
        try:
            cresci = WebDriverWait(navegador, 5).until(EC.visibility_of_element_located((By.XPATH, './/p[@class="ShortListingInfoSection_advertiser__EA_EW"]'))).text
        
        except :
            cresci = "sem creci"
        sleep(1)
        
        # Capturando a URL da página atual
        url = navegador.current_url  
        sleep(1)
        
        # Colocando as variáveis numa lista
        lista_imoveis.append({'valor_imovel': valor_imovel, 'area_imovel': area_imovel, 'cresci': cresci,
                              'telefone1': telefone1, 'telefone2': telefone2, 'url': url})
        
        
        print(tipo_contrato)
        print(valor_imovel)
        print(area_imovel)
        print(cresci)
        #print(imobiliaria)
        print(telefone1)
        print(telefone2)
        print(url)
        print("-" * 70)
        
        navegador.close()
        sleep(2)
        navegador.switch_to.window(aba_principal)
        sleep(2)
    
    for imovel in lista_imoveis:
        print(f"{imovel['valor_imovel']:<10}{imovel['area_imovel']:<5}{imovel['cresci']:<10}{imovel['imobiliaria']:<20}{imovel['telefone1']:<10}{imovel['telefone2']:<10}{imovel['url']:<50}")
        print("-" * 70)
 
   
input('Enter para encerrar...')