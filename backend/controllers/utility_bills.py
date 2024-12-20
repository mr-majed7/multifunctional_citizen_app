from db_connect import get_db_connection


def fetch_bills(nid_number):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM utility_bills WHERE nid_number = %s", (nid_number,))
            bills = cursor.fetchall()

            return bills, None

    except Exception as e:
        return None, str(e)

    finally:
        connection.close()


def update_bill_status(bill_id,status):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE utility_bills SET status = %s WHERE bill_id = %s",
                (status, bill_id)
            )
            connection.commit()

            if cursor.rowcount == 0:
                return "Bill not found or status unchanged", 404

            return "Bill status updated successfully", 200

    except Exception as e:
        return str(e), 500

    finally:
        connection.close()
    