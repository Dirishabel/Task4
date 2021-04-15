import sqlite3
conn = sqlite3.connect('telegram_task.sqlite')
cursor = conn.cursor()
# cursor.execute("""
# CREATE TABLE Users (
#         UserID          INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_UserID PRIMARY KEY,
#         first_name      VARCHAR(50),
#         last_name       VARCHAR(50),
#         username        VARCHAR(50),
#         language        VARCHAR(4)
#    )""")
cursor.execute("""
CREATE TABLE Keywords (
        UserID          INT NOT NULL,
        keyword_name    VARCHAR(50)
   )""")
cursor.execute("""
CREATE TABLE Subscribes (
        UserID          INT NOT NULL,
        subscribe_name  VARCHAR(50),
        subscribe_id  VARCHAR(50)
   )""")
conn.close()