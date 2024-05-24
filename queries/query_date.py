from .connection import connection_decorator


@connection_decorator
def execute_query_date(connection, date):

    cursor = connection.cursor()
    query = f"""
    SELECT P.title, P.author, T.name_theater
    FROM Showings S
    JOIN Plays P ON S.play_id = P.play_id
    JOIN Theaters T ON S.theater_id = T.theater_id
    JOIN Show_dates D ON S.show_date_id = D.show_date_id
    WHERE D.showing_date = '{date}';
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return results

