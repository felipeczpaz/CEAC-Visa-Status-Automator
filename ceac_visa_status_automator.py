import time
import webbrowser

def print_message():
    message = """
/************************************************************
 *                                                          *
 *   Flowhooks Software - All Rights Reserved               *
 *          (c) 2025 Felipe Cezar Zwerchowski Paz LTDA.     *
 *                                                          *
 *  This software is proprietary.                           *
 *  Unauthorized use, reproduction, or distribution is      *
 *  strictly prohibited.                                     *
 *                                                          *
 *  Author: Felipe Cezar Paz (git@felipecezar.com)          *
 *  File:                                                  *
 *  Description:                                            *
 *                                                          *
 ************************************************************/
"""
    print(message)
    print("O acesso ao sistema foi revogado. Para restabelecer o acesso, é necessário firmar um contrato de SaaS para utilização do software.")

if __name__ == "__main__":
    print_message()
    time.sleep(1)

    # URL para redirecionamento
    url = "https://flowhooks.digital/"
    webbrowser.open(url)
    print("Você foi redirecionado para o nosso site. Agradecemos pelo seu interesse!")
