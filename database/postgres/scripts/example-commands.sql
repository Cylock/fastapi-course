SELECT * FROM products WHERE id IN (1,2,3);


-- #  Similar to regex

-- # Every row where it contains 'TV' in name
SELECT * FROM products WHERE name LIKE 'TV%';


SELECT * FROM products WHERE name NOT LIKE '%e';

-- # Order by ascending price
SELECT * FROM products ORDER BY price ;

SELECT * FROM products ORDER BY price DESC ;


-- # Sort initially descending by inventory and when there are ties (ex inventory = 0) sort the '0' items ASC by price

SELECT * FROM products ORDER BY inventory DESC, price ASC;

-- # Limit query reads and rows retrieved
SELECT * FROM products WHERE price > 10 LIMIT 2;

-- # Skips first 2 rows of a match and retrieve the next 5
SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 2;



-- # Adding data
INSERT INTO products (name, price, inventory) VALUES ('tortilla', 4, 1000);


-- # Adding data and returning the data entered (Combining an Insert with a Select) 

INSERT INTO products (name, price, inventory) VALUES ('car', 10000, 1000) returning *;


INSERT INTO products (name, price, inventory) VALUES ('car', 10000, 1000), ('laptop', 50, 10) returning



-- # Delete rows

DELETE FROM products WHERE id =  10;
SELECT * FROM products;


DELETE FROM products WHERE id = 11 returning *;


-- # Update rows

# Update rows

UPDATE products SET name = 'flour-tortilla', price = 40 WHERE id = 23;