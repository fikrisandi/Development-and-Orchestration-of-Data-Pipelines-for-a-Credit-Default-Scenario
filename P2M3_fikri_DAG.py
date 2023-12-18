import psycopg2
import re
import pandas as pd
import datetime as dt
import warnings
from elasticsearch import Elasticsearch
warnings.filterwarnings("ignore")

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Identitas
'''
=================================================
Milestone 3

Nama  : Muhammad Fikri Sandi Pratama
Batch : FTDS-024-RMT

Program ini dibuat untuk melakukan automatisasi transform dan load data dari PostgreSQL ke ElasticSearch. 
Untuk dataset yang digunakan adalah dataset `dropout and academic success`. Kumpulan data tersebut mencakup informasi yang diketahui pada saat pendaftaran siswa, jalur akademik, demografi, dan faktor sosial ekonomi.
Tedapat 3 klasifikasi yaitu (dropout, enrolled, and graduate).

Objektivitas :
1. Mampu menggunakan Apache Airflow
2. Mampu melakukan validasi data dengan menggunakan Great Expectations
3. Mampu memahami konsep NoSQL secara keseluruhan.
4. Mampu mempersiapkan data untuk digunakan sebelum masuk ke database NoSQL.
5. Mampu mengolah dan memvisualisasikan data dengan menggunakan Kibana.
=================================================
'''

# A. Fetch Data Postgres
def fetch_data():
    '''
    Fungsi ini digunakan untuk melakukan pengambilan data pada postgres dengan bantuan query, 
    kemudian data akan disimpan dalam bentuk csv. Fungsi ini akan dipanggil pada proses DAG.
    '''
    connection = psycopg2.connect(
            database = 'airflow',
            user = 'airflow',
            password = 'airflow',
            host = 'postgres', 
            port = '5432'             
        )
    
    # get all data
    select_query = 'SELECT * FROM table_m3'
    df = pd.read_sql(select_query, connection)
    
    connection.close()
    
    df.to_csv('/opt/airflow/dags/P2M3_fikri_data_raw.csv', index=False)
    
# B. Cleaning Data
def data_cleaning():
    df = pd.read_csv('/opt/airflow/dags/P2M3_fikri_data_raw.csv')
    '''
    Pada fungsi ini akan dilakukan proses pembersihan data sesuai dengan keriteria soal sebelum dibersihkan data akan dimuat dahulu, namun jika dalam kasus real maka disesuaikan dengan datanya.
    Proses yang dilakukan didalamnya ada 4, diantaranya:
    1. Drop Duplicated
    2. Mengubah value kolom float menjadi int
    3. Normalisasi Nama Kolom
    4. Handling Missing Value
    
    setelah itu disimpan dengan nama yang berbeda dengan sebelumnya.
    '''
    # 1. Drop Duplicated
    df = df.drop_duplicates()
    
    # 2. Mengubah value kolom float menjadi int
    def converter(kolom):
        if kolom.dtypes == 'float64':
            return kolom.astype('int')
        else:
            return kolom
    
    df = df.apply(converter)
    
    # 3. Normalisasi Column Name
    def kolom_bersih(column):
        return re.sub(r'[^a-zA-Z0-9_]', '', column.lower().replace(' ', '_'))

    df.columns = map(kolom_bersih, df.columns)
    
    # 4. Drop missing value
    df = df.dropna()
    
    # save into_csv
    df.to_csv('/opt/airflow/dags/P2M3_fikri_data_clean.csv', index=True)
    
# C. Elasticsearch
def insert_into_elastic_manual():
    df = pd.read_csv('/opt/airflow/dags/P2M3_fikri_data_clean.csv')
    '''
    Pada fungsi akan menggunakan elasticsearch untuk keperluan memasukkan data kedalam elastichsearch dan kemudian akan dihubungkan kedalam kibana untuk keperluan visualisasi data.
    '''
    # check connection
    es = Elasticsearch('http://elasticsearch:9200')
    print('Connection status : ', es.ping())
    
    # insert csv file to elastic search
    failed_insert = []
    for i, r in df.iterrows():
        doc = r.to_json()
        try:
            print(i, r['target'])
            res = es.index(index='index', doc_type="doc", body=doc)
        except:
            print('Index Gagal : ', r['index'])
            failed_insert.append(r['index'])
            pass
    
    print('DONE')
    print('Failed Insert', failed_insert)
    
# 4. Data Pipeline
'''
Pada proses ini mengatur penjadwalan yaitu menggunakan waktu Indonesia, kemudian dimulai dengan tanggal 26 November 2023.
'''
default_args = {
    'owner': 'fikri',
    'start_date': dt.datetime(2023,11,26) - dt.timedelta(hours=7), 
    'retries':0,
    'retry_delay': dt.timedelta(minutes=5)
}
'''
    Kemudian untuk intervalnya dilakukan pada tiap hari pada jam 06.30 pagi hari.
'''
with DAG(
    
    "P2M3",
    description='P2M3 ML Pipeline',
    schedule_interval='30 6 * * *',
    default_args=default_args, 
    catchup=False) as dag:
    
    node_start = BashOperator(
        task_id='starting',
        bash_command='echo "I am reading the CSV now ....."'
    )
    
    node_fetch_data = PythonOperator(
        task_id='fetch-data',
        python_callable=fetch_data
    )
    
    node_data_cleaning = PythonOperator(
        task_id='data-cleaning',
        python_callable=data_cleaning
    )
    
    node_insert_data_to_elastic = PythonOperator(
        task_id='insert-data-to-elastic',
        python_callable=insert_into_elastic_manual
    )
    
    node_start >> node_fetch_data >> node_data_cleaning >> node_insert_data_to_elastic

# Latar Belakang adanya report

# Pada negara portugal terdapat beberapa mahasiswa yang putus saat menjadi proses pendidikan tinggi sehingga perlu melakukan analisis dan pemaparan kondisi mahasiswa pada negara tersebut. 

# Untuk berkontribusi pada pengurangan angka putus sekolah dan kegagalan dalam pendidikan tinggi, dengan memaparkan faktor apa saja yang memengaruhi.

# - Menteri Pendidikan Negara Portugal, untuk mengatasi kondisi pendidikan dan SDM negara portugal.
# - Menteri Sosial Negara Portugal,  

# 1 penggunaan Bar Plot -> Umur mahasiswa yang menempuh pendidikan tinggi
# 1 penggunaan Pie Chart -> Target
# 1 penggunaan Vertical Bar Plot -> Profesi Ortu
# -> Jumlah beasiswa dan Hutang
#  Nilai per semester
#  Jurusan
# Status Pernikahan
#  App Order