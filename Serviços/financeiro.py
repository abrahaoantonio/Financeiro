from Database import crud
from datetime import date
from Database import database

##### Conta ######

def cadastrar_conta(nome, tipo, saldo=0):
    if not nome:
        raise ValueError('O nome da conta é obrigatório')
    if saldo is None:
        saldo = 0

    if saldo < 0: 
        raise ValueError('O saldo não pode ser negativo.')
    return crud.criar_conta(nome=nome,
                       tipo=tipo,
                       saldo=saldo)

def obter_contas():
    return crud.listar_contas()

def obter_conta(conta_id):
    conta = crud.buscar_conta(conta_id)

    if conta is None:
        raise ValueError('Conta não encontrada')
    return conta

def editar_conta(id, nome=None, tipo=None, saldo=None):

    obter_conta(id)

    if nome is not None and not nome:
        raise ValueError('O nome da conta não pode ser vazio.')

    if saldo is not None and saldo < 0:
        raise ValueError('O saldo não pode ser negativo.')

    return crud.atualizar_conta(id=id,
                           nome=nome,
                           tipo=tipo,
                           saldo=saldo)

def remover_conta(id):

    obter_conta(id)

    return crud.excluir_conta(id)


#### Categoria ####

def cadastrar_categoria (nome, tipo):
    if not nome:
        raise ValueError('O nome da categoria é obrigatório.')
    if not tipo:
        raise ValueError('O tipo da categoria é Obrigatório.')
    
    return crud.criar_categoria(nome=nome,
                           tipo=tipo)

def obter_categorias(categoria_id):

    return crud.listar_categorias()

def obter_categoria(categoria_id):

    categoria = crud.buscar_categoria(categoria_id)

    if categoria is None:
        raise ValueError('Categoria não encontrada')
    
    return categoria

def editar_categoria(id, nome=None, tipo=None):

    obter_categoria(id)

    if nome is not None and not nome:
        raise ValueError('O nome da categoria não pode ser vazio')

    return crud.atualizar_categoria(id=id,
                               nome=nome,
                               tipo=tipo)

def remover_categoria(id):

    obter_categoria(id)

    return crud.excluir_categoria(id)

# Transações #

def cadastrar_transacao(conta_id,categoria_id,descricao,valor,tipo,categoria,parcelas,data):

    if not conta_id:
        raise ValueError("A conta é obrigatória.")

    if not categoria_id:
        raise ValueError("A categoria é obrigatória.")

    if not descricao:
        raise ValueError("A descrição é obrigatória.")

    if valor is None or valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    if tipo not in ["entrada", "saida"]:
        raise ValueError("O tipo da transação deve ser 'entrada' ou 'saida'.")

    if parcelas is None:
        parcelas = 1

    return crud.criar_transacao(conta_id=conta_id,
        categoria_id=categoria_id,
        descricao=descricao,
        valor=valor,
        tipo=tipo,
        categoria=categoria,
        parcelas=parcelas,
        data=data)


def obter_transacoes():

    return crud.listar_transacoes()

def obter_transacao(transacao_id):

    transacao = crud.buscar_transacao(transacao_id)

    if transacao is None:
        raise ValueError('Transação não encontrada')

    return transacao

def editar_transacao(id,conta_id=None,categoria_id=None,descricao=None,valor=None,tipo=None,categoria=None,parcelas=None,data=None):

    obter_transacao(id)

    if valor is not None and valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    if tipo is not None and tipo not in ["entrada", "saida"]:
        raise ValueError("O tipo da transação deve ser 'entrada' ou 'saida'.")

    return crud.atualizar_transacao(id=id,
        conta_id=conta_id,
        categoria_id=categoria_id,
        descricao=descricao,
        valor=valor,
        tipo=tipo,
        categoria=categoria,
        parcelas=parcelas,
        data=data)

def remover_transacao(id):

    obter_transacao(id)

    return crud.excluir_transacao(id)


#### Cartão ####

def cadastrar_cartao(conta_id, categoria_id, descricao, valor, tipo, parcelas, data):

    if not conta_id:
        raise ValueError("A conta é obrigatória.")

    if valor is None or valor <= 0:  # <-- Valor não pode ser zero
        raise ValueError("O valor deve ser maior que zero.")

    if parcelas is None:
        parcelas = 1

    return crud.criar_cartao(conta_id=conta_id,
        categoria_id=categoria_id,
        descricao=descricao,
        valor=valor,
        tipo=tipo,
        parcelas=parcelas,
        data=data)

def obter_cartoes():

    return crud.listar_cartoes()

def obter_cartao(cartao_id):

    cartao = crud.buscar_cartao(cartao_id)

    if cartao is None:
        raise ValueError('Cartão não encontrado')
    
    return cartao

def editar_cartao(id,conta_id=None,categoria_id=None,descricao=None,valor=None,tipo=None,parcelas=None,data=None):

    obter_cartao(id)

    if valor is not None and valor <= 0:
        raise ValueError('O valor deve ser maior que zero')

    return crud.atualizar_cartao(id=id,
        conta_id=conta_id,
        categoria_id=categoria_id,
        descricao=descricao,
        valor=valor,
        tipo=tipo,
        parcelas=parcelas,
        data=data)

def remover_cartao(id):

    obter_cartao(id)

    return crud.excluir_cartao(id)

#### Faturas ####

def cadastrar_fatura(cartao_id,mes,ano,valor,data_vencimento,status):

    if not cartao_id:
        raise ValueError('O Cartão é obrigatório.')

    if valor is None or valor < 0:
        raise ValueError('O valor da fatura não pode ser negativo')

    return crud.criar_fatura(cartao_id=cartao_id,
        Mês=mes,
        ano=ano,
        Valor=valor,
        data_vencimento=data_vencimento,
        Status=status)

def obter_faturas():

    return crud.listar_faturas()

def obter_fatura(fatura_id):

    fatura = crud.buscar_fatura(fatura_id)

    if fatura is None: 
        raise ValueError('Fatura não encontrada')

    return fatura

def editar_fatura(id,cartao_id=None,mes=None,ano=None,valor=None,data_vencimento=None,status=None):

    obter_fatura(id)

    if valor is None or valor < 0:
        raise ValueError('O valor da fatura não pode ser negativo.')

    return crud.atualizar_fatura(id=id,
        cartao_id=cartao_id,
        Mês=mes,
        ano=ano,
        Valor=valor,
        data_vencimento=data_vencimento,
        Status=status)

def remover_fatura(id):

    obter_fatura(id)

    return crud.excluir_fatura(id)


#### Investimento #####

def cadastrar_investimento(nome,tipo,valor,transacao_id):

    if not nome:
        raise ValueError('O nome do investimento é obrigatório')

    if valor is None or valor <= 0: 
        raise ValueError('O valor tem que ser maior que zero.')

    return crud.criar_investimento(Nome=nome,
        Tipo=tipo,
        Valor=valor,
        transacao_id=transacao_id)

def obter_investimentos():

    return crud.listar_investimentos()

def obter_investimento(investimento_id):

    investimento = crud.buscar_investimento(investimento_id)

    if investimento is None:
        raise ValueError('Investimento não encontrado.')

    return investimento

def editar_investimento(id,nome=None,tipo=None,valor=None,transacao_id=None):

    obter_investimento(id)

    if valor is not None and valor <= 0:
        raise ValueError('O valor deve ser maior que zero.')

    return crud.atualizar_investimento(id=id,
        Nome=nome,
        Tipo=tipo,
        Valor=valor,
        transacao_id=transacao_id)

def remover_investimento(id):

    obter_investimento(id)

    return crud.excluir_investimento(id)


#### Regras ####

def calcular_saldo(receitas, despesas):

    Saldo = receitas - despesas

    return receitas - despesas

def calcular_saldo_conta(conta_id):

    conta = crud.buscar_conta(conta_id)

    if conta is None:
        raise ValueError('Conta não encontrada')

    transacoes = obter_transacoes()

    receitas = sum(float(t.valor) for t in transacoes if t.conta_id == conta_id and t.tipo == "entrada")

    despesas = sum(float(t.valor) for t in transacoes if t.conta_id == conta_id and t.tipo == "saida")

    return calcular_saldo(receitas, despesas)

def calcular_receit_mes(mes,ano):

    transacoes = obter_transacoes()

    total = 0

    for t in transacoes:
        if t.tipo != "entrada":
            continue

        data = t.data

        if hasattr(data, "year"):
            if data.month == mes and data.year == ano:
                total += float(t.valor)

            else:
                data = str(data)

                if data.startswith(f'{ano}-{mes:02d}'):
                    total += float(t.valor)

    return total

def calcular_gastos_mes(mes, ano):

    transacoes = obter_transacoes()

    total = 0

    for t in transacoes:
        if t.tipo != "saida":
            continue
        data = t.data

        if hasattr(data, "year"):
            if data.month == mes and data.year == ano:
                total += float(t.valor)

        else:
            data = str(data)

            if data.startswith(f'{ano}-{mes:02d}'):
                total += float(t.valor)

    return total

def calcular_saldo_mes(mes,ano):

    receitas = calcular_receit_mes(mes,ano)
    despesas = calcular_gastos_mes(mes,ano)

    return calcular_saldo(receitas,despesas)

def calcular_taxa_invest(receitas, despesas):

    if receitas <= 0:
        return 0
    saldo = calcular_saldo(receitas, despesas)

    return (saldo / receitas) * 100


### Regras faturas ###


def calcular_total_fatura(fatura_id):

    fatura = crud.buscar_fatura(fatura_id)

    if fatura is None:
        raise ValueError('Fatura não encontrada.')

    transacoes = crud.listar_transacoes(fatura_id)

    total = sum(transacao.valor for transacao in transacoes)

    return total

def fechar_fatura(fatura_id):

    fatura = crud.buscar_fatura(fatura_id)

    if fatura is None:
        raise ValueError('Fatura não encontrada.')

    if fatura.Status == "Fechada":
        raise ValueError('A fatura está fechada')

    if fatura.Status == "Paga":
        raise ValueError('Fatura paga.')

    total = calcular_total_fatura(fatura_id)

    return crud.atualizar_fatura(id=fatura_id,
                                 Valor=total,
                                 Status="Fechada")

def pagar_fatura(fatura_id):

    fatura = crud.buscar_fatura(fatura_id)

    if fatura is None:
        raise ValueError('Fatura não encontrada')

    if fatura.Status == "Paga":
        raise ValueError('A Fatura já foi paga')

    if fatura.Status != "Fechada":
        raise ValueError('A fatura precisa estar fechada para ser paga.')

    return crud.atualizar_fatura(id=fatura_id, Status="Paga")

def verificar_faturas_atrasadas():

    faturas = crud.listar_faturas()

    hoje = date.today()

    for fatura in faturas:
        if (fatura.data_vencimento < hoje and fatura.Status != "Paga" and fatura.Status !="Atrasada"):

            crud.atualizar_fatura(id=fatura.id, Status="Atrasada")

def obter_fatura_atual(cartao_id):
    faturas = crud.listar_faturas(cartao_id)

    for fatura in faturas:

        if fatura.Status == "Aberta":
            return fatura
        
    return None

def obter_proxima_fatura(cartao_id):
    faturas = crud.listar_faturas()

    faturas_cartao = [fatura for fatura in faturas if fatura.cartao_id == cartao_id]

    faturas_cartao.sort(key=lambda fatura:(
        int(fatura.ano),
        int(fatura.Mês)
    ))

    for i, fatura in enumerate(faturas_cartao):
        if fatura.Status == "Aberta":

            if i + 1 < len(faturas_cartao):
                return faturas_cartao[ i + 1]
            
            return None
        
        return None

#### Regras parcelamento ######




### PARCELAMENTO ####


def calcular_valor_parcela(valor_total, quantidade_parcelas):
    
    if quantidade_parcelas <= 0:
        return None

    return valor_total / quantidade_parcelas


def criar_parcelamento(descricao,valor_total,quantidade_parcelas,data_inicio,cartao_id=None,conta_id=None):

    valor_parcela = calcular_valor_parcela(valor_total,quantidade_parcelas)

    if valor_parcela is None:
        return None

    parcelamento = crud.criar_parcelamento(
        descricao=descricao,
        valor_total=valor_total,
        quantidade_parcelas=quantidade_parcelas,
        valor_parcela=valor_parcela,
        data_inicio=data_inicio,
        cartao_id=cartao_id,
        conta_id=conta_id
    )

    return parcelamento


def buscar_parcelamento(parcelamento_id):
    
    parcelamentos = crud.listar_parcelamentos()

    for parcelamento in parcelamentos:

        if parcelamento.id == parcelamento_id:
            return parcelamento

    return None


def atualizar_parcelamento(parcelamento_id,descricao=None,valor_total=None,quantidade_parcelas=None):

    parcelamento = buscar_parcelamento(parcelamento_id)

    if parcelamento is None:
        return None

    if descricao is not None:
        parcelamento.descricao = descricao

    if valor_total is not None:
        parcelamento.valor_total = valor_total

    if quantidade_parcelas is not None:
        parcelamento.quantidade_parcelas = quantidade_parcelas

    if (
        valor_total is not None
        or quantidade_parcelas is not None
    ):
        parcelamento.valor_parcela = (
            parcelamento.valor_total
            / parcelamento.quantidade_parcelas
        )

    return crud.atualizar_parcelamento(parcelamento)


def excluir_parcelamento(parcelamento_id):
    

    parcelamento = buscar_parcelamento(parcelamento_id)

    if parcelamento is None:
        return False

    crud.excluir_parcelamento(parcelamento_id)

    return True



#### PARCELAS ###


def calcular_parcelas_pendentes(parcelamento_id):
    
    parcelas = crud.listar_parcelas()

    parcelas_parcelamento = [parcela for parcela in parcelas if parcela.parcelamento_id == parcelamento_id]

    parcelas_pendentes = [
        parcela
        for parcela in parcelas_parcelamento
        if parcela.Status == "Pendente"
    ]

    return len(parcelas_pendentes)


def calcular_parcelas_pagas(parcelamento_id):

    parcelas = crud.listar_parcelas()

    parcelas_parcelamento = [
        parcela
        for parcela in parcelas
        if parcela.parcelamento_id == parcelamento_id
    ]

    parcelas_pagas = [
        parcela
        for parcela in parcelas_parcelamento
        if parcela.Status == "Pago"
    ]

    return len(parcelas_pagas)


def obter_proxima_parcela(parcelamento_id):

    parcelas = crud.listar_parcelas()

    parcelas_parcelamento = [parcela for parcela in parcelas if parcela.parcelamento_id == parcelamento_id]

    parcelas_parcelamento.sort(
        key=lambda parcela: parcela.numero)

    for parcela in parcelas_parcelamento:

        if parcela.Status == "Pendente":
            return parcela

    return None


def obter_ultima_parcela(parcelamento_id):
    

    parcelas = crud.listar_parcelas()

    parcelas_parcelamento = [
        parcela
        for parcela in parcelas
        if parcela.parcelamento_id == parcelamento_id
    ]

    parcelas_parcelamento.sort(
        key=lambda parcela: parcela.numero
    )

    if parcelas_parcelamento:
        return parcelas_parcelamento[-1]

    return None


def obter_parcela(parcelamento_id, numero):
    

    parcelas = crud.listar_parcelas()

    for parcela in parcelas:

        if (
            parcela.parcelamento_id == parcelamento_id
            and parcela.numero == numero
        ):
            return parcela

    return None


def pagar_parcela(parcela_id):
    

    parcelas = crud.listar_parcelas()

    for parcela in parcelas:

        if parcela.id == parcela_id:

            if parcela.Status == "Pago":
                return parcela

            parcela.Status = "Pago"

            return crud.atualizar_parcela(parcela)

    return None


def verificar_parcelamento_quitado(parcelamento_id):
    

    parcelas = crud.listar_parcelas()

    parcelas_parcelamento = [
        parcela
        for parcela in parcelas
        if parcela.parcelamento_id == parcelamento_id
    ]

    if not parcelas_parcelamento:
        return False

    for parcela in parcelas_parcelamento:

        if parcela.Status != "Pago":
            return False

    return True


def calcular_valor_pendente(parcelamento_id):
    

    parcelas = crud.listar_parcelas()

    parcelas_parcelamento = [
        parcela
        for parcela in parcelas
        if parcela.parcelamento_id == parcelamento_id
    ]

    valor_pendente = 0

    for parcela in parcelas_parcelamento:

        if parcela.Status == "Pendente":
            valor_pendente += parcela.valor

    return valor_pendente


def calcular_valor_pago(parcelamento_id):
    

    parcelas = crud.listar_parcelas()

    parcelas_parcelamento = [
        parcela
        for parcela in parcelas
        if parcela.parcelamento_id == parcelamento_id
    ]

    valor_pago = 0

    for parcela in parcelas_parcelamento:

        if parcela.Status == "Pago":
            valor_pago += parcela.valor

    return valor_pago


def cancelar_parcela(parcela_id):
    

    parcelas = crud.listar_parcelas()

    for parcela in parcelas:

        if parcela.id == parcela_id:

            parcela.Status = "Cancelada"

            return crud.atualizar_parcela(parcela)

    return None


def cancelar_parcelamento(parcelamento_id):
    

    parcelas = crud.listar_parcelas()

    parcelas_parcelamento = [
        parcela
        for parcela in parcelas
        if parcela.parcelamento_id == parcelamento_id
    ]

    for parcela in parcelas_parcelamento:

        if parcela.Status == "Pendente":
            parcela.Status = "Cancelada"

            crud.atualizar_parcela(parcela)

    return True






    





