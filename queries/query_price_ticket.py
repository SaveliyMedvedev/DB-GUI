from .connection import connection_decorator


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

