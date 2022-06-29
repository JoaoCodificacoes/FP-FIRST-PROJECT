
def corrigir_palavra(palavra):
    """
     corrigir_palavra:cad.carateres -> cad.carateres
     A funcao corrigir_palavra transforma a palavra na palavra correta
    """
    outputlst = []
    for letra in palavra:
        if outputlst and (abs(ord(letra) - ord(outputlst[-1])) == 32):  # se seguida de uma letra maiscula,estiver
            # uma minuscula igual ou vice-versa
            outputlst.pop(-1)  # elimina-se a letra anterior da lista e passa-se a proxima letra
        else:
            outputlst.append(letra)
    palavra = ''.join(outputlst)
    return palavra


def eh_anagrama(cad1, cad2):
    """
    eh_anagrama:cad.carateres x cad.carateres -> booleano
    A funcao eh_anagrama verifica se os argumentos dados sao anagramas
    """
    cad1, cad2 = cad1.casefold(), cad2.casefold()
    lstcad1, lstcad2 = sorted(cad1), sorted(cad2)
    return lstcad1 == lstcad2


def remover_anagramas(anagramlst):
    """
    remover_anagramas:lista -> cad.carateres
    a funcao remover_anagrmas recebe uma lista de palavras e remove os anagramas nela contidos
    """

    count = 0
    outputlst = []
    for i in range(len(anagramlst) - 1):
        if count != 0:
            i += 1  # se a palavra anterior na lista tiver sido um anagrama com a seguinte,
            # este procedimento salta a palavra seguinte
        palavra1 = anagramlst[i]
        count = 0
        while i < len(anagramlst) - 1:
            i += 1
            palavra2 = anagramlst[i]
            if palavra1.casefold() != palavra2.casefold() and eh_anagrama(palavra1, palavra2):
                outputlst += [palavra2]
                count += 1  # faz saltar a proxima palavra

    corrigido = [palavra for palavra in anagramlst if palavra not in outputlst]  # remove os anagramas subsquentes
    return " ".join(corrigido)


def corrigir_doc(cadeia):
    """
    corrigir_doc:cad.carateres -> cad.carateres
    A funcao corrigir_doc recebe uma cadeia de carateres na qual retira os anagramas e corrije as palavras
    """

    if type(cadeia) != str or not cadeia.replace(" ", "").isalpha() or cadeia.count("  ") >= 1:
        raise ValueError("corrigir_doc: argumento invalido")
    cadeialst = cadeia.split()
    if len(cadeialst) < 1:
        raise ValueError("corrigir_doc: argumento invalido")
    anagramlst = []
    for palavra in cadeialst:
        if type(palavra) != str or len(palavra) < 1:
            raise ValueError("corrigir_doc: argumento invalido")
        anagramlst += [corrigir_palavra(palavra)]
    return remover_anagramas(anagramlst)


def obter_posicao(letra, n):
    """
    obter_posicao:cad.carateres x inteiro -> inteiro
    A funcao obter_posicao recebe um carater,responsavel pelo movimento, e um inteiro que corresponde a posicao atual.
    Esta devolve a posicao apos o movimento
    """
    if letra == "C" and n not in [1, 2, 3]:
        n -= 3
    elif letra == "B" and n not in [7, 8, 9]:
        n += 3
    elif letra == "E" and n not in [1, 4, 7]:
        n -= 1
    elif letra == "D" and n not in [3, 6, 9]:
        n += 1
    return n


def obter_digito(caracteres, n):
    """ obter_digito:cad.carateres x inteiro -> inteiro A funcao obter_digito recebe uma cadeia carateres
    responsavel pelos movimentos e o inteiro que corresponde a posicao atual.
    Esta devolve a posicao apos a sequencia de movimentos
    """
    for letra in caracteres:
        n = obter_posicao(letra, n)
    return n


def obter_pin(tuplo):
    """
    obter_pin:tuplo->tuplo A funcao obter_pin recebe um tuplo com sequencias de movimentos e
    devolve um tuplo de inteiros com a posicao apos cada sequencia de movimentos
    """
    if type(tuplo) != tuple or len(tuplo) < 4 or len(tuplo) > 10:
        raise ValueError("obter_pin: argumento invalido")

    n = 5
    tuplofinal = ()
    for seq in tuplo:
        if type(seq) != str or len(seq) < 1:
            raise ValueError("obter_pin: argumento invalido")
        for letra in seq:
            if letra not in ["C", "B", "D", "E"]:
                raise ValueError("obter_pin: argumento invalido")
        n = obter_digito(seq, n)
        tuplofinal += (n,)
    return tuplofinal


def eh_entrada(argumento):
    """
    eh_entrada:universal -> booleano
    A funcao eh_entrada verifica se o argumento recebido e uma entrada BDB
    """
    if type(argumento) != tuple or len(argumento) != 3:
        return False

    cifra = argumento[0]
    cifrareduzida = cifra.replace("-", "")  # filtra carateres desnecessarios da cifra
    if type(cifra) != str or cifra.count("--") >= 1 or not cifrareduzida.islower() or cifra[0] == "-" or \
            cifra[len(cifra) - 1] == "-" or cifra == "" or not cifrareduzida.isalpha():
        return False

    checksum = argumento[1]
    if type(checksum) != str or checksum[0] != "[" or checksum[len(checksum) - 1] != "]" or len(checksum) != 7:
        return False
    conteudo = checksum[1:len(checksum) - 1]  # filtra carateres desnecessarios do checksum
    if not conteudo.isalpha():
        return False

    tuplon = argumento[2]
    if type(tuplon) != tuple or len(tuplon) < 2:
        return False
    for numero in tuplon:
        if type(numero) != int or numero <= 0:
            return False
    return True


def cifraparacontrolo(conteudocifra):
    """
    cifraparacontrolo:cad.carateres->cad.carateres
    A funcao cifraparacontrolo recebe a cifra filtrada(apenas letras) e
    devolve o controlo filtrado(apenas letras)
    """
    dici = {}
    lst1 = []
    cifraord = sorted(conteudocifra)
    for letra in cifraord:
        if letra not in dici:
            dici[letra] = 1
        else:
            dici[letra] += 1
    while len(lst1) < 5:
        values = list(dici.values())
        keys = list(dici.keys())
        maior = keys[values.index(max(values))]  # Escolhe a chave com maior valor do dicionario
        lst1 += maior
        dici.pop(maior)  # remove a maior chave
    return "".join(lst1)


def validar_cifra(cifra, checksum):
    """
    validar:cifra:cad.carateres x cad.carateres -> booleano
    A funcao validar_cifra recebe uma cifra e uma sequencia de controlo e
    verifica se estas sao coerentes
    """
    conteudocifra = cifra.replace("-", "")
    conteudocontrolo = checksum[1:len(checksum) - 1]
    controlo = cifraparacontrolo(conteudocifra)
    return conteudocontrolo == controlo


def filtrar_bdb(lista):
    """
    filtrar_bdb:lista ->lista
    A funcao filtrar_bdb recebe uma lista de entradas BDB e
    devolve uma lista com as erradas
    """
    listanova = []
    if type(lista) != list or len(lista) < 1:
        raise ValueError("filtrar_bdb: argumento invalido")

    for entrada in lista:
        if not eh_entrada(entrada):
            raise ValueError("filtrar_bdb: argumento invalido")
        if not validar_cifra(entrada[0], entrada[1]):
            listanova += [entrada]
    return listanova


def obter_num_seguranca(tuplo):
    """
    obter_num_seguranca:tuplo -> inteiro
    A funcao num_seguranca recebe um tuplo e devolve o numero de seguranca
    """
    diferenca = max(tuplo)
    for index in range(1, len(tuplo)):
        num1 = tuplo[index]
        while index > 0:
            index -= 1
            num2 = tuplo[index]
            newdiferenca = abs(num1 - num2)
            if newdiferenca < diferenca:
                diferenca = newdiferenca
    return diferenca


def decifrar_texto(cadeia, n):
    """
    decifrar_texto:cad.carateres x inteiro -> cad.carateres
    A funcao decifrar_texto recebe uma cadeia de carateres e
    um numero de seguranca e devolve a cadeia de carateres decifrada
    """
    cadeia = cadeia.replace("-", " ")
    while n > 26:
        n -= 26  # retira ate n estar no espetro  0-26

    for letra in range(len(cadeia)):
        num = n
        if cadeia[letra] != " ":
            if letra % 2 == 0:
                if cadeia[letra] == "z":
                    num -= 1
                    cadeia = cadeia[:letra] + "a" + cadeia[letra + 1:]  # Visto que avança um lugar retira-se um ao num
                num += 1
            else:
                if cadeia[letra] == "a":
                    num += 1
                    cadeia = cadeia[:letra] + "z" + cadeia[letra + 1:]  # Visto que se recua um lugar adiciona-se um
                    # ao num
                num -= 1
            while ord(cadeia[letra]) + num > 122:  # se a soma ainda for maior que 122 retira-se 26 ao num
                num -= 26
            cadeia = cadeia[:letra] + chr(ord(cadeia[letra]) + num) + cadeia[letra + 1:]
    return cadeia


def decifrar_bdb(lista):
    """
    decifrar_bdb:lista ->lista
    A funcao decifrar_bdb recebe uma lista de entradas bdb e
    devolve uma lista com as cadeias de carateres decifradas
    """
    if type(lista) != list or len(lista) < 1:
        raise ValueError("decifrar_bdb: argumento invalido")
    lst = []
    for entrada in lista:
        if not eh_entrada(entrada):
            raise ValueError("decifrar_bdb: argumento invalido")
        lst += [decifrar_texto(entrada[0], obter_num_seguranca(entrada[2]))]
    return lst


def eh_utilizador(arg):
    """
    eh_utilizador:universal ->booleano
    A funcao eh_utilizador verifica se o argumento recebido e
    coerente com as regras necessarias para ser utilizador
    """
    if type(arg) is not dict or len(arg) != 3 or "name" not in arg.keys() \
            or "pass" not in arg.keys() or "rule" not in arg.keys() or type(arg["name"]) is not str \
            or type(arg["pass"]) is not str or len(arg["name"]) < 1 or len(arg["pass"]) < 1 \
            or type(arg["rule"]) is not dict:
        return False
    regras = arg["rule"]
    if "vals" not in regras.keys() or "char" not in regras.keys():
        return False
    valores = regras["vals"]
    char = regras["char"]
    if type(valores) is not tuple or type(char) is not str or len(valores) != 2 \
            or len(char) != 1 or valores[0] < 0 or valores[1] < 0 or valores[0] > valores[1]:
        return False
    return True


def eh_senha_valida(senha, regras):
    """
    eh_senha_valida:cad.carateres x dicionario ->booleano
    A funcao eh_senha_valida verifica se a senha recebida cumpre as regras recebidas e gerais.
    """
    countvogais = 0
    countconsecutivos = 0
    countletra = 0
    lastchar = None
    letra = regras["char"]
    min1 = regras["vals"][0]
    max1 = regras["vals"][1]

    for char in senha:
        if char in "aeiou" and countvogais < 3:
            countvogais += 1
        if char == lastchar and countconsecutivos < 1:
            countconsecutivos += 1
        lastchar = char
        if char == letra:
            countletra += 1
    return not (countvogais < 3 or countconsecutivos < 1 or countletra < min1 or countletra > max1)


def filtrar_senhas(lista):
    """
    filtrar_senhas:lista ->lista
    A funcao filtrar_senhas recebe uma lista de entradas BDB e
    devolve uma lista ordenada alfabeticamente das erradas.
    """
    outputlst = []
    if type(lista) is not list or len(lista) < 1:
        raise ValueError("filtrar_senhas: argumento invalido")
    for dicionario in lista:
        if not eh_utilizador(dicionario):
            raise ValueError("filtrar_senhas: argumento invalido")
        if not eh_senha_valida(dicionario["pass"], dicionario["rule"]):
            outputlst += [dicionario["name"]]

    return sorted(outputlst)
