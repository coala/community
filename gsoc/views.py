from django.shortcuts import render
from django.http import Http404
import logging

from .data import get_org_data
from .data import get_projects_data
from community.git import get_owner
from gsoc.config import get_year

logger = logging.getLogger(__name__ + '.index')
org_name = get_owner()
year = get_year()


def index(request):
    try:
        org = get_org_data()
    except FileNotFoundError:
        logger.info('GSoC data not available')
        raise Http404
    else:
        for key in org.keys():
            id = org.get(key).get('id')
            name = org.get(key).get('name')
            tagline = org.get(key).get('tagline')
            description = org.get(key).get('description')
            tech = []
            for technology in org.get(key).get('technologies').values():
                tech.append(technology)

            return render(request, 'gsoc.html', {'id': id,
                                                 'name': name,
                                                 'tagline': tagline,
                                                 'description': description,
                                                 'tech': tech
                                                 })


def projects(request):
    try:
        org = get_org_data()
    except FileNotFoundError:
        logger.info('GSoC data not available')
        raise Http404
    else:
        for key in org.keys():
            name = org.get(key).get('name')
        projects = get_projects_data()
        projects_list = []
        for key in projects.keys():
            mentors = []
            for mentor in projects.get(key).get('mentors').values():
                mentors.append(mentor)
            item = {
                'id': projects.get(key).get('id'),
                'summary': projects.get(key).get('summary'),
                'title': projects.get(key).get('title'),
                'student': projects.get(key).get('student'),
                'code': projects.get(key).get('project_code'),
                'link': projects.get(key).get('project_link'),
                'mentors': mentors
            }
            projects_list.append(item)
        return render(request, 'gsoc_projects.html',
                      {
                        'project_list': projects_list,
                        'org_name': name
                      })
