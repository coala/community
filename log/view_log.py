from django.http import HttpResponse

def index(request):
    logs = get_logs()
    return HttpResponse('<br>'.join(logs))

def get_logs():
    with open('./_site/community.log') as log_file:
        for line in log_file:
            yield line.rstrip()
