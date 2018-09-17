coala_mentors = [
]

corobo_mentors = [
]

gitmate_mentors = [
]

pm_mentors = [
]

# Note this includes all issues scheduled in 2017, most of which are
# already completed.
# They are automatically skipped for 2018, and will be shown as completed
# in GCI 2017, or after GCI.
# All 'gci-leaders' tasks are completed, and are not available in GCI 2018,
# due to rule changes by Google around identity.
# As of 17 Sept there were 30 issues ready, and 18 new moban issues.
all_issues = {
    'manu-chroma/username-availability-checker': {
        'short_name': 'username-availability',
        'mentors': [],
        'low': {
            22: {'Python', 'Flask', 'heroku'},
            21: {'tooltop', 'Flask', 'Python', 'heroku'},
            33: {'GitHub', 'Flask', 'Python', 'heroku'},
            37: {'Gravatar', 'Flask', 'Python', 'heroku'},
            38: {'Travis', 'Python', 'CI'},
            39: {'openSUSE', 'Flask', 'Python', 'heroku'},
            40: {'Wikimedia', 'Flask', 'Python', 'heroku'},
            51: {'asciinema', 'Flask', 'Python', 'heroku'},
        },
        'medium': {
            11: {'regex', 'Python', 'Flask', 'heroku'},
            31: {'pytest', 'Flask', 'async', 'Travis'},
            30: {'env', 'Python', 'Flask', 'heroku'},
            24: {'OpenHub', 'DeviantArt', 'Flask', 'Python'},
            47: {'pytest', 'Flask', 'Python', 'random'},
            15: {'RAML', 'Flask', 'Python', 'heroku'},
            52: {'JavaScript', 'Flask', 'Python', 'heroku'},
            66: {'OpenHub'},
        },
        'high': {
            25: {'heroku', 'Flask', 'Python', 'OSINT'},
            35: {'avatar', 'Flask', 'Python', 'OSINT'},
            36: {'pytest', 'Flask', 'Python'},
        },
    },
    'community': {
        'mentors': corobo_mentors + gitmate_mentors,
        'newcomer': {
            10: {'README', 'markdown'},
        },
        'low': {
            5: None,
            6: None,
            7: {'time'},
            8: {'Travis'},
            40: {'Twitter'},
            57: {'RSS', 'GCI'},
        },
        'medium': {
            1: {'logo'},
            3: {'data', 'JSON', 'mock'},
            9: {'logging'},
            42: {'django', 'logo'},
            56: {'IGitt'},
            
        },
        'high': {
            25: {'analytics'}
        }
    },
    'landing': {
        'gitlab_id': 2239655,
        'mentors': gitmate_mentors,
        'newcomer': {
        },
        'low': {
            26: {'bots', 'markdown'},
            47: {'CORS', 'Django'},
        },
        'high': {
            44: {'cron', 'GitHub'},
        },
    },
    'cEPs': {
        'mentors': [],
        'newcomer': {
        },
        'low': {
            73: None,
        },
    },
    'devops': {
        'mentors': [],
        'newcomer': {
        },
        'low': {
        },
        'medium': {
            55: {'emoji', 'twemoji', 'tofu', 'devops'},
        },
    },
    'gh-board': {
        'mentors': [],
        'low': {
            3: None,
        },
        'medium': {
            6: None,
        },
    },
    'gci-leaders': {
        'mentors': [],
        'newcomer': {
            2: {'README', 'markdown'},
            6: {'license', 'MIT'},
            22: {'UI', 'HTML'},
            24: {'UI', 'HTML'},
            26: {'UI', 'HTML'},
            30: {'HTML'},
        },
        'low': {
            1: {'timezones'},
            3: {},
            16: None,
            11: {'.coafile', 'linting', 'eslint'},
            17: {'UI'},
            21: {'UI', 'HTML'},
            25: {'UI', 'logo', 'rights'},
            27: {'GitHub', 'API', 'open data'},
            29: {'Mobile', 'HTML'},
            34: {'linting', '.coafile'},
            57: {'JSON', 'YAML', 'NodeJS'},
            64: {'Twitter', 'Google+'},
            71: {'HTML', 'CSS'},
            80: {'Redundant code'},
            73: {'Catrobat', 'template'},
            88: {'OpenGraph', 'Facebook', 'UI'},
            102: {'Wikidata', 'StackOverflow', 'UI'}
        },
        'medium': {
            4: {'scraping'},
            5: {'scraping'},
            7: {'GitHub'},
            9: {'GitLab'},
            23: {'UI', 'random', 'math', 'Node', 'JavaScript'},
            32: {'GitHub', 'API'},
            33: {'Gender', 'Gendergap', 'NLP'},
            38: {'i18n'},
            54: {'twitter', 'outreach'},
            51: None,
            65: {'RSS', 'ATOM'},
            70: {'Google Groups'},
            77: {'scrapping', 'UI'},
            89: {'Netlify', 'UI'},
            93: {'GitHub'},
            100: {'GitHub'},
        },
        'high': {
            # 8: {'GitHub', 'api'},
            35: {'NLP'},
            53: {'npm', 'chat', 'UI'},
            63: {'Wikipedia', 'Wikidata', 'sparql'},
            91: {'RSS'},
        },
    },
    'corobo': {
        'mentors': corobo_mentors,
        'newcomer': {
            251: {'markdown', 'chatops'},
            345: {'stackoverflow'},
            367: {'documentation'},
            229: {'markdown'},
            307: {'documentation'},
            385: {'documentation'},
            329: None,
            362: None,
            401: {'documentation'},
            250: {'emoji'},
            426: None,
        },
        'low': {
            335: None,
            337: None,
            296: None,
            252: None,
            166: None,
            369: None,
            384: None,
            469: None,
            336: None,
            412: None,
            426: None,
        },
        'medium': {
            333: None,
            391: None,
            257: {'jinja2'},
            420: {'analysis', 'IGitt'}
        },
        'high': {
            171: None,
        }
    },
    'documentation': {
        'mentors': coala_mentors[:30],
        'newcomer': {
            492: None,
            358: ['bash', 'docker'],
        },
        'low': {
            478: {'CI', '.coafile', 'spelling'},
            382: {'docker', 'travis', 'CI', 'reStructuredText'},
            259: {'Java', 'reStructuredText'},
        }
    },
    'projects': {
        'mentors': coala_mentors[:30],
        'newcomer': {
            221: None,
        },
        'low': {
            359: ['AngularJS'],
            354: ['AngularJS'],
        }
    },
    'coala-quickstart': {
        'mentors': coala_mentors[:30],
        'low': {
            158: ['logging', 'python3'],
            171: ['pytest', 'AppVeyor CI', 'setup.cfg', 'Python3'],
        }
    },
    'coala-utils': {
        'gitlab_id': 1259821,
    },
    'coala': {
        'mentors': {
            'aspects': ['foo@bar.com'],
            '*': coala_mentors[:30],
        },
        'newcomer': {
            4771: None,
            4840: None,
            4879: None,
            4017: None,
        },
        'low': {
            4583: None,
            4816: {'CI', '.coafile', 'spelling'},
            4886: None,
            4887: None,
            4888: None,
        },
        'medium': {
            4514: {'Debian', 'packaging', 'csslint'},
            4952: {'shellcheck', '.coafile', 'apt-get', 'TravisCI'},
            4982: {'aspects', 'indentation', 'style'},
        },
    },
    'package_manager': {
        'gitlab_id': 2180762,
        'mentors': pm_mentors,
        'newcomer': {
            155: None,
            127: None,
            109: None,
            84: None,
        },
        'low': {
            125: {'Go'},
            118: {'apt-get', 'Ubuntu'},
            73: {'Rscript', 'doctest', 'docstring'},
            104: {'grep', 'regex'},
            163: {'docstring'},
            167: {'exit-codes', 'shell', 'sarge'},
        },
        'medium': {
            138: {'Go'},
            115: {'Perl', 'CPAN'},
            122: {'PHP', 'PEAR'},
            131: {'macOS', 'MacPorts'},
            29: {'Windows', 'NuGet'},
        },
        'high': {
            67: {'Haskell'},
        },
    },
    'cib': {
        'gitlab_id': 1490040,
    },
    'gitmate/open-source/IGitt': {
        'gitlab_id': 765988,
        'mentors': pm_mentors,
        'low': {
            79: None,
            76: {'YAML'},
            69: None,
            82: None,
            49: None,
            81: {'GitHub', 'exceptions', 'logging'},
            54: {'vcr', 'unittest'}
        },
        'medium': {
            90: {'GitHub', 'GitLab'},
        }
    },
    'gitmate/open-source/gitmate-2': {
        'gitlab_id': 1415047,
        'mentors': gitmate_mentors,
        'low': {
            207: {'django'},
        },
    },
    'gitmate/open-source/gitmate-2-frontend': {
        'gitlab_id': 3092199,
        'mentors': gitmate_mentors,
        'low': {
            62: {'UI', 'Angular', 'Node', 'JavaScript'},
            63: {'UI', 'Angular', 'Node', 'JavaScript'},
        },
        'medium': {
            74: {'UI', '404', 'error'},
        }
    },
    'coala-brackets': {
        'mentors': [],
        'low': {},
        'medium': {
            7: {'unit tests', 'CI', 'JavaScript', 'Node'},
        }
    }
}
