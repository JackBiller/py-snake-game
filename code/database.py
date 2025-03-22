import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        """Inicializa a conexão com o banco de dados e cria as tabelas necessárias."""
        self.connection = sqlite3.connect('snake_game.db')
        self.cursor = self.connection.cursor()
        self._criar_tabelas()
        
        # Inicializa as moedas se não existirem
        self.cursor.execute('SELECT COUNT(*) FROM configuracoes WHERE chave = "moedas"')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('INSERT INTO configuracoes (chave, valor) VALUES (?, ?)', ('moedas', '0'))
            self.connection.commit()

    def _criar_tabelas(self):
        """Cria as tabelas necessárias se não existirem."""
        # Verifica se a tabela historico_partidas existe
        self.cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='historico_partidas'
        ''')
        tabela_existe = self.cursor.fetchone() is not None

        if not tabela_existe:
            # Cria a tabela historico_partidas com a nova estrutura
            self.cursor.execute('''
                CREATE TABLE historico_partidas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pontuacao INTEGER NOT NULL,
                    velocidade TEXT NOT NULL,
                    data_hora DATETIME NOT NULL,
                    tempo_jogo INTEGER NOT NULL DEFAULT 0
                )
            ''')
        else:
            # Verifica se a coluna tempo_jogo existe
            self.cursor.execute('PRAGMA table_info(historico_partidas)')
            colunas = self.cursor.fetchall()
            tem_coluna_tempo = any(coluna[1] == 'tempo_jogo' for coluna in colunas)
            
            if not tem_coluna_tempo:
                # Cria uma tabela temporária com a nova estrutura
                self.cursor.execute('''
                    CREATE TABLE historico_partidas_temp (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pontuacao INTEGER NOT NULL,
                        velocidade TEXT NOT NULL,
                        data_hora DATETIME NOT NULL,
                        tempo_jogo INTEGER NOT NULL DEFAULT 0
                    )
                ''')
                
                # Copia os dados da tabela antiga para a nova
                self.cursor.execute('''
                    INSERT INTO historico_partidas_temp (pontuacao, velocidade, data_hora)
                    SELECT pontuacao, velocidade, data_hora FROM historico_partidas
                ''')
                
                # Remove a tabela antiga
                self.cursor.execute('DROP TABLE historico_partidas')
                
                # Renomeia a tabela temporária
                self.cursor.execute('ALTER TABLE historico_partidas_temp RENAME TO historico_partidas')

        # Verifica se a tabela configuracoes existe
        self.cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='configuracoes'
        ''')
        tabela_existe = self.cursor.fetchone() is not None

        if not tabela_existe:
            # Cria a tabela configuracoes com a nova estrutura
            self.cursor.execute('''
                CREATE TABLE configuracoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chave TEXT NOT NULL UNIQUE,
                    valor TEXT NOT NULL
                )
            ''')
            
            # Insere configurações padrão
            self.cursor.execute('''
                INSERT INTO configuracoes (chave, valor)
                VALUES 
                    ('velocidade', '10'),
                    ('moedas', '0')
            ''')
        else:
            # Verifica se a tabela tem a estrutura correta
            self.cursor.execute('PRAGMA table_info(configuracoes)')
            colunas = self.cursor.fetchall()
            tem_coluna_chave = any(coluna[1] == 'chave' for coluna in colunas)
            tem_coluna_valor = any(coluna[1] == 'valor' for coluna in colunas)
            
            if not (tem_coluna_chave and tem_coluna_valor):
                # Cria uma tabela temporária com a nova estrutura
                self.cursor.execute('''
                    CREATE TABLE configuracoes_temp (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chave TEXT NOT NULL UNIQUE,
                        valor TEXT NOT NULL
                    )
                ''')
                
                # Insere as configurações padrão
                self.cursor.execute('''
                    INSERT INTO configuracoes_temp (chave, valor)
                    VALUES 
                        ('velocidade', '10'),
                        ('moedas', '0')
                ''')
                
                # Remove a tabela antiga
                self.cursor.execute('DROP TABLE configuracoes')
                
                # Renomeia a tabela temporária
                self.cursor.execute('ALTER TABLE configuracoes_temp RENAME TO configuracoes')

        self.connection.commit()

    def salvar_partida(self, pontuacao, velocidade_texto, tempo_jogo):
        """
        Salva o resultado de uma partida no histórico.
        
        Args:
            pontuacao: Número de maçãs coletadas
            velocidade_texto: Texto indicando a velocidade (LENTO, MODERADO, RÁPIDO)
            tempo_jogo: Tempo de jogo em segundos
        """
        self.cursor.execute('''
            INSERT INTO historico_partidas (pontuacao, velocidade, data_hora, tempo_jogo)
            VALUES (?, ?, ?, ?)
        ''', (pontuacao, velocidade_texto, datetime.now(), tempo_jogo))
        self.connection.commit()

    def obter_melhores_pontuacoes(self, limite=9):
        """Obtém as melhores pontuações do histórico.
        
        Args:
            limite (int): Número máximo de resultados a retornar. Padrão é 9.
            
        Returns:
            list: Lista de tuplas (pontuacao, velocidade, data_hora, tempo_jogo)
        """
        self.cursor.execute('''
            SELECT pontuacao, velocidade, data_hora, tempo_jogo 
            FROM historico_partidas 
            ORDER BY pontuacao DESC, tempo_jogo ASC 
            LIMIT ?
        ''', (limite,))
        return self.cursor.fetchall()

    def salvar_velocidade(self, velocidade):
        """
        Salva a configuração de velocidade escolhida pelo usuário.
        
        Args:
            velocidade: Valor numérico da velocidade (8, 10 ou 12)
        """
        self.cursor.execute('''
            UPDATE configuracoes
            SET valor = ?
            WHERE chave = 'velocidade'
        ''', (str(velocidade),))
        self.connection.commit()

    def obter_velocidade(self):
        """
        Retorna a última velocidade configurada.
        
        Returns:
            int: Valor da velocidade
        """
        self.cursor.execute('SELECT valor FROM configuracoes WHERE chave = "velocidade"')
        return int(self.cursor.fetchone()[0])

    def fechar(self):
        """Fecha a conexão com o banco de dados."""
        self.connection.close()

    def calcular_moedas(self, pontuacao, velocidade):
        """Calcula quantas moedas o jogador ganhou baseado na pontuação e velocidade.
        
        Args:
            pontuacao (int): Número de maçãs coletadas
            velocidade (str): Velocidade do jogo ('LENTO', 'MODERADO' ou 'RÁPIDO')
            
        Returns:
            int: Número de moedas ganhas
        """
        # Define os pesos para cada velocidade
        pesos = {
            'LENTO': 1,
            'MODERADO': 2,
            'RÁPIDO': 3
        }
        
        # Calcula as moedas baseado na pontuação e velocidade
        moedas = pontuacao * pesos.get(velocidade, 1)
        return moedas

    def adicionar_moedas(self, moedas):
        """Adiciona moedas ao total do jogador.
        
        Args:
            moedas (int): Número de moedas a adicionar
        """
        self.cursor.execute('UPDATE configuracoes SET valor = CAST(valor AS INTEGER) + ? WHERE chave = "moedas"', (moedas,))
        self.connection.commit()

    def obter_moedas(self):
        """Obtém o total de moedas do jogador.
        
        Returns:
            int: Total de moedas
        """
        self.cursor.execute('SELECT valor FROM configuracoes WHERE chave = "moedas"')
        return int(self.cursor.fetchone()[0]) 