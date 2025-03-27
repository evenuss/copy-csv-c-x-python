#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <libpq-fe.h>

void check_exec_status(PGconn *conn, PGresult *res, const char *message) {
    if (PQresultStatus(res) != PGRES_COMMAND_OK) {
        fprintf(stderr, "ERROR: %s: %s\n", message, PQerrorMessage(conn));
        PQclear(res);
        PQfinish(conn);
        exit(1);
    }
}

int main() {
    // Catat waktu mulai
    clock_t start_time = clock();

    PGconn *conn = PQconnectdb("dbname=coppegadaian user=postgres password=admin host=localhost");
    
    if (PQstatus(conn) != CONNECTION_OK) {
        fprintf(stderr, "Connection failed: %s\n", PQerrorMessage(conn));
        PQfinish(conn);
        return 1;
    }
    printf("Connected to PostgreSQL!\n");

    // Pastikan tabel sudah ada
    PGresult *res = PQexec(conn, 
        "CREATE TABLE IF NOT EXISTS users ("
        "id SERIAL PRIMARY KEY, "
        "name VARCHAR(50), "
        "email VARCHAR(100), "
        "created_at TIMESTAMP, "
        "price FLOAT, "
        "status VARCHAR(20), "
        "description TEXT)"
    );
    check_exec_status(conn, res, "Table creation failed");
    PQclear(res);

    printf("Starting INSERT process using COPY...\n");

    // Load CSV dari file Python
    char copy_sql[512];
    snprintf(copy_sql, sizeof(copy_sql), 
        "COPY users (id,name, email, created_at, price, status, description) "
        "FROM STDIN WITH (FORMAT csv, HEADER true)");

    res = PQexec(conn, copy_sql);
    if (PQresultStatus(res) != PGRES_COPY_IN) {
        fprintf(stderr, "COPY command failed: %s\n", PQerrorMessage(conn));
        PQclear(res);
        PQfinish(conn);
        return 1;
    }
    PQclear(res);

    // Kirim data dari file CSV ke PostgreSQL
    FILE *csv = fopen("clean_data.csv", "r");
    if (!csv) {
        fprintf(stderr, "Error opening CSV file.\n");
        PQfinish(conn);
        return 1;
    }

    char buffer[8192];
    while (fgets(buffer, sizeof(buffer), csv)) {
        if (PQputCopyData(conn, buffer, strlen(buffer)) != 1) {
            fprintf(stderr, "Error sending data to PostgreSQL: %s\n", PQerrorMessage(conn));
            fclose(csv);
            PQputCopyEnd(conn, "Error during COPY");
            PQfinish(conn);
            return 1;
        }
    }
    fclose(csv);
    
    // Selesaikan COPY
    if (PQputCopyEnd(conn, NULL) != 1) {
        fprintf(stderr, "Error finishing COPY: %s\n", PQerrorMessage(conn));
        PQfinish(conn);
        return 1;
    }

    // Catat waktu selesai
    clock_t end_time = clock();
    double elapsed_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    printf("Insert completed using COPY!\n");
    printf("Total time taken: %.2f seconds\n", elapsed_time);

    PQfinish(conn);
    return 0;
}
