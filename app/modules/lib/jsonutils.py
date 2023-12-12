
from json import load, dump
from logging import warning

class JsonUtils:

    @classmethod
    def write_json(cls, data, identificador, filename) -> str:
        """Função para escrever no arquivo json."""

        try:
            with open(filename, 'r') as file:
                file_data = load(file)
        except FileNotFoundError:
            warning("Não encontrei o arquivo 'cache.json'.")
            file_data = {}

        file_data[identificador] = data

        try:
            with open(filename, 'w') as file:
                dump(file_data, file)
        except FileNotFoundError:
            warning("Não encontrei o arquivo 'cache.json'.")
            return "Não encontrei o arquivo json."

    @classmethod
    def read_and_remove_first_item(cls, filename) -> tuple or str:
        """Função para ler e remover o primeiro item do arquivo json."""
        try:
            with open(filename, 'r+') as file:
                data = load(file)
                items = list(data.items())
                if len(items) == 0:
                    return "Não há mensagens para serem enviadas."
                first_item = items.pop(0)
                data = dict(items)
                file.seek(0)  # Move o cursor para o início do arquivo
                dump(data, file)
                file.truncate()  # Remove o restante do conteúdo do arquivo
        except FileNotFoundError:
            warning("Não encontrei o arquivo 'cache.json'.")
            return "Não encontrei o arquivo json."

        return first_item
