# from tasks import add
#
# if __name__ == '__main__':
#     print('start task')
#     result = add.delay(8, 8)
#     print("end task")
#     print(result.ready())

from celery_app import task1, task2

# task1.add.delay(2, 4)
# task2.multiply.delay(4, 5)
print("end ....")
