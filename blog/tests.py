from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .views import Post


class BlogTest(TestCase) :
    # Datos de configuración de un usuario de prueba
    @classmethod
    def setUpTestData(cls) :
        cls.user = get_user_model().objects.create_user(
            username = 'Un usuario', email = 'correo@mail.com', password = 'secreta'
        )

        # Datos de prueba de un post
        cls.post = Post.objects.create(
            title = 'Un titulo',
            body = 'Este es el contenido',
            author = cls.user
        )

    def test_post_model(self) :
        self.assertEqual(self.post.title, 'Un titulo')
        self.assertEqual(self.post.body, 'Este es el contenido')
        self.assertEqual(self.post.author.username, 'Un usuario')
        self.assertEqual(str(self.post), 'Un titulo')
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')


    def test_url_exists_at_correct_listView(self) : 
        response = self.client.get('/') 
        self.assertEqual(response.status_code, 200)
    
    def test_url_exists_at_correct_detailView(self) : 
        response = self.client.get('/post/1/') 
        self.assertEqual(response.status_code, 200)

    def test_post_listView(self) :
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este es el contenido')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detailView(self) :
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/100000/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Este es el contenido')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_createview(self) :
        response = self.client.post(
            reverse('post_new'),
            {
                'title': 'New title',
                'body': 'New text',
                'author': self.user.id   
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'New title')
        self.assertEqual(Post.objects.last().body, 'New text')


    def test_post_updateview(self) :
        response = self.client.post(
            reverse('post_edit', args='1'),
            {
                'title': 'Update title',
                'body': 'Update text',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Update title')
        self.assertEqual(Post.objects.last().body, 'Update text')


    def test_post_deleteview(self) :
        response = self.client.post(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)





