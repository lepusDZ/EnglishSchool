from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def am_pm(value):
    if value == "до полудня":
        return "AM"
    elif value == "після полудня":
        return "PM"
    else:
        return value  # Return the input value unchanged if it's not one of the Ukrainian time formats

@register.filter
def is_due(homework):
    """
    Custom template filter to check if the homework is due in the future.
    """
    return homework.date > timezone.now()


@register.simple_tag
def get_homework_file(day, homework_dict):
    if day in homework_dict:
        homework = homework_dict[day]
        return homework[0].file

@register.simple_tag
def get_homework_name(day, homework_dict):
    if day in homework_dict:
        homework = homework_dict[day]
        return homework[0].title

