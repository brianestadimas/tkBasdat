# get user object based on request token
#(this is because we dont impl correct auth (django's way)
# as its need for BASDAT secific requirement)

def generate_token(user_id):
    pass

# use bcrypt to decrypt token

def check_if_token_correct(token):
    pass

def get_user_based_on_token(token):
    pass


# TODO refactor this somewhere else
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]