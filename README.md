# 🚀 C vs. Python: Inserting 1 Million Rows into PostgreSQL  

This project compares the performance of **C** and **Python** when inserting 1 million rows into a PostgreSQL database using the `COPY` command.  

## 📊 Experiment Results  

| Language | Time Taken |
|----------|-----------|
| **C** | **0.28 seconds** ⏩ |
| **Python** | **4.24 seconds** 🐍 |

## 📌 Why the Difference?  

✅ **C is faster because:**  
- Low-level memory management  
- No runtime overhead like Python  
- No Global Interpreter Lock (GIL)  

🐍 **Python is slower, but offers:**  
- Simplicity and readability  
- Rich ecosystem and libraries  
- Easier debugging and maintenance  

## 🛠️ How to Run the Experiment  

### 1️⃣ Setup PostgreSQL  
Ensure you have PostgreSQL installed and running. Update the database credentials in the code if necessary.  

### 2️⃣ Generate Dummy Data  
Before inserting data, generate the CSV file using:  
```bash
python generate.py
```
This will create a file named `dummy_data.csv` with 1 million rows.  

### 3️⃣ Run the C Implementation  
Compile and execute the C program:  
```bash
gcc -o insert_postgres insert_postgres.c -lpq
./insert_postgres
```

### 4️⃣ Run the Python Implementation  
Execute the Python script:  
```bash
python insert_postgres.py
```

### 5️⃣ Check Database  
Verify that the data is inserted properly in PostgreSQL using:  
```sql
SELECT COUNT(*) FROM users;
```

## 📌 Conclusion  
If raw performance is a priority, **C** is the winner. However, for ease of development and maintainability, **Python** remains a strong choice.  
