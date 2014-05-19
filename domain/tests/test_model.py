# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.db import IntegrityError, transaction

from common import factory

class TestStaff(TestCase):

    def test_create_staff(self):

        staff1 = factory.create_staff('crosalot', 'crosalot@kmail.com', 'password', ' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th')
        self.assertEqual(staff1.first_name, ' Crosalot')
        self.assertEqual(staff1.last_name, 'Opendream ')
        self.assertEqual(staff1.username, 'crosalot')
        self.assertEqual(staff1.email, 'crosalot@kmail.com')
        self.assertEqual(staff1.occupation, 'Developer')
        self.assertEqual(staff1.description, 'Opensource')
        self.assertEqual(staff1.homepage_url, 'http://opendream.co.th')
        self.assertEqual(staff1.get_full_name(), 'Crosalot Opendream')
        self.assertEqual(staff1.get_short_name(), 'Crosalot.O')


        staff2 = factory.create_staff('panudate', 'panudate@kmail.com', 'password', ' Panudate', 'Vasinwattana', 'Tester', 'Unittest', 'http://opendream.in.th')
        self.assertEqual(staff2.first_name, ' Panudate')
        self.assertEqual(staff2.last_name, 'Vasinwattana')
        self.assertEqual(staff2.username, 'panudate')
        self.assertEqual(staff2.email, 'panudate@kmail.com')
        self.assertEqual(staff2.occupation, 'Tester')
        self.assertEqual(staff2.description, 'Unittest')
        self.assertEqual(staff2.homepage_url, 'http://opendream.in.th')
        self.assertEqual(staff2.get_full_name(), 'Panudate Vasinwattana')
        self.assertEqual(staff2.get_short_name(), 'Panudate.V')

        staff3 = factory.create_staff(first_name=' Panudate ')
        self.assertEqual(staff3.get_full_name(), 'Panudate')
        self.assertEqual(staff3.get_short_name(), 'Panudate')

        staff4 = factory.create_staff(last_name=' Vasinwattana ')
        self.assertEqual(staff4.get_full_name(), 'Vasinwattana')
        self.assertEqual(staff4.get_short_name(), 'Vasinwattana')



        try:
            with transaction.atomic():
                factory.create_staff('crosalot')

            self.assertTrue(0, 'Duplicate username allowed.')

        except IntegrityError:
            pass


        try:
            with transaction.atomic():
                factory.create_staff(email='crosalot@kmail.com')

            self.assertTrue(0, 'Duplicate username allowed.')

        except IntegrityError:
            pass


class TestPeople(TestCase):

    def test_create_people(self):

        people1 = factory.create_people('dream.p', 'Dream', 'Politic', 'Prime Minister', 'Black shirt', 'http://dream.politic.com')
        self.assertEqual(people1.first_name, 'Dream')
        self.assertEqual(people1.last_name, 'Politic')
        self.assertEqual(people1.permalink, 'dream.p')
        self.assertEqual(people1.occupation, 'Prime Minister')
        self.assertEqual(people1.description, 'Black shirt')
        self.assertEqual(people1.homepage_url, 'http://dream.politic.com')
        self.assertEqual(people1.get_full_name(), 'Dream Politic')
        self.assertEqual(people1.get_short_name(), 'Dream.P')


        people2 = factory.create_people('open.p', 'Open', 'Politic', 'Minister', 'White shirt', 'http://open.politic.com')
        self.assertEqual(people2.first_name, 'Open')
        self.assertEqual(people2.last_name, 'Politic')
        self.assertEqual(people2.permalink, 'open.p')
        self.assertEqual(people2.occupation, 'Minister')
        self.assertEqual(people2.description, 'White shirt')
        self.assertEqual(people2.homepage_url, 'http://open.politic.com')
        self.assertEqual(people2.get_full_name(), 'Open Politic')
        self.assertEqual(people2.get_short_name(), 'Open.P')



        try:
            with transaction.atomic():
                factory.create_people('dream.p')

            self.assertTrue(0, 'Duplicate permalink allowed.')

        except IntegrityError:
            pass


