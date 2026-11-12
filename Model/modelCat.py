import mysql.connector

from Classes.clsCat import ClsCat
from Classes.clsReportByHealthStatus import ClsReportByHealthStatus
from Model.DbData import DbData


class ModelCat:
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

    @staticmethod
    def _cat_from_row(row) -> ClsCat:
        return ClsCat(
            pet_id=row[0],
            code=row[1],
            name=row[2],
            born_year=row[3],
            color=row[4],
            health_status=row[5],
            cat_id=row[6],
            breed=row[7],
        )

    def create_pet(self, cat: ClsCat) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO tb_pet (code, name, born_year, color, health_status) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    cat.get_code(),
                    cat.get_name(),
                    cat.get_born_year(),
                    cat.get_color(),
                    cat.get_health_status(),
                ),
            )
            pet_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO tb_cat (breed, id_pet) VALUES (%s, %s)",
                (cat.get_breed(), pet_id),
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
                "p.health_status, c.id, c.breed "
                "FROM tb_pet AS p INNER JOIN tb_cat AS c ON p.id = c.id_pet "
                "WHERE p.code = %s",
                (code,),
            )
            row = cursor.fetchone()
            return self._cat_from_row(row) if row is not None else None
        finally:
            cursor.close()
            conn.close()

    def edit_pet(self, cat: ClsCat) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT 1 FROM tb_cat WHERE id = %s AND id_pet = %s",
                (cat.get_cat_id(), cat.get_pet_id()),
            )
            if cursor.fetchone() is None:
                conn.rollback()
                return False
            cursor.execute(
                "UPDATE tb_pet SET code = %s, name = %s, born_year = %s, "
                "color = %s, health_status = %s WHERE id = %s",
                (
                    cat.get_code(),
                    cat.get_name(),
                    cat.get_born_year(),
                    cat.get_color(),
                    cat.get_health_status(),
                    cat.get_pet_id(),
                ),
            )
            cursor.execute(
                "UPDATE tb_cat SET breed = %s WHERE id = %s",
                (cat.get_breed(), cat.get_cat_id()),
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def delete_pet(self, cat: ClsCat) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM tb_cat WHERE id = %s AND id_pet = %s",
                (cat.get_cat_id(), cat.get_pet_id()),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                return False
            cursor.execute("DELETE FROM tb_pet WHERE id = %s", (cat.get_pet_id(),))
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
                "p.health_status, c.id, c.breed "
                "FROM tb_pet AS p INNER JOIN tb_cat AS c ON p.id = c.id_pet"
            )
            return [self._cat_from_row(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def list_pet_by_health_status(self) -> list:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT health_status, COUNT(*) FROM tb_pet GROUP BY health_status"
            )
            return [
                ClsReportByHealthStatus(status, amount)
                for status, amount in cursor.fetchall()
            ]
        finally:
            cursor.close()
            conn.close()

    def list_cat_by_health_status(self) -> list:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT p.health_status, COUNT(*) "
                "FROM tb_pet AS p INNER JOIN tb_cat AS c ON p.id = c.id_pet "
                "GROUP BY p.health_status"
            )
            return [
                ClsReportByHealthStatus(status, amount)
                for status, amount in cursor.fetchall()
            ]
        finally:
            cursor.close()
            conn.close()
