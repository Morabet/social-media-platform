#!/usr/bin/env python3
""" """

import unittest
from datetime import datetime, time
from models.base_model import BaseModel
import uuid


class TestBaseModel(unittest.TestCase):
    """ """

    def setUp(self):
        """Set up the test case environment"""
        pass

    def test_initialization_no_args(self):
        """Test BaseModel initialization without arguments"""
        model = BaseModel()
        self.assertIsNotNone(model.id)
        self.assertIsInstance(model.id, str)
        self.assertIsNotNone(model.created_at)
        self.assertIsInstance(model.created_at, datetime)
        self.assertTrue(len(model.id) > 0)

    def test_initialization_with_existing_id(self):
        """Test BaseModel initialization with existing 'id' in kwargs"""
        custom_id = str(uuid.uuid4())
        model = BaseModel(id=custom_id)
        self.assertEqual(model.id, custom_id)

    def test_initialization_created_at_as_str(self):
        """Test BaseModel initialization with existing 'id' in kwargs"""
        custom_created_at = datetime.now().isoformat()
        model = BaseModel(created_at=custom_created_at)
        self.assertEqual(model.created_at.isoformat(), custom_created_at)

    def test_to_dict(self):
        """Test conversion of BaseModel to dictionary"""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertEqual(model_dict["id"], model.id)
        self.assertEqual(model_dict["created_at"],
                         model.created_at.isoformat())
        self.assertNotIn("_sa_instance_state", model_dict)

    def test_to_dict_with_extra_attribute(self):
        """Test to_dict method with extra attribute added to BaseModel"""
        model = BaseModel()
        model.name = "Test Model"
        model_dict = model.to_dict()

        self.assertEqual(model_dict["name"], "Test Model")

    def tearDown(self):
        """Clean up the test case environment"""
        pass


if __name__ == '__main__':
    unittest.main()
