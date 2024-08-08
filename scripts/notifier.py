from airflow.operators.email import EmailOperator

def send_email(task_id, to, subject, html_content, dag):
    operator = EmailOperator(
        task_id=task_id,
        to=to,
        subject=subject,
        html_content=html_content,
        dag=dag
    )
    return operator