CREATE CONSTRAINT person_name_unique IF NOT EXISTS FOR (person:Person) REQUIRE person.name IS UNIQUE;

CREATE CONSTRAINT movie_title_unique IF NOT EXISTS FOR (movie:Movie) REQUIRE movie.title IS UNIQUE;

CREATE CONSTRAINT genre_name_unique IF NOT EXISTS FOR (genre:Genre) REQUIRE genre.name IS UNIQUE;

UNWIND [
  {title: 'Matrix', genre: 'Ciencia ficción'},
  {title: 'Inception', genre: 'Ciencia ficción'},
  {title: 'Interestelar', genre: 'Ciencia ficción'},
  {title: 'Coco', genre: 'Animación'},
  {title: 'Toy Story', genre: 'Animación'},
  {title: 'Titanic', genre: 'Romance'},
  {title: 'El Padrino', genre: 'Crimen'},
  {title: 'Parásitos', genre: 'Thriller'}
] AS row
MERGE (movie:Movie {title: row.title})
MERGE (genre:Genre {name: row.genre})
MERGE (movie)-[:IN_GENRE]->(genre);

UNWIND [
  {person: 'Ana', movie: 'Matrix', score: 5},
  {person: 'Ana', movie: 'Inception', score: 5},
  {person: 'Ana', movie: 'Interestelar', score: 4},
  {person: 'Luis', movie: 'Matrix', score: 5},
  {person: 'Luis', movie: 'Inception', score: 4},
  {person: 'Luis', movie: 'Interestelar', score: 5},
  {person: 'Luis', movie: 'Parásitos', score: 4},
  {person: 'Carlos', movie: 'Matrix', score: 4},
  {person: 'Carlos', movie: 'Interestelar', score: 5},
  {person: 'Carlos', movie: 'El Padrino', score: 5},
  {person: 'Sofía', movie: 'Inception', score: 5},
  {person: 'Sofía', movie: 'Parásitos', score: 5},
  {person: 'Sofía', movie: 'El Padrino', score: 3},
  {person: 'María', movie: 'Coco', score: 5},
  {person: 'María', movie: 'Toy Story', score: 5},
  {person: 'María', movie: 'Titanic', score: 4},
  {person: 'Diego', movie: 'Titanic', score: 5},
  {person: 'Diego', movie: 'Coco', score: 4},
  {person: 'Diego', movie: 'Toy Story', score: 4}
] AS row
MERGE (person:Person {name: row.person})
MERGE (movie:Movie {title: row.movie})
MERGE (person)-[rating:RATED]->(movie)
SET rating.score = row.score;
