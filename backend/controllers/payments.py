from db_connect import get_db_connection

def add_payment_details(payment_details):
    payment_id = payment_details.get('payment_id')
    payment_type = payment_details.get('type')
    amount = payment_details.get('amount')
    date = payment_details.get('date')
    time = payment_details.get('time')
    cardholders_name = payment_details.get('cardholders_name')
    card_number = payment_details.get('card_number')

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO payments (payment_id, type, amount, date, time, cardholders_name, card_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (payment_id, payment_type, amount, date, time, cardholders_name, card_number))
            connection.commit()

        return {'message': 'Payment stored successfully'}, 201

    except Exception as e:
        return {'error': str(e)}, 500

    finally:
        connection.close()
