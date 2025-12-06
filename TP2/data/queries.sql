SELECT * FROM users WHERE active = TRUE;

SELECT name, salary FROM users WHERE salary > 4000.00;

SELECT name, join_date FROM users WHERE join_date > '2023-12-31';

SELECT name, role FROM users WHERE role = 'admin' OR role = 'librarian';

SELECT name, department FROM users WHERE department = 'fiction' AND active = TRUE;

SELECT name, active FROM users WHERE NOT active;

SELECT name, salary FROM users ORDER BY salary DESC;

SELECT name, join_date FROM users ORDER BY join_date ASC, name ASC;

SELECT COUNT(*) AS total_users FROM users;

SELECT SUM(salary) AS total_salary FROM users;

SELECT role, AVG(salary) AS avg_salary FROM users GROUP BY role;

SELECT department, COUNT(*) AS count_per_dept FROM users GROUP BY department;

SELECT name, salary, department FROM users WHERE salary BETWEEN 3000.00 AND 5000.00 AND department = 'tech';

SELECT role, MAX(salary) AS max_salary FROM users GROUP BY role;

SELECT name, join_date, role, salary FROM users WHERE EXTRACT(YEAR FROM join_date) = 2024 AND (role = 'user' OR salary < 3000.00);