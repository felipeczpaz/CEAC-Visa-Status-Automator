import os
import re
import logging
from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchWindowException

# Disable WebDriver logging
logging.getLogger('selenium').setLevel(logging.CRITICAL + 1)

# Global variable to hold the WebDriver instance
driver = None

def initialize_driver():
    global driver
    # Configure Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")  # Maximizes the Chrome window (optional)

    # Initialize Chrome WebDriver with configured options
    driver = webdriver.Chrome(options=chrome_options)

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

def find_files_and_extract_info(start_dir, specific_string):
    try:
        found_files = []

        # Loop through all files and directories in the start_dir
        for root, _, files in os.walk(start_dir):
            for file in files:
                # Check if the specific_string is in the current file's name
                if specific_string.lower() in file.lower():
                    # Check if "CONFIRMAÇÃO" is also in the file's name
                    if "CONFIRMAÇÃO".lower() in file.lower() or "CONFIRMACAO".lower() in file.lower():
                        full_path = os.path.join(root, file)
                        print(f"\n{file}")
                        # Extract information from PDF and append to found_files
                        surname, year_of_birth, passport_number, confirmation_number, location_selected = extract_information_from_pdf(full_path)
                        found_files.append({
                            'pdf_path': full_path,
                            'surname': surname,
                            'year_of_birth': year_of_birth,
                            'passport_number': passport_number,
                            'confirmation_number': confirmation_number,
                            'location_selected': location_selected
                        })

        # If no matching file is found
        if not found_files:
            print(f"Nenhum arquivo contendo '{specific_string}' e 'CONFIRMAÇÃO' ou 'CONFIRMACAO' encontrado em '{start_dir}' e seus subdiretórios.")
        else:
            if len(found_files) > 1:
                print(f"\nEncontrados {len(found_files)} arquivos:")
                for index, file_info in enumerate(found_files):
                    passport_number = file_info['passport_number'] or 'Impossível extrair'  # Get passport number or assign 'Impossível extrair'
                    print(f"{index + 1}: {os.path.basename(file_info['pdf_path'])} - Passaporte: {passport_number}")

                while True:
                    try:
                        user_choice = int(input(f"Selecione o índice do arquivo desejado (1-{len(found_files)}): "))
                        if 1 <= user_choice <= len(found_files):
                            selected_file = found_files[user_choice - 1]
                            break
                        else:
                            print("Índice inválido. Por favor, selecione um índice válido.")
                    except ValueError:
                        print("Entrada inválida. Por favor, insira um número.")

            else:
                selected_file = found_files[0]

            # Call automate_form_fill on the selected file
            automate_form_fill(selected_file['surname'], selected_file['passport_number'], selected_file['confirmation_number'], selected_file['location_selected'], selected_file['pdf_path'])

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

def extract_information_from_pdf(pdf_path):
    try:
        # Initialize variables to store extracted information
        surname = ''
        year_of_birth = ''
        passport_number = ''
        confirmation_number = ''
        location_selected = ''

        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)

            # Extract text from each page
            for page_num in range(len(reader.pages)):
                text = reader.pages[page_num].extract_text()

                # Extract surname
                if "Name\nProvided:" in text:
                    start_index = text.find("Name\nProvided:") + len("Name\nProvided:")
                    end_index = text.find(",", start_index)
                    surname = text[start_index:end_index].strip()

                # Extract year of birth
                if "Date Of Birth:" in text:
                    start_index = text.find("Date Of Birth:") + len("Date Of Birth:")
                    year_of_birth_match = re.search(r'\d{4}', text[start_index:])
                    if year_of_birth_match:
                        year_of_birth = year_of_birth_match.group()

                # Extract passport number
                passport_match = re.search(r'Passport\nNumber:\s*(\w+)', text, re.IGNORECASE)
                if passport_match:
                    passport_number = passport_match.group(1)

                # Extract confirmation number
                confirmation_match = re.search(r'Confirmation\nNo:\s*(\w+)', text, re.IGNORECASE)
                if confirmation_match:
                    confirmation_number = confirmation_match.group(1)

                # Extract Location Selected
                location_match = re.search(r'Location Selected:\s*(.*)', text, re.IGNORECASE)
                if location_match:
                    location_selected = location_match.group(1).strip()

        # Print extracted information
        print(f"Sobrenome: {surname}")
        print(f"Ano de Nascimento: {year_of_birth}")
        print(f"Número do Passaporte: {passport_number}")
        print(f"Número de Confirmação: {confirmation_number}")
        print(f"Local Selecionado: {location_selected}")

        # Check if all variables are empty
        if not any([surname, year_of_birth, passport_number, confirmation_number, location_selected]):
            return None, None, None, None, None  # Retorna valores None se os dados estiverem vazios

        return surname, year_of_birth, passport_number, confirmation_number, location_selected

    except Exception as e:
        print(f"Ocorreu um erro ao extrair informações do arquivo {pdf_path}: {str(e)}")
        return None, None, None, None, None  # Retorna valores None em caso de erro

# Exemplo de uso:
if __name__ == "__main__":
    try:
        folder_path = r'Z:\0001 - ASV GERAL\CONFIRMAÇÕES DE ENVIO DE FORMULARIOS DS-160'  # Substitua pelo caminho da sua pasta

        while True:
            # Solicita ao usuário o nome a ser procurado
            name_to_find = input("Digite o nome a ser encontrado nos arquivos PDF (ou 'q' para sair): ")

            if name_to_find.lower() == 'q':
                break

            # Check if name_to_find has at least 3 alphabetical characters and may include spaces
            if re.match(r'^[a-zA-Z ]{3,}$', name_to_find):
                find_files_and_extract_info(folder_path, name_to_find)
            else:
                print("O nome deve conter pelo menos 3 caracteres alfabéticos e pode incluir espaços.")

    finally:
        if driver is not None:
            driver.quit()
