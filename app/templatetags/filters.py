from datetime import datetime

from django import template

register = template.Library()


@register.filter
def get_now(user):
    now = datetime.now()
    try:
        return now
    # return len(user.profissional.contratodeservico_set.filter(created_at__month=now.month, status='EM ANDAMENTO'))
    except (Exception,):
        return 0
