import datetime

from django.test import TestCase

# Create your tests here.
from note.models import Note
from user.models import User


class NoteTestCase(TestCase):
    def test_create_data(self):
        user=User.objects.create(username="lee123",password="123", created_time=datetime.time,updated_time=datetime.time)
        user=User.objects.get(id=1)
        print(user.username)
        Note.objects.create(title="python大全", content="这是关于python的书", created_time=datetime.time,updated_time=datetime.time,user=user)



