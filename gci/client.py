# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The GCI API Client.  A thin wrapper around the GCI API.

Exmple usage:

client = gciclient.GCIAPIClient(
      auth_token='xxxxxxxxxxxxxx',
      url_prefix='https://codein.withgoogle.com',
      debug=False)

client.NewTask(myTaskDict)
"""

import json
import logging
import sys

if sys.version_info[0] == 2:
    import urlparse
else:
    from urllib import parse as urlparse


import requests


class GCIAPIClient(object):
  """GCIAPIClient provides a thin wrapper around the GCI Task API.

  A GCIAPIClient simplifies working with tasks by forming the HTTP requests on
  behalf of the caller.

  Attributes:
    url_prefix: A string prefix for the codin URL
    headers: A dictionary of HTTP headers
  """

  def __init__(self, auth_token=None,
               url_prefix='https://codein.withgoogle.com/',
               debug=False):
    self.url_prefix = urlparse.urljoin(url_prefix, 'api/program/current/')
    self.headers = {
        'Authorization': 'Bearer %s' % auth_token,
        'Content-Type': 'application/json',
    }

    if debug:
      logging.basicConfig()
      logging.getLogger().setLevel(logging.DEBUG)
      requests_log = logging.getLogger('requests.packages.urllib3')
      requests_log.setLevel(logging.DEBUG)
      requests_log.propagate = True

  def _Url(self, path):
    return urlparse.urljoin(self.url_prefix, path) + '/'

  def ListTasks(self, page=1):
    """Fetches a list of tasks.

    Args:
      page: Which page of results to return.

    Returns:
      A JSON encoded list of tasks.

    Raises:
      HTTPError: a 4XX client error or 5XX server error response was returned.
    """
    r = requests.get(self._Url('tasks'), headers=self.headers,
                     params={'page': page})
    r.raise_for_status()
    return r.json()

  def GetTask(self, task_id):
    """Fetches a single task.

    Args:
      task_id: An integer id for the task.

    Returns:
        A JSON encoded task.

    Raises:
      HTTPError: a 4XX client error or 5XX server error response was returned.
    """
    r = requests.get(self._Url('tasks/%d' % task_id), headers=self.headers)
    r.raise_for_status()
    return r.json()

  def NewTask(self, task):
    """Creates a single new task.

    Args:
      task: A task object.

    Returns:
      A JSON encoded response.

    Raises:
      HTTPError: a 4XX client error or 5XX server error response was returned.
    """
    r = requests.post(self._Url('tasks'), headers=self.headers,
                      data=json.dumps(task))
    r.raise_for_status()
    return r.json()

  def UpdateTask(self, task_id, task):
    """Modifies a single task.

    Args:
      task_id: An integer id for the task.
      task: A task object.

    Returns:
      A JSON encoded response.

    Raises:
      HTTPError: a 4XX client error or 5XX server error response was returned.
    """
    r = (
        requests.put(
            self._Url('tasks/%d' % task_id), data=json.dumps(task),
            headers=self.headers))
    r.raise_for_status()
    return r.json()

  def DeleteTask(self, task_id):
    """Deletes a single task.

    Args:
      task_id: An integer id for the task.

    Returns:
      A JSON encoded response, if there is content in the response.
      Otherwise None.

    Raises:
      HTTPError: a 4XX client error or 5XX server error response was returned.
    """
    r = (
        requests.delete(
            self._Url('tasks/%d' % task_id),
            headers=self.headers))
    r.raise_for_status()
    # DELETE returns nothing on success, don't try and parse it.
    if r.content:
      return r.json()
    return

  def ListTaskInstances(self, page=1):
    """Fetches a list of tasks.

    Args:
      page: Which page of results to return.

    Returns:
      A JSON encoded list of task instances.

    Raises:
      HTTPError: a 4XX client error or 5XX server error response was returned.
    """
    r = requests.get(self._Url('instances'), headers=self.headers,
                     params={'page': page})
    r.raise_for_status()
    return r.json()

  def GetTaskInstance(self, task_instance_id):
    """Fetches a single task.

    Args:
      task_instance_id: An integer id for the task instance.

    Returns:
        A JSON encoded task instance.

    Raises:
      HTTPError: a 4XX client error or 5XX server error response was returned.
    """
    r = requests.get(self._Url('instances/%d' % task_instance_id),
                     headers=self.headers)
    r.raise_for_status()
    return r.json()
