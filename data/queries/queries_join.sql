SELECT b.id, b.title, b.genre, u.name AS added_by
FROM books b
INNER JOIN users u ON b.user_id = u.id
ORDER BY b.id;

SELECT u.id, u.name, u.username, COALESCE(b.title, 'Sem livros') AS livro
FROM users u
LEFT JOIN books b ON u.id = b.user_id
ORDER BY u.id;

SELECT b.id, b.title, u.name AS added_by
FROM books b
RIGHT JOIN users u ON b.user_id = u.id
WHERE b.id IS NOT NULL
ORDER BY b.id;