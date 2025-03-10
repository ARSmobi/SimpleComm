from channels.testing import WebsocketCommunicator
from django.test import TestCase, Client
import pytest
import asyncio
from django.conf import settings
from django.urls import reverse, resolve
from twisted.words.protocols.jabber.jstrports import client

from ..SimpleComm.asgi import application


def test_installed_apps():
    assert 'channels' in settings.INSTALLED_APPS
    assert 'chat' in settings.INSTALLED_APPS

def test_asgi_application():
    assert settings.ASGI_APPLICATION == 'SimpleComm.asgi.application'

def test_channel_layer():
    assert 'channel.layers.InMemoryChannelLayer' == settings.CHANNEL_LAYER['default']['BACKEND']

def test_chat_url():
    path = reverse('room', kwargs={'room_name': 'testroom'})
    assert resolve(path).view_name == 'room'

@pytest.mark.asyncio
async def test_chat_consumer():
    communicator = WebsocketCommunicator(application, 'ws/chat/testroom/')
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.disconnect()

class ChatTestCase(TestCase):
    def test_room_view(self):
        client = Client()
        response = client.get('/chat/testroom/')
        assert response.status_code == 200
