# Week 5 Assignment
## Task 2
- **Create a new database named  website.** 

    *MyAQL語法*
    ```sql
    CREATE DATABASE website;
    ```
    *結果*  
    <img src="./img/task2-1.png" alt="建立資料庫結果" width="400px">
-  **Create a new table named  member  , in the  website  database,  designed as below:**  

    | Column Name     | Description                                                                                   |
    | ---------------- | --------------------------------------------------------------------------------------------- |
    | id               | Unique ID for Member in Non-Negative Integer. Primary Key. Auto Increment.                    |
    | name             | Name < 255 Characters. Cannot be Empty.                                                       |
    | email            | Email < 255 Characters. Cannot be Empty.                                                      |
    | password         | Password < 255 Characters. Cannot be Empty.                                                   |
    | follower_count   | Follower Count in Non-Negative Integer. Cannot be Empty. Default to 0.                        |
    | time             | Signup DateTime. Cannot be Empty. Default to Current Time.                                    |  

    *MyAQL語法*
    ```sql
    USE website;
    CREATE TABLE member (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        follower_count INT UNSIGNED NOT NULL DEFAULT 0,
        time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);
    ```
    *結果*  
    <img src="./img/task2-2-1.png" alt="建立資料表結果" width="500px">
    <img src="./img/task2-2.png" alt="建立資料表結果" width="800px">  

## Task 3
-  **INSERT a new row to the member table where name, email and password must be set to  test ,  test@test.com , and  test . INSERT additional  4 rows with arbitrary data.**  
    *MyAQL語法*
    ```sql
    INSERT INTO member (name, email, password)
    VALUES ('test', 'test@test.com', 'test');
    INSERT INTO member (name, email, password)
    VALUES ('Alice', 'Alice1010@test.com', '1010Alice');
    INSERT INTO member (name, email, password)
    VALUES ('Bob', 'youknowbob@test.com', 'YesIKnow');
    INSERT INTO member (name, email, password)
    VALUES ('Cindy', 'cindyiscute@test.com', 'ABCabc123');
    INSERT INTO member (name, email, password)
    VALUES ('Cindy', 'cindyiscute@test.com', 'ABCabc123');
    INSERT INTO member (name, email, password)
    VALUES ('Diana', 'disneyland@test.com', 'MickeyMouse');
    ```
    *結果*  
    <img src="./img/task3-1.png" alt="建立資料結果" width="800px">
    
-   **SELECT all rows from the member table.**    
    *MyAQL語法*
    ```sql
    SELECT * FROM member;
    ```
    *結果*  
    <img src="./img/task3-2.png" alt="查詢資料表member結果" width="800px">

-  **SELECT all rows from the member table, in descending order of time.**  
    *MyAQL語法*
    ```sql
    SELECT * FROM member
    ORDER BY time DESC;
    ```
    *結果*  
    <img src="./img/task3-3.png" alt="查詢資料表member結果" width="800px">

-   **SELECT total 3 rows, second to fourth, from the member table, in descending order of time.**  
    *MyAQL語法*
    ```sql
    SELECT * FROM member
    ORDER BY time DESC
    LIMIT 3 OFFSET 1;
    ```
    *結果*  
    <img src="./img/task3-4.png" alt="查詢資料表member結果" width="800px">

-   **SELECT rows where email equals to  test@test.com .**   
    *MyAQL語法*
    ```sql
    SELECT * FROM member
    WHERE email = 'test@test.com';
    ```
    *結果*  
    <img src="./img/task3-5.png" alt="查詢資料表member結果" width="800px">

-   **SELECT rows where name includes the  es  keyword.**  
    *MyAQL語法*
    ```sql
    SELECT * FROM member
    WHERE name LIKE '%es%';
    ```
    *結果*  
    <img src="./img/task3-6.png" alt="查詢資料表member結果" width="800px">

-   **SELECT rows where email equals to  test@test.com  and  password equals to  test .**  
    *MyAQL語法*
    ```sql
    SELECT * FROM member
    WHERE email = 'test@test.com' and password = 'test';
    ```
    *結果*  
    <img src="./img/task3-7.png" alt="查詢資料表member結果" width="800px">

-   **UPDATE data in name column to  test2  where email equals  to  test@test.com .**  
    *MyAQL語法*
    ```sql
    UPDATE member
    SET name = 'test2'
    WHERE email = 'test@test.com';
    ```
    *結果*  
    <img src="./img/task3-8.png" alt="查詢資料表member結果" width="800px">

## Task 4
-   **SELECT how many rows from the member table.**  
    *MyAQL語法*
    ```sql
    SELECT COUNT(*) FROM member;
    ```
    *結果*  
    <img src="./img/task4-1.png" alt="計算資料表member資料數結果" width="400px">

-   **SELECT the sum of follower_count of all the rows from the member table.**  
    *MyAQL語法*
    ```sql
    SELECT SUM(follower_count) FROM member;
    ```
    *結果*  
    <img src="./img/task4-2.png" alt="計算資料表member總和結果" width="400px">

-   **SELECT the average of follower_count of all the rows from the member table.**  
    *MyAQL語法*
    ```sql
    SELECT AVG(follower_count) FROM member;
    ```
    *結果*  
    <img src="./img/task4-3.png" alt="計算資料表member平均結果" width="400px">

-   **SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.**  
    *MyAQL語法*
    ```sql
    SELECT AVG(follower_count)
    FROM (
        SELECT * FROM member
        ORDER BY follower_count DESC
        LIMIT 2
    ) AS top2
    ```
    *結果*  
    <img src="./img/task4-4.png" alt="計算資料表member平均結果" width="400px">

## Task 5
-   **Create a new table named  message  , in the  website  database.  designed as below:** 

    | Column Name | Description |
    | --- | --- |
    | id |   Unique ID for Message in Non-Negative Integer. Primary Key. Auto Increment. |
    | member_id | Member ID for Message Sender. Cannot be Empty. Must be Foreign Key refer to the id column in the member table. |
    | content | Content < 65535 Characters. Cannot be Empty. |
    | like_count | Like Count in Non-Negative Integer. Cannot be Empty. Default to 0. |
    | time | Publish DateTime. Cannot be Empty. Default to Current Time. |

    *MyAQL語法*
    ```sql
    CREATE TABLE message (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    member_id INT UNSIGNED NOT NULL,
    content TEXT NOT NULL,
    like_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES member(id)
    );
    ```
    *結果*  
    <img src="./img/task5-1.png" alt="建立資料表message結果" width="800px">

-   **SELECT all messages, including sender names. We have to JOIN the member table to get that.**  
    *MyAQL語法*
    ```sql
    SELECT message.*, member.name
    FROM message
    LEFT JOIN member
    ON message.member_id = member.id;
    ```
    *結果*  
    <img src="./img/task5-2.png" alt="查詢綜合資料表結果" width="800px">

-   **SELECT all messages, including sender names, where sender email equals to test@test.com . We have to JOIN the member table to  filter and get that.**  
    *MyAQL語法*
    ```sql
    SELECT message.*, member.name
    FROM message
    JOIN member
    ON message.member_id = member.id
    WHERE member.email = 'test@test.com';
    ```
    *結果*  
    <img src="./img/task5-3.png" alt="查詢綜合資料表結果" width="800px">

-   **Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender email equals to  test@test.com .**  
    *MyAQL語法*
    ```sql
    SELECT AVG(message.like_count) FROM message
    JOIN member ON message.member_id = member.id
    WHERE member.email = 'test@test.com';
    ```
    *結果*  
    <img src="./img/task5-4.png" alt="查詢綜合資料表結果" width="600px">

-   **Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender email.**  
    *MyAQL語法*
    ```sql
    SELECT member.email, AVG(message.like_count) FROM message
    JOIN member ON message.member_id = member.id
    GROUP BY member.email;
    ```
    *結果*  
    <img src="./img/task5-5.png" alt="查詢綜合資料表結果" width="600px">
