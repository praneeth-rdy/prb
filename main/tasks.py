from background_task import background

@background(schedule=60, remove_existing_tasks=True)
def contact_erp_task():
    print('Hello..')