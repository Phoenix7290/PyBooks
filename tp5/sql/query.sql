SELECT 
    b.title, 
    b.description, 
    b.genre, 
    sp.url, 
    sp.scraped_at,
    u.name AS adicionado_por
FROM books b
JOIN scraped_pages sp ON sp.title_extracted = b.title
JOIN users u ON b.user_id = u.id
WHERE sp.success = true
ORDER BY sp.scraped_at DESC;