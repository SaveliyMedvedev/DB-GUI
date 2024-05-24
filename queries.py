from connection import connection_decorator


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


@connection_decorator
def execute_query_price_ticket(connection, ticket_id):

    cursor = connection.cursor()
    query = f"""
    SELECT R.price
    FROM Tickets T
    JOIN Rows_ R ON T.row_id = R.row_id
    WHERE T.ticket_id = {ticket_id};
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return results


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
