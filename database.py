import pymysql

timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="interferon",
  host="mysql-398cba37-interferon-7.e.aivencloud.com",
  password="AVNS_dD6_gSj5Lmz2i0cI6D_",
  read_timeout=timeout,
  port=12182,
  user="avnadmin",
  write_timeout=timeout,
)

def load_encryption_types():
  with connection.cursor() as cursor:
    cursor.execute("select cte.enum_type, ct.crypt_type from cryptography_types_enum as cte join cryptography_types as ct on cte.id = ct.id where ct.id = 1")
    results = cursor.fetchall()

    for result in results:
      if "enum_type" in result and "crypt_type" in result:
        print(f"{result["enum_type"]}, {result["crypt_type"]}")

    return results
  