RATED_MOVIES = """
MATCH (person:Person {name: $name})-[rating:RATED]->(movie:Movie)
      -[:IN_GENRE]->(genre:Genre)
RETURN movie.title AS movie_title,
       genre.name AS genre_name,
       rating.score AS rating_score
ORDER BY rating_score DESC, movie_title
"""

SIMILAR_TASTE_MATCH = """
MATCH (person:Person {name: $name})-[rating:RATED]->(movie:Movie)
      <-[peer_rating:RATED]-(peer:Person)
WHERE rating.score >= $min_score
  AND peer_rating.score >= $min_score
  AND peer <> person
"""

SIMILAR_PEOPLE = SIMILAR_TASTE_MATCH + """
RETURN peer.name AS similar_name,
       count(movie) AS shared_count,
       collect(movie.title) AS shared_titles
ORDER BY shared_count DESC, similar_name
"""

RECOMMENDATIONS = SIMILAR_TASTE_MATCH + """
WITH DISTINCT person, peer
MATCH (peer)-[liked:RATED]->(recommended:Movie)
WHERE liked.score >= $min_score
  AND NOT (person)-[:RATED]->(recommended)
RETURN recommended.title AS recommended_title,
       count(DISTINCT peer) AS recommended_by,
       round(avg(liked.score) * 10) / 10 AS average_score
ORDER BY recommended_by DESC, average_score DESC, recommended_title
LIMIT $limit
"""

PERSON_NAMES = """
MATCH (person:Person)
RETURN person.name AS person_name
ORDER BY person_name
"""

RESET_EXAMPLE_DATA = """
MATCH (node)
WHERE node:Person OR node:Movie OR node:Genre
DETACH DELETE node
"""
