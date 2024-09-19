from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from textwrap import dedent

with DAG(
    'hw_5_elina-galimova-agb6776',
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

    bash_tasks=[]
    for i in range(0, 6):
        bash_task = BashOperator(
            task_id = f'print_template_vars_{i}',
            bash_command="""
                            echo "Execution timestamp: {{ ts }}"
                            echo "Run id: {{run_id}}"
                            """,
            doc_md=dedent(f"""
                                # Pyth Task {i}

                                **Описание:** Эта задача вызывает функцию `print_task_number`, которая выводит номер задачи.

                                *Функция:* `print_task_number(task_number)`

                                _Параметры:_ 
                                        - `task_number`: Номер текущей задачи.

                                _Примечание:_ Этот task_id используется для отслеживания Python задач в интерфейсе Airflow.

                                """)
        )
        bash_tasks.append(bash_task)

    for i in range(len(bash_tasks)-1):
        bash_tasks[i] >> bash_tasks[i+1]