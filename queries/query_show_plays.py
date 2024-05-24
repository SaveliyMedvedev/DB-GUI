from .connection import connection_decorator


@connection_decorator
def show_plays(connection):

    cursor = connection.cursor()
    query = f"""
    SELECT *
    FROM Plays
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return results

