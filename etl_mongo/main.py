from db import MongoConnection
from etl import Transformer
from config import Config
from etl import Extractor
from etl import Loader


def main():
    # Extraindo os dados da fonte
    extracted_data = Extractor.from_csv(Config.input_file)

    # Transformando os dados
    transformed_data = Transformer.clean_data(extracted_data)

    # Criando a conexão com o banco MongoDB
    mongo_connection = MongoConnection(
        Config.mongo_uri, Config.db_name, Config.collection_name
    )
    mongo_connection.connect()

    # Carregando os dados para o destino
    loader = Loader(mongo_connection)
    loader.load_to_mongo(transformed_data)

    # Fechando a conexão
    mongo_connection.close()


if __name__ == "__main__":
    main()
