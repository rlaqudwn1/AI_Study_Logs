from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def print_world() -> None:
 print("world")

with DAG(
    dag_id="hello_world",
    description="My_dags",
    start_date=days_ago(2), # 2일전부터 시작
    schedule_interval="0 6 * * *", # 매일 6에 실행
    tags=["my_dags"],
    catchup=False
) as dag:

    t1 = BashOperator(
        task_id="print_hello",
        bash_command="echo Hello",
        owner="admin",
        retries=3, # 재시도 리트라이 횟수
        retry_delay=timedelta(minutes=5), # 재시도 리트라이 시간
    )

    t2 = PythonOperator(
        task_id="print_world",
        python_callable=print_world,
        depends_on_past=True,
        owner="admin",
        retries=3,
        retry_delay=timedelta(minutes=5)
    )

    # Task 순서
    t1 >> t2

#catchup : 과거에 지나간 일자의 DAG을 실행할지 결정하는 옵션
# True : DAG에서 정의한 start_date 에서 현재까지 미실행된 모든 스케쥴에 대해서 실행한다

# FALSE : 과거에 있는 스케쥴을 실행하지 않음.

# depends_on_past 과거에 의존할 것인가

# 이전 Task와 상관없이 작업을 수행하고 싶은지 고민한다
# True: 이전 DAG이 성공으로 완료되어야 이후의 DAG이 실행된다
# False :  이전 DAG의 여부와 관계없이 Scheduler 임의로 실행


