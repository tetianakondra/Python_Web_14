from datetime import date

import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (get_contacts,
    get_contact_by_id,
    get_contact_by_email,
    get_contacts_by_first_name,
    get_contacts_by_last_name,
    get_contacts_with_birthday,
    create,
    remove,
    update,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=2, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact_by_id(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_by_id_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact_by_id(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_by_email_found(self):
        contact = Contact()
        self.session.query().filter().all.return_value = contact
        result = await get_contact_by_email(contact_email="test@test.ua", user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_by_email_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await get_contact_by_email(contact_email="test@test.ua", user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_by_first_name_found(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_first_name(contact_first_name="FirstName", user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_first_name_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await get_contacts_by_first_name(contact_first_name="FirstName", user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_by_last_name_found(self):
        contacts = [Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_last_name(contact_last_name="LastName", user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_last_name_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await get_contacts_by_last_name(contact_last_name="LastName", user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_with_birthdays(self):
        contacts = [Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_with_birthday(days=7, user=self.user, db=self.session)
        if len(result) == 0:
            self.assertEqual(result, [])
        else:
            self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactModel(id=3, first_name="FirstName", last_name="LastName",
                            email="email@email.com", phone="0123456789", birthday=date(year=2012, month=12, day=12))
        result = await create(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.email, body.email)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_contact_found(self):
        contact = ContactModel(id=3, first_name="FirstName", last_name="LastName",
                            email="email@email.com", phone="0123456789", birthday=date(year=2012, month=12, day=12), user_id=1)
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update(contact_id=1, body=contact, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        contact = ContactModel(id=3, first_name="FirstName", last_name="LastName",
                            email="email@email.com", phone="0123456789", birthday=date(year=2012, month=12, day=12), user_id=1)
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update(contact_id=1, body=contact, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove(contact_id=3, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove(contact_id=3, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
