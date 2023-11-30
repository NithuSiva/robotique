import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)
        
def main():
    database = r"C:/Users/Ni2/Documents/M1_git/robotique/db/face_reco.db"

    individu = """CREATE TABLE individu(
                                        id_individu INT AUTO_INCREMENT,
                                        prenom VARCHAR(50),
                                        nom VARCHAR(50),
                                        PRIMARY KEY(id_individu)
                                );"""

    image = """CREATE TABLE image(
                                    id_image INT AUTO_INCREMENT,
                                    chemin VARCHAR(100),
                                    date_creation DATETIME,
                                    id_individu INT NOT NULL,
                                    PRIMARY KEY(id_image),
                                    FOREIGN KEY(id_individu) REFERENCES individu(id_individu)
                                );"""

    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()
    # create tables
    if conn is not None:
        # create projects table
        liste_table = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print("Liste : ", liste_table)
        create_table(conn, individu)

        # create tasks table
        create_table(conn, image)
    else:
        print("Error! cannot create the database connection.")

main()