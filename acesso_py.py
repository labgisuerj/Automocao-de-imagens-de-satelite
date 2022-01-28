import os.path
import os
import blowfish
import ast

#se o arquivo de login existe e o usuario diz que quer usar, lê arquivo
#se o arquivo não existe ou usuario nao quer usar o existente, então pede credenciais, pergunta se quer salvar no arquivo

def exists():
    diretorio = (os.path.dirname(os.path.realpath(__file__)))
    file_login = diretorio+"\logintest.txt"
    archive_login = os.path.exists(file_login)
    return archive_login

dictlogins = {}
login = '.'

def solicitar_credenciais():
    global login
    while login != "" and len(dictlogins) <= 3:
        login = input("Entre com seu login ou deixe vazio para prosseguir: ")
        if login != '':
            password = input("Entre com sua senha da USGS: ")
            dictlogins[login] = password 
    
    save_disc =  input("deseja salvar credenciais(S/N)?  ")
    if save_disc == "S":
        chave_cpt= input("Insira a chave para salvar os logins: ")
        
        gravar_credenciais(dictlogins,chave_cpt)
		
def recuperar_credencias(chave):
    contador=0
    credenciais_lidas = False
    diretorio = (os.path.dirname(os.path.realpath(__file__)))
    file_login = diretorio+"\logintest.txt"
    while not credenciais_lidas and contador<3:
        open_paste = open(file_login, "rb")
        paste = open_paste.read()
        cipher = blowfish.Cipher(chave.encode('utf8'))
        data_decrypted = b"".join(cipher.decrypt_ecb_cts(paste))
        print(data_decrypted)
       
			
        if data_decrypted[:4] == b"usgs":
            print("Login efetuado com sucesso!")
            credenciais_lidas= True
            

            credenciais_convert=(data_decrypted.decode('utf-8'))
            credenciais_convert = credenciais_convert.replace("usgs", "")
            print(credenciais_convert)
            row_credenciais = ast.literal_eval(str(credenciais_convert))
            print(row_credenciais)
            print(type(row_credenciais))
            print(row_credenciais.keys())
            login1= list(row_credenciais.keys())[0]
            senha1= row_credenciais[list(row_credenciais.keys())[0]]
            login2=list(row_credenciais.keys())[1]
            senha2= row_credenciais[list(row_credenciais.keys())[1]]
            login3=list(row_credenciais.keys())[2]
            senha3= row_credenciais[list(row_credenciais.keys())[2]]

            print(senha1)

            authentication = [login1, senha1, login2, senha2, login3, senha3]
            print(type(login1))
 
        else:
            print("chave errada")
            contador += 1
            data_decrypted = ""
            print("Senha incorreta, tente novamente")
				
    open_paste.close()	
      
    return authentication
	      
def gravar_credenciais(credenciais, cpt_chave):
    diretorio = (os.path.dirname(os.path.realpath(__file__)))
    file_login = diretorio+"\logintest.txt"
    paste_open = open(file_login, "wb")
    cipher = blowfish.Cipher(cpt_chave.encode('utf8'))
    content_cpt = b"usgs" + str(credenciais).encode('utf8')
    data_encrypted = b"".join(cipher.encrypt_ecb_cts(content_cpt))  
    paste_open.write(data_encrypted) 
    paste_open.close()

def inicializar_autenticacao():
    login_sucess = False
    login_valido = exists()
    if login_valido:
        arquivo_disco = input("Quer usar o arquivo salvo em sua máquina(S/N)?:  ")
         
        if arquivo_disco == "S":
            senha_cpt = input("Insira a chave para recuperar os logins: ")
            vericacao_acesso = recuperar_credencias(senha_cpt)
            dados=vericacao_acesso
            
            if vericacao_acesso == "":
                solicitar_credenciais()
                
            else:
                login_sucess = True
                                
    if not login_sucess:
        solicitar_credenciais()
       
    return dados
                