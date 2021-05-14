import re
import json
import os
import sys

from django.views.generic import TemplateView

from community.views import get_header_and_footer
from community.git import (
    get_org_name,
    get_owner,
    get_deploy_url,
    get_upstream_deploy_url
)


class BuildLogsView(TemplateView):
    template_name = 'build_logs.html'

    def copy_build_logs_json(self, ci_build_jsons):
        """
        Copy the build logs detailed JSON file from ./_site directory to
         ./static and ./public directories
        :param ci_build_jsons: A dict of directories path
        :return: A boolean, whether the build file is copied
        """
        if os.path.isfile(ci_build_jsons['public_path']):
            if sys.platform == 'linux':
                os.popen('cp {} {}'.format(
                    ci_build_jsons['site_path'],
                    ci_build_jsons['public_path']))
                os.popen('cp {} {}'.format(
                    ci_build_jsons['site_path'],
                    ci_build_jsons['static_path']))
            else:
                os.popen('copy {} {}'.format(
                    ci_build_jsons['site_path'],
                    ci_build_jsons['public_path']))
                os.popen('copy {} {}'.format(
                    ci_build_jsons['site_path'],
                    ci_build_jsons['static_path']))
            return True
        return False

    def create_and_copy_build_logs_json(self, logs, level_specific_logs):
        """
        Create a build logs detailed json file in ./_site directory and copy
        that file in the ./static and ./public/static directories
        :param logs: A list of all lines in build log file
        :param level_specific_logs: A dict containing logs divided in their
        respective categories
        :return: A boolean, whether the files were copied or not
        """
        ci_build_jsons = {
            'site_path': './_site/ci-build-detailed-logs.json',
            'public_path': './public/static/ci-build-detailed-logs.json',
            'static_path': './static/ci-build-detailed-logs.json'
        }
        with open(ci_build_jsons['site_path'], 'w+') as build_logs_file:
            data = {
                'logs': logs,
                'logs_level_Specific': level_specific_logs
            }
            json.dump(data, build_logs_file, indent=4)
        return self.copy_build_logs_json(ci_build_jsons)

    def get_build_logs(self, log_file_path):
        """
        :param log_file_path: build logs file path
        :return: a tuple of two where the first element in tuple refers to
        a list of build logs in the file, and the second element is a dict
        which categorizes the build logs into 5 categories - INFO, DEBUG,
        WARNING, ERROR nad CRITICAL
        """
        log_lines = []
        log_level_specific_lines = {
            'INFO': [],
            'DEBUG': [],
            'WARNING': [],
            'ERROR': [],
            'CRITICAL': []
        }
        with open(log_file_path) as log_file:
            previous_found_level = None
            for line in log_file:
                log_lines.append(line)
                levels = re.findall(r'\[[A-Z]+]', line)
                if levels:
                    level = levels[0]
                    level = previous_found_level = level[1:-1]
                    log_level_specific_lines[level].append(line)
                elif previous_found_level:
                    log_level_specific_lines[previous_found_level].append(
                        line)
        return log_lines, log_level_specific_lines

    def check_build_logs_stored(self):
        """
        Check whether the build logs json file is copied to _site and public
        directories or not
        :return: A Boolean
        """
        log_file_path = './_site/community.log'
        log_file_exists = os.path.isfile(log_file_path)
        if log_file_exists:
            logs, level_specific_logs = self.get_build_logs(log_file_path)
            return self.create_and_copy_build_logs_json(logs,
                                                        level_specific_logs)
        return False

    def get_build_info(self):
        """
        Get the information about build, like who deployed the website i.e.
        owner, name of the organization or user etc.
        :return: A dict having information about build related details
        """
        data = {
            'Org name': get_org_name(),
            'Owner': get_owner(),
            'Deploy URL': get_deploy_url(),
        }
        try:
            data['Upstream deploy URL'] = get_upstream_deploy_url()
        except RuntimeError:
            data['Upstream deploy URL'] = 'Not found'
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_header_and_footer(context)
        context['build_info'] = self.get_build_info()
        context['logs_stored'] = self.check_build_logs_stored()
        return context
