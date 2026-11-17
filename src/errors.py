class RecommenderError(Exception):
    pass


class ConfigurationError(RecommenderError):
    pass


class InvalidInputError(RecommenderError):
    pass


class GraphDatabaseError(RecommenderError):
    pass


class PersonNotFoundError(RecommenderError):
    pass
