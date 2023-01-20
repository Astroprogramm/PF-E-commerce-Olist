AIRFLOW_UID=50000
AIRFLOW_GID=50000import pandas as pd 
import numpy as np
import sqlalchemy
import os
from sqlalchemy import create_engine
from datetime import datetime
from airflow import DAG
from sqlalchemy import MetaData
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

import logging


def Closed_deals():
    cadena_conexion = 'mysql+pymysql://root:123456789@localhost:3306/ecommerceolist'
    engine = create_engine(cadena_conexion)
    Closed_deals_df = pd.read_csv(r'C:\Users\DIEZ\Desktop\MySpace\airflow\datasets\olist_closed_deals_dataset.csv')
    Closed_deals_df.mql_id = Closed_deals_df.mql_id.astype('string')
    Closed_deals_df.seller_id = Closed_deals_df.seller_id.astype('string')
    Closed_deals_df.sdr_id = Closed_deals_df.sdr_id.astype('string')
    Closed_deals_df.sr_id = Closed_deals_df.sr_id.astype('string')
    Closed_deals_df.sdr_id = Closed_deals_df.sdr_id.astype('string')
    Closed_deals_df.business_segment = Closed_deals_df.business_segment.astype('string')
    Closed_deals_df.lead_type = Closed_deals_df.lead_type.astype('string')
    Closed_deals_df.lead_behaviour_profile = Closed_deals_df.lead_behaviour_profile.astype('string')
    Closed_deals_df.has_company = Closed_deals_df.has_company.astype('string')
    Closed_deals_df.has_gtin = Closed_deals_df.has_gtin.astype('string')
    Closed_deals_df.average_stock = Closed_deals_df.average_stock.astype('string')
    Closed_deals_df.business_type = Closed_deals_df.business_type.astype('string')
    Closed_deals_df.won_date = pd.to_datetime(Closed_deals_df.won_date)
    
    Closed_deals_df.to_sql('Closed_deals', engine, if_exists='replace', index = False)
    
    return print('Carga del datasets Closed_deals Exitosa')

def Customer():
    cadena_conexion = 'mysql+pymysql://root:123456789@localhost:3306/ecommerceolist'
    engine = create_engine(cadena_conexion)
    Customers_df= pd.read_csv(r'C:\Users\DIEZ\Desktop\MySpace\airflow\datasets\olist_customers_dataset.csv')
    Customers_df.customer_id = Customers_df.customer_id.astype('string')
    Customers_df.customer_unique_id = Customers_df.customer_unique_id.astype('string')
    Customers_df.customer_city = Customers_df.customer_city.astype('string')
    Customers_df.customer_state = Customers_df.customer_state.astype('string')
    
    Customers_df.to_sql('Customers', engine, index = False, if_exists= 'replace')
    
    return print('Carga del dataset Customers Extitosa')

def Geolocation():
    cadena_conexion = 'mysql+pymysql://root:123456789@localhost:3306/ecommerceolist'
    engine = create_engine(cadena_conexion)
    
    Geolocation_df = pd.read_csv(r'C:\Users\DIEZ\Desktop\MySpace\airflow\datasets\olist_geolocation_dataset.csv')
    Geolocation_df.geolocation_city = Geolocation_df.geolocation_city.astype('string')
    Geolocation_df.geolocation_state = Geolocation_df.geolocation_state.astype('string')
    
    Geolocation_df.to_sql('Customers', engine, index = False, if_exists= 'replace')
    
    return print('Cargo el dataset Geolocation con exito')

def Marketing_qualif_leads():
    cadena_conexion = 'mysql+pymysql://root:123456789@localhost:3306/ecommerceolist'
    engine = create_engine(cadena_conexion)
    
    Marketing_qualif_leads_df = pd.read_csv(r'C:\Users\DIEZ\Desktop\MySpace\airflow\datasets\olist_marketing_qualified_leads_dataset.csv')
    Marketing_qualif_leads_df.mql_id = Marketing_qualif_leads_df.mql_id.astype('string')
    Marketing_qualif_leads_df.landing_page_id = Marketing_qualif_leads_df.landing_page_id.astype('string')
    Marketing_qualif_leads_df.origin = Marketing_qualif_leads_df.origin.astype('string')
    Marketing_qualif_leads_df.first_contact_date = pd.to_datetime(Marketing_qualif_leads_df.first_contact_date)
    
    Marketing_qualif_leads_df.to_sql('Marketing_qualif_leads', engine, index = False, if_exists= 'replace')
    
    return print('Cargo el dataset Marketing_qualif_leads con exito')

def Order_items():
    cadena_conexion = 'mysql+pymysql://root:123456789@localhost:3306/ecommerceolist'
    engine = create_engine(cadena_conexion)
    
    Order_items_df = pd.read_csv(r'C:\Users\DIEZ\Desktop\MySpace\airflow\datasets\olist_order_items_dataset.csv')
    Order_items_df.order_id = Order_items_df.order_id.astype('string')
    Order_items_df.product_id = Order_items_df.product_id.astype('string')
    Order_items_df.seller_id = Order_items_df.seller_id.astype('string')
    Order_items_df.shipping_limit_date = pd.to_datetime(Order_items_df.shipping_limit_date)
    
    Order_items_df.to_sql('Order_items', engine, index = False, if_exists= 'replace')
    
    return print('Cargo el dataset Order_items exitosamente')

def Order_Payments():
    cadena_conexion = 'mysql+pymysql://root:123456789@localhost:3306/ecommerceolist'
    engine = create_engine(cadena_conexion)
    
    Order_payments_df = pd.read_csv(r'C:\Users\DIEZ\Desktop\MySpace\airflow\datasets\olist_order_payments_dataset.csv')
    Order_payments_df.order_id = Order_payments_df.order_id.astype('string')
    Order_payments_df.payment_type = Order_payments_df.payment_type.astype('string')
    
    Order_payments_df.to_sql('Order_payments', engine, index = False, if_exists= 'replace')
    
    return print('Cargo el dataset Order_payments exitosamente')

def  Order_Reviews():
    cadena_conexion = 'mysql+pymysql://root:123456789@localhost:3306/ecommerceolist'
    engine = create_engine(cadena_conexion)
    
    Order_reviews_df = pd.read_csv(r'C:\Users\DIEZ\Desktop\MySpace\airflow\datasets\olist_order_reviews_dataset.csv')
    Order_reviews_df.review_id = Order_reviews_df.review_id.astype('string')
    Order_reviews_df.order_id = Order_reviews_df.order_id.astype('string')
    Order_reviews_df.review_comment_title = Order_reviews_df.review_comment_title.astype('string')
    Order_reviews_df.review_comment_message = Order_reviews_df.review_comment_message.astype('string')
    Order_reviews_df.review_creation_date = pd.to_datetime(Order_reviews_df.review_creation_date)
    Order_reviews_df.review_answer_timestamp = pd.to_datetime(Order_reviews_df.review_answer_timestamp)
    
    Order_reviews_df.to_sql('Order_reviews', engine, index = False, if_exists = 'replace')
    
    return print('Cargo el dataset Order_reviews exitosamente')

def Orders():
    cadena_conexion = 'mysql+pymysql://root:123456789@localhost:3306/ecommerceolist'
    engine = create_engine(cadena_conexion)
    
    Orders_df = pd.read_csv(r'C:\Users\DIEZ\Desktop\MySpace\airflow\datasets\olist_orders_dataset.csv')
    Orders_df.customer_id = Orders_df.customer_id.astype('string')
    Orders_df.order_id = Orders_df.order_id.astype('string')
    Orders_df.order_status = Orders_df.order_status.astype('string')
    Orders_df.order_purchase_timestamp = pd.to_datetime(Orders_df.order_purchase_timestamp)
    Orders_df.order_approved_at = pd.to_datetime(Orders_df.order_approved_at)
    Orders_df.order_delivered_carrier_date = pd.to_datetime(Orders_df.order_delivered_carrier_date)
    Orders_df.order_delivered_customer_date = pd.to_datetime(Orders_df.order_delivered_customer_date)
    Orders_df.order_estimated_delivery_date = pd.to_datetime(Orders_df.order_estimated_delivery_date)

    Orders_df.to_sql('Orders', engine, index = False, if_exists = 'replace')
    
    return print('Se cargo el dataset Orders exitosamente')

def Products():
    cadena_conexion = 'mysql+pymysql://root:123456789@localhost:3306/ecommerceolist'
    engine = create_engine(cadena_conexion)
    
    Products_df = pd.read_csv(r'C:\Users\DIEZ\Desktop\MySpace\airflow\datasets\olist_products_dataset.csv')
    Products_df.product_id = Products_df.product_id.astype('string')
    Products_df.product_category_name = Products_df.product_category_name.astype('string')
    Products_df.product_name_lenght = Products_df.product_name_lenght.astype('float')
    
    Products_df.to_sql('Products', engine, index = False, if_exists = 'replace')
    
    return print('Se cargo el dataset Products exitosamente')

def Sellers():
    cadena_conexion = 'mysql+pymysql://root:123456789@localhost:3306/ecommerceolist'
    engine = create_engine(cadena_conexion)
    
    Sellers_df = pd.read_csv(r'C:\Users\DIEZ\Desktop\MySpace\airflow\datasets\olist_sellers_dataset.csv')
    Sellers_df.seller_id = Sellers_df.seller_id.astype('string')
    Sellers_df.seller_city = Sellers_df.seller_city.astype('string')
    Sellers_df.seller_state= Sellers_df.seller_state.astype('string')
    
    Sellers_df.to_sql('Sellers', engine, index = False, if_exists = 'replace')
    
    return print('Se cargo el dataset Sellers exitosamente')

def Category_translat():
    cadena_conexion = 'mysql+pymysql://root:123456789@localhost:3306/ecommerceolist'
    engine = create_engine(cadena_conexion)
    
    Category_translat_df = pd.read_csv(r'C:\Users\DIEZ\Desktop\MySpace\airflow\datasets\product_category_name_translation.csv')
    Category_translat_df.product_category_name = Category_translat_df.product_category_name.astype('string')
    Category_translat_df.product_category_name_english = Category_translat_df.product_category_name_english.astype('string')
    
    Category_translat_df.to_sql('Category_translat', engine,index = False, if_exists = 'replace')
    
    return print('Se cargo el dataset Category_translat exitosamente')

def ImputeNulls(datasets_names):
    for dataset in datasets_names:
        for column in dataset.columns:
            #Null imputation in strings
            if dataset[column].dtype == 'string[python]':
                if dataset[column].isnull().sum() >=1:
                    dataset[column].fillna('No data', inplace=True)
            #Null imputation in float64:
            elif dataset[column].dtype == 'float64':
                if dataset[column].isnull().sum() >=1:
                    dataset[column].fillna(0, inplace=True)
            #Null imputation in int64:
            elif dataset[column].dtype == 'int64':
                if dataset[column].isnull().sum() >=1:
                    dataset[column].fillna(0, inplace=True)
            #Null imputation in datetime
            elif dataset[column].dtype == 'datetime64[ns]':
                if dataset[column].isnull().sum() >=1:
                    dataset[column].fillna('No data', inplace=True)
                    
with DAG(dag_id = 'ETL_tablas', schedule= '@once' , start_date= datetime(2023,1,19, )) as dag:
   task01 = PythonOperator(task_id = 'Closed_deal' , python_callable = Closed_deals)
   task02 = PythonOperator(task_id='Customer', python_callable= Customer)
   task03 = PythonOperator(task_id ='Geolo', python_callable= Geolocation)
   task04 = PythonOperator(task_id ='Marke', python_callable= Marketing_qualif_leads)
   task05 = PythonOperator(task_id ='Order_Item', python_callable= Order_items)
   task06 = PythonOperator(task_id ='Order_paym', python_callable= Order_Payments)
   task07 = PythonOperator(task_id ='Order_revi', python_callable= Order_items)
   task08 = PythonOperator(task_id ='Order_', python_callable= Orders)
   task09 = PythonOperator(task_id ='Product', python_callable= Products)
   task101 = PythonOperator(task_id ='Seller', python_callable= Sellers)
   task111 = PythonOperator(task_id ='Categ', python_callable= Category_translat)

   task01 >> task02 >> task03 >> task04 >> task05 >> task06 >> task07 >> task08 >> task09 >> task101 >> task111