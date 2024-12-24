from db_connect import get_db_connection
import uuid

def submit_request(user_id, req_type, ticket_no, document_type, document_number, form_data):
    try:
        connection = get_db_connection()
        description = f"Document Type: {document_type}, {document_type} number: {document_number}, "
        description += ", ".join([f"{key}:{value}" for key, value in form_data.items()])
        req_id = str(uuid.uuid4())

        with connection.cursor() as cursor:
            query = """
                INSERT INTO service_requests (req_id, user_id, ticket_no, type, description)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (req_id, user_id, ticket_no, req_type, description))
            connection.commit()

            return {
                "message": "Form data successfully submitted",
                "req_bill": req_id,
                "ticket_no": ticket_no,
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        connection.close()
