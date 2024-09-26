from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.models import Variable

def choose_branch():

    is_startml = Variable.get('')

    if is_startml==True:
        return 'startml_desc'
    else:
        return 'not_startml_desc'

def startml_for_people():
    print('StartML is a starter course for ambitious people')

def not_this_course():
    print('Not a startML course, sorry')

with DAG(
        dag_id='hw_13_elina',
        start_date=datetime(2024, 1, 1),
        schedule_interval='@daily',  # DAG будет запускаться каждый день
        catchup=False,  # Не догонять пропущенные выполнения
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        }
) as dag:
    start_operators = DummyOperator(
        task_id='before_branching'
    )

    branching_operator=BranchPythonOperator(
        task_id='determine_course',
        python_callable=choose_branch
    )

    yes_startml_course=PythonOperator(
        task_id='startml_desc',
        python_callable=startml_for_people
    )
    not_startml_course = PythonOperator(
        task_id='not_startml_desc',
        python_callable=not_this_course
    )

    end_operators = DummyOperator(
        task_id='after_branching'
    )