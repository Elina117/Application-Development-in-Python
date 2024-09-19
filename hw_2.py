from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def print_execution_date(ds, **kwargs):
    print(f"Execution date is {ds}")

# Определяем DAG
with DAG(
        'hw_2_elina-galimova-agb6776',

        start_date=datetime(2024, 1, 1),
        schedule_interval='@daily',  # DAG будет запускаться каждый день
        catchup=False,  # Не догонять пропущенные выполнения
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
        }
) as dag:
    # Оператор Bash для получения рабочего каталога
    bash_oper = BashOperator(
        task_id='get_working_directory',
        bash_command='pwd'
    )

    # Оператор Python для печати даты выполнения
    pyth_oper = PythonOperator(
        task_id='print_execution_date',
        python_callable=print_execution_date
    )

    # Определяем порядок выполнения задач
    bash_oper >> pyth_oper
