import os
import re
import threading
import functools
from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchWindowException
 
driver = None
 
def initialize_driver():
    global driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
 
def quit_driver(driver):
    try:
        driver.quit()
    except WebDriverException as e:
        print(f"Error while quitting WebDriver: {e}")
 
def automate_form_fill(surname, passport_number, confirmation_number, location_selected, pdf_path):
    try:
        if surname is None and passport_number is None and confirmation_number is None and location_selected is None:
            print("\nErro: Os dados do PDF não puderam ser lidos. Todas as variáveis estão vazias. Abrindo o arquivo PDF.")
            # Executa o arquivo PDF (substitua pela sua lógica)
            # Exemplo: abrir o arquivo PDF usando o visualizador padrão de PDF
            os.startfile(pdf_path)
            return
 
        global driver
        if driver is None:
            initialize_driver()
 
        try:
            # Open the webpage
            driver.get("https://ceac.state.gov/CEACStatTracker/Status.aspx?App=NIV")
 
            # Select location from dropdown by option value
            location_dropdown = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Location_Dropdown"))
            ))
            location_dropdown.select_by_value(location_selected)
 
            # Wait until the Visa Case Number input field is visible
            visa_case_number_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Visa_Case_Number"))
            )
            visa_case_number_element.send_keys(confirmation_number)
 
            # Wait until the Passport Number input field is visible
            passport_number_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Passport_Number"))
            )
            passport_number_element.send_keys(passport_number)
 
            # Wait until the Surname input field is visible
            surname_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Surname"))
            )
            surname_element.send_keys(surname)
 
        except NoSuchWindowException:
            print("Browser window closed. Reopening browser and retrying.")
            initialize_driver()  # Reinitialize the WebDriver
            automate_form_fill(surname, passport_number, confirmation_number, location_selected, pdf_path)  # Retry the operation
 
        except Exception as e:
            print(f"Ocorreu um erro ao preencher o formulário: {str(e)}")
 
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
 
@functools.lru_cache(maxsize=None)
def extract_information_from_pdf(pdf_path):
    try:
        surname = ''
        year_of_birth = ''
        passport_number = ''
        confirmation_number = ''
        location_selected = ''
 
        with open(pdf_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            for page_num in range(len(reader.pages)):
                text = reader.pages[page_num].extract_text()
 
                if "Name\nProvided:" in text:
                    start_index = text.find("Name\nProvided:") + len("Name\nProvided:")
                    end_index = text.find(",", start_index)
                    surname = text[start_index:end_index].strip()
 
                if "Date Of Birth:" in text:
                    start_index = text.find("Date Of Birth:") + len("Date Of Birth:")
                    year_of_birth_match = re.search(r'\d{4}', text[start_index:])
                    if year_of_birth_match:
                        year_of_birth = year_of_birth_match.group()
 
                passport_match = re.search(r'Passport\nNumber:\s*(\w+)', text, re.IGNORECASE)
                if passport_match:
                    passport_number = passport_match.group(1)
 
                confirmation_match = re.search(r'Confirmation\nNo:\s*(\w+)', text, re.IGNORECASE)
                if confirmation_match:
                    confirmation_number = confirmation_match.group(1)[:10]
 
                location_match = re.search(r'Location Selected:\s*(.*)', text, re.IGNORECASE)
                if location_match:
                    location_selected = location_match.group(1).strip()[:3]
 
        print(f"Sobrenome: {surname}")
        print(f"Ano de Nascimento: {year_of_birth}")
        print(f"Número do Passaporte: {passport_number}")
        print(f"Número de Confirmação: {confirmation_number}")
        print(f"Local Selecionado: {location_selected}")
 
        if not any([surname, year_of_birth, passport_number, confirmation_number, location_selected]):
            return None, None, None, None, None
 
        return surname, year_of_birth, passport_number, confirmation_number, location_selected
 
    except Exception as e:
        print(f"Ocorreu um erro ao extrair informações do arquivo {pdf_path}: {str(e)}")
        return None, None, None, None, None
 
def find_files_and_extract_info(start_dir, specific_string):
    try:
        found_files = []
        specific_words = specific_string.lower().split()
        with os.scandir(start_dir) as entries:
            for entry in entries:
                if entry.is_file() and all(word in entry.name.lower() for word in specific_words) \
                        and ("confirmação" in entry.name.lower() or "confirmacao" in entry.name.lower()):
                    full_path = entry.path
                    print(f"\n{entry.name}")
                    surname, year_of_birth, passport_number, confirmation_number, location_selected = extract_information_from_pdf(full_path)
                    found_files.append({
                        'pdf_path': full_path,
                        'surname': surname,
                        'year_of_birth': year_of_birth,
                        'passport_number': passport_number,
                        'confirmation_number': confirmation_number,
                        'location_selected': location_selected
                    })
 
        if not found_files:
            print(f"\nNenhum arquivo contendo '{specific_string}' e 'CONFIRMAÇÃO' ou 'CONFIRMACAO' encontrado em '{start_dir}' e seus subdiretórios.")
        else:
            if len(found_files) > 1:
                print(f"\nEncontrados {len(found_files)} arquivos:")
                for index, file_info in enumerate(found_files):
                    passport_number = file_info['passport_number'] or 'Impossível extrair'
                    print(f"{index + 1}: {os.path.basename(file_info['pdf_path'])} - Passaporte: {passport_number}")
 
                user_choice = get_valid_user_choice(len(found_files))
                selected_file = found_files[user_choice - 1] if user_choice is not None else None
 
            else:
                selected_file = found_files[0]
 
            if selected_file:
                automate_form_fill(selected_file['surname'], selected_file['passport_number'], selected_file['confirmation_number'], selected_file['location_selected'], selected_file['pdf_path'])
 
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
 
def get_valid_user_choice(num_choices):
    while True:
        try:
            user_input = input(f"Selecione o índice do arquivo desejado (1-{num_choices}), 'c' para cancelar: ").strip().lower()
            
            if user_input == 'c':
                return None  # User chose to cancel
            
            user_choice = int(user_input)
            
            if 1 <= user_choice <= num_choices:
                return user_choice
            else:
                print("Índice inválido. Por favor, selecione um índice válido.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
 
if __name__ == "__main__":
    try:
        folder_path = r'Z:\0001 - ASV GERAL\CONFIRMAÇÕES DE ENVIO DE FORMULARIOS DS-160'
 
        initialize_driver()
 
        while True:
            name_to_find = input("\nDigite o nome a ser encontrado nos arquivos PDF: ")
 
            if re.match(r'^[a-zA-Z ]{3,}$', name_to_find):
                find_files_and_extract_info(folder_path, name_to_find)
            else:
                print("O nome deve conter pelo menos 3 caracteres alfabéticos e pode incluir espaços.")
 
    finally:
        if driver is not None:
            # Start a thread to quit the WebDriver asynchronously
            quit_thread = threading.Thread(target=quit_driver, args=(driver,))
            quit_thread.start()
            driver = None
 
