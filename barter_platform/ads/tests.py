from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal


class AdTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', password='12345')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test Description',
            category='toys',
            condition='new'
        )

    def test_create_ad(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('create_ad'), {
            'title': 'New Ad',
            'description': 'Some text',
            'category': 'electronics',
            'condition': 'used',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title='New Ad').exists())

    def test_edit_ad_by_owner(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('edit_ad', args=[self.ad.id]), {
            'title': 'Updated Title',
            'description': 'Updated description',
            'category': 'books',
            'condition': 'used',
        })
        self.ad.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.ad.title, 'Updated Title')

    def test_edit_ad_by_not_owner(self):
        self.client.login(username='otheruser', password='12345')
        response = self.client.post(reverse('edit_ad', args=[self.ad.id]), {
            'title': 'Hacked Title',
        })
        self.ad.refresh_from_db()
        self.assertNotEqual(self.ad.title, 'Hacked Title')
        self.assertRedirects(response, reverse('ads_list'))

    def test_delete_ad_by_owner(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_ad', args=[self.ad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())

    def test_search_ads(self):
        response = self.client.get(reverse('ads_list'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ad')

    def test_filter_ads_by_category_and_condition(self):
        response = self.client.get(reverse('ads_list'), {'category': 'toys', 'condition': 'new'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ad')


class ExchangeProposalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='12345')
        self.user2 = User.objects.create_user(username='user2', password='12345')

        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Ad 1',
            description='Desc 1',
            category='books',
            condition='used'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Ad 2',
            description='Desc 2',
            category='sports',
            condition='new'
        )

    def test_create_proposal(self):
        self.client.login(username='user2', password='12345')
        response = self.client.post(reverse('create_proposal'), {
            'ad_sender': self.ad2.id,
            'ad_receiver': self.ad1.id,
            'comment': 'Would you trade?',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ExchangeProposal.objects.filter(ad_sender=self.ad2, ad_receiver=self.ad1).exists())

    def test_accept_proposal_by_receiver(self):
        proposal = ExchangeProposal.objects.create(
            user=self.user2,
            ad_sender=self.ad2,
            ad_receiver=self.ad1,
            comment='Interested?',
            status='W'
        )
        self.client.login(username='user1', password='12345')
        response = self.client.post(reverse('update_proposal_status', args=[proposal.id, 'Y']))
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'Y')

    def test_reject_proposal_by_receiver(self):
        proposal = ExchangeProposal.objects.create(
            user=self.user2,
            ad_sender=self.ad2,
            ad_receiver=self.ad1,
            comment='Trade please',
            status='W'
        )
        self.client.login(username='user1', password='12345')
        response = self.client.post(reverse('update_proposal_status', args=[proposal.id, 'N']))
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'N')

    def test_cannot_accept_someone_elses_proposal(self):
        proposal = ExchangeProposal.objects.create(
            user=self.user2,
            ad_sender=self.ad2,
            ad_receiver=self.ad1,
            comment='Unauthorized test',
            status='W'
        )
        self.client.login(username='user2', password='12345')
        response = self.client.post(reverse('update_proposal_status', args=[proposal.id, 'Y']))
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'W')  # не изменился

    def test_filter_proposals(self):
        proposal = ExchangeProposal.objects.create(
            user=self.user2,
            ad_sender=self.ad2,
            ad_receiver=self.ad1,
            comment='Test filter',
            status='W'
        )
        response = self.client.get(reverse('proposals_list'), {'status': 'W'})
        self.assertContains(response, 'Test filter')
