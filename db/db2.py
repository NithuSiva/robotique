import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, table):
    try:
        c = conn.cursor()
        c.execute(table)
        c.close()
        print("Création de table avec succes !")
    except sqlite3.Error as e:
        print("err insert table :", e)

def insert_into_individu(database, nom, prenom):
    conn = create_connection(database)

    try: 
        c = conn.cursor()
        sql = "INSERT INTO individu (nom, prenom) VALUES(?, ?)"
        val = (nom, prenom)
        c.execute(sql, val)
        conn.commit()
        print("Enregistrement inséré avec succès dans la table !")
        c.close()
        conn.close()
        print("Connextion fermé !")
    except sqlite3.Error as e:
        print("err insert individu :", e)

def insert_into_images(database, imgs):

    conn = create_connection(database)
    print("IMAGE LIST", imgs)
    try: 
        cur = conn.cursor()
        sql = f"INSERT INTO images (nom_img, id_individu) VALUES('{imgs[0]}', {imgs[1]});"
        cur.execute(sql)
        conn.commit()
        print("Enregistrement inséré avec succès dans la table !")
        cur.close()
        conn.close()
        print("Connextion fermé !")
    except sqlite3.Error as e:
        print("err insert image :", e)

def creation_DB(database):

    conn = create_connection(database)


    individu = """CREATE TABLE individu(
        id_individu INTEGER PRIMARY KEY AUTOINCREMENT,
        prenom VARCHAR(50),
        nom VARCHAR(50)
        );"""
    image = """CREATE TABLE images(
        id_image INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_img VARCHAR(100),
        id_individu INT NOT NULL,
        FOREIGN KEY(id_individu) REFERENCES individu(id_individu)
        );"""
    # create a database connection
    cur = conn.cursor()
    # create tables
    if conn is not None:
        # create projects table on verifie si les tables existe 
        liste_table = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        # si les tables n'existe pas on va les creer 
        if not liste_table :
            # create tables
            create_table(conn, individu)
            create_table(conn, image)
        cur.close()
        conn.close()
    else:
        print("Error! cannot create the database connection.")

def voir_table_DB(database, table):
    
    conn = create_connection(database)

    try:
        if conn is not None:
            cur = conn.cursor()
            table_data = cur.execute(f"SELECT * FROM {table}").fetchall()
        cur.close()
        conn.close()
    except sqlite3.Error as e:
        print("err insert image :", e)

def get_invidivu_list(database):
    conn = create_connection(database)
    try:
        if conn is not None:
            cur = conn.cursor()
            table_data = cur.execute(f"SELECT * FROM individu").fetchall()
        cur.close()
        conn.close()
        return table_data
    except sqlite3.Error as e:
        print("err get individu list :", e)

def main():

    database = r"C:/Users/Ni2/Documents/M1_git/robotique/db/myDB.db"
    
    creation_DB(database)



# main()