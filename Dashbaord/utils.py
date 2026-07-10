import calendar
from datetime import timedelta, datetime
from django.utils import timezone


def get_date_range_from_request(request):

    filter_type = request.GET.get('filter', 'all_time')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    month_str = request.GET.get('month')
    year_str = request.GET.get('year')

    now_date = timezone.now()
    start_date = None
    end_date = now_date

    if filter_type == 'today':
        start_date = now_date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif filter_type == 'this_week':
        start_date = (now_date - timedelta(days=now_date.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    elif filter_type == 'this_month':
        start_date = now_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif filter_type == 'this_year':
        start_date = now_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif filter_type == 'custom_month' and month_str and year_str:
        try:
            m, y = int(month_str), int(year_str)
            last_day = calendar.monthrange(y, m)[1]
            start_date = now_date.replace(year=y, month=m, day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = now_date.replace(year=y, month=m, day=last_day, hour=23, minute=59, second=59, microsecond=999999)
        except ValueError:
            pass
    elif filter_type == 'custom_year' and year_str:
        try:
            y = int(year_str)
            start_date = now_date.replace(year=y, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = now_date.replace(year=y, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        except ValueError:
            pass
    elif filter_type == 'custom' and start_date_str and end_date_str:
        try:
            parsed_start = datetime.strptime(start_date_str, "%Y-%m-%d")
            parsed_end = datetime.strptime(end_date_str, "%Y-%m-%d")
            start_date = timezone.make_aware(parsed_start) if timezone.is_naive(parsed_start) else parsed_start
            end_date = (timezone.make_aware(parsed_end) if timezone.is_naive(parsed_end) else parsed_end).replace(
                hour=23, minute=59, second=59, microsecond=999999
            )
        except ValueError:
            pass

    return start_date, end_date
