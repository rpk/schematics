# coding=utf-8
from unittest import TestCase
from schematics.models import Model
from schematics.types import StringType
from schematics.types.compound import PolymorphicType


class Parent(Model):
    model_type = StringType(required=True)


class Person(Parent):
    name = StringType()


class Item(Parent):
    description = StringType()


class Container(Model):
    obj = PolymorphicType(type_attr_map={
        'I': Item,
        'P': Person
    }, attr_name='model_type')


class SchematicsSubclassTypeTests(TestCase):
    def test_serializes_into_heterogenous_types(self):
        c = Container(**{
            'obj': {
                'model_type': 'I',
                'description': 'test description'
            }
        })

        self.assertEqual(c.obj.description, 'test description')

        c2 = Container(**{
            'obj': {
                'model_type': 'P',
                'name': 'test name'
            }
        })

        self.assertEqual(c2.obj.name, 'test name')