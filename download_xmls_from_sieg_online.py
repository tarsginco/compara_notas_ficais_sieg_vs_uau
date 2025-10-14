from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions 
from smb.SMBConnection import SMBConnection
from time import sleep
import shutil
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.environ.get("USERNAME_SIEG",)
PASSWORD = os.environ.get("PASSWORD_SIEG")
USERNAME_SERVER = os.environ.get("USERNAME_SERVER")
PASSWORD_SERVER = os.environ.get("PASSWORD_SERVER")


today =  date.today()
#checa a data de para carregar as notas do sieg
if today.day >= 20:
    DATAINIEMISSAO = date(2025,today.month,1)
    DATAFIMEMISSAO = date(2025,today.month,21)
else:
    DATAINIEMISSAO = date(2025,(today.month-1),1)
    DATAFIMEMISSAO = date(2025,(today.month),1)

DATAINIEMISSAO = DATAINIEMISSAO.strftime("%d-%m-%Y")
DATAFIMEMISSAO = DATAFIMEMISSAO.strftime("%d-%m-%Y")

SERVER_IP = "10.10.1.8"
SERVER_NAME =  'tuiuiu'
SHARE_NAME = "01 - Área Livre"
REMOTE_PATH_FILE = r"FISCAL\NFs Pendentes UAU"
TEMP_PATH = "/home/fernandatrentino/Ginco/temp"
FILE_NAME ="Relatorio Xml Cofre SIEG"


def save_dowloaded_file():

    conn = SMBConnection(
        USERNAME_SERVER, 
        PASSWORD_SERVER,
        "ubuntu_client", 
        SERVER_NAME
    )
    try:
        connected = conn.connect(SERVER_IP)
        print('Servidor remoto conectado com sucesso')
    except Exception as e:
        print(f"Erro ao conectar ao servidor {SHARE_NAME}: {e}")
        connected = False

    if connected:
        for file in os.listdir(TEMP_PATH):
            try:
                with open(os.path.join(TEMP_PATH,file), 'rb') as fp:
                    remote_path = f"{REMOTE_PATH_FILE}\{file}"
                    print('Remote path:',remote_path)
                    conn.storeFile(SHARE_NAME, remote_path, fp)
                
                print(f"Arquivos foram salvos em {SHARE_NAME} com sucesso!")
                conn.close()
                
                return True
            
            except Exception as e:
                print(f"Arquivos não foram salvos em {SHARE_NAME} devido a {e}")  
                conn.close()

                return False
        
def download_file(driver,type):
    wait = WebDriverWait(driver, 5)

    href = '' if type == 'nfe' else type
    
    try:
        if type =='nfe':
            driver.get(f"""https://cofre.sieg.com/pesquisa-avancada""")
        else:
            driver.get(f"""https://cofre.sieg.com/pesquisa-avancada-{href}""")
        
        print(f"Navegando para {driver.title}")
            
        try:
            add_filter = wait.until(expected_conditions.presence_of_element_located((By.XPATH,"//span[@class='las la-plus']")))
        except Exception as err:
            print(err)
        
        add_filter.click()
        wait
        
        select_filter = driver.find_elements(By.XPATH,"//select[@class='fields form-control']")
        for filter in select_filter: 
            select_object = Select(filter)                                      
            select_object.select_by_value("EmissionDate")
            wait

        select_conditions = [Select(select_conditions) for select_conditions in driver.find_elements(By.XPATH,"//select[@class='conditions form-control']")]                              
        select_conditions[0].select_by_value("$gte") #maior igual
        select_conditions[1].select_by_value("$lt") #menor
        wait

        select_emiss_date = driver.find_elements(By.XPATH,"//input[@class='form-control input-search EmissionDate']")
        select_emiss_date[0].send_keys(DATAINIEMISSAO)
        wait
        select_emiss_date[1].send_keys(DATAFIMEMISSAO)
        wait
        
        driver.find_element(By.ID,'btnSearch').click()
        wait 
               
        try:

            export_excel = wait.until(expected_conditions.presence_of_element_located((By.ID,f"""MainContent_cphMainContent_advancedsearch{href}_ExcelLinkBtn""")))
        except Exception as err:
            print(err)
        
        print('Exportando planilha..')
        export_excel.click()
        sleep(10)
            

        new_file_name = ''
        #renomeia arquivos em temp
        while not os.listdir(TEMP_PATH):
            print('Aguardando exportação da planilha')  
            wait          
        for file in os.listdir(TEMP_PATH):
            name_base = file[:24]
            year = today.strftime("%y")
            file_date =  f"20.{today.month}.{year}" if today.day >= 20 else f"02.{today.month}.{year}"
            new_file_name = f"{name_base} - {file_date} - {type}.xlsx"
            os.rename(
                os.path.join(TEMP_PATH,file), 
                os.path.join(TEMP_PATH,new_file_name)
            )
            print(f'{new_file_name} salva com sucesso!')
            
            
        #salvar arquivos que estão em TEMP_PATH no servidor remoto SHARE_NAME
        saved_file = save_dowloaded_file()

        #deletar arquivos em temp depois de salvar no servidor remoto
        if saved_file:
            os.remove(os.path.join(TEMP_PATH,new_file_name))


    except Exception as err:
        print(err)

def get_data_from_sieg():

    options = Options()
    options.add_argument('--headless')  # sem interface
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs", {
        "download.default_directory": TEMP_PATH,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True  # Set to False if you want to disable safe browsing warnings
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)

    driver.get('https://hub.sieg.com/')
    #manter essa resolução para buscar todo o conteudo da tabela
    driver.set_window_size(1200, 800) 

    username_div = driver.find_element(By.ID,"txtEmail")
    password_div = driver.find_element(By.ID,"txtPassword")

    #login
    username_div.send_keys(USERNAME)
    sleep(2)
    password_div.send_keys(PASSWORD)
    sleep(2)
    loggin_input= driver.find_element(By.ID,"btnSubmit")
    sleep(2)
    loggin_input.click()


    try:
        wait.until(lambda driver: "login" not in driver.title.lower())
    except Exception:
        pass


    if driver.title != "Login - Console SIEG":
        print(f'Login em {driver.title} realizado com sucesso')
    else:
        print(loggin_input.text)

    nf_types = [ "nfe", "nfse", "cte"]
    for nf_type in nf_types:
        download_file(driver,nf_type)
    
    driver.quit()

if __name__ == '__main__':
    get_data_from_sieg()