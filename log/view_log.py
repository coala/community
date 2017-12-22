from django.shortcuts import render


def index(request):
    logs = '<br>'.join(get_logs()).split('<br>')
    return render(request, 'logs.html', context={
        'logs': logs
    })


def get_logs():
    with open('./_site/community.log') as log_file:
        for line in log_file:
            yield line.rstrip()
