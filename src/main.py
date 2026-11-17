import argparse
import sys

import config
import report
from database import MovieGraphRepository
from errors import (
    ConfigurationError,
    InvalidInputError,
    PersonNotFoundError,
    RecommenderError,
)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Recomendador de películas con Neo4j")
    parser.add_argument(
        "--name", default=config.DEFAULT_PERSON_NAME, help="persona a consultar"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="borra los datos de ejemplo antes de cargarlos",
    )
    return parser.parse_args()


def validate_person_name(raw_name):
    person_name = raw_name.strip()
    if not person_name:
        raise InvalidInputError("El nombre no puede estar vacío.")
    if len(person_name) > config.MAX_PERSON_NAME_LENGTH:
        raise InvalidInputError(
            f"El nombre no puede superar {config.MAX_PERSON_NAME_LENGTH} caracteres."
        )
    if not config.PERSON_NAME_PATTERN.fullmatch(person_name):
        raise InvalidInputError(
            "El nombre solo puede tener letras, espacios, apóstrofes y guiones."
        )
    return person_name


def read_seed_statements(seed_file_path):
    if not seed_file_path.is_file():
        raise ConfigurationError(
            f"No se encontró el archivo de datos: {seed_file_path}"
        )
    content = seed_file_path.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in content.split(";")]
    return [statement for statement in statements if statement]


def fetch_rated_movies_or_raise(repository, person_name):
    rated_movies = repository.fetch_rated_movies(person_name)
    if not rated_movies:
        known_names = ", ".join(repository.fetch_person_names())
        raise PersonNotFoundError(
            f"No hay datos de '{person_name}'. Personas disponibles: {known_names}"
        )
    return rated_movies


def show_report(repository, person_name):
    rated_movies = fetch_rated_movies_or_raise(repository, person_name)
    similar_people = repository.fetch_similar_people(person_name)
    recommendations = repository.fetch_recommendations(person_name)
    report.print_table(
        f"1) Películas que vio {person_name}", rated_movies, report.RATED_MOVIES_LABELS
    )
    report.print_table(
        f"2) Personas con gustos parecidos a {person_name}",
        similar_people,
        report.SIMILAR_PEOPLE_LABELS,
    )
    report.print_table(
        f"3) Recomendaciones para {person_name}",
        recommendations,
        report.RECOMMENDATION_LABELS,
    )


def run(arguments):
    person_name = validate_person_name(arguments.name)
    settings = config.load_settings()
    seed_statements = read_seed_statements(config.SEED_FILE_PATH)
    with MovieGraphRepository(settings) as repository:
        repository.verify_connection()
        print(f"Conectado a {settings.uri}")
        if arguments.reset:
            repository.reset_example_data()
            print("Datos de ejemplo anteriores eliminados.")
        repository.load_seed_data(seed_statements)
        print("Datos de ejemplo cargados.")
        show_report(repository, person_name)


def main():
    arguments = parse_arguments()
    try:
        run(arguments)
    except RecommenderError as error:
        sys.exit(f"Error: {error}")


if __name__ == "__main__":
    main()
