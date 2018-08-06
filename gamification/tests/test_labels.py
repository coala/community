from django.test import TestCase

from data.models import Label
from gamification.labels import get_sorted_labels


class GetSortedLabelsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Label.objects.create(name='difficulty/newcomer')
        Label.objects.create(name='type/bug')
        Label.objects.create(name='status/invalid')
        Label.objects.create(name='status/duplicate')

    def test_get_sorted_labels(self):
        labels_list1 = Label.objects.values('name')
        sorted_labels_list = get_sorted_labels(labels_list1)
        expected_labels_list = ['status/invalid']
        self.assertEquals(sorted_labels_list, expected_labels_list)

        Label.objects.filter(name='status/invalid').delete()
        labels_list2 = Label.objects.values('name')
        sorted_labels_list = get_sorted_labels(labels_list2)
        expected_labels_list = ['status/duplicate']
        self.assertEquals(sorted_labels_list, expected_labels_list)

        Label.objects.filter(name='status/duplicate').delete()
        labels_list3 = Label.objects.values('name')
        sorted_labels_list = get_sorted_labels(labels_list3)
        expected_labels_list = ['difficulty/newcomer', 'type/bug']
        self.assertEquals(sorted_labels_list, expected_labels_list)
