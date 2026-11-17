INDENT = "  "
COLUMN_GAP = "  "
RULE_CHARACTER = "-"
NO_RESULTS_TEXT = "(sin resultados)"
LIST_SEPARATOR = ", "

RATED_MOVIES_LABELS = {
    "movie_title": "pelicula",
    "genre_name": "genero",
    "rating_score": "puntaje",
}
SIMILAR_PEOPLE_LABELS = {
    "similar_name": "persona",
    "shared_count": "peliculas_en_comun",
    "shared_titles": "cuales",
}
RECOMMENDATION_LABELS = {
    "recommended_title": "pelicula",
    "recommended_by": "recomendada_por",
    "average_score": "promedio",
}


def format_cell(value):
    if isinstance(value, list):
        return LIST_SEPARATOR.join(sorted(value))
    return str(value)


def format_row(cells, widths):
    padded_cells = [cell.ljust(width) for cell, width in zip(cells, widths)]
    return (INDENT + COLUMN_GAP.join(padded_cells)).rstrip()


def print_table(title, records, column_labels):
    print(f"\n{title}")
    if not records:
        print(INDENT + NO_RESULTS_TEXT)
        return
    header_cells = list(column_labels.values())
    body_rows = [
        [format_cell(record[key]) for key in column_labels] for record in records
    ]
    widths = [
        max(len(cell) for cell in column) for column in zip(header_cells, *body_rows)
    ]
    print(format_row(header_cells, widths))
    print(format_row([RULE_CHARACTER * width for width in widths], widths))
    for row in body_rows:
        print(format_row(row, widths))
