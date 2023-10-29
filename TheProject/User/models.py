from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

from django.db.models.signals import post_delete, m2m_changed
from django.dispatch import receiver

from .usertasks import send_message
from TheProject.celery import app

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    telegram_id = models.IntegerField(_('telegram id'),blank=True, null=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Homework(models.Model):
    title = models.CharField(_('Title'), max_length=300)
    description = models.TextField(_('Description'))
    date = models.DateTimeField(_('Date'), default=timezone.now)
    file = models.URLField(_('File'))
    user = models.ManyToManyField(CustomUser)
    celery_check = models.BooleanField(_('Telegram notifications'), blank=True)
    celery_task_id = models.CharField(max_length=36, blank=True, null=True)

    def __str__(self):
        return self.description
    

@receiver(m2m_changed, sender=Homework.user.through)
def homework_created(sender, instance, action, **kwargs):
    if action == 'post_add' and instance.celery_check:
        # Users have been assigned and celery_check is True
        chat_ids = list(instance.user.select_related('customusermodel').values_list('telegram_id', flat=True))
        result = set_notifications(instance.date, chat_ids, instance)
        instance.celery_task_id = result
        instance.save()


@receiver(post_delete, sender=Homework)
def homework_deleted(sender, instance, **kwargs):
    task_ids = instance.celery_task_id
    
    task_ids = task_ids.strip("][").replace("'","").split(', ')
    if task_ids:
            try:
                app.control.revoke(task_ids, terminate=False)
            except TimeoutError as e:
                print(e)

def set_notifications(due_date, chat_ids, hw):
    difference = (due_date-timezone.now()).days
    message = f"Title: {hw.title}\nDescription: {hw.description}\nDue date: {hw.date.strftime('%Y-%m-%d %H:%M')}\nHomework file: {hw.file}"
    returnList = []
    result = False
    
    for chat_id in chat_ids:
        send_message({'chat_id': chat_id,
                    'text':f"You got a new homework!\n\n{message}"})
        if difference > 7:
            result = send_notifications(chat_id, 
                                [(due_date-timedelta(days=5)),(due_date-timedelta(days=3)),(due_date-timedelta(days=1)),(due_date-timedelta(hours=12)),(due_date-timedelta(hours=3))],
                                [f"Your homework is due in 5 days!\n\n{message}",
                                 
                                f"Your homework is due in 3 days!\n\n{message}",
                                
                                f"Your homework is due in 1 day!\n\n{message}",
                                
                                f"Your homework is due in 12 hours!\n\n{message}",
                                
                                f"Your homework is due in 3 hours!\n\n{message}"])
        elif difference > 3:
            result = send_notifications(chat_id, 
                                [(due_date-timedelta(days=1)),(due_date-timedelta(hours=12)),(due_date-timedelta(hours=3))],
                                [f"Your homework is due in 1 day!\n\n{message}",
                                
                                f"Your homework is due in 12 hours!\n\n{message}",
                                
                                f"Your homework is due in 3 hours!\n\n{message}"])
        elif difference >= 1:
            result = send_notifications(chat_id, 
                                [(due_date-timedelta(hours=12)),(due_date-timedelta(hours=3))],
                                [f"Your homework is due in 12 hours!\n\n{message}",
                                
                                f"Your homework is due in 3 hours!\n\n{message}"])
        if result:
            returnList.append(result)
    return [item for sublist in returnList for item in sublist] # Nested list -> Flat list



def send_notifications(chat_id, dates, answers):
    tasksList = []
    for date,answer in zip(dates,answers):
        data = {
                                        'chat_id': chat_id,
                                        'text': answer
                                    }
        result = send_message.apply_async(args=[data], eta=date, expires=(date + timedelta(hours=2)))
        print('send_not', result.id)
        tasksList.append(result.id)
    print('send_not taskList', tasksList)
    return tasksList
