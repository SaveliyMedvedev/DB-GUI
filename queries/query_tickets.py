from .connection import connection_decorator


@connection_decorator
def execute_query_tickets(connection, play_id, date):

    cursor = connection.cursor()
    query = f"""
    SELECT COUNT(K.ticket_id) AS ticket_count, T.name_theater
    FROM Tickets K
    JOIN Showings S ON K.showing_id = S.showing_id
    JOIN Theaters T ON S.theater_id = T.theater_id
    JOIN Show_dates D ON S.show_date_id = D.show_date_id
    WHERE D.showing_date = '{date}' AND S.play_id = {play_id}
    GROUP BY T.name_theater;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return results

