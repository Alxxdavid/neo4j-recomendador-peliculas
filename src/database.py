from neo4j import GraphDatabase
from neo4j.exceptions import DriverError, Neo4jError

import config
import queries
from errors import GraphDatabaseError


class MovieGraphRepository:
    def __init__(self, settings):
        self._database = settings.database
        try:
            self._driver = GraphDatabase.driver(
                settings.uri, auth=(settings.username, settings.password)
            )
        except (DriverError, ValueError) as error:
            raise GraphDatabaseError(f"URI de conexión no válido: {error}") from error

    def __enter__(self):
        return self

    def __exit__(self, *exception_details):
        self._driver.close()

    def verify_connection(self):
        try:
            self._driver.verify_connectivity()
        except (DriverError, Neo4jError) as error:
            raise GraphDatabaseError(
                f"No se pudo conectar a la base de datos: {error}"
            ) from error

    def load_seed_data(self, statements):
        for statement in statements:
            self._execute(statement)

    def reset_example_data(self):
        self._execute(queries.RESET_EXAMPLE_DATA)

    def fetch_person_names(self):
        records = self._execute(queries.PERSON_NAMES)
        return [record["person_name"] for record in records]

    def fetch_rated_movies(self, person_name):
        return self._execute(queries.RATED_MOVIES, {"name": person_name})

    def fetch_similar_people(self, person_name):
        parameters = {"name": person_name, "min_score": config.MINIMUM_LIKED_SCORE}
        return self._execute(queries.SIMILAR_PEOPLE, parameters)

    def fetch_recommendations(self, person_name):
        parameters = {
            "name": person_name,
            "min_score": config.MINIMUM_LIKED_SCORE,
            "limit": config.MAX_RECOMMENDATIONS,
        }
        return self._execute(queries.RECOMMENDATIONS, parameters)

    def _execute(self, statement, parameters=None):
        try:
            with self._driver.session(database=self._database) as session:
                result = session.run(statement, parameters)
                return [record.data() for record in result]
        except (DriverError, Neo4jError) as error:
            raise GraphDatabaseError(
                f"Falló la operación en la base de datos: {error}"
            ) from error
