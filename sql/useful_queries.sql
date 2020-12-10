/* display duplicates */
-- SELECT food_name, COUNT(*) FROM food_registry2 GROUP BY food_name HAVING COUNT(*) > 1;

/* create and fill tables */
-- SOURCE /home/2020/hunter/fall/43501/nj5074/food_db/documentation/load.sql

/* show how many of each type of food has ever been purchased */
/* variations: user_id, out of available, limit */
SELECT food_types.food_name, COUNT(food_instances.food_id) * food_instances.quantity as num_purchases FROM
	food_types JOIN food_instances
	ON (food_types.food_id = food_instances.food_id)
	GROUP BY food_types.food_id, food_instances.quantity
	ORDER BY num_purchases DESC LIMIT 4;
/*+-----------------+---------------+
  | food_name       | num_purchases |
  +-----------------+---------------+
  | Port wine       |            30 |
  | Serenata wafers |            30 |
  | CALDO PAELLA    |            28 |
  | Rindsgulasch    |            28 |
  +-----------------+---------------+*/



/* ========================================================================== */
/* NOTE: all of these can work for all history by removing available clause */

/* show how many items are in the fridge right now */
SELECT SUM(quantity) AS items_in_fridge FROM food_instances WHERE available=TRUE;
/*+-----------------+
  | items_in_fridge |
  +-----------------+
  |            3406 |
  +-----------------+*/

/* show how many items user has in the fridge right now */
SELECT SUM(quantity) AS items_in_fridge FROM food_instances WHERE user_id = 1 AND available=TRUE;
/*+-----------------+
  | items_in_fridge |
  +-----------------+
  |             179 |
  +-----------------+*/

/* show how many items user (with name) has in the fridge right now */
SELECT users.user_name, SUM(quantity) AS items_in_fridge FROM
	food_instances JOIN users ON (users.user_id = food_instances.user_id)
	WHERE food_instances.user_id = 1 AND food_instances.available=TRUE;
/*+-----------+-----------------+
  | user_name | items_in_fridge |
  +-----------+-----------------+
  | John      |             179 |
  +-----------+-----------------+*/

/* show how many items each user has in fridge ordered by id */
SELECT users.user_name, SUM(quantity) AS items_in_fridge FROM
	food_instances JOIN users ON (users.user_id = food_instances.user_id)
	WHERE food_instances.available=TRUE
	GROUP BY users.user_name, users.user_id
	ORDER BY users.user_id;
/*+-----------+-----------------+
  | user_name | items_in_fridge |
  +-----------+-----------------+
  | John      |             179 |
  | William   |             162 |
  | Mary      |              96 |
  | James     |             135 |
  +-----------+-----------------+*/

/* show how many items each user has in fridge ordered by num items */
SELECT users.user_name, SUM(quantity) AS items_in_fridge FROM
	food_instances JOIN users ON (users.user_id = food_instances.user_id)
	WHERE food_instances.available=TRUE
	GROUP BY users.user_name
	ORDER BY items_in_fridge DESC;
/*+-----------+-----------------+
  | user_name | items_in_fridge |
  +-----------+-----------------+
  | Fred      |             187 |
  | Walter    |             187 |
  | Harry     |             179 |
  | John      |             179 |
  +-----------+-----------------+*/
/* ========================================================================== */




/* ========================================================================== */
/* top x in fridge expiring soon */
SELECT food_types.food_name, food_instances.expiration_date FROM
	food_types JOIN food_instances ON (food_types.food_id = food_instances.food_id)
	WHERE food_instances.available = TRUE
	GROUP BY food_types.food_id, food_instances.expiration_date
	ORDER BY food_instances.expiration_date LIMIT 10;
/*+--------------------------------------+-----------------+
  | food_name                            | expiration_date |
  +--------------------------------------+-----------------+
  | Quail                                | 2020-11-27      |
  | Original gluco biscuits              | 2020-11-27      |
  | Nopal                                | 2020-11-27      |
  | NERDS Candy Bulk                     | 2020-11-27      |
  +--------------------------------------+-----------------+*/

/* top x things in fridge expiring soon (not yet expired) */
SELECT food_types.food_name, food_instances.expiration_date FROM
	food_types JOIN food_instances ON (food_types.food_id = food_instances.food_id)
	WHERE food_instances.available = TRUE and food_instances.expiration_date >= CURDATE()
	GROUP BY food_types.food_id, food_instances.expiration_date
	ORDER BY food_instances.expiration_date LIMIT 10;
/*+------------------------------------------+-----------------+
  | food_name                                | expiration_date |
  +------------------------------------------+-----------------+
  | Therapeutic nutrition                    | 2020-12-04      |
  | Punjabi sarsoon da saag                  | 2020-12-04      |
  | Alphonso Mango                           | 2020-12-04      |
  | Ocean spray juice cranberry raspberry    | 2020-12-04      |
  +------------------------------------------+-----------------+*/
/* ========================================================================== */



/* ========================================================================== */
/* money spent in total by everyone */
SELECT CONCAT("$", FORMAT(SUM(total_price),2)) as total_spent from food_instances;
/*+-------------+
  | total_spent |
  +-------------+
  | $10,777.85  |
  +-------------+*/

/* money spent by specific user (with name) */
SELECT users.user_name, CONCAT("$", FORMAT(SUM(total_price),2)) AS total_spent FROM
	food_instances JOIN users ON (users.user_id = food_instances.user_id)
	WHERE food_instances.user_id = 1;
/*+-----------+-------------+
  | user_name | total_spent |
  +-----------+-------------+
  | John      | $498.17     |
  +-----------+-------------+*/

/* money spent by each user */
SELECT users.user_name, CONCAT("$", FORMAT(SUM(total_price),2)) AS total_spent FROM
	food_instances JOIN users ON (users.user_id = food_instances.user_id)
	GROUP BY users.user_name
	ORDER BY total_spent DESC;
/*+-----------+-------------+
  | user_name | total_spent |
  +-----------+-------------+
  | Charles   | $595.83     |
  | Thomas    | $530.77     |
  | Walter    | $512.10     |
  | Alice     | $506.82     |
  +-----------+-------------+*/

/* money spent by each user this week */
SELECT users.user_name, CONCAT("$", FORMAT(SUM(total_price),2)) AS total_spent FROM
	food_instances JOIN users ON (users.user_id = food_instances.user_id)
	WHERE purchase_date <= CURDATE() and purchase_date >= CURDATE() - 7
	GROUP BY users.user_name
	ORDER BY total_spent DESC;
/*+-----------+-------------+
  | user_name | total_spent |
  +-----------+-------------+
  | Charles   | $72.70      |
  | Walter    | $63.82      |
  | Margaret  | $53.58      |
  | Thomas    | $52.33      |
  +-----------+-------------+*/
/* ========================================================================== */

/* show most recently purchased items (with full info) */
SELECT users.user_name, food_types.food_name, food_instances.quantity,
	CONCAT("$", FORMAT(food_instances.total_price, 2)) as total_spent,
	stores.store_name, food_instances.purchase_date
FROM food_instances
JOIN users ON (users.user_id = food_instances.user_id)
JOIN food_types ON (food_types.food_id = food_instances.food_id)
JOIN stores ON (stores.store_id = food_instances.food_id)
ORDER BY food_instances.purchase_date
LIMIT 10;
/*+-----------+-----------------------------------------------------------+----------+-------------+---------------------------------+---------------+
  | user_name | food_name                                                 | quantity | total_spent | store_name                      | purchase_date |
  +-----------+-----------------------------------------------------------+----------+-------------+---------------------------------+---------------+
  | Charles   | Entenmann's cake louisiana crunch                         |        4 | $5.29       | El Economico Restaurant         | 2020-10-01    |
  | John      | Crispy French Crackers                                    |        3 | $24.58      | Tasty Deli                      | 2020-10-01    |
  | Mary      | Gourmet meat sauce                                        |        4 | $4.43       | Crown Donut Restaurant          | 2020-10-01    |
  | Sarah     | Quesadilla                                                |        1 | $9.67       | Mooncake Foods                  | 2020-10-01    |
  +-----------+-----------------------------------------------------------+----------+-------------+---------------------------------+---------------+*/

/* price of an item over a period of time */
SELECT food_types.food_name, CONCAT("$", FORMAT(food_instances.total_price/food_instances.quantity, 2)) as price, food_instances.purchase_date
FROM food_instances
LEFT JOIN food_types ON (food_types.food_id = food_instances.food_id)
WHERE food_instances.food_id = 1399
GROUP BY food_instances.food_id, food_types.food_name,food_instances.total_price, food_instances.quantity, food_instances.purchase_date
ORDER BY purchase_date DESC;
/*+-----------------------------------+-------+---------------+
  | food_name                         | price | purchase_date |
  +-----------------------------------+-------+---------------+
  | Spice drops colorful spiced candy | $0.06 | 2020-11-22    |
  | Spice drops colorful spiced candy | $0.51 | 2020-11-12    |
  | Spice drops colorful spiced candy | $3.84 | 2020-10-28    |
  | Spice drops colorful spiced candy | $1.37 | 2020-10-09    |
  | Spice drops colorful spiced candy | $5.86 | 2020-10-01    |
  +-----------------------------------+-------+---------------+*/

/* fraction of all items ever which are healthy (i.e healthy_scale >= 7) */
SELECT CONCAT(FORMAT(percentage_of_healthy_items,2),"%")as percentage_of_healthy_items
FROM (SELECT (100*
(SELECT COUNT(*) as num_healthy_items from(
SELECT COUNT(food_instances.food_id) as num_purchases, food_types.health_scale
FROM food_types
JOIN food_instances ON (food_types.food_id = food_instances.food_id)
WHERE food_types.health_scale >= 7
GROUP BY food_types.food_id, food_types.health_scale
ORDER BY num_purchases) as c)
/
(SELECT COUNT(*) as total_items from(
SELECT COUNT(food_instances.food_id) as num_purchases, food_types.health_scale
FROM food_types
JOIN food_instances ON (food_types.food_id = food_instances.food_id)
GROUP BY food_types.food_id, food_types.health_scale
ORDER BY num_purchases) as a ))AS percentage_of_healthy_items)as w;
/*+-----------------------------+
  | percentage_of_healthy_items |
  +-----------------------------+
  | 30.30%                      |
  +-----------------------------+*/

