from db import DB_Connector


class TaskScheduler:
    def __init__(self, db_file):
        self.db_connector = DB_Connector(db_file)

    def add_task(self,
                 task_name, description,
                 priority, status, deadline, comment):
        self.db_connector.add_record(task_name,
                                     description, priority,
                                     status, deadline, comment)

    def delete_task(self, record_id):
        self.db_connector.delete_record(record_id)

    def update_task(self, record_id,
                    task_name, description, priority,
                    status, deadline, comment):
        self.db_connector.update_record(record_id,
                                        task_name,
                                        description, priority, status,
                                        deadline, comment)

    def get_all_tasks(self):
        return self.db_connector.get_all_records()

    def get_tasks_by_params(self, **params):
        return self.db_connector.get_records_by_params(**params)

    def close(self):
        self.db_connector.close_connection()


if __name__ == "__main__":
    scheduler = TaskScheduler("scheduler.db")

    scheduler.close()
