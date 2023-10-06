#!/usr/bin/python3
"""This module defines the console for the application"""

import re
import unittest
from console import HBNBCommand
from io import StringIO
from unittest import TestCase
from unittest.mock import patch
from uuid import UUID
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
            }


class TestHBNBCommand(TestCase):
    """This is the Unittest class for the console application"""
    def setUp(self):
        """
        This methods sets up some variables before running the tests
        """
        # Keep track of newly created ids to be destroyed after
        # The key will be the id and value will be the class name
        self.created_ids = {}
        return super().setUp()

    def tearDown(self):
        """
        This method deletes all the newly created entries during testing
        """
        for key, value in self.created_ids.items():
            HBNBCommand().onecmd(f'destroy {value} {key}')
        return super().tearDown()

    def test_EOF(self):
        """
        Unittest for the HBNBCommand.do_EOF function
        Happens when the input terminates or user enters EOF
        """
        self.assertRaises(SystemExit, HBNBCommand().onecmd, 'EOF')

    def test_quit(self):
        """
        Unittest for the HBNBCommand.do_quit function
        Happens when the user types in the quit command
        """
        self.assertRaises(SystemExit, HBNBCommand().onecmd, 'quit')

    def test_help(self):
        """
        Unittest for the HBNBCommand.do_help function
        """
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd('help')
            self.assertTrue(
                "Documented commands (type help <topic>):" in out.getvalue())
        # Existing command
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd('help help')
            self.assertTrue(HBNBCommand.do_help.__doc__ in out.getvalue())
        # None existent command
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd('help command_not_present')
            self.assertEqual('*** No help on command_not_present',
                             out.getvalue().strip())

    def test_emptyline(self):
        """
        Unittest for the HBNBCommand.emptyline
        This is when a user enters a new line without any input
        """
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd('\n')
            self.assertTrue(len(out.getvalue()) == 0)

    def test_create(self):
        """
        Unittest for the HBNBCommand.do_create function
        """
        for model_name in classes:
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name}')
                id = out.getvalue().strip()
                # An excetion will be thrown here if this is not a valid uuid
                UUID(id)
                self.created_ids[id] = f'{model_name}'
            # Testingn create with arguments
            with patch('sys.stdout', new=StringIO()) as out:
                command = f'create {model_name} name="val" num=1 fnum=1.0'
                HBNBCommand().onecmd(command)
                id = out.getvalue().strip()
                # An excetion will be thrown here if this is not a valid uuid
                UUID(id)
                self.created_ids[id] = f'{model_name}'
            # For a class that does not exist
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd('create NonExistentModel')
                result = out.getvalue().strip()
                self.assertEqual("** class doesn't exist **", result)

    def test_destroy(self):
        """
        Unittest for the HBNBCommand.do_destroy function
        """
        id = ''
        for model_name in classes:
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name}')
                id = out.getvalue().strip()
                UUID(id)
            # For normal destroying
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'destroy {model_name} {id}')
                result = out.getvalue().strip()
                self.assertEqual(len(result), 0)
            # For a class that does not exist
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'destroy NonExistentModel {id}')
                result = out.getvalue().strip()
                self.assertEqual("** class doesn't exist **", result)
            # For an id that does not exist
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'destroy {model_name} {id}')
                result = out.getvalue().strip()
                self.assertEqual("** no instance found **", result)

    def test_show(self):
        """
        Unittest for the HBNBCommand.do_show function
        """
        id = ''
        for model_name in classes:
            # Create some new object and get the id
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name}')
                id = out.getvalue().strip()
                UUID(id)
                self.created_ids[id] = model_name
            # For normal expected output
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'show {model_name} {id}')
                result = out.getvalue().strip()
                pattern = f'^\\[{model_name}\\] \\({id}\\) \\{{.*\\}}$'
                self.assertTrue(re.search(pattern, result))
            # When class does not exist
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd('show NoneExistingModel id')
                result = out.getvalue().strip()
                self.assertEqual("** class doesn't exist **", result)
            # When id does not exist
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'show {model_name} id-does-not-exist')
                result = out.getvalue().strip()
                self.assertEqual("** no instance found **", result)
            # When class name is not supplied
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd('show')
                result = out.getvalue().strip()
                self.assertEqual("** class name missing **", result)
            # When id is not supplied
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'show {model_name}')
                result = out.getvalue().strip()
                self.assertEqual("** instance id missing **", result)

    def test_update(self):
        """
        Unittest for the HBNBCommand.do_update function
        """
        pass
        """
        id = ''
        for model_name in classes:
            # Create some new object and get the id
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name}')
                id = out.getvalue().strip()
                UUID(id)
                self.created_ids[id] = model_name
            at_name = 'email'
            at_value = 'fakemail@service.com'
            # For normal running of update
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(
                    f'update {model_name} {id} {at_name} {at_value}')
                result = out.getvalue().strip()
                self.assertEqual(len(result), 0)
            # Test that the attribute was added successfully
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'show {model_name} {id}')
                result = out.getvalue().strip()
                pattern = f'^\\[{model_name}\\] \\({id}\\) '\
                    f'\\{{.*\'{at_name}\': \'{at_value}\'.*\\}}$'
                self.assertTrue(re.search(pattern, result))
            # When class does not exist
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(
                    f'update NonExistentClass {id} {at_name} {at_value}')
                result = out.getvalue().strip()
                self.assertEqual("** class doesn't exist **", result)
            # When id does not exist
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(
                    f'update {model_name} id-absent {at_name} {at_value}')
                result = out.getvalue().strip()
                self.assertEqual("** no instance found **", result)
            # When id is not valid for the class
            with patch('sys.stdout', new=StringIO()) as out:
                not_model = model_name
                if not_model == 'BaseModel':
                    not_model = 'User'
                else:
                    not_model = 'BaseModel'
                HBNBCommand().onecmd(
                    f'update {not_model} {id} {at_name} {at_value}')
                result = out.getvalue().strip()
                self.assertEqual("** no instance found **", result)
            # When class name is not supplied
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd('update')
                result = out.getvalue().strip()
                self.assertEqual("** class name missing **", result)
            # When id is not supplied
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'update {model_name}')
                result = out.getvalue().strip()
                self.assertEqual("** instance id missing **", result)
            # When attribute name is not supplied
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'update {model_name} {id}')
                result = out.getvalue().strip()
                self.assertEqual("** attribute name missing **", result)
            # When attribute value is not supplied
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'update {model_name} {id} {at_name}')
                result = out.getvalue().strip()
                self.assertEqual("** value missing **", result)
        """

    def test_count(self):
        """
        Unittest for the syntax of commands in the form Class.count()
        Where Class is a supported class in the application
        """
        id = ''
        for model_name in classes:
            # Create some new object and get the id
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name}')
                id = out.getvalue().strip()
                UUID(id)
                self.created_ids[id] = model_name
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'count {model_name}')
                result = out.getvalue().strip()
                pattern = f'\\d+$'
                self.assertTrue(re.search(pattern, result))

    def test_all(self):
        """
        Unittest for the HBNBCommand.do_all function
        """
        id = ''
        for model_name in classes:
            # Create some new object and get the id
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name}')
                id = out.getvalue().strip()
                UUID(id)
                self.created_ids[id] = model_name
            id2 = ''
            model_name2 = 'User'
            # Create some different object and get the id
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name2}')
                id2 = out.getvalue().strip()
                UUID(id2)
                self.created_ids[id2] = model_name2
            # For normal expected output
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'all {model_name}')
                result = out.getvalue().strip()
                pattern = f'^\\[("\\[{model_name}\\] \\(.*\\) '\
                    f'\\{{.*\\}},?")*\\]$'
                self.assertTrue(re.search(pattern, result))
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'all {model_name2}')
                result = out.getvalue().strip()
                pattern = f'^\\[("\\[{model_name2}\\] \\(.*\\) '\
                    f'\\{{.*\\}},?")*\\]$'
                self.assertTrue(re.search(pattern, result))
            # When class does not exist
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd('all NoneExistingModel')
                result = out.getvalue().strip()
                self.assertEqual("** class doesn't exist **", result)
            # When class name is not supplied
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd('all')
                result = out.getvalue().strip()
                pattern = '^\\[("\\[.*\\] \\(.*\\) \\{.*\\},?")*\\]$'
                self.assertTrue(re.search(pattern, result))

    def test_class_all(self):
        """
        Unittest for the syntax of commands in the form Class.all()
        Where Class is a supported class in the application
        """
        id = ''
        for model_name in classes:
            # Create some new object and get the id
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name}')
                id = out.getvalue().strip()
                UUID(id)
                self.created_ids[id] = model_name
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'{model_name}.all()')
                result = out.getvalue().strip()
                p = f'^\\[(\"\\[{model_name}\\] \\(.*\\) \\{{.*\\}},?)*\"\\]$'
                self.assertTrue(re.search(p, result))

    def test_class_count(self):
        """
        Unittest for the syntax of commands in the form Class.count()
        Where Class is a supported class in the application
        """
        id = ''
        for model_name in classes:
            # Create some new object and get the id
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name}')
                id = out.getvalue().strip()
                UUID(id)
                self.created_ids[id] = model_name
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'{model_name}.count()')
                result = out.getvalue().strip()
                pattern = f'\\d+$'
                self.assertTrue(re.search(pattern, result))

    def test_class_show(self):
        """
        Unittest for the syntax of commands in the form Class.show("id")
        Where Class is a supported class in the application
        id must be a quoted string (double quotes)
        """
        id = ''
        for model_name in classes:
            # Create some new object and get the id
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name}')
                id = out.getvalue().strip()
                UUID(id)
                self.created_ids[id] = model_name
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'{model_name}.show("{id}")')
                result = out.getvalue().strip()
                pattern = f'^\\[{model_name}\\] \\({id}\\) \\{{.*\\}}$'
                self.assertTrue(re.search(pattern, result))
            # When id does not exist
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'{model_name}.show("id-does-not-exist")')
                result = out.getvalue().strip()
                self.assertEqual("** no instance found **", result)
            # When the argument is not double quoted
            with patch('sys.stdout', new=StringIO()) as out:
                command = f'{model_name}.show({id})'
                HBNBCommand().onecmd(command)
                result = out.getvalue().strip()
                pattern = f'^\\[{model_name}\\] \\({id}\\) \\{{.*\\}}$'
                self.assertTrue(re.search(pattern, result))

    def test_class_destroy(self):
        """
        Unittest for the syntax of commands in the form:
        Class.destroy("id")
        Where Class is a supported class in the application
        id and attribute_name must be a quoted string (double quotes)
        value must be quoted if it is a string
        """
        id = ''
        for model_name in classes:
            # Create some new object and get the id
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name}')
                id = out.getvalue().strip()
                UUID(id)
            # When id is not valid for the class
            with patch('sys.stdout', new=StringIO()) as out:
                invalid = 'BaseModel'
                if model_name == 'BaseModel':
                    invalid = 'User'
                HBNBCommand().onecmd(
                    f'{invalid}.destroy("{id}")')
                result = out.getvalue().strip()
                self.assertEqual("** no instance found **", result)
            # For normal running of destroy
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(
                    f'{model_name}.destroy("{id}")')
                result = out.getvalue().strip()
                self.assertEqual(len(result), 0)
            # When id does not exist
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(
                    f'{model_name}.destroy("id-not-in-storage")')
                result = out.getvalue().strip()
                self.assertEqual("** no instance found **", result)

    def test_class_update(self):
        """
        Unittest for the syntax of commands in the form:
        Class.update("id", "attribute_name", value)
        Where Class is a supported class in the application
        id and attribute_name must be a quoted string (double quotes)
        value must be quoted if it is a string
        """
        id = ''
        for model_name in classes:
            # Create some new object and get the id
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'create {model_name}')
                id = out.getvalue().strip()
                UUID(id)
                self.created_ids[id] = model_name
            # For normal running of update
            vals = '{\'first_name\': "John", "age": 89, "email":"fake@al.com"}'
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(
                    f'{model_name}.update("{id}", {vals})')
                result = out.getvalue().strip()
                self.assertEqual(len(result), 0)
            # Test that the attribute was added successfully
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(f'show {model_name} {id}')
                result = out.getvalue().strip()
                pattern = f'^\\[{model_name}\\] \\({id}\\) '\
                    f'\\{{.*\'age\': 89.*\\}}$'
                self.assertTrue(re.search(pattern, result))
            # When id does not exist
            with patch('sys.stdout', new=StringIO()) as out:
                HBNBCommand().onecmd(
                    f'{model_name}.update("id-not-in-storage", {vals})')
                result = out.getvalue().strip()
                self.assertEqual("** no instance found **", result)
            # When id is not valid for the class
            with patch('sys.stdout', new=StringIO()) as out:
                if model_name == 'BaseModel':
                    model_name = 'User'
                else:
                    model_name = 'BaseModel'
                HBNBCommand().onecmd(
                    f'{model_name}.update("{id}", {vals})')
                result = out.getvalue().strip()
                self.assertEqual("** no instance found **", result)

    def test_default(self):
        """
        Unittest for the case when the command is not supported
        """
        with patch('sys.stdout', new=StringIO()) as out:
            command = 'nonexistingcommand'
            HBNBCommand().onecmd(command)
            res = out.getvalue().strip()
            self.assertEqual(f"*** Unknown syntax: {command}", res)


if __name__ == '__main__':
    unittest.main()
