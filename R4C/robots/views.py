from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import RobotForm


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
