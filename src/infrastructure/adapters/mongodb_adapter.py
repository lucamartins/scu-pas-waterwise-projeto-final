from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any

class MongoDBAdapter:
    def __init__(self, connection_string: str, database_name: str):
        """
        Inicializa o adaptador com a string de conexão e o nome do banco de dados.
        """
        self._client = AsyncIOMotorClient(connection_string)
        self._database = self._client[database_name]

    def get_database(self) -> Any:
        """
        Retorna a instância do banco de dados.
        """
        return self._database

    def get_collection(self, collection_name: str) -> Any:
        """
        Retorna a instância de uma coleção específica do banco de dados.
        """
        return self._database[collection_name]

    async def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self._client.close()
