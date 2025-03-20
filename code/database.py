import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        """Inicializa a conexão com o banco de dados e cria as tabelas necessárias."""
        self.connection = sqlite3.connect('snake_game.db')
        self.cursor = self.connection.cursor()
        self._criar_tabelas()

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
            # Cria a tabela configuracoes
            self.cursor.execute('''
                CREATE TABLE configuracoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    velocidade INTEGER NOT NULL,
                    ultima_atualizacao DATETIME NOT NULL
                )
            ''')
            
            # Insere configuração padrão
            self.cursor.execute('''
                INSERT INTO configuracoes (velocidade, ultima_atualizacao)
                VALUES (?, ?)
            ''', (10, datetime.now()))

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

    def obter_melhores_pontuacoes(self, limite=10):
        """
        Retorna as melhores pontuações registradas.
        
        Args:
            limite: Número máximo de resultados a retornar
            
        Returns:
            list: Lista de tuplas (pontuacao, velocidade, data_hora, tempo_jogo)
        """
        self.cursor.execute('''
            SELECT pontuacao, velocidade, datetime(data_hora), tempo_jogo
            FROM historico_partidas
            ORDER BY pontuacao DESC
            LIMIT ?
        ''', (limite,))
        resultados = self.cursor.fetchall()
        
        # Converte as strings de data/hora em objetos datetime
        resultados_formatados = []
        for pontuacao, velocidade, data_hora_str, tempo_jogo in resultados:
            try:
                data_hora = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
                resultados_formatados.append((pontuacao, velocidade, data_hora, tempo_jogo))
            except ValueError:
                # Se houver erro na conversão, mantém a string original
                resultados_formatados.append((pontuacao, velocidade, data_hora_str, tempo_jogo))
        
        return resultados_formatados

    def salvar_velocidade(self, velocidade):
        """
        Salva a configuração de velocidade escolhida pelo usuário.
        
        Args:
            velocidade: Valor numérico da velocidade (8, 10 ou 12)
        """
        self.cursor.execute('''
            UPDATE configuracoes
            SET velocidade = ?, ultima_atualizacao = ?
            WHERE id = 1
        ''', (velocidade, datetime.now()))
        self.connection.commit()

    def obter_velocidade(self):
        """
        Retorna a última velocidade configurada.
        
        Returns:
            int: Valor da velocidade
        """
        self.cursor.execute('SELECT velocidade FROM configuracoes WHERE id = 1')
        return self.cursor.fetchone()[0]

    def fechar(self):
        """Fecha a conexão com o banco de dados."""
        self.connection.close() 