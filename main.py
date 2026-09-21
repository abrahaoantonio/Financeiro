import sys
from datetime import date

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QComboBox, QDateEdit, QDoubleSpinBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QPushButton, QStackedWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from models import Bancos, Conta, Historico, Investimento, Status, Tipos, criar_tabelas
from viwer import criar_conta, evolucao_investimentos, excluir_conta, excluir_investimento, gastos_por_categoria, investimentos_por_categoria, listar_contas, listar_investimentos, movimentar_dinheiro, proximo_id_conta, proximo_id_historico, proximo_id_investimento, registrar_investimento, resumo_entradas_saidas, total_contas, total_investimentos, transferir_saldo


class Grafico(FigureCanvas):
    def __init__(self):
        self.figura = Figure(figsize=(5, 3.2), tight_layout=True, facecolor="#ffffff")
        self.eixo = self.figura.add_subplot(111)
        super().__init__(self.figura)

    def sem_dados(self, titulo):
        self.eixo.clear()
        self.eixo.set_title(titulo)
        self.eixo.text(0.5, 0.5, "Ainda não há dados", ha="center", va="center")
        self.eixo.set_xticks([])
        self.eixo.set_yticks([])
        self.draw_idle()


class JanelaFinanceira(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Poupatonho")
        self.resize(1200, 820)
        self._aplicar_estilo()
        self._montar_interface()
        self.atualizar_tela()

    def _montar_interface(self):
        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        barra_lateral = QWidget()
        barra_lateral.setObjectName("barraLateral")
        barra_lateral.setFixedWidth(245)
        menu = QVBoxLayout(barra_lateral)
        menu.setContentsMargins(20, 28, 20, 24)
        menu.setSpacing(10)
        titulo = QLabel("POUPATONHO")
        titulo.setObjectName("tituloSistema")
        subtitulo = QLabel("Sua vida financeira,\nsob controle.")
        subtitulo.setObjectName("subtituloSistema")
        menu.addWidget(titulo)
        menu.addWidget(subtitulo)
        menu.addSpacing(28)

        self.paginas = QStackedWidget()
        paginas = [
            ("▦  Visão geral", self._aba_graficos()),
            ("▣  Bancos", self._aba_bancos()),
            ("↕  Movimentações", self._aba_movimentacoes()),
            ("◈  Investimentos", self._aba_investimentos()),
        ]
        self.botoes_navegacao = []
        for indice, (texto, pagina) in enumerate(paginas):
            botao = QPushButton(texto)
            botao.setProperty("navegacao", True)
            botao.setCheckable(True)
            botao.setCursor(Qt.CursorShape.PointingHandCursor)
            botao.clicked.connect(lambda _, i=indice: self.mudar_pagina(i))
            menu.addWidget(botao)
            self.botoes_navegacao.append(botao)
            self.paginas.addWidget(pagina)
        menu.addStretch()
        rodape = QLabel("Controle financeiro pessoal")
        rodape.setObjectName("rodape")
        menu.addWidget(rodape)

        conteudo = QWidget()
        conteudo_layout = QVBoxLayout(conteudo)
        conteudo_layout.setContentsMargins(30, 24, 30, 30)
        cabecalho = QHBoxLayout()
        self.total_label = QLabel()
        self.total_label.setObjectName("saldoTotal")
        atualizar = QPushButton("Atualizar")
        atualizar.clicked.connect(self.atualizar_tela)
        cabecalho.addWidget(self.total_label)
        cabecalho.addStretch()
        cabecalho.addWidget(atualizar)
        conteudo_layout.addLayout(cabecalho)
        conteudo_layout.addWidget(self.paginas)
        layout.addWidget(barra_lateral)
        layout.addWidget(conteudo)
        self.setCentralWidget(central)
        self.mudar_pagina(0)

    def mudar_pagina(self, indice):
        self.paginas.setCurrentIndex(indice)
        for posicao, botao in enumerate(self.botoes_navegacao):
            botao.setChecked(posicao == indice)

    def _aplicar_estilo(self):
        self.setStyleSheet("""
            QMainWindow { background: #f4f7fb; color: #24324a; }
            #barraLateral { background: #172a46; }
            #tituloSistema { color: #ffffff; font-size: 23px; font-weight: 800; letter-spacing: 1px; }
            #subtituloSistema { color: #a9b9d1; font-size: 12px; }
            #rodape { color: #7185a4; font-size: 10px; }
            #saldoTotal { color: #172a46; font-size: 22px; font-weight: 700; }
            #saldoInvestimentos { color: #376ee8; font-size: 20px; font-weight: 700; padding: 4px 0; }
            QPushButton {
                background: #376ee8; color: white; border: none; border-radius: 11px;
                min-height: 38px; padding: 0 16px; font-weight: 600;
            }
            QPushButton:hover { background: #285bd0; }
            QPushButton:pressed { background: #1f4ebc; }
            QPushButton[navegacao="true"] {
                background: transparent; color: #c8d5e9; text-align: left;
                border-radius: 12px; padding-left: 14px; font-weight: 600;
            }
            QPushButton[navegacao="true"]:hover { background: #243d61; color: white; }
            QPushButton[navegacao="true"]:checked { background: #376ee8; color: white; }
            QGroupBox { background: white; border: 1px solid #e1e8f2; border-radius: 14px; margin-top: 13px; padding: 15px 10px 10px; font-weight: 700; color: #24324a; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; }
            QLineEdit, QComboBox, QDoubleSpinBox, QDateEdit { background: #f8faff; border: 1px solid #d9e2ef; border-radius: 9px; min-height: 34px; padding: 0 8px; color: #24324a; }
            QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QDateEdit:focus { border: 2px solid #376ee8; }
            QTableWidget { background: white; border: 1px solid #e1e8f2; border-radius: 12px; gridline-color: #edf1f6; }
            QHeaderView::section { background: #edf3fb; color: #52647e; border: none; padding: 9px; font-weight: 700; }
            QLabel { color: #52647e; }
        """)

    def _aba_graficos(self):
        aba = QWidget()
        grade = QGridLayout(aba)
        self.grafico_fluxo, self.grafico_gastos, self.grafico_evolucao = Grafico(), Grafico(), Grafico()
        grade.addWidget(self._quadro("Entradas e saídas", self.grafico_fluxo), 0, 0)
        grade.addWidget(self._quadro("Gastos por categoria", self.grafico_gastos), 0, 1)
        grade.addWidget(self._quadro("Crescimento dos investimentos", self.grafico_evolucao), 1, 0, 1, 2)
        return aba

    def _aba_bancos(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)
        grade = QGridLayout()
        grupo_banco = QGroupBox("Criar banco")
        form_banco = QFormLayout(grupo_banco)
        self.banco_novo = QComboBox()
        for banco in Bancos:
            self.banco_novo.addItem(banco.value, banco)
        self.saldo_inicial = self._campo_valor()
        criar = QPushButton("Criar banco")
        criar.clicked.connect(self.criar_banco)
        form_banco.addRow("Banco:", self.banco_novo)
        form_banco.addRow("Saldo inicial:", self.saldo_inicial)
        form_banco.addRow(criar)
        grupo_rapido = QGroupBox("Registrar entrada ou saída")
        form_rapido = QFormLayout(grupo_rapido)
        self.conta_rapida, self.tipo_rapido, self.valor_rapido = QComboBox(), self._combo_tipos(), self._campo_valor()
        rapido = QPushButton("Registrar")
        rapido.clicked.connect(lambda: self.registrar_movimentacao("Sem categoria"))
        form_rapido.addRow("Conta:", self.conta_rapida)
        form_rapido.addRow("Tipo:", self.tipo_rapido)
        form_rapido.addRow("Valor:", self.valor_rapido)
        form_rapido.addRow(rapido)
        grupo_transferencia = QGroupBox("Transferência entre bancos")
        form_transferencia = QFormLayout(grupo_transferencia)
        self.conta_origem, self.conta_destino, self.valor_transferencia = QComboBox(), QComboBox(), self._campo_valor()
        transferir = QPushButton("Transferir")
        transferir.clicked.connect(self.transferir)
        form_transferencia.addRow("Origem:", self.conta_origem)
        form_transferencia.addRow("Destino:", self.conta_destino)
        form_transferencia.addRow("Valor:", self.valor_transferencia)
        form_transferencia.addRow(transferir)
        grade.addWidget(grupo_banco, 0, 0)
        grade.addWidget(grupo_rapido, 0, 1)
        grade.addWidget(grupo_transferencia, 0, 2)
        layout.addLayout(grade)
        self.tabela_contas = QTableWidget(0, 4)
        self.tabela_contas.setHorizontalHeaderLabels(["ID", "Banco", "Status", "Saldo"])
        self.tabela_contas.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela_contas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_contas.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(QLabel("Selecione uma conta para excluí-la (saldo zero e sem histórico)."))
        layout.addWidget(self.tabela_contas)
        excluir = QPushButton("Excluir banco selecionado")
        excluir.clicked.connect(self.excluir_banco)
        layout.addWidget(excluir, alignment=Qt.AlignmentFlag.AlignRight)
        return aba

    def _aba_movimentacoes(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)
        grupo = QGroupBox("Registrar movimentação com categoria")
        formulario = QFormLayout(grupo)
        self.conta_movimento, self.tipo_movimento = QComboBox(), self._combo_tipos()
        self.categoria_movimento = QComboBox()
        self.categoria_movimento.setEditable(True)
        self.categoria_movimento.addItems(["Salário", "Alimentação", "Moradia", "Transporte", "Lazer", "Saúde"])
        self.valor_movimento, self.data_movimento = self._campo_valor(), self._campo_data()
        registrar = QPushButton("Registrar movimentação")
        registrar.clicked.connect(lambda: self.registrar_movimentacao(self.categoria_movimento.currentText()))
        formulario.addRow("Conta:", self.conta_movimento)
        formulario.addRow("Tipo:", self.tipo_movimento)
        formulario.addRow("Categoria:", self.categoria_movimento)
        formulario.addRow("Valor:", self.valor_movimento)
        formulario.addRow("Data:", self.data_movimento)
        formulario.addRow(registrar)
        layout.addWidget(grupo)
        layout.addStretch()
        return aba

    def _aba_investimentos(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)
        self.saldo_investimentos_label = QLabel()
        self.saldo_investimentos_label.setObjectName("saldoInvestimentos")
        layout.addWidget(self.saldo_investimentos_label)
        grupo = QGroupBox("Registrar investimento")
        formulario = QFormLayout(grupo)
        self.nome_investimento, self.categoria_investimento = QComboBox(), QComboBox()
        for campo, valores in ((self.nome_investimento, ["Tesouro Direto", "CDB", "Ações", "ETF", "FII"]), (self.categoria_investimento, ["Renda fixa", "Ações", "Fundos imobiliários", "ETFs", "Criptoativos"])):
            campo.setEditable(True)
            campo.addItems(valores)
        self.valor_investimento, self.data_investimento = self._campo_valor(), self._campo_data()
        registrar = QPushButton("Registrar investimento")
        registrar.clicked.connect(self.registrar_investimento)
        formulario.addRow("Ativo:", self.nome_investimento)
        formulario.addRow("Categoria:", self.categoria_investimento)
        formulario.addRow("Valor aplicado:", self.valor_investimento)
        formulario.addRow("Data:", self.data_investimento)
        formulario.addRow(registrar)
        formulario.setVerticalSpacing(4)
        grupo.setMaximumWidth(390)
        grupo.setMaximumHeight(205)
        self.tabela_investimentos = QTableWidget(0, 4)
        self.tabela_investimentos.setHorizontalHeaderLabels(["ID", "Ativo", "Categoria", "Valor aplicado"])
        self.tabela_investimentos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela_investimentos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_investimentos.horizontalHeader().setStretchLastSection(True)
        self.tabela_investimentos.setMaximumHeight(155)
        vender = QPushButton("Vender / excluir investimento selecionado")
        vender.clicked.connect(self.vender_investimento)
        painel_vendas = QWidget()
        vendas_layout = QVBoxLayout(painel_vendas)
        vendas_layout.setContentsMargins(0, 0, 0, 0)
        vendas_layout.addWidget(QLabel("Selecione um investimento para registrar a venda."))
        vendas_layout.addWidget(self.tabela_investimentos)
        vendas_layout.addWidget(vender, alignment=Qt.AlignmentFlag.AlignRight)
        topo = QHBoxLayout()
        topo.addWidget(grupo)
        topo.addWidget(painel_vendas, 1)
        layout.addLayout(topo)
        grade = QGridLayout()
        self.grafico_aportes, self.grafico_carteira = Grafico(), Grafico()
        grade.addWidget(self._quadro("Aportes por investimento", self.grafico_aportes), 0, 0)
        grade.addWidget(self._quadro("Diversificação da carteira", self.grafico_carteira), 0, 1)
        layout.addLayout(grade)
        return aba

    @staticmethod
    def _quadro(titulo, conteudo):
        grupo = QGroupBox(titulo)
        layout = QVBoxLayout(grupo)
        layout.addWidget(conteudo)
        return grupo

    @staticmethod
    def _campo_valor():
        campo = QDoubleSpinBox()
        campo.setRange(0.01, 9_999_999.99)
        campo.setDecimals(2)
        campo.setPrefix("R$ ")
        return campo

    @staticmethod
    def _campo_data():
        campo = QDateEdit()
        campo.setDate(date.today())
        campo.setCalendarPopup(True)
        return campo

    @staticmethod
    def _combo_tipos():
        campo = QComboBox()
        campo.addItem("Entrada", Tipos.ENTRADA)
        campo.addItem("Saída", next(tipo for tipo in Tipos if tipo != Tipos.ENTRADA))
        return campo

    def criar_banco(self):
        try:
            criar_conta(Conta(id=proximo_id_conta(), banco=self.banco_novo.currentData(), status=Status.ATIVO, valor=self.saldo_inicial.value()))
            self.atualizar_tela()
        except Exception as erro:
            self._erro(erro)

    def excluir_banco(self):
        linha = self.tabela_contas.currentRow()
        if linha < 0:
            self._erro("Selecione um banco na tabela.")
            return
        if QMessageBox.question(self, "Excluir banco", "Deseja excluir o banco selecionado?") == QMessageBox.StandardButton.Yes:
            try:
                excluir_conta(int(self.tabela_contas.item(linha, 0).text()))
                self.atualizar_tela()
            except Exception as erro:
                self._erro(erro)

    def registrar_movimentacao(self, categoria):
        detalhada = categoria != "Sem categoria"
        conta = self.conta_movimento if detalhada else self.conta_rapida
        tipo = self.tipo_movimento if detalhada else self.tipo_rapido
        valor = self.valor_movimento if detalhada else self.valor_rapido
        data_registro = self.data_movimento.date().toPython() if detalhada else date.today()
        if not categoria.strip():
            self._erro("Informe uma categoria.")
            return
        try:
            movimentar_dinheiro(Historico(id=proximo_id_historico(), conta_id=conta.currentData(), categoria=categoria.strip(), tipo=tipo.currentData(), valor=valor.value(), data=data_registro))
            self.atualizar_tela()
        except Exception as erro:
            self._erro(erro)

    def transferir(self):
        try:
            if self.conta_origem.currentData() == self.conta_destino.currentData():
                raise ValueError("Selecione bancos diferentes.")
            transferir_saldo(self.conta_origem.currentData(), self.conta_destino.currentData(), self.valor_transferencia.value())
            self.atualizar_tela()
        except Exception as erro:
            self._erro(erro)

    def registrar_investimento(self):
        nome, categoria = self.nome_investimento.currentText().strip(), self.categoria_investimento.currentText().strip()
        if not nome or not categoria:
            self._erro("Informe o ativo e a categoria.")
            return
        try:
            registrar_investimento(Investimento(id=proximo_id_investimento(), nome=nome, categoria=categoria, valor=self.valor_investimento.value(), data=self.data_investimento.date().toPython()))
            self.atualizar_tela()
        except Exception as erro:
            self._erro(erro)

    def vender_investimento(self):
        linha = self.tabela_investimentos.currentRow()
        if linha < 0:
            self._erro("Selecione um investimento na tabela.")
            return
        resposta = QMessageBox.question(
            self, "Vender investimento", "Confirma a venda e remoção do investimento selecionado?"
        )
        if resposta == QMessageBox.StandardButton.Yes:
            try:
                id_investimento = int(self.tabela_investimentos.item(linha, 0).text())
                excluir_investimento(id_investimento)
                self.atualizar_tela()
            except Exception as erro:
                self._erro(erro)

    def atualizar_tela(self):
        contas = listar_contas()
        self.total_label.setText(f"Saldo em bancos: R$ {total_contas():,.2f}")
        self.saldo_investimentos_label.setText(f"Saldo total investido: R$ {total_investimentos():,.2f}")
        self._atualizar_combos_contas(contas)
        self._atualizar_tabela_investimentos()
        self.tabela_contas.setRowCount(len(contas))
        for linha, conta in enumerate(contas):
            for coluna, valor in enumerate([str(conta.id), conta.banco.value, conta.status.value, f"R$ {conta.valor:,.2f}"]):
                item = QTableWidgetItem(valor)
                if coluna in (0, 3):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.tabela_contas.setItem(linha, coluna, item)
        self._desenhar_graficos()

    def _atualizar_tabela_investimentos(self):
        investimentos = listar_investimentos()
        self.tabela_investimentos.setRowCount(len(investimentos))
        for linha, investimento in enumerate(investimentos):
            valores = [
                str(investimento.id), investimento.nome, investimento.categoria,
                f"R$ {investimento.valor:,.2f}",
            ]
            for coluna, valor in enumerate(valores):
                self.tabela_investimentos.setItem(linha, coluna, QTableWidgetItem(valor))

    def _atualizar_combos_contas(self, contas):
        for combo in (self.conta_rapida, self.conta_movimento, self.conta_origem, self.conta_destino):
            atual = combo.currentData()
            combo.clear()
            for conta in contas:
                if conta.status == Status.ATIVO:
                    combo.addItem(f"{conta.banco.value} — ID {conta.id}", conta.id)
            indice = combo.findData(atual)
            combo.setCurrentIndex(indice if indice >= 0 else 0)

    def _desenhar_graficos(self):
        totais = resumo_entradas_saidas()
        eixo = self.grafico_fluxo.eixo
        eixo.clear()
        eixo.bar(totais.keys(), totais.values(), color=["#2e8b57", "#c0392b"])
        eixo.set_title("Entradas e saídas")
        eixo.set_ylabel("R$")
        self.grafico_fluxo.draw_idle()
        self._rosca(self.grafico_gastos, gastos_por_categoria(), "Gastos por categoria")
        evolucao = evolucao_investimentos()
        if not evolucao:
            self.grafico_evolucao.sem_dados("Crescimento dos investimentos")
        else:
            eixo = self.grafico_evolucao.eixo
            eixo.clear()
            eixo.plot([item[0] for item in evolucao], [item[1] for item in evolucao], marker="o", color="#2874a6")
            eixo.set_title("Crescimento dos investimentos")
            eixo.set_ylabel("Valor acumulado (R$)")
            eixo.tick_params(axis="x", rotation=30)
            self.grafico_evolucao.draw_idle()
        investimentos = listar_investimentos()
        if not investimentos:
            self.grafico_aportes.sem_dados("Aportes por investimento")
        else:
            eixo = self.grafico_aportes.eixo
            eixo.clear()
            eixo.bar([item.nome for item in investimentos], [item.valor for item in investimentos], color="#8e44ad")
            eixo.set_title("Aportes por investimento")
            eixo.set_ylabel("R$")
            eixo.tick_params(axis="x", rotation=30)
            self.grafico_aportes.draw_idle()
        self._rosca(self.grafico_carteira, investimentos_por_categoria(), "Diversificação da carteira")

    @staticmethod
    def _rosca(grafico, dados, titulo):
        if not dados:
            grafico.sem_dados(titulo)
            return
        grafico.eixo.clear()
        grafico.eixo.pie(dados.values(), labels=dados.keys(), autopct="%1.1f%%", wedgeprops={"width": 0.45})
        grafico.eixo.set_title(titulo)
        grafico.draw_idle()

    def _erro(self, mensagem):
        QMessageBox.warning(self, "Não foi possível concluir", str(mensagem))


if __name__ == "__main__":
    criar_tabelas()
    aplicativo = QApplication(sys.argv)
    janela = JanelaFinanceira()
    janela.show()
    sys.exit(aplicativo.exec())
