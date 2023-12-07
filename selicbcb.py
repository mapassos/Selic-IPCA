def main():
    data = retrieve_selic()

    try:
        with open('selic.csv') as old_file:
            old_data = old_file.readlines()
    except:
        old_data = []

    if len(data) > len(old_data):
        to_csv(data)
        print(f'Saving to csv file')
    else:
        print('No new data available!')
    return 0

def to_csv(data_list: list):
    import csv
    
    with open('selic.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data_list)

def retrieve_selic() -> list:
    '''Retrieves selic table as a list of list from bcb website'''
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options

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
        cols = row.find_elements('tag name', "td")
        content.append([])
        for col in cols:
            content[-1].append(col.text) 
    driver.implicitly_wait(2)
    driver.quit()
    return content

if __name__ == '__main__':
    main()
