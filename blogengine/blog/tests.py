import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Post
# Create your tests here.


def create_post(post_title, days):
    """
    Создать пост с заголовком post_title с указанным в днях (days)
    сдвигом даты публикации относительно текущего времени. Сдвиг может
    быть как положительным, так и отрицательным.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(title=post_title, pub_date=time)


class PostsListViewTests(TestCase):
    def test_no_posts(self):
        """
        При отсутствии постов показывать соответствующее сообщение.
        """
        response = self.client.get(reverse('posts_list_url'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Публикации отсутствуют.")
        self.assertQuerysetEqual(
            response.context['page_object'].object_list, []
        )

    def test_past_post(self):
        """
        Посты с датой публикации старше относительно текущего времени
        отображаются в списке на странице.
        """
        create_post(post_title="Опубликованный пост.", days=-30)
        response = self.client.get(reverse('posts_list_url'))
        self.assertQuerysetEqual(
            response.context['page_object'].object_list,
            ['<Post: Опубликованный пост.>']
        )

    def test_future_post(self):
        """
        Посты, запланированные к публикации позже относительно текущего
        времени не отображаются в списке на странице.
        """
        create_post(post_title="Опубликованный пост.", days=30)
        response = self.client.get(reverse('posts_list_url'))
        self.assertContains(response, "Публикации отсутствуют.")
        self.assertQuerysetEqual(
            response.context['page_object'].object_list, []
        )

    def test_future_post_and_past_post(self):
        """
        При наличии заготовленного для публикации поста
        и уже опубликованного отображается только последний.
        """
        create_post(post_title="Опубликованный пост 1.", days=-30)
        create_post(post_title="Опубликованный пост 2.", days=30)
        response = self.client.get(reverse('posts_list_url'))
        self.assertQuerysetEqual(
            response.context['page_object'].object_list,
            ['<Post: Опубликованный пост 1.>']
        )

    def test_two_past_posts(self):
        """
        В списке постов может быть несколько опубликованных записей.
        """
        create_post(post_title="Опубликованный пост 1.", days=-30)
        create_post(post_title="Опубликованный пост 2.", days=-5)
        response = self.client.get(reverse('posts_list_url'))
        self.assertQuerysetEqual(
            response.context['page_object'].object_list,
            ['<Post: Опубликованный пост 2.>', '<Post: Опубликованный пост 1.>']
        )


class PostDetailViewTests(TestCase):
    def test_future_post(self):
        """
        Попытка отобразить отдельную страницу для ещё не вышедшего поста
        возвращает ошибку 404.
        """
        future_post = create_post(
            post_title='Пост из будущего.', days=5)
        url = reverse('post_detail_url', args=(future_post.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_post(self):
        """
        Для уже опубликованных постов доступны детализированные представления.
        """
        past_post = create_post(
            post_title='Опубликованный пост.', days=-5)
        url = reverse('post_detail_url', args=(past_post.slug,))
        response = self.client.get(url)
        self.assertContains(response, past_post.title)


class PostModelTests(TestCase):

    def test_was_published_recently_with_old_post(self):
        """
        was_published_recently() возвращает False для постов, чья
        дата публикации (поле pub_date) больше одного дня.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_post = Post(pub_date=time)
        self.assertIs(old_post.was_published_recently(), False)

    def test_was_published_recently_with_recent_post(self):
        """
        was_published_recently() возвращает True для постов, чья
        дата публикации (поле pub_date) варьируется в пределах текущего дня.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_post = Post(pub_date=time)
        self.assertIs(recent_post.was_published_recently(), True)

    def test_was_published_recently_with_future_post(self):
        """
        was_published_recently() возвращает False для постов, чья
        дата публикации (поле pub_date) запланирована в будущем.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(pub_date=time)
        self.assertIs(future_post.was_published_recently(), False)
