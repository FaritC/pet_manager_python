import mysql.connector

from Classes.clsDog import ClsDog
from Classes.clsReportByHealthStatus import ClsReportByHealthStatus
from Model.DbData import DbData


class ModelDog:
    def __init__(self):
        self.db_data = DbData()

    def _get_connection(self):
        return mysql.connector.connect(
            host=self.db_data.get_host(),
            port=self.db_data.get_port(),
            user=self.db_data.get_user(),
            password=self.db_data.get_password(),
            database=self.db_data.get_database(),
        )

    def create_pet(self, dog: ClsDog) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO tb_pet (code, name, born_year, color, health_status) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    dog.get_code(),
                    dog.get_name(),
                    dog.get_born_year(),
                    dog.get_color(),
                    dog.get_health_status(),
                ),
            )
            pet_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO tb_dog (breed, pedigree, id_pet) VALUES (%s, %s, %s)",
                (dog.get_breed(), dog.is_pedigree(), pet_id),
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def search_pet(self, code: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT p.id, p.code, p.name, p.born_year, p.color, "
                "p.health_status, d.id, d.breed, d.pedigree "
                "FROM tb_pet AS p INNER JOIN tb_dog AS d ON p.id = d.id_pet "
                "WHERE p.code = %s",
                (code,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return ClsDog(
                pet_id=row[0],
                code=row[1],
                name=row[2],
                born_year=row[3],
                color=row[4],
                health_status=row[5],
                dog_id=row[6],
                breed=row[7],
                pedigree=bool(row[8]),
            )
        finally:
            cursor.close()
            conn.close()

    def edit_pet(self, dog: ClsDog) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT 1 FROM tb_dog WHERE id = %s AND id_pet = %s",
                (dog.get_dog_id(), dog.get_pet_id()),
            )
            if cursor.fetchone() is None:
                conn.rollback()
                return False
            cursor.execute(
                "UPDATE tb_pet SET code = %s, name = %s, born_year = %s, "
                "color = %s, health_status = %s WHERE id = %s",
                (
                    dog.get_code(),
                    dog.get_name(),
                    dog.get_born_year(),
                    dog.get_color(),
                    dog.get_health_status(),
                    dog.get_pet_id(),
                ),
            )
            cursor.execute(
                "UPDATE tb_dog SET breed = %s, pedigree = %s WHERE id = %s",
                (dog.get_breed(), dog.is_pedigree(), dog.get_dog_id()),
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def delete_pet(self, dog: ClsDog) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM tb_dog WHERE id = %s AND id_pet = %s",
                (dog.get_dog_id(), dog.get_pet_id()),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                return False
            cursor.execute("DELETE FROM tb_pet WHERE id = %s", (dog.get_pet_id(),))
            if cursor.rowcount == 0:
                conn.rollback()
                return False
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def list_pet(self) -> list:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT p.id, p.code, p.name, p.born_year, p.color, "
                "p.health_status, d.id, d.breed, d.pedigree "
                "FROM tb_pet AS p INNER JOIN tb_dog AS d ON p.id = d.id_pet"
            )
            return [
                ClsDog(
                    pet_id=row[0],
                    code=row[1],
                    name=row[2],
                    born_year=row[3],
                    color=row[4],
                    health_status=row[5],
                    dog_id=row[6],
                    breed=row[7],
                    pedigree=bool(row[8]),
                )
                for row in cursor.fetchall()
            ]
        finally:
            cursor.close()
            conn.close()

    def list_dog_by_health_status(self) -> list:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT p.health_status, COUNT(*) "
                "FROM tb_pet AS p INNER JOIN tb_dog AS d ON p.id = d.id_pet "
                "GROUP BY p.health_status"
            )
            return [
                ClsReportByHealthStatus(status, amount)
                for status, amount in cursor.fetchall()
            ]
        finally:
            cursor.close()
            conn.close()
