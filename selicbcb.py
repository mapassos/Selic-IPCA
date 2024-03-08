def main():
    data = retrieve_selic()

    try:
        with open('selic.csv') as old_file:
            old_data = old_file.readlines()
    except:
        old_data = []
    print(len(data))
    print(len(old_data))
    if len(data) > len(old_data):
        save_to_csv(data)
        print(f'Saving as selic.csv')
    else:
        print('No new data available!')
    return 0

def save_to_csv(data_list: list):
    import csv
    
    with open('selic.csv', 'w', newline='') as csv_file:
        write = csv.writer(csv_file)
        write.writerows(data_list)
    print('Saved!')

def retrieve_selic() -> list:
    '''Retrieves selic table as a list of list from bcb website'''
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options = options)

    url = "https://www.bcb.gov.br/controleinflacao/historicotaxasjuros"

    driver.get(url)
    assert driver.title is not None
    
    table = driver.find_element('id', 'historicotaxasjuros')
    rows = table.find_elements('tag name', "tr")

    content = []
    
    for row in rows:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(('class name', 'text-center')))
        cols = row.find_elements('tag name', "td")
        if len(cols) > 0:
            content.append([])
            for col in cols:
                content[-1].append(col.text)
    assert len(content) > 2
    driver.quit()
    return content

if __name__ == '__main__':
    main()
