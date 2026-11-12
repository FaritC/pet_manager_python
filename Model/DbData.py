import os


class DbData:

    def __init__(self):
        self.__host = os.getenv("PET_DB_HOST", "localhost")
        self.__port = int(os.getenv("PET_DB_PORT", "3306"))
        self.__database = os.getenv("PET_DB_NAME", "administracionmascotasbd")
        self.__user = os.getenv("PET_DB_USER", "root")
        self.__password = os.getenv("PET_DB_PASSWORD", "")
        self.__driver = "mysql.connector"

    def get_driver(self) -> str:
        return self.__driver

    def get_host(self) -> str:
        return self.__host

    def get_port(self) -> int:
        return self.__port

    def get_database(self) -> str:
        return self.__database

    def get_user(self) -> str:
        return self.__user

    def get_password(self) -> str:
        return self.__password

    def get_url(self) -> str:
        return (
            f"mysql://{self.__user}:{self.__password}@{self.__host}:"
            f"{self.__port}/{self.__database}"
        )