# CEAC Visa Status Automator

## Description
This script automates the process of checking visa application status on the CEAC (Consular Electronic Application Center) website by extracting necessary information from PDF files containing visa confirmation details and filling out the corresponding web form fields.

## Purpose
The purpose of this script is to streamline the process of checking visa application status by:
- Automatically extracting data (surname, passport number, confirmation number, etc.) from PDF files.
- Filling out the visa status tracking form on the CEAC website based on the extracted information.

## Prerequisites
- Python 3.x
- Required Python packages (`PyPDF2`, `selenium`)

## Installation
1. Clone the repository:
   ```git clone https://github.com/felipeczpaz/CEAC-Visa-Status-Automator```
2. Install dependencies:
   ```pip install PyPDF2 selenium```

## Usage
1. Ensure your Chrome browser is up to date.
2. Modify the `folder_path` variable in `main()` to point to the directory containing your PDF files.
3. Run the script:
   ```python ceac_visa_status_automator.py```

4. Enter the name to search for in the PDF files when prompted. The script will:
- Search for PDF files containing the specified name and visa confirmation data.
- Automatically extract relevant information from the PDF files.
- Navigate to the CEAC website and fill out the visa status tracking form using the extracted data.

## Features
- **PDF Processing**: Extracts essential visa application details (surname, passport number, confirmation number) from PDF files.
- **Web Automation**: Uses Selenium to automate the process of filling out the CEAC visa status tracking form.
- **Error Handling**: Includes robust error handling to manage exceptions during PDF extraction and web automation processes.

## Example
```bash
python ceac_visa_status_automator.py
Digite o nome a ser encontrado nos arquivos PDF (ou 'q' para sair): John Doe
```

## Notes
- Ensure that the PDF files in the specified directory adhere to the expected format for accurate data extraction.
- This script is tailored for the CEAC website and may require adjustments for other visa application tracking systems.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
