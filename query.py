import psycopg2
from config import load_config

def get_vendors():
    """ Retrieve data from the vendors table """
    config  = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_name")
                print("The number of parts: ", cur.rowcount)
                
                # row = cur.fetchone()  # Lấy từng dòng
                # while row is not None:
                #     print(row)
                #     row = cur.fetchone()

                rows = cur.fetchall()  #Lấy tất cả các dòng
                for row in rows:
                    print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def iter_row(cursor, size=10): # Mỗi lần chỉ tải 10  dòng vào bộ nhớ giúp tiết kiệm tài nguyên
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row  # yield biến hàm này thành một generator, giúp tiết kiệm bộ nhớ vì nó không cần tải toàn bộ dữ liệu vào một lúc.
def get_part_vendors():
    """ Retrieve data from the vendors table """
    config  = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT part_name, vendor_name
                    FROM parts
                    INNER JOIN vendor_parts ON vendor_parts.part_id = parts.part_id
                    INNER JOIN vendors ON vendors.vendor_id = vendor_parts.vendor_id
                    ORDER BY part_name;
                """)
            
                for row in iter_row(cur, 10):
                    if not row:
                        print("Error!")
                    else:
                        print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)



if __name__ == '__main__':
    #get_vendors()
    get_part_vendors()