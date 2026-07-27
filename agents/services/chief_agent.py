from .router import route_query


def handle_query(question):
    return route_query(question)