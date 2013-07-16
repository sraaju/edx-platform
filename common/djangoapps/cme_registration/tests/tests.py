"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from student.models import Registration, UserProfile
from cme_registration.models import CmeUserProfile


class TestCmeRegistration(TestCase):
    
#     def setUp(self):
# 
#         self.course = CourseFactory.create()


    def test_badly_formed_message(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {})
        self.assertContains(response, '{"field": "username", "value": "Error (401 username). E-mail us.", "success": false}')
    
         
    def test_profession_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
#                                          'stanford_affiliated': '1', 
#                                          'honor_code': 'true',
#                                          'terms_of_service': 'true', 
                                          'profession': ''})
        self.assertContains(response, '{"field": "profession", "value": "Choose your profession.", "success": false}')
        
        
    def test_license_number_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
      #                                    'stanford_affiliated': '1', 'honor_code': 'true',
      #                                    'terms_of_service': 'true', 
                                          'profession': 'AA', 
                                          'license_number': ''})
        self.assertContains(response, '{"field": "license_number", "value": "Enter your license number.", "success": false}')
        
        
    def test_patient_population_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
        #                                  'stanford_affiliated': '1', 'honor_code': 'true',
        #                                  'terms_of_service': 'true', 
                                          'profession': 'AA', 
                                          'license_number': '123', 
                                          'patient_population': ''})
        self.assertContains(response, '{"field": "patient_population", "value": "Choose your patient population", "success": false}')
        
            
    def test_specialty_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
         #                                 'stanford_affiliated': '1', 'honor_code': 'true',
         #                                 'terms_of_service': 'true', 
                                          'profession': 'AA', 
                                          'license_number': '123', 
                                          'patient_population': 'BB', 
                                          'specialty': ''})
        self.assertContains(response, '{"field": "specialty", "value": "Choose your specialty", "success": false}')
        
        
#     def test_sub_specialty_required(self):
#          
#         url = reverse('cme_create_account')
#         response = self.client.post(url, {'username': 'testuser', 'email': 'test@email.com', 'password': '1234', 'name': 'Chester Tester', 'stanford_affiliated': '1', 'honor_code': 'true',
#                                           'terms_of_service': 'true', 'profession': 'AA', 'license_number': '123', 'patient_population': 'BB', 'specialty': 'CC', 'sub_specialty': ''})
#         self.assertContains(response, '{"field": "sub_specialty", "value": "Choose your sub-specialty", "success": false}')
#         
        
    def test_sub_specialty_not_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
      #                                    'stanford_affiliated': '1', 'honor_code': 'true',
      #                                    'terms_of_service': 'true', 
                                          'profession': 'AA', 
                                          'license_number': '123', 
                                          'patient_population': 'BB', 
                                          'specialty': 'CC',
                                          'address_1': ''})
        self.assertContains(response, '{"field": "address_1", "value": "Enter your Address 01", "success": false}')
        
        
    def test_address_1_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
        #                                  'stanford_affiliated': '1', 'honor_code': 'true',
        #                                  'terms_of_service': 'true', 
                                          'profession': 'AA', 
                                          'license_number': '123', 
                                          'patient_population': 'BB', 
                                          'specialty': 'CC', 
                                          'sub_specialty': 'DD', 
                                          'address_1': ''})
        self.assertContains(response, '{"field": "address_1", "value": "Enter your Address 01", "success": false}')
        
        
    def test_city_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
         #                                 'stanford_affiliated': '1', 'honor_code': 'true',
         #                                 'terms_of_service': 'true', 
                                          'profession': 'AA', 
                                          'license_number': '123', 
                                          'patient_population': 'BB', 
                                          'specialty': 'CC', 
                                          'sub_specialty': 'DD',
                                          'address_1': 'EE',
                                          'city': ''})
        self.assertContains(response, '{"field": "city", "value": "Enter your city", "success": false}')
        
        
    def test_state_province_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
     #                                     'stanford_affiliated': '1', 'honor_code': 'true',
     #                                     'terms_of_service': 'true', 
                                          'profession': 'AA', 
                                          'license_number': '123', 
                                          'patient_population': 'BB', 
                                          'specialty': 'CC', 
                                          'sub_specialty': 'DD', 
                                          'address_1': 'EE', 
                                          'city': 'FF', 
                                          'state_province': ''})
        self.assertContains(response, '{"field": "state_province", "value": "Choose your state/Province", "success": false}')
        
        
    def test_postal_code_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
                                          'stanford_affiliated': '1', 'honor_code': 'true',
                                          'terms_of_service': 'true', 
                                          'profession': 'AA', 
                                          'license_number': '123', 
                                          'patient_population': 'BB', 
                                          'specialty': 'CC', 
                                          'sub_specialty': 'DD', 
                                          'address_1': 'EE', 
                                          'city': 'FF', 
                                          'state_province': 'GG', 
                                          'postal_code': ''})
        self.assertContains(response, '{"field": "postal_code", "value": "Enter your postal code", "success": false}')
        
        
    def test_country_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
               #                           'stanford_affiliated': '1', 'honor_code': 'true',
               #                           'terms_of_service': 'true', 
                                          'profession': 'AA', 
                                          'license_number': '123', 
                                          'patient_population': 'BB', 
                                          'specialty': 'CC', 
                                          'sub_specialty': 'DD', 
                                          'address_1': 'EE', 
                                          'city': 'FF', 
                                          'state_province': 'GG', 
                                          'postal_code': 'HH', 
                                          'country': ''})
        self.assertContains(response, '{"field": "country", "value": "Choose your country", "success": false}')
        
        
    def test_phone_number_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
               #                           'stanford_affiliated': '1', 'honor_code': 'true',
               #                           'terms_of_service': 'true', 
                                          'profession': 'AA', 
                                          'license_number': '123', 
                                          'patient_population': 'BB', 
                                          'specialty': 'CC', 
                                          'sub_specialty': 'DD', 
                                          'address_1': 'EE', 
                                          'city': 'FF', 
                                          'state_province': 'GG', 
                                          'postal_code': 'HH', 
                                          'country': 'II', 
                                          'phone_number': ''})
        self.assertContains(response, '{"field": "phone_number", "value": "Enter your phone number", "success": false}')
        
        
    def test_hear_about_us_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
                 #                         'stanford_affiliated': '1', 'honor_code': 'true',
                 #                         'terms_of_service': 'true', 
                                          'profession': 'AA', 
                                          'license_number': '123', 
                                          'patient_population': 'BB', 
                                          'specialty': 'CC', 
                                          'sub_specialty': 'DD', 
                                          'address_1': 'EE', 
                                          'city': 'FF', 
                                          'state_province': 'GG', 
                                          'postal_code': 'HH', 
                                          'country': 'II', 
                                          'phone_number': 'JJ', 
                                          'hear_about_us': ''})
        self.assertContains(response, '{"field": "hear_about_us", "value": "Choose how you heard about us", "success": false}')
        
        
        
        
    def test_specialty_other(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
                                          'stanford_affiliated': '0',
                                          'honor_code': 'true',
                                          'terms_of_service': 'true', 
                                          'profession': 'profession', 
                                          'license_number': 'license_number', 
                                          'patient_population': 'patient_population', 
                                          'specialty': 'Other',
                                          'specialty_free': '', 
                                          'address_1': 'address_1', 
                                          'city': 'city', 
                                          'state_province': 'state_province', 
                                          'postal_code': 'postal_code', 
                                          'country': 'country', 
                                          'phone_number': 'phone_number', 
                                          'hear_about_us': 'hear_about_us'})
        
        self.assertContains(response, '{"field": "specialty", "value": "Enter your specialty.", "success": false}')         
        
        
    def test_sub_specialty_other(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
                                          'stanford_affiliated': '0',
                                          'honor_code': 'true',
                                          'terms_of_service': 'true', 
                                          'profession': 'profession', 
                                          'license_number': 'license_number', 
                                          'patient_population': 'patient_population', 
                                          'specialty': 'specialty',
                                          'sub_specialty': 'Other',
                                          'sub_specialty_free': '',
                                          'address_1': 'address_1', 
                                          'city': 'city', 
                                          'state_province': 'state_province', 
                                          'postal_code': 'postal_code', 
                                          'country': 'country', 
                                          'phone_number': 'phone_number', 
                                          'hear_about_us': 'hear_about_us'})
        
        self.assertContains(response, '{"field": "sub_specialty", "value": "Enter your sub-specialty.", "success": false}')    
        
        
    def test_hear_about_us_other(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
                                          'stanford_affiliated': '0',
                                          'honor_code': 'true',
                                          'terms_of_service': 'true', 
                                          'profession': 'profession', 
                                          'license_number': 'license_number', 
                                          'patient_population': 'patient_population', 
                                          'specialty': 'specialty',
                                          'sub_specialty': 'sub_specialty',
                                          'address_1': 'address_1', 
                                          'city': 'city', 
                                          'state_province': 'state_province', 
                                          'postal_code': 'postal_code', 
                                          'country': 'country', 
                                          'phone_number': 'phone_number', 
                                          'hear_about_us': 'Other',
                                          'hear_about_us_free': ''})
        
        self.assertContains(response, '{"field": "hear_about_us", "value": "Enter how you heard about us.", "success": false}')  
        
        
    def test_stanford_affiliated_required(self):
        
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
 #                                         'stanford_affiliated': '0',
                                          'honor_code': 'true',
                                          'terms_of_service': 'true', 
                                          'profession': 'profession', 
                                          'license_number': 'license_number', 
                                          'patient_population': 'patient_population', 
                                          'specialty': 'specialty',
                                          'sub_specialty': 'sub_specialty',
                                          'address_1': 'address_1', 
                                          'city': 'city', 
                                          'state_province': 'state_province', 
                                          'postal_code': 'postal_code', 
                                          'country': 'country', 
                                          'phone_number': 'phone_number', 
                                          'hear_about_us': 'Other',
                                          'hear_about_us_free': 'hear_about'})
        self.assertContains(response, '{"field": "stanford_affiliated", "value": "Select whether, or not, you are affiliated with Stanford.", "success": false}')        

    def test_honour_code_required(self):
        
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
                                          'stanford_affiliated': '0',
 #                                         'honor_code': 'true',
                                          'terms_of_service': 'true', 
                                          'profession': 'profession', 
                                          'license_number': 'license_number', 
                                          'patient_population': 'patient_population', 
                                          'specialty': 'specialty',
                                          'sub_specialty': 'sub_specialty',
                                          'address_1': 'address_1', 
                                          'city': 'city', 
                                          'state_province': 'state_province', 
                                          'postal_code': 'postal_code', 
                                          'country': 'country', 
                                          'phone_number': 'phone_number', 
                                          'hear_about_us': 'Other',
                                          'hear_about_us_free': 'hear_about'})
        self.assertContains(response, '{"field": "honor_code", "value": "To enroll, you must follow the honor code.", "success": false}')        
        
        
    def test_tos_required(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
                                          'stanford_affiliated': '0',
                                          'honor_code': 'true',
 #                                         'terms_of_service': 'true', 
                                          'profession': 'profession', 
                                          'license_number': 'license_number', 
                                          'patient_population': 'patient_population', 
                                          'specialty': 'specialty',
                                          'sub_specialty': 'sub_specialty',
                                          'address_1': 'address_1', 
                                          'city': 'city', 
                                          'state_province': 'state_province', 
                                          'postal_code': 'postal_code', 
                                          'country': 'country', 
                                          'phone_number': 'phone_number', 
                                          'hear_about_us': 'Other',
                                          'hear_about_us_free': 'hear_about'})
        self.assertContains(response, '{"field": "terms_of_service", "value": "You must accept the terms of service.", "success": false}')
        

    def test_stanford_affiliated_choose(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
                                          'stanford_affiliated': '1',
                                          'how_stanford_affiliated': '',
                                          'honor_code': 'true',
                                          'terms_of_service': 'true', 
                                          'profession': 'profession', 
                                          'license_number': 'license_number', 
                                          'patient_population': 'patient_population', 
                                          'specialty': 'specialty', 
                                          'sub_specialty': 'sub_specialty', 
                                          'address_1': 'address_1', 
                                          'city': 'city', 
                                          'state_province': 'state_province', 
                                          'postal_code': 'postal_code', 
                                          'country': 'country', 
                                          'phone_number': 'phone_number', 
                                          'hear_about_us': 'hear_about_us'})
        
        self.assertContains(response, '{"field": "stanford_affiliated", "value": "Choose how you are affiliated with Stanford.", "success": false}')              
        
        
    def test_stanford_affiliated_other(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
                                          'stanford_affiliated': '1',
                                          'how_stanford_affiliated': 'Other',
                                          'how_stanford_affiliated_free': '',
                                          'honor_code': 'true',
                                          'terms_of_service': 'true', 
                                          'profession': 'profession', 
                                          'license_number': 'license_number', 
                                          'patient_population': 'patient_population', 
                                          'specialty': 'specialty', 
                                          'sub_specialty': 'sub_specialty', 
                                          'address_1': 'address_1', 
                                          'city': 'city', 
                                          'state_province': 'state_province', 
                                          'postal_code': 'postal_code', 
                                          'country': 'country', 
                                          'phone_number': 'phone_number', 
                                          'hear_about_us': 'hear_about_us'})
        
        self.assertContains(response, '{"field": "how_stanford_affiliated", "value": "Enter how you are affiliated with Stanford.", "success": false}') 
        
        
    def test_db_records_created(self):
         
        url = reverse('cme_create_account')
        response = self.client.post(url, {'username': 'testuser', 
                                          'email': 'test@email.com', 
                                          'password': '1234', 
                                          'name': 'Chester Tester', 
                                          'stanford_affiliated': '1',
                                          'how_stanford_affiliated': 'j\'st affiliat\'d',
                                          'honor_code': 'true',
                                          'terms_of_service': 'true', 
                                          'profession': 'profession', 
                                          'license_number': 'license_number', 
                                          'patient_population': 'patient_population', 
                                          'specialty': 'specialty', 
                                          'sub_specialty': 'sub_specialty', 
                                          'address_1': 'address_1', 
                                          'city': 'city', 
                                          'state_province': 'state_province', 
                                          'postal_code': 'postal_code', 
                                          'country': 'country', 
                                          'phone_number': 'phone_number', 
                                          'hear_about_us': 'hear_about_us'})
        
        #Check page displays success
        self.assertContains(response, '{"success": true}')
        
        #Check user was created
        user = User.objects.filter(email='test@email.com')
        self.assertEqual(1, len(user))
        
        #Check registration was created
        registration = Registration.objects.filter(user=user[0])
        self.assertEqual(1, len(registration))
        
        #Check cme_user_profile was created
        cme_user_profile = CmeUserProfile.objects.filter(user=user[0],
                                                         name='Chester Tester')
        self.assertEqual(1, len(cme_user_profile))
        
        #Check user_profile was created
        user_profile = UserProfile.objects.filter(user=user[0])
        self.assertEqual(1, len(user_profile))
