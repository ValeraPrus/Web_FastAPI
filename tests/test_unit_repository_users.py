import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session


from src.database.models import User
from src.schemas import UserModel
from src.repository.users import create_user, update_token, confirmed_email


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_create_user(self):
        body = UserModel(username="Vovan", email="mynew@gmail.com", password="12345678")
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)

    @patch('src.repository.users.User')
    async def test_update_token(self, Mock_User):
        mock_user = Mock_User.return_value
        token = 'new token'
        await update_token(mock_user, token, self.session)
        self.assertEqual(token, mock_user.refresh_token)
        self.session.commit.assert_called_once()

    @patch('src.repository.users.get_user_by_email')
    async def test_confirmed_email(self, MockGetUserByEmail):
        mock_get = MockGetUserByEmail.return_value = User()
        await confirmed_email('mynew@ukr.net', self.session)
        self.assertEqual(mock_get.confirmed, True)
        self.session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
