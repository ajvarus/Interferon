import pymysql
import dotenv
import os

dotenv.load_dotenv()

timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db=os.getenv("DB_NAME"),
  host=os.getenv("DB_HOST"),
  password=os.getenv("DB_SECRET"),
  read_timeout=timeout,
  port=int(os.getenv("DB_PORT")),
  user=os.getenv("DB_USER"),
  write_timeout=timeout,
)

def load_cryptography_types():
  with connection.cursor() as cursor:
    cursor.execute("select id, crypt_type, display_name from cryptography_types")
    results = cursor.fetchall()
    return results

def load_selected_crypt_type(crypt_id):
  query = '''
    select id, crypt_type, display_name
    from cryptography_types
    where id = %s
  '''
  with connection.cursor() as cursor:
    cursor.execute(query, (crypt_id,))
    results = cursor.fetchall()
    return results[0]
  
def load_selected_enum_type(enum_id):
  query = '''
    select enum_id, id, enum_type
    from cryptography_types_enum
    where enum_id = %s
  '''
  with connection.cursor() as cursor:
    cursor.execute(query, (enum_id))
    results = cursor.fetchall()
    return results[0]

def load_crypt_type_enums(crypt_id):
  query = """
    select cte.enum_type, cte.enum_id, ct.crypt_type, ct.id
    from cryptography_types_enum as cte 
    join cryptography_types as ct 
    on cte.id = ct.id 
    where ct.id = %s
  """
  with connection.cursor() as cursor:
    cursor.execute(query, (crypt_id,))
    results = cursor.fetchall()

    return results