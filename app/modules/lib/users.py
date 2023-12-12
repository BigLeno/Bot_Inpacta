
from modules.lib.credentials import get_users_id, get_users_names

# para rodar localmente
# from credentials import get_users_id, get_users_names

from logging import warning, info

class User:
    def __init__(self, userid, username, privileges):
        self.id = userid
        self.name = username
        self.privileges = privileges

class Users:
    def __init__(self) -> None:
        info("Inicializando lista de usuários...")
        userid1, userid2, userid3, userid4, userid5, userid6 = get_users_id()
        username1, username2, username3, username4, username5, username6 = get_users_names()
        self.list_users = []
        self.add_users(User(userid1, username1, 'admin'))
        self.add_users(User(userid2, username2, 'user'))
        self.add_users(User(userid3, username3, 'user'))
        self.add_users(User(userid4, username4, 'user'))
        self.add_users(User(userid5, username5, 'coord'))
        self.add_users(User(userid6, username6, 'coord'))
        info("Lista de usuários inicializada com sucesso!")

    def add_users(self, user: User) -> None:
        if not isinstance(user, User):
            warning("Não foi possível adicionar os usuários.")
            return
        self.list_users.append(user)
        
