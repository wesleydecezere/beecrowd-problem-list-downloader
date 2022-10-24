import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def write_csv(file_name, header, data):
  with open(file_name, 'w', encoding='UTF8', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(header)
      writer.writerows(data)

class ProblemsDownloader:
  def __init__(self):
    self.service = Service('/home/wesley/Documents/chromedriver_linux64/chromedriver')
    self.service.start()
    self.driver = webdriver.Remote(self.service.service_url)
    self.url = "https://www.beecrowd.com.br/judge/pt"

  def open(self, url):
    self.driver.get(url)

  def close(self):
    self.driver.close()

  def login(self):
    email = input("email: ")
    password = input("senha: ")

    driver = self.driver
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    login_btn = driver.find_element(By.XPATH, "//input[@value='Entrar']")

    email_field.clear()
    email_field.send_keys(email)
    password_field.clear()
    password_field.send_keys(password)

    login_btn.click()

    try:
      self.close_overlay()
    except:
      print("Email ou senha incorretos, tente novamente.\n")
      self.login()

  def close_overlay(self):
    self.driver.find_element(By.CSS_SELECTOR, ".mfp-close").click()

  def next_page(self):
    next_btn = self.driver.find_element(By.CSS_SELECTOR, ".next > a")
    self.driver.execute_script("arguments[0].click();", next_btn)

  def get_num_pages(self):
    table_info_txt = self.driver.find_element(By.ID, "table-info").get_attribute('outerText')
    return int(list(table_info_txt)[-1])

  def get_problems_page(self):
    driver = self.driver
    rows = driver.find_elements(By.XPATH, "//tr")[1:]
    problemas = list()

    for row in rows:
      cols = row.find_elements(By.XPATH, "td")
      if len(cols) == 1: break      

      id_elememnt = row.find_element(By.CSS_SELECTOR, "td.id > a")
      id = id_elememnt.get_attribute("outerText")
      link = id_elememnt.get_attribute("href")

      name = row.find_element(By.CSS_SELECTOR, "td.large").get_attribute("outerText")
      assunto = row.find_element(By.CSS_SELECTOR, "td.wide > strong").get_attribute("original-title").replace(';', ',')
      resolucoes = row.find_elements(By.CSS_SELECTOR, "td.small")[1].get_attribute("outerText")
      nivel = row.find_elements(By.CSS_SELECTOR, "td.tiny")[1].get_attribute("outerText")
            
      problemas.append([id, name, assunto, resolucoes, nivel, link])

    return problemas

  def get_problems(self, topic):
    url = f'{self.url}/problems/index/{topic}'
    self.open(url)

    problems = []    
    num_pages = self.get_num_pages()

    for i in range(num_pages):
      print(f'> Página {i+1} de {num_pages}...')
      if i > 0: self.next_page()
      problems += self.get_problems_page()

    print("> Todas as páginas lidas com sucesso!")
    return problems

  def run(self, topics):
    self.open(self.url)
    self.login()

    header = ['ID', 'Nome', 'Assunto', 'Número de resoluções', 'Nível', 'Link']

    for topic in topics:     
      print(f"\nLendo problemas do tópico {topic}")

      problems = self.get_problems(topic)
      file_name = f'topico-{topic}.csv'
      write_csv(file_name, header, problems)

      print(f"Problemas do tópico {topic} salvos no arquivo '{file_name}' :D")

    self.close()


topics = range(1, 9)
bee = ProblemsDownloader()
bee.run(topics)