QUERIES={
    "select_user": """
        SELECT UserID FROM Users WHERE UserID = {0}
    """,
    'get_user_keywords': """
        SELECT keyword_name FROM Keywords WHERE UserID = {0}
    """,
    'get_user_subscribes': """
        SELECT subscribe_name FROM Subscribes WHERE UserID = {0}
    """,
    "insert_user": """
        INSERT INTO Users(UserID, first_name, last_name, username, language)
        VALUES({0}, '{1}', '{2}', '{3}', '{4}')
    """,
    'insert_keyword': """
        INSERT INTO Keywords(UserID, keyword_name)
        VALUES({0},'{1}')
    """,
    'is_user_keyword': """
        SELECT UserID FROM Keywords
        WHERE UserID = {0}
        AND keyword_name = '{1}'
    """,
    'add_subscribe': """
        INSERT INTO Subscribes (UserID, subscribe_name, subscribe_id)
        VALUES({0},'{1}','{2}')
    """,
    'is_user_subscribe': """
        SELECT UserID FROM Subscribes
        WHERE UserID = {0}
        AND subscribe_name = '{1}' 
    """,
    'delete_keyword': """
        DELETE FROM Keywords
        WHERE UserID={0}
        AND keyword_name = '{1}'
    """,
    'delete_subscribe': """
        DELETE FROM Subscribes
        WHERE UserID={0}
        AND subscribe_name = '{1}'
    """,
    'get_user_subscribe_id': """
        SELECT subscribe_id FROM Subscribes WHERE UserID = {0}
    """,
}