from gamification.models import (
    Level,
    BadgeActivity,
    Badge,
)


def create_levels():
    """
    Create levels which will be used in the gamification system.
    """
    level_objects_list = [
        Level(number=1, min_score=0, max_score=5, name='Fresher'),
        Level(number=2, min_score=5, max_score=20, name='Beginner-I'),
        Level(number=3, min_score=20, max_score=30, name='Beginner-II'),
        Level(number=4, min_score=30, max_score=40, name='Intermediate-I'),
        Level(number=5, min_score=40, max_score=50, name='Intermediate-II'),
        Level(number=6, min_score=50, max_score=60, name='Master'),
        Level(number=7, min_score=60, max_score=70, name='Expert'),
        Level(number=8, min_score=70, max_score=200, name='Legend'),
    ]
    Level.objects.bulk_create(level_objects_list)


def create_badge_activities():
    b_activity__object_list = [
        BadgeActivity(
            name='Created a difficulty/newcomer type/bug issue'),
        BadgeActivity(
            name='Created a difficulty/low type/bug issue'),
        BadgeActivity(
            name='Solved a importance/high issue'),
        BadgeActivity(
            name='Solved a importance/medium issue'),
        BadgeActivity(
            name='Solved a importance/critical issue'),
        BadgeActivity(
            name='Created a area/documentation difficulty/newcomer issue'),
        BadgeActivity(
            name='Created a area/documentation difficulty/low issue'),
        BadgeActivity(
            name='Created a difficulty/newcomer type/feature issue'),
        BadgeActivity(
            name='Created a difficulty/low type/feature issue'),
        BadgeActivity(
            name='Created a area/genericbears bear proposal issue'),
        BadgeActivity(
            name='Created a area/nativebears bear proposal issue'),
        BadgeActivity(
            name='Created a area/lintbears bear proposal issue'),
        BadgeActivity(
            name='Created a difficulty/newcomer issue'),
        BadgeActivity(
            name='Created a difficulty/low issue'),
        BadgeActivity(
            name='Created a bear proposal issue'),
        BadgeActivity(
            name='Solved a bear proposal issue'),
        BadgeActivity(
            name='Solved a difficulty/newcomer issue'),
        BadgeActivity(
            name='Solved a difficulty/low issue'),
        BadgeActivity(
            name='Solved a difficulty/newcomer type/bug issue'),
        BadgeActivity(
            name='Solved a difficulty/low type/bug issue'),
        BadgeActivity(
            name='Created a area/documentation issue'),
        BadgeActivity(
            name='Solved a area/documentation issue'),
        BadgeActivity(
            name='Solved a difficulty/newcomer type/feature issue'),
        BadgeActivity(
            name='Solved a difficulty/low type/feature issue'),
        BadgeActivity(
            name='Solved a area/genericbears bear proposal issue'),
        BadgeActivity(
            name='Solved a area/lintbears bear proposal issue'),
    ]
    BadgeActivity.objects.bulk_create(b_activity__object_list)


def create_badges():
    badge_objects_list = [
        Badge(
            number=1,
            name='The Bug Finder',
            details='The one who find bugs in the existing codebase',
        ),
        Badge(
            number=2,
            name='The Bear Hunter',
            details='The one who create issues about new bears',
        ),
        Badge(
            number=3,
            name='The Bear Writer',
            details='The one who write new bears',
        ),
        Badge(
            number=4,
            name='The Bug Solver',
            details='The one who find bugs in the existing codebase',
        ),
        Badge(
            number=5,
            name='The Helper',
            details='The one who help the community',
        ),
        Badge(
            number=6,
            name='The Quick Helper',
            details='The one who help the community even quicker',
        ),
        Badge(
            number=7,
            name='The Reviewer',
            details='The one who review others pull requests',
        ),
        Badge(
            number=8,
            name='The Super Reviewer',
            details='The one who is the legend of reviewing',
        ),
        Badge(
            number=9,
            name='The Doc-Care',
            details='The one who takes care of the docs',
        ),
        Badge(
            number=10,
            name='The All-Rounder',
            details='The one who can apply for the org developer role',
        ),
    ]
    Badge.objects.bulk_create(badge_objects_list)


def add_activities_to_badges():
    """
    This method adds activities to the badges created above.

    Note that there are no acitivites added in 'The Reviewer'
    and 'The Super Reviewer' badges.
    """
    # Adding activities to the bug hunter badge
    bug_hunter_badge = Badge.objects.get(
        name='The Bug Finder')
    bug_hunter_activity1 = BadgeActivity.objects.get(
        name='Created a difficulty/newcomer type/bug issue')
    bug_hunter_activity2 = BadgeActivity.objects.get(
        name='Created a difficulty/low type/bug issue')
    bug_hunter_activities_list = [
        bug_hunter_activity1,
        bug_hunter_activity2,
    ]
    bug_hunter_badge.b_activities.add(*bug_hunter_activities_list)

    # Adding activities to the bear hunter badge
    bear_hunter_badge = Badge.objects.get(
        name='The Bear Hunter')
    bear_hunter_activity1 = BadgeActivity.objects.get(
        name='Created a area/genericbears bear proposal issue')
    bear_hunter_activity2 = BadgeActivity.objects.get(
        name='Created a bear proposal issue')
    bear_hunter_activities_list = [
        bear_hunter_activity1,
        bear_hunter_activity2,
    ]
    bear_hunter_badge.b_activities.add(*bear_hunter_activities_list)

    # Adding activities to the bear writer badge
    bear_writer_badge = Badge.objects.get(
        name='The Bear Writer')
    bear_writer_activity1 = BadgeActivity.objects.get(
        name='Solved a area/genericbears bear proposal issue')
    bear_writer_activity2 = BadgeActivity.objects.get(
        name='Solved a area/lintbears bear proposal issue')
    bear_writer_activities_lits = [
        bear_writer_activity1,
        bear_writer_activity2,
    ]
    bear_writer_badge.b_activities.add(*bear_writer_activities_lits)

    # Adding activities to the bug solver badge
    bug_solver_badge = Badge.objects.get(
        name='The Bug Solver')
    bug_solver_activity1 = BadgeActivity.objects.get(
        name='Solved a difficulty/newcomer type/bug issue')
    bug_solver_activity2 = BadgeActivity.objects.get(
        name='Solved a difficulty/low type/bug issue')
    bug_solver_activities_list = [
        bug_solver_activity1,
        bug_solver_activity2,
    ]
    bug_solver_badge.b_activities.add(*bug_solver_activities_list)

    # Adding activities to the helper badge
    the_helper_badge = Badge.objects.get(
        name='The Helper')
    the_helper_activity1 = BadgeActivity.objects.get(
        name='Solved a importance/medium issue')
    the_helper_activity2 = BadgeActivity.objects.get(
        name='Solved a importance/high issue')
    the_helper_activities_list = [
        the_helper_activity1,
        the_helper_activity2,
    ]
    the_helper_badge.b_activities.add(*the_helper_activities_list)

    # Adding activities to the quick helper badge
    the_quick_helper_badge = Badge.objects.get(
        name='The Quick Helper')
    the_quick_helper_activity1 = BadgeActivity.objects.get(
        name='Solved a importance/high issue')
    the_quick_helper_activity2 = BadgeActivity.objects.get(
        name='Solved a importance/critical issue')
    the_quick_helper_activities_list = [
        the_quick_helper_activity1,
        the_quick_helper_activity2,
    ]
    the_quick_helper_badge.b_activities.add(*the_quick_helper_activities_list)

    # Adding activities to the doc care badge
    the_doc_care_badge = Badge.objects.get(
        name='The Doc-Care')
    the_doc_care_activity1 = BadgeActivity.objects.get(
        name='Created a area/documentation issue')
    the_doc_care_activity2 = BadgeActivity.objects.get(
        name='Solved a area/documentation issue')
    the_doc_care_activities_list = [
        the_doc_care_activity1,
        the_doc_care_activity2,
    ]
    the_doc_care_badge.b_activities.add(*the_doc_care_activities_list)

    # Adding activities to the all-rounder badge
    all_rounder_badge = Badge.objects.get(
        name='The All-Rounder')
    all_rounder_activity1 = BadgeActivity.objects.get(
        name='Solved a difficulty/newcomer issue')
    all_rounder_activity2 = BadgeActivity.objects.get(
        name='Solved a difficulty/low issue')
    all_rounder_activities_list = [
        all_rounder_activity1,
        all_rounder_activity2,
    ]
    all_rounder_badge.b_activities.add(
        *all_rounder_activities_list)
