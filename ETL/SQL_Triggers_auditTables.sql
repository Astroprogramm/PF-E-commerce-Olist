SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE audit_closed_deals(
	id_audit_closed_deals INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	mql_id VARCHAR(100),
    seller_id VARCHAR(100),
    sdr_id VARCHAR(100),
    sr_id varchar(100), 
	won_date datetime, 
	business_segment varchar(100), 
	lead_type varchar(100), 
	lead_behaviour_profile varchar(100), 
	has_company varchar(20), 
	has_gtin varchar(20), 
	average_stock varchar(50), 
	business_type varchar(50), 
	declared_product_catalog_size double, 
	declared_monthly_revenue double,
    date_update datetime,
    user VARCHAR(20)
);

DROP TRIGGER IF EXISTS inserts_closed_deals;
CREATE TRIGGER inserts_closed_deals
AFTER INSERT ON closed_deals
FOR EACH ROW 
INSERT INTO audit_closed_deals (mql_id, seller_id, sdr_id, sr_id, won_date, business_segment, lead_type, lead_behaviour_profile, has_company, has_gtin, average_stock, business_type, declared_product_catalog_size, declared_monthly_revenue,date_update,user)
VALUES (NEW.mql_id, NEW.seller_id, NEW.sdr_id, NEW.sr_id, NEW.won_date, NEW.business_segment, NEW.lead_type, NEW.lead_behaviour_profile,
		NEW.has_company, NEW.has_gtin, NEW.average_stock, NEW.business_type, NEW.declared_product_catalog_size, NEW.declared_monthly_revenue, now(), current_user());



CREATE TABLE audit_order_items(
	order_id varchar(100), 
	order_item_id bigint,
	product_id varchar(100), 
	seller_id varchar(100), 
	shipping_limit_date datetime, 
	price double, 
	freight_value double,
    date_update datetime,
    user varchar(20)
);

DROP TRIGGER IF EXISTS inserts_order_items;
CREATE TRIGGER inserts_order_items
AFTER INSERT ON order_items
FOR EACH ROW 
INSERT INTO audit_order_items (order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value,date_update,user)
VALUES (NEW.order_id, NEW.order_item_id, NEW.product_id, NEW.seller_id, NEW.shipping_limit_date, NEW.price, NEW.freight_value, now(), current_user());

CREATE TABLE audit_order_payments(
	order_id varchar(100), 
	payment_sequential bigint, 
	payment_type varchar(50), 
	payment_installments bigint, 
	payment_value double,
    date_update datetime,
    user VARCHAR(20)
);

DROP TRIGGER IF EXISTS inserts_order_payments;
CREATE TRIGGER inserts_order_payments
AFTER INSERT ON order_payments
FOR EACH ROW 
INSERT INTO audit_order_payments (order_id, payment_sequential, payment_type, payment_installments, payment_value,date_update,user)
VALUES (NEW.order_id, NEW.payment_sequential, NEW.payment_type, NEW.payment_installments, NEW.payment_value, now(), current_user());

CREATE TABLE audit_order_reviews(
	review_id varchar(100),
	order_id varchar(100), 
	review_score bigint,
	review_comment_title varchar(100), 
	review_comment_message varchar(500), 
	review_creation_date datetime,
	review_answer_timestamp datetime,
    date_update datetime,
    user VARCHAR(20)
);

DROP TRIGGER IF EXISTS inserts_order_reviews;
CREATE TRIGGER inserts_order_reviews
AFTER INSERT ON order_reviews
FOR EACH ROW 
INSERT INTO audit_order_reviews (review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date,review_answer_timestamp,date_update,user)
VALUES (NEW.review_id,NEW.order_id, NEW.review_score, NEW.review_comment_title, NEW.review_comment_message, NEW.review_creation_date,NEW.review_answer_timestamp, now(), current_user());


CREATE TABLE audit_order(
	order_id varchar(100),
	customer_id varchar(100), 
	order_status varchar(50), 
	order_purchase_timestamp datetime, 
	order_approved_at text ,
	order_delivered_carrier_date text, 
	order_delivered_customer_date text, 
	order_estimated_delivery_date datetime,
    date_update datetime,
    user VARCHAR(20)
);

DROP TRIGGER IF EXISTS inserts_order;
CREATE TRIGGER inserts_order
AFTER INSERT ON orders
FOR EACH ROW 
INSERT INTO audit_order (order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date,order_delivered_customer_date,order_estimated_delivery_date,date_update,user)
VALUES (NEW.order_id, NEW.customer_id, NEW.order_status, NEW.order_purchase_timestamp, NEW.order_approved_at ,NEW.order_delivered_carrier_date,NEW.order_delivered_customer_date, NEW.order_estimated_delivery_date,now(), current_user());

CREATE TABLE audit_products(
	product_id varchar(100),
	product_category_name varchar(100) ,
	product_name_lenght double ,
	product_description_lenght double ,
	product_photos_qty double ,
	product_weight_g double ,
	product_length_cm double ,
	product_height_cm double ,
	product_width_cm double ,
	date_update datetime,
    user VARCHAR(20)
);

DROP TRIGGER IF EXISTS inserts_products;
CREATE TRIGGER inserts_products
AFTER INSERT ON products
FOR EACH ROW 
INSERT INTO audit_products (product_id, product_category_name, product_name_lenght, product_description_lenght, product_photos_qty, product_weight_g,product_length_cm,product_height_cm,product_width_cm,date_update,user)
VALUES (NEW.product_id, NEW.product_category_name, NEW.product_name_lenght, NEW.product_description_lenght, NEW.product_photos_qty ,NEW.product_weight_g,NEW.product_length_cm, NEW.product_height_cm,NEW.product_width_cm,now(), current_user());

CREATE TABLE audit_sellers(
	seller_id varchar(100),
	seller_zip_code_prefix bigint ,
	seller_city varchar(50) ,
	seller_state varchar(50),
    date_update datetime,
    user varchar(20)
);

DROP TRIGGER IF EXISTS inserts_sellers;
CREATE TRIGGER inserts_sellers
AFTER INSERT ON sellers
FOR EACH ROW 
INSERT INTO audit_sellers (seller_id, seller_zip_code_prefix, seller_city, seller_state,date_update,user)
VALUES (NEW.seller_id, NEW.seller_zip_code_prefix, NEW.seller_city, NEW.seller_state,now(), current_user());

CREATE TABLE audit_customers(
	customer_id varchar(100),
    customer_unique_id varchar(100),
	customer_zip_code_prefix bigint ,
	customer_city varchar(50) ,
	customer_state varchar(50),
    date_update datetime,
    user varchar(20)
);

DROP TRIGGER IF EXISTS inserts_customers;
CREATE TRIGGER inserts_customers
AFTER INSERT ON customers
FOR EACH ROW 
INSERT INTO audit_customers (customer_id, customer_unique_id,customer_zip_code_prefix, customer_city, customer_state,date_update,user)
VALUES (NEW.customer_id, NEW.customer_unique_id,NEW.customer_zip_code_prefix, NEW.customer_city, NEW.customer_state,now(), current_user());

CREATE TABLE audit_marketing_qualif(
	mql_id varchar(100),
	first_contact_date datetime ,
	landing_page_id varchar(100) ,
	origin varchar(80),
    date_update datetime,
    user varchar(20)
);

DROP TRIGGER IF EXISTS inserts_marketing_qualif;
CREATE TRIGGER inserts_marketing_qualif
AFTER INSERT ON marketing_qualif_leads
FOR EACH ROW 
INSERT INTO audit_marketing_qualif (mql_id, first_contact_date,landing_page_id, origin,date_update,user)
VALUES (NEW.mql_id, NEW.first_contact_date, NEW.landing_page_id, NEW.origin, now(), current_user());

CREATE TABLE audit_category_translat(
	product_category_name varchar(100),
	product_category_name_english varchar(100),
    date_update datetime,
    user varchar(20)
);

DROP TRIGGER IF EXISTS inserts_category_translat;
CREATE TRIGGER inserts_category_translat
AFTER INSERT ON category_translat
FOR EACH ROW 
INSERT INTO audit_category_translat (product_category_name,product_category_name_english ,date_update,user)
VALUES (NEW.product_category_name, NEW.product_category_name_english, now(), current_user());

CREATE TABLE audit_geolocation(
	geolocation_zip_code_prefix bigint,
	geolocation_lat double, 
	geolocation_lng double, 
	geolocation_city varchar(50), 
	geolocation_state varchar(50),
    date_update datetime,
    user varchar(20)
);

DROP TRIGGER IF EXISTS inserts_geolocation;
CREATE TRIGGER inserts_geolocation
AFTER INSERT ON geolocation
FOR EACH ROW 
INSERT INTO audit_geolocation (geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state,date_update,user)
VALUES (NEW.geolocation_zip_code_prefix, NEW.geolocation_lat, NEW.geolocation_lng, NEW.geolocation_city,NEW.geolocation_state,now(), current_user());