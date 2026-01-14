from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from room.models import Room


def rooms_url():
    return reverse("room:rooms-list")


def room_detail_url(room_id: int) -> str:
    return reverse("room:rooms-detail", args=[room_id])


def create_user(**params):
    defaults = {
        "email": "user@test.com",
        "username": "user1",
        "password": "test12345",
    }
    defaults.update(params)
    return get_user_model().objects.create_user(**defaults)


def create_admin(**params):
    defaults = {
        "email": "admin@test.com",
        "username": "admin1",
        "password": "test12345",
    }
    defaults.update(params)
    return get_user_model().objects.create_superuser(**defaults)


def create_room(**params):
    defaults = {
        "number": "101",
        "type": Room.RoomType.SINGLE,
        "price_per_night": "50.00",
        "capacity": 2,
    }
    defaults.update(params)
    return Room.objects.create(**defaults)


class PublicRoomApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_rooms_allowed_for_anon(self):
        create_room(number="101")
        create_room(number="102")

        res = self.client.get(rooms_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_create_room_forbidden_for_anon(self):
        payload = {
            "number": "777",
            "type": Room.RoomType.SINGLE,
            "price_per_night": "99.99",
            "capacity": 1,
        }

        res = self.client.post(rooms_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRoomApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="user@test.com", password="test12345")
        self.client.force_authenticate(self.user)

    def test_create_room_forbidden_for_non_admin(self):
        payload = {
            "number": "888",
            "type": Room.RoomType.SUITE,
            "price_per_night": "200.00",
            "capacity": 4,
        }

        res = self.client.post(rooms_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_room_forbidden_for_non_admin(self):
        room = create_room(number="150")

        payload = {"capacity": 10}

        res = self.client.patch(room_detail_url(room.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_room_forbidden_for_non_admin(self):
        room = create_room(number="151")

        res = self.client.delete(room_detail_url(room.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminRoomApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = create_admin(email="admin@test.com", password="test12345")
        self.client.force_authenticate(self.admin)

    def test_create_room_success(self):
        payload = {
            "number": "900",
            "type": Room.RoomType.DOUBLE,
            "price_per_night": "120.00",
            "capacity": 3,
        }

        res = self.client.post(rooms_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Room.objects.filter(number="900").exists())

    def test_patch_room_success(self):
        room = create_room(number="901", capacity=2)

        payload = {"capacity": 5}

        res = self.client.patch(room_detail_url(room.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        room.refresh_from_db()
        self.assertEqual(room.capacity, 5)

    def test_put_room_success(self):
        room = create_room(number="902")

        payload = {
            "number": "902",
            "type": Room.RoomType.SUITE,
            "price_per_night": "300.00",
            "capacity": 6,
        }

        res = self.client.put(room_detail_url(room.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        room.refresh_from_db()
        self.assertEqual(room.type, Room.RoomType.SUITE)
        self.assertEqual(str(room.price_per_night), "300.00")
        self.assertEqual(room.capacity, 6)

    def test_delete_room_success(self):
        room = create_room(number="903")

        res = self.client.delete(room_detail_url(room.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Room.objects.filter(id=room.id).exists())

    def test_filter_by_type(self):
        create_room(number="1001", type=Room.RoomType.SINGLE)
        create_room(number="1002", type=Room.RoomType.SUITE)

        res = self.client.get(rooms_url(), {"type": Room.RoomType.SUITE})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["number"], "1002")

    def test_filter_by_capacity(self):
        create_room(number="1101", capacity=2)
        create_room(number="1102", capacity=4)

        res = self.client.get(rooms_url(), {"capacity": 4})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["number"], "1102")
