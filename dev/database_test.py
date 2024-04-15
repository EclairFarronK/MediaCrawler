import mysql.connector

# 建立数据库连接
conn = mysql.connector.connect(
    host="43.156.129.154",
    user="tsp",
    password="199409_ad",
    database="tsp"
)

# 获取游标
cursor = conn.cursor()
sql = "INSERT INTO bvid (user_id, name,bvid) VALUES (%s, %s, %s)"
data = [

]

# 批量执行SQL语句
cursor.executemany(sql, data)

conn.commit()
# 关闭游标和连接
cursor.close()
conn.close()
