import asyncio
import telegram
from .models import Task, Employee
from django.conf import settings

def send_task_notification(task_id, employee_id, message_type):
    task = Task.objects.get(id=task_id)
    employee = Employee.objects.get(id=employee_id)
    token = settings.TELEGRAM_TOKEN
    chat_id = employee.telegram_chat_id
    bot = telegram.Bot(token=token)
    if message_type == 'started':
        message = f'Вы получили новую задачу:"{task.task_text}"'
    elif message_type == 'returned':
        message = f'Задача "{task.task_text}" возвращена в работу.'
    elif message_type == 'edit':
        message = f'Задача "{task.task_text}" отредактирована.'

    async def send_telegram_message(chat_id, message):
        await bot.send_message(chat_id=chat_id, text=message)

    if chat_id is not None:
        asyncio.run(send_telegram_message(chat_id=chat_id, message=message))
