# Import for the Desktop Bot
from botcity.core import DesktopBot, Backend

# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Importar a minha biblioteca github: mbOpenTsk
from functions.setBible import *

def main():
   
    desktop_bot = DesktopBot()
    webbot = WebBot()
    opnBrowse = Browser_config()
    opnDesk = DesktopUtils()

    # Implement here your logic...
    opnBrowse.Open_browser(webbot, "CHROME", False, "https://jornadarpa.com.br/alunos/desafios/sistemas/extrato/index.html")

    dados = opnBrowse.Web_scrap(webbot, "/html/body/div[2]/div/div/div/div/div/table")

    # Converter o DataFrame para uma lista de listas
    dados = dados.values.tolist()

    # Abrir o Aplicativo desktop Bank
    title_bank = "Alex Diogo - Bank"
    opnDesk.Open_Application(desktop_bot, 
                             "E:\RPA\DRIVERS\Banco.exe", 
                             title_bank, Backend.WIN_32)
    
    #instanciar o Bank
    bank_window = desktop_bot.find_app_window(title=title_bank, class_name="WindowsForms10.Window.8.app.0.141b42a_r7_ad1")
   # Mapear os botões de Débito e Crédito
    btn_Debito = desktop_bot.find_app_element(from_parent_window=bank_window, auto_id="radioButton_Debito")
    btn_Credito = desktop_bot.find_app_element(from_parent_window=bank_window, auto_id="radioButton_Credito")
    # Mapear o campos de valor, data e descrição
    campo_descricao = desktop_bot.find_app_element(from_parent_window=bank_window, auto_id="textBox_Descricao")
    campo_valor = desktop_bot.find_app_element(from_parent_window=bank_window, auto_id="textBox_Valor") 
    campo_data = desktop_bot.find_app_element(from_parent_window=bank_window, auto_id="textBox_Data")   
    # Mapear o botão de Gravar
    btn_gravar = desktop_bot.find_app_element(from_parent_window=bank_window, auto_id="button_Gravar")
    
    for linha in dados:
       
        # Desempacotamento dos valores em variáveis
        ID, Descricao, Tipo, valor, data = linha
       
        # verificar condição se Débito ou Crédito
        if Tipo == "Débito":
            btn_Debito.click()
        else:
            btn_Credito.click()
        # Preencher os campos de descrição, valor e data
        campo_descricao.set_text(Descricao)
        campo_valor.set_text(str(valor))
        campo_data.set_text(data)   
        btn_gravar.click()

    # Fechar a aplicação 
    opnDesk.Close_Apllication(desktop_bot, "Banco")


    # Comparar valor extraídos
    try:
        # Obter o valor total do site
        totalValorSite = webbot.find_element("/html/body/div[2]/div/div/div/div/div/b", by=By.XPATH)
        if totalValorSite:
            texto_total = totalValorSite.text.strip()  # Pega o texto e remove espaços extras
                        
            # Converter para float corretamente
            totalValor = float(texto_total.replace('.', '').replace(',', '.'))
            print(f"Valor total do Site encontrado R$ {totalValor:.2f}")
        else:
            print("Elemento não encontrado.")
    except Exception as e:
        print("Erro ao tentar processar o elemento:", str(e))

    try:

        # Inicializar o total
        total_calculado = 0

        # Iterar sobre as linhas de dados
        for linha in dados:
            # Extrair os valores das colunas relevantes
            Tipo = linha[2]  # Coluna que indica "Débito" ou "Crédito"
            valor = float(linha[3].replace('.', '').replace(',', '.'))  # Converter o valor para float

            # Verificar se é Débito ou Crédito
            if Tipo == "Débito":
                valor = -valor  # Tornar negativo para Débito

            # Somar ao total calculado
            total_calculado += valor

        # Exibir o total calculado
        print(f"Valor total do Webscrap encontrado R${total_calculado:.2f}")

    except Exception as e:
        print("Erro ao tentar processar os valores:", str(e))

    if totalValor == total_calculado:
        print("Perfeito, lançamentos estão OK")
    else:
        print("Valores não conferem! Revisar lançamentos.")





def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
