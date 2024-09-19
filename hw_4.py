from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from textwrap import dedent

def print_execution_date(ds, **kwargs):
    print(f"Execution date is {ds}")

# Определяем DAG
with DAG(
        'hw_4_elina-galimova-agb6776',
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

    bash_tasks = []
    for i in range(10):
        bash_task = BashOperator(
            task_id = f'bash_task_{i}',
            bash_command=f'echo This is Bash task number {i}',
            doc_md=dedent(f"""
                        # Bash Task {i}

                        **Описание:** Эта задача выполняет команду `echo` для вывода номера задачи в Bash.

                        *Команда:* `echo This is Bash task number {i}`

                        _Примечание:_ Используйте этот task_id для отслеживания задач в интерфейсе Airflow.
                        """)
        )
        bash_tasks.append(bash_task)

    pyth_tasks = []
    for i in range(20):
        pyth_oper = PythonOperator(
            task_id=f'print_task_{i}',
            python_callable=print_execution_date,
            op_kwargs=f"task number is: {i}",
            doc_md=dedent(f"""
                        # Pyth Task {i}
                        
                        **Описание:** Эта задача вызывает функцию `print_task_number`, которая выводит номер задачи.

                        *Функция:* `print_task_number(task_number)`

                        _Параметры:_ 
                                - `task_number`: Номер текущей задачи.

                        _Примечание:_ Этот task_id используется для отслеживания Python задач в интерфейсе Airflow.

                        """)
        )
        pyth_tasks.append(pyth_oper)

    for bash_task in bash_tasks:
        for pyth_oper in pyth_tasks:
            bash_task >> pyth_oper
