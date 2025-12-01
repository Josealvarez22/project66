
from database.db_manager import DBManager
from views.main_window import MainWindow

if __name__ == "__main__":
    # base de datos y tablas
    db = DBManager()
    db.crear_tablas()

    # 2. Iniciar interfaz 
    app = MainWindow()
    app.mainloop()