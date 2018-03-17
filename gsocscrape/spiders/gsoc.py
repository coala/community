import scrapy
import string
import json
import logging

from ruamel.yaml import YAML
import os.path
from collections import OrderedDict
from community.git import get_owner
from gsoc.config import get_year


logger = logging.getLogger(__name__ + '.index')
org_name = get_owner()
year = get_year()
yaml = YAML()


class GsocSpider(scrapy.Spider):
    name = 'gsoc'
    start_urls = [
        'https://summerofcode.withgoogle.com/archive/{}/organizations'
        .format(year),
    ]

    def parse(self, response):
        home_url = 'https://summerofcode.withgoogle.com/'\
                   'archive/{}/organizations/'.format(year)
        selector = "//li[contains(.,'{org_name}')]/a/@href".format(
            org_name=org_name)
        organization_link = response.xpath(selector)

        if(organization_link):
            organization_link = organization_link[0].extract().split('/')[4]
        else:
            logger.info('Organisation {} does not exist in GSoC for {}'.format(
                org_name, year
            ))
            return

        follow_link = home_url + organization_link
        yield response.follow(follow_link, self.parse_org)

    def parse_org(self, response):
        project_url = 'https://summerofcode.withgoogle.com/'\
                      'archive/{}/projects/'.format(year)

        technology = {}

        id = response.url.split('/')[-2]
        org_name = response.css('h3.banner__title::text')[0].extract()
        org_tagline = response.css('h4.org__tagline::text')[0].extract()
        org_long_description = response.xpath(
            "//div[@class='org__long-description']")[0].extract()
        org_technologies = response.xpath(".//div[@class='org__meta']/div"
                                          "[contains(.,'Technologies')]/ul/"
                                          'li/text()').extract()

        count = 0
        for tech in org_technologies:
            technology['%s' % str(count)] = tech
            count = count + 1

        item = {
            'id': id,
            'name': org_name,
            'tagline': org_tagline,
            'description': org_long_description,
            'technologies': technology
        }
        org_data = {}
        org_data[int(item['id'])] = item

        with open(os.path.join('_site', 'gsoc_org_info.yaml'), 'w') as f:
            yaml.dump(org_data, f)

        # Overwrite any previous data with empty dataset
        open(os.path.join('_site', 'gsoc_project_info.yaml'), 'w').close()

        for res in response.css('a.archive-project-card__link'):
            link = res.xpath('@href').extract()[0]
            link = link.split('/')[4]
            url_project = project_url + link
            yield response.follow(url_project, self.parse_project)

    def parse_project(self, response):
        mentors = []
        org_url = 'https://summerofcode.withgoogle.com/'\
                  'archive/{}/organizations/'.format(year)
        page = response.url.split('/')[-2]

        project_id = page
        project_title = response.css('h3.banner__title::text')[0].extract()
        project_summary = response.xpath(
            "//div[@class='org__long-description']")[0].extract()
        project_organization_code = response.css(
            'md-card.org__info-card a::attr(href)')[0].extract().split('/')[4]
        project_link = response.url
        project_organization_url = org_url + project_organization_code
        project_organization_name = response.css('md-card.org__info-card '
                                                 'a::text')[3].extract()
        project_code = response.css('md-card.org__info-card '
                                    'a::attr(href)')[1].extract()
        project_student = response.xpath(
            ".//div[@class='org__meta']/div[contains(.,'Student')]/"
            'div/text()')[0].extract()
        project_mentors = response.xpath(
            ".//div[@class='org__meta']/div[contains(.,'Mentors')]"
            '/ul/li/text()').extract()
        ment = {}
        count = 0
        for mentor in project_mentors:
            ment['%s' % str(count)] = mentor
            count = count + 1

        item = {
            'id': project_id,
            'title': project_title,
            'summary': project_summary,
            'student': project_student,
            'mentors': ment,
            'organization_name': project_organization_name,
            'organization_code': project_organization_code,
            'organization_url': project_organization_url,
            'project_link': project_link,
            'project_code': project_code
        }
        project_data = {}
        project_data[int(item['id'])] = item

        with open(os.path.join('_site', 'gsoc_project_info.yaml'), 'a') as f:
            yaml.dump(project_data, f)
