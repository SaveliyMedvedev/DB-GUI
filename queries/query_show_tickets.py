from .connection import connection_decorator


@connection_decorator
def execute_query_show_tickets(connection):
    
    cursor = connection.cursor()
    query = f"""
    SELECT K.ticket_id, R.row_number_, P.title, P.author, D.showing_date, T.name_theater
    FROM Tickets K
    JOIN Rows_ R ON K.row_id = R.row_id
    JOIN Showings S ON K.showing_id = S.showing_id
    JOIN Plays P ON S.play_id = P.play_id
    JOIN Show_dates D ON S.show_date_id = D.show_date_id
    JOIN Theaters T ON S.theater_id = T.theater_id
    ORDER BY K.ticket_id;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return results
