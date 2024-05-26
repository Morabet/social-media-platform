#!/usr/bin/env python3
""" """

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from models.user import User
import bcrypt


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)

    def setUp(self):
        self.session = TestUser.Session()
        self.user = User(
            name="John Doe",
            user_name="johndoe",
            email="john.doe@example.com",
            password="securepassword123"
        )

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_password_hashing_not_none(self):
        hashed = self.user.password_hashing("password")
        self.assertIsNotNone(hashed)

    def test_password_hashing_comparison(self):
        password = "examplePassword"
        hashed = self.user.password_hashing(password)
        self.assertTrue(bcrypt.checkpw(
            password.encode('utf-8'), hashed.encode('utf-8')))

    def test_verify_password_correct(self):
        self.assertTrue(self.user.verify_password("securepassword123"))

    def test_verify_password_incorrect(self):
        self.assertFalse(self.user.verify_password("wrongpassword"))

    def test_user_init_with_password_hashing(self):
        hashed_password = self.user.password
        self.assertTrue(bcrypt.checkpw("securepassword123".encode(
            'utf-8'), hashed_password.encode('utf-8')))

    def test_user_init_without_password(self):
        with self.assertRaises(KeyError):
            user = User(name="Jane Doe", email="jane.doe@example.com")

    def test_user_creation_in_database(self):
        self.session.add(self.user)
        self.session.commit()
        retrieved_user = self.session.query(User).one()
        self.assertEqual(retrieved_user.email, "john.doe@example.com")

    def test_user_creation_missing_email(self):
        with self.assertRaises(TypeError):
            user_missing_email = User(
                name="Tom Smith",
                user_name="tomsmith",
                password="password321"
            )


if __name__ == '__main__':
    unittest.main()
