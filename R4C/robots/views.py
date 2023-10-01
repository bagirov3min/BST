from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Count
from .forms import RobotForm
from .models import Robot
from datetime import datetime, timedelta
import json
import os
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd


@csrf_exempt
def add_robot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = RobotForm(data)

        if form.is_valid():
            robot = form.save(commit=False)
            robot_serial = f"{robot.model}-{robot.version}"
            robot.serial = robot_serial
            robot.save()
            return JsonResponse({'message': 'Robot created successfully'}, status=201)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)


def generate_excel(request):
    start_date = datetime(2023, 9, 25, 0, 0)
    current_date = datetime.now()
    while current_date >= start_date + timedelta(days=7):
        start_date += timedelta(days=7)
    end_date = datetime.now()

    wb = Workbook()
    models = Robot.objects.values_list("model", flat=True).distinct()
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"summary_{current_time}.xlsx"
    data_found = False

    for model in models:
        data = Robot.objects.filter(
            model=model,
            created__range=(start_date, end_date)
        ).values("model", "version").annotate(total=Count("id"))

        df = pd.DataFrame.from_records(data)

        if not df.empty:
            data_found = True
            ws = wb.create_sheet(title=model)
            for row in dataframe_to_rows(df, index=False, header=True):
                ws.append(row)
    if data_found:
        default_sheet = wb.get_sheet_by_name("Sheet")
        wb.remove(default_sheet)
        file_path = os.path.join(settings.MEDIA_ROOT, 'excel_files', file_name)
        wb.save(file_path)
        return JsonResponse({"file_url": os.path.join(settings.MEDIA_URL, 'excel_files', file_name)})
    return JsonResponse({'errors': "На этой неделе еще не было создано роботов"}, status=400)