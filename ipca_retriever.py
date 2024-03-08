def main():
    retrieve_ipca()
    return 0

def file_unzipper(ipca_file, path):
    import os
    #unzipping file
    from zipfile import ZipFile
    with ZipFile(ipca_file , 'r') as zip:
        zip.extractall(path)
        file_name = zip.namelist()[0]    
    print('Unzip completed')
    return file_name

def retrieve_ipca() -> str:

    import os
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    cur_path = os.getcwd()

    options = Options()
    options.add_argument('--headless')
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", cur_path)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

    driver = webdriver.Firefox(options=options)

    url = "https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html?=&t=downloads"

    driver.get(url)
    assert driver.title is not None

    WebDriverWait(driver, 3).until(EC.presence_of_element_located(('id', 'Precos_Indices_de_Precos_ao_Consumidor/IPCA_anchor'))).click()

    #removing privacy policy popup
    polpriv_pop = driver.find_element('id', 'cookie-container')
    driver.execute_script('arguments[0].remove();', polpriv_pop)
    
    #retrieving file
    driver.find_element('id','Precos_Indices_de_Precos_ao_Consumidor/IPCA/Serie_Historica_anchor').click()
    element = driver.find_element('id', 'ftpLoad')
    driver.execute_script("arguments[0].style.visibility='hidden'", element)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(('id', 'j1_74_anchor')))
    ipca_file = driver.find_element('id', 'j1_74_anchor').text
    driver.find_element('id', 'j1_74_anchor').click()
    print('Download Completed')
    
    driver.quit()
    
    
    ipca_unzipped_filename = file_unzipper(ipca_file, cur_path)
    return ipca_unzipped_filename

if __name__ == '__main__':
    main()