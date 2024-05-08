from celery import Celery, shared_task, chain
import database as db
from crypto import key_gen

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

@shared_task
def load_crypt_enums_task():
    return db.load_all_crypt_enums()

@shared_task
def create_user_task(uid, master_key):
    if db.create_user(uid, master_key):
        return None
    else:
        raise ValueError("Failed to create user")

@shared_task
def insert_keys_task(enum_ids, uid, master_key):
   
    if db.insert_keys_into_enum_table(uid, 
                                      enum_ids, 
                                      key_gen.generate_derived_key(master_key),
                                      master_key):
        pass
    else:
        raise ValueError("Failed to insert keys")


# You could chain these tasks together as a separate shared task.
@shared_task
def handle_keygen(uid, encoded_master_key):
    print("In the process")
    result = chain(
        load_crypt_enums_task.si(),
        insert_keys_task.s(uid, encoded_master_key)
    )()
    print("Didn't make it out")
    return {"status": "Chain started", "task_id": result.id}

@shared_task
def handle_user_creation(uid, master_key):
    result = chain(
        create_user_task.s(uid, master_key),
        signup_success_callback.si()
    )() 
    return result

@shared_task
def signup_success_callback():
    if True:
        # Task executed successfully
        print("Signup process completed successfully")
    else:
        # Task execution failed
        print("Signup process failed")