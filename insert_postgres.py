import psycopg2
import time

# Konfigurasi koneksi PostgreSQL
DB_NAME = "coppegadaian"
DB_USER = "postgres"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
CSV_FILE = "dummy_data.csv"  # Sesuaikan dengan path CSV

def connect_db():
    """Membuka koneksi ke PostgreSQL."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        print("Connected to PostgreSQL!")
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        exit(1)

def create_table(cursor):
    """Membuat tabel jika belum ada."""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS userspy (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT NOW(),
            price FLOAT,
            status VARCHAR(20),
            description TEXT
        )
        """
    )

def insert_data():
    """Mengimpor data dari CSV ke PostgreSQL menggunakan COPY."""
    conn = connect_db()
    cursor = conn.cursor()

    # Buat tabel jika belum ada
    create_table(cursor)
    conn.commit()
    print("Table users checked/created.")

    # Bersihkan tabel (Opsional: Hapus jika tidak ingin truncate data lama)
    cursor.execute("TRUNCATE TABLE userspy RESTART IDENTITY CASCADE")
    conn.commit()
    print("Table users truncated.")

    # Proses Insert
    print("Starting INSERT process using COPY...")
    start_time = time.time()

    try:
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            next(f)  # Skip header
            cursor.copy_expert(
                "COPY userspy(id,name, email, created_at, price, status, description) FROM STDIN WITH (FORMAT csv, HEADER true)", f
            )
        conn.commit()
        print("Insert completed using COPY!")

    except Exception as e:
        print("Error:", e)
        conn.rollback()

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    insert_data()
