import json
import logging

from django_future.csrf import ensure_csrf_cookie
from django.conf import settings
from django.core.validators import validate_email, validate_slug, ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from student.models import (Registration, UserProfile)
from cme_registration.models import CmeUserProfile
from student.views import try_change_enrollment

from mitxmako.shortcuts import render_to_response, render_to_string

from statsd import statsd

log = logging.getLogger("mitx.student")


@ensure_csrf_cookie
def register_user(request, extra_context={}):
    """
    This view will display the non-modal registration form
    """
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))

    SPECIALTY_CHOICES = {}
    SUB_SPECIALTY_CHOICES = {}

    PATIENT_POPULATION_CHOICES = (('Adult', 'Adult'),
                                  ('Pediatric', 'Pediatric'),
                                  ('Both', 'Both (Adult/Pediatric)'))
    SPECIALTY_CHOICES['Adult'] = (('Addiction_Medicine', 'Addiction Medicine'),
                                  ('Allergy', 'Allergy'),
                                  ('Anesthesiology', 'Anesthesiology'),
                                  ('Cardiology', 'Cardiology'),
                                  ('Complimentary_Medicine', 'Complimentary Medicine'),
                                  ('Critical_Care_Medicine_&_ICU', 'Critical Care Medicine & ICU'),
                                  ('Dentistry', 'Dentistry'),
                                  ('Dermatology', 'Dermatology'),
                                  ('Emergency_Medicine', 'Emergency Medicine'),
                                  ('Endocrinology', 'Endocrinology'),
                                  ('Family_Practice', 'Family Practice'),
                                  ('Gastroenterology_&_Hepatology', 'Gastroenterology & Hepatology'),
                                  ('General_Practice', 'General Practice'),
                                  ('Gerontology', 'Gerontology'),
                                  ('Head_&_Neck_Surgery', 'Head & Neck Surgery'),
                                  ('Health_Education', 'Health Education'),
                                  ('Hematology', 'Hematology'),
                                  ('Immunology_&_Rheumatology', 'Immunology & Rheumatology'),
                                  ('Infectious_Disease', 'Infectious Disease'),
                                  ('Internal_Medicine', 'Internal Medicine'),
                                  ('Nephrology', 'Nephrology'),
                                  ('Neurology', 'Neurology'),
                                  ('Neurosurgery', 'Neurosurgery'),
                                  ('Nutrition', 'Nutrition'),
                                  ('Obstetrics & Gynecology', 'Obstetrics & Gynecology'),
                                  ('Oncology', 'Oncology'),
                                  ('Ophthalmology', 'Ophthalmology'),
                                  ('Orthopaedic_Surgery', 'Orthopaedic Surgery'),
                                  ('Palliative_Care', 'Palliative Care'),
                                  ('Pathology', 'Pathology'),
                                  ('Pharmacology', 'Pharmacology'),
                                  ('Physical_Medicine_&_Rehabilitation', 'Physical Medicine & Rehabilitation'),
                                  ('Psychiatry', 'Psychiatry'),
                                  ('Psychology', 'Psychology'),
                                  ('Public_Health', 'Public Health'),
                                  ('Pulmonology', 'Pulmonology'),
                                  ('Radiology', 'Radiology'),
                                  ('Radiation_Oncology', 'Radiation Oncology'),
                                  ('Surgery', 'Surgery'),
                                  ('Transplant', 'Transplant'),
                                  ('Urology', 'Urology'))

    SPECIALTY_CHOICES['Pediatric'] = (('Addiction_Medicine', 'Addiction Medicine'),
                                      ('Adolescent_Medicine', 'Adolescent Medicine'),
                                      ('Allergy', 'Allergy'),
                                      ('Anesthesiology', 'Anesthesiology'),
                                      ('Cardiology', 'Cardiology'),
                                      ('Complimentary_Medicine', 'Complimentary Medicine'),
                                      ('Critical_Care_Medicine_&_ICU', 'Critical Care Medicine & ICU'),
                                      ('Dentistry', 'Dentistry'),
                                      ('Dermatology', 'Dermatology'),
                                      ('Emergency_Medicine', 'Emergency Medicine'),
                                      ('Endocrinology', 'Endocrinology'),
                                      ('Family_Practice', 'Family Practice'),
                                      ('Gastroenterology_&_Hepatology', 'Gastroenterology & Hepatology'),
                                      ('General_Practice', 'General Practice'),
                                      ('Head_&_Neck_Surgery', 'Head & Neck Surgery'),
                                      ('Health_Education', 'Health Education'),
                                      ('Hematology', 'Hematology'),
                                      ('Immunology_&_Rheumatology', 'Immunology & Rheumatology'),
                                      ('Infectious_Disease', 'Infectious Disease'),
                                      ('Internal_Medicine', 'Internal Medicine'),
                                      ('Neonatology', 'Neonatology'),
                                      ('Nephrology', 'Nephrology'),
                                      ('Neurology', 'Neurology'),
                                      ('Neurosurgery', 'Neurosurgery'),
                                      ('Nutrition', 'Nutrition'),
                                      ('Obstetrics_&_Gynecology', 'Obstetrics & Gynecology'),
                                      ('Oncology', 'Oncology'),
                                      ('Ophthalmology', 'Ophthalmology'),
                                      ('Orthopaedic_Surgery', 'Orthopaedic Surgery'),
                                      ('Pathology', 'Pathology'),
                                      ('Pediatrics', 'Pediatrics'),
                                      ('Pharmacology', 'Pharmacology'),
                                      ('Physical_Medicine_&_Rehabilitation', 'Physical Medicine & Rehabilitation'),
                                      ('Psychiatry', 'Psychiatry'),
                                      ('Psychology', 'Psychology'),
                                      ('Public_Health', 'Public Health'),
                                      ('Pulmonology', 'Pulmonology'),
                                      ('Radiology', 'Radiology'),
                                      ('Radiation_Oncology', 'Radiation Oncology'),
                                      ('Surgery', 'Surgery'),
                                      ('Transplant', 'Transplant'),
                                      ('Urology', 'Urology'),
                                      ('Other', 'Other, please enter:'))

    SPECIALTY_CHOICES['Both'] = (('Addiction_Medicine', 'Addiction Medicine'),
                                                   ('Adolescent_Medicine', 'Adolescent Medicine'),
                                                   ('Allergy', 'Allergy'),
                                                   ('Anesthesiology', 'Anesthesiology'),
                                                   ('Cardiology', 'Cardiology'),
                                                   ('Complimentary_Medicine', 'Complimentary Medicine'),
                                                   ('Critical_Care_Medicine_&_ICU', 'Critical Care Medicine & ICU'),
                                                   ('Dentistry', 'Dentistry'),
                                                   ('Dermatology', 'Dermatology'),
                                                   ('Emergency_Medicine', 'Emergency Medicine'),
                                                   ('Endocrinology', 'Endocrinology'),
                                                   ('Family_Practice', 'Family Practice'),
                                                   ('Gastroenterology_&_Hepatology', 'Gastroenterology & Hepatology'),
                                                   ('General_Practice', 'General Practice'),
                                                   ('Gerontology', 'Gerontology'),
                                                   ('Head_&_Neck_Surgery', 'Head & Neck Surgery'),
                                                   ('Health_Education', 'Health Education'),
                                                   ('Hematology', 'Hematology'),
                                                   ('Immunology_&_Rheumatology', 'Immunology & Rheumatology'),
                                                   ('Infectious_Disease', 'Infectious Disease'),
                                                   ('Internal_Medicine', 'Internal Medicine'),
                                                   ('Neonatology', 'Neonatology'),
                                                   ('Nephrology', 'Nephrology'),
                                                   ('Neurology', 'Neurology'),
                                                   ('Neurosurgery', 'Neurosurgery'),
                                                   ('Nutrition', 'Nutrition'),
                                                   ('Obstetrics_&_Gynecology', 'Obstetrics & Gynecology'),
                                                   ('Oncology', 'Oncology'),
                                                   ('Ophthalmology', 'Ophthalmology'),
                                                   ('Orthopaedic_Surgery', 'Orthopaedic Surgery'),
                                                   ('Palliative_Care', 'Palliative Care'),
                                                   ('Pathology', 'Pathology'),
                                                   ('Pediatrics', 'Pediatrics'),
                                                   ('Pharmacology', 'Pharmacology'),
                                                   ('Physical_Medicine_&_Rehabilitation', 'Physical Medicine & Rehabilitation'),
                                                   ('Psychiatry', 'Psychiatry'),
                                                   ('Psychology', 'Psychology'),
                                                   ('Public_Health', 'Public Health'),
                                                   ('Pulmonology', 'Pulmonology'),
                                                   ('Radiology', 'Radiology'),
                                                   ('Radiation_Oncology', 'Radiation Oncology'),
                                                   ('Surgery', 'Surgery'),
                                                   ('Transplant', 'Transplant'),
                                                   ('Urology', 'Urology'),
                                                   ('Other', 'Other, please enter:'))

    SUB_SPECIALTY_CHOICES['Cardiology'] = (('Cardiopulmonary', 'Cardiopulmonary'),
                                           ('Cardiothoracic', 'Cardiothoracic'),
                                           ('Cardiovascular_Disease', 'Cardiovascular Disease'),
                                           ('Cath_Angio_Lab', 'Cath Angio/Lab'),
                                           ('Electrophysiology', 'Electrophysiology'),
                                           ('Interventional_Cardiology', 'Interventional Cardiology'),
                                           ('Surgery', 'Surgery'),
                                           ('Vascular', 'Vascular'),
                                           ('Other', 'Other, please enter:'))

    SUB_SPECIALTY_CHOICES['Internal_Medicine'] = (('Cardiology', 'Cardiology'),
                                                  ('Dermatology', 'Dermatology'),
                                                  ('Endocrinology_Gerontology_&_Metabolism', 'Endocrinology, Gerontology & Metabolism'),
                                                  ('Gastroenterology_&_Hepatology', 'Gastroenterology & Hepatology'),
                                                  ('Hematology', 'Hematology'),
                                                  ('Immunology_&_Rheumatology', 'Immunology & Rheumatology'),
                                                  ('Infectious_Disease', 'Infectious Disease'),
                                                  ('Nephrology', 'Nephrology'),
                                                  ('Preventative_Medicine', 'Preventative Medicine'),
                                                  ('Pulmonary', 'Pulmonary'),
                                                  ('Other', 'Other, please enter:'))

    SUB_SPECIALTY_CHOICES['Obstetrics_Gynecology'] = (('Gynecology', 'Gynecology'),
                                                        ('Obstetrics', 'Obstetrics'),
                                                        ('Maternal_&_Fetal_Medicine', 'Maternal & Fetal Medicine'),
                                                        ('Women_Health', 'Women\'s Health'),
                                                        ('Other', 'Other, please enter:'))

    SUB_SPECIALTY_CHOICES['Oncology'] = (('Breast', 'Breast'),
                                         ('Gastroenterology', 'Gastroenterology'),
                                         ('Gynecology', 'Gynecology'),
                                         ('Hematology', 'Hematology'),
                                         ('Medical', 'Medical'),
                                         ('Radiation', 'Radiation'),
                                         ('Surgical', 'Surgical'),
                                         ('Urology', 'Urology'),
                                         ('Other', 'Other, please enter:'))

    SUB_SPECIALTY_CHOICES['Palliative_Care'] = (('Hospice', 'Hospice'),
                                                ('Other', 'Other, please enter:'))

    SUB_SPECIALTY_CHOICES['Pediatrics'] = (('Adolescent_Medicine', 'Adolescent Medicine'),
                                           ('Allergy', 'Allergy'),
                                           ('Anesthesiology', 'Anesthesiology'),
                                           ('Cardiac_Surgery', 'Cardiac Surgery'),
                                           ('Cardiology', 'Cardiology'),
                                           ('Critical_Care', 'Critical Care'),
                                           ('Dermatology', 'Dermatology'),
                                           ('Emergency', 'Emergency'),
                                           ('Endocrinology', 'Endocrinology'),
                                           ('Family Practice', 'Family Practice'),
                                           ('Gastroenterology', 'Gastroenterology'),
                                           ('Hematology_&_Oncology', 'Hematology & Oncology'),
                                           ('Immunology_&_Rheumatology', 'Immunology & Rheumatology'),
                                           ('Internal_Medicine', 'Internal Medicine'),
                                           ('Infectious_Disease', 'Infectious Disease'),
                                           ('Neonatology', 'Neonatology'),
                                           ('Nephrology', 'Nephrology'),
                                           ('Neurology', 'Neurology'),
                                           ('Obstetrics_&_Gynecology', 'Obstetrics & Gynecology'),
                                           ('Otolaryngology_Head_&_Neck', 'Otolaryngology/ Head & Neck'),
                                           ('Oncology', 'Oncology'),
                                           ('Ophthalmology', 'Ophthalmology'),
                                           ('Orthopaedic_Surgery', 'Orthopaedic Surgery'),
                                           ('Osteopathy', 'Osteopathy'),
                                           ('Pathology', 'Pathology'),
                                           ('Pediatric_Intensive_Care', 'Pediatric Intensive Care'),
                                           ('Psychiatry', 'Psychiatry'),
                                           ('Psychology', 'Psychology'),
                                           ('Pulmonary', 'Pulmonary'),
                                           ('Radiology', 'Radiology'),
                                           ('Surgery', 'Surgery'),
                                           ('Urology', 'Urology'),
                                           ('Other', 'Other, please enter:'))

    SUB_SPECIALTY_CHOICES['Pulmonology'] = (('Critical_Care', 'Critical Care'),
                                            ('Respiratory', 'Respiratory'),
                                            ('Other', 'Other, please enter:'))

    SUB_SPECIALTY_CHOICES['Surgery'] = (('Bariatric_Surgery', 'Bariatric Surgery'),
                                        ('Cardiac_Surgery', 'Cardiac Surgery'),
                                        ('Cardiothoracic_Surgery', 'Cardiothoracic Surgery'),
                                        ('Colon_&_Rectal_Surgery', 'Colon & Rectal Surgery'),
                                        ('Emergency_Medicine', 'Emergency Medicine'),
                                        ('Gastrointestinal_Surgery', 'Gastrointestinal Surgery'),
                                        ('Neurosurgery', 'Neurosurgery'),
                                        ('Oral_&_Maxillofacial_Surgery', 'Oral & Maxillofacial Surgery'),
                                        ('Orthopaedic_Surgery', 'Orthopaedic Surgery'),
                                        ('Plastic_&_Reconstructive_Surgery', 'Plastic & Reconstructive Surgery'),
                                        ('Surgical_Critical_Care', 'Surgical Critical Care'),
                                        ('Surgical_Oncology', 'Surgical Oncology'),
                                        ('Thoracic_Surgery', 'Thoracic Surgery'),
                                        ('Trauma_Surgery', 'Trauma Surgery'),
                                        ('Upper_Extremity_Hand_Surgery', 'Upper Extremity/ Hand Surgery'),
                                        ('Vascular_Surgery', 'Vascular Surgery'),
                                        ('Other', 'Other, please enter:'))

    SUB_SPECIALTY_CHOICES['Transplant'] = (('Solid_Organ', 'Solid Organ'),
                                           ('Blood_and_Bone_Marrow', 'Blood and Bone Marrow'),
                                           ('Other', 'Other, please enter:'))

    context = {
        'course_id': request.GET.get('course_id'),
        'enrollment_action': request.GET.get('enrollment_action'),
        'patient_population_choices': PATIENT_POPULATION_CHOICES,
        'specialty_choices': SPECIALTY_CHOICES,
        'sub_specialty_choices': SUB_SPECIALTY_CHOICES
    }
    context.update(extra_context)

    return render_to_response('cme_register.html', context)


@ensure_csrf_cookie
def cme_create_account(request, post_override=None):
    '''
    JSON call to create new edX account.
    Used by form in signup_modal.html, which is included into navigation.html
    '''
    js = {'success': False}

    post_vars = post_override if post_override else request.POST

    # if doing signup for an external authorization, then get email, password, name from the eamap
    # don't use the ones from the form, since the user could have hacked those
    # unless originally we didn't get a valid email or name from the external auth
    DoExternalAuth = 'ExternalAuthMap' in request.session
    if DoExternalAuth:
        eamap = request.session['ExternalAuthMap']
        try:
            validate_email(eamap.external_email)
            email = eamap.external_email
        except ValidationError:
            email = post_vars.get('email', '')
        if eamap.external_name.strip() == '':
            name = post_vars.get('name', '')
        else:
            name = eamap.external_name
        password = eamap.internal_password
        post_vars = dict(post_vars.items())
        post_vars.update(dict(email=email, name=name, password=password))
        log.info('In create_account with external_auth: post_vars = %s' % post_vars)

    # Confirm we have a properly formed request
    for a in ['username', 'email', 'password', 'name']:
        if a not in post_vars:
            js['value'] = "Error (401 {field}). E-mail us.".format(field=a)
            js['field'] = a
            return HttpResponse(json.dumps(js))

    # Can't have terms of service for certain SHIB users, like at Stanford
    tos_not_required = (settings.MITX_FEATURES.get("AUTH_USE_SHIB")
                        and settings.MITX_FEATURES.get('SHIB_DISABLE_TOS')
                        and DoExternalAuth
                        and ("shib" in eamap.external_domain))

    required_post_vars = ['username', 'email', 'name', 'password', 'profession', 'license_number', 'patient_population', 
                          'specialty', 'address_1', 'city', 'state_province', 'postal_code', 'country', 'phone_number', 'hear_about_us']
    
    #Validate required felds
    error = validate_required_fields(required_post_vars, post_vars)
    if error != None:
        return HttpResponse(json.dumps(error))

    #Validate required check boxes
    error = validate_required_boxes(post_vars, tos_not_required)
    if error != None:
        return HttpResponse(json.dumps(error))

    #Validate required radio buttons
    error = validate_required_radios(post_vars)
    if error != None:
        return HttpResponse(json.dumps(error))

    #Validate required secondary fields
    error = validate_required_secondaries(post_vars)
    if error != None:
        return HttpResponse(json.dumps(error))
    
    try:
        validate_email(post_vars['email'])
    except ValidationError:
        js['value'] = "Valid e-mail is required.".format(field=a)
        js['field'] = 'email'
        return HttpResponse(json.dumps(js))

    try:
        validate_slug(post_vars['username'])
    except ValidationError:
        js['value'] = "Username should only consist of A-Z and 0-9, with no spaces.".format(field=a)
        js['field'] = 'username'
        return HttpResponse(json.dumps(js))

    # Ok, looks like everything is legit.  Create the account.
    ret = _do_cme_create_account(post_vars)
    if isinstance(ret, HttpResponse):  # if there was an error then return that
        return ret
    (user, cme_user_profile, registration) = ret

    d = {'name': post_vars['name'],
         'key': registration.activation_key,
         }

    # composes activation email
    subject = render_to_string('emails/activation_email_subject.txt', d)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message = render_to_string('emails/activation_email.txt', d)

    try:
        if settings.MITX_FEATURES.get('REROUTE_ACTIVATION_EMAIL'):
            dest_addr = settings.MITX_FEATURES['REROUTE_ACTIVATION_EMAIL']
            message = ("Activation for %s (%s): %s\n" % (user, user.email, cme_user_profile.name) +
                       '-' * 80 + '\n\n' + message)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [dest_addr], fail_silently=False)
        elif not settings.GENERATE_RANDOM_USER_CREDENTIALS:
            res = user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
    except:
        log.warning('Unable to send activation email to user', exc_info=True)
        js['value'] = 'Could not send activation e-mail.'
        return HttpResponse(json.dumps(js))

    # Immediately after a user creates an account, we log them in. They are only
    # logged in until they close the browser. They can't log in again until they click
    # the activation link from the email.
    login_user = authenticate(username=post_vars['username'], password=post_vars['password'])
    login(request, login_user)
    request.session.set_expiry(0)

    if DoExternalAuth:
        eamap.user = login_user
        eamap.dtsignup = datetime.datetime.now(UTC)
        eamap.save()
        log.info("User registered with external_auth %s" % post_vars['username'])
        log.info('Updated ExternalAuthMap for %s to be %s' % (post_vars['username'], eamap))

        if settings.MITX_FEATURES.get('BYPASS_ACTIVATION_EMAIL_FOR_EXTAUTH'):
            log.info('bypassing activation email')
            login_user.is_active = True
            login_user.save()

    try_change_enrollment(request)

    statsd.increment("common.student.account_created")

    js = {'success': True}
    HttpResponse(json.dumps(js), mimetype="application/json")

    response = HttpResponse(json.dumps({'success': True}))

    # set the login cookie for the edx marketing site
    # we want this cookie to be accessed via javascript
    # so httponly is set to None

    if request.session.get_expire_at_browser_close():
        max_age = None
        expires = None
    else:
        max_age = request.session.get_expiry_age()
        expires_time = time.time() + max_age
        expires = cookie_date(expires_time)

    response.set_cookie(settings.EDXMKTG_COOKIE_NAME,
                        'true', max_age=max_age,
                        expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        path='/',
                        secure=None,
                        httponly=None)
    return response


def _do_cme_create_account(post_vars):
    """
    Given cleaned post variables, create the User and UserProfile objects, as well as the
    registration for this user.

    Returns a tuple (User, UserProfile, Registration).

    Note: this function is also used for creating test users.
    """
    user = User(username=post_vars['username'],
                email=post_vars['email'],
                is_active=False)
    user.set_password(post_vars['password'])
    registration = Registration()
    # TODO: Rearrange so that if part of the process fails, the whole process fails.
    # Right now, we can have e.g. no registration e-mail sent out and a zombie account
    try:
        user.save()
    except IntegrityError:
        js = {'success': False}
        # Figure out the cause of the integrity error
        if len(User.objects.filter(username=post_vars['username'])) > 0:
            js['value'] = "An account with the Public Username  '" + post_vars['username'] + "' already exists."
            js['field'] = 'username'
            return HttpResponse(json.dumps(js))

        if len(User.objects.filter(email=post_vars['email'])) > 0:
            js['value'] = "An account with the Email '" + post_vars['email'] + "' already exists."
            js['field'] = 'email'
            return HttpResponse(json.dumps(js))

        raise

    registration.register(user)

    cme_user_profile = CmeUserProfile(user=user)

    #UserProfile fields
    cme_user_profile.name = post_vars['name']

    #CmeUserProfile fields
    cme_user_profile.profession = post_vars.get('profession')
    cme_user_profile.professional_designation = post_vars.get('professional_designation')
    cme_user_profile.license_number = post_vars.get('license_number')
    cme_user_profile.organization = post_vars.get('organization')
    cme_user_profile.stanford_affiliated = True if post_vars.get('stanford_affiliated') == '1' else False

    if post_vars.get('how_stanford_affiliated') == 'Other':
        cme_user_profile.how_stanford_affiliated = post_vars.get('how_stanford_affiliated_free')
    else:
        cme_user_profile.how_stanford_affiliated = post_vars.get('how_stanford_affiliated')

    cme_user_profile.patient_population = post_vars.get('patient_population')

    if post_vars.get('specialty') == 'Other':
        cme_user_profile.specialty = post_vars.get('specialty_free')
    else:
        cme_user_profile.specialty = post_vars.get('specialty')

    if post_vars.get('sub_specialty') == 'Other':
        cme_user_profile.sub_specialty = post_vars.get('sub_specialty_free')
    else:
        cme_user_profile.sub_specialty = post_vars.get('sub_specialty')

    cme_user_profile.address_1 = post_vars.get('address_1')
    cme_user_profile.address_2 = post_vars.get('address_2')
    cme_user_profile.city = post_vars.get('city')
    cme_user_profile.state_province = post_vars.get('state_province')
    cme_user_profile.postal_code = post_vars.get('postal_code')
    cme_user_profile.country = post_vars.get('country')
    cme_user_profile.phone_number = post_vars.get('phone_number')
    cme_user_profile.extension = post_vars.get('extension')
    cme_user_profile.fax = post_vars.get('fax')

    if post_vars.get('hear_about_us') == 'Other':
        cme_user_profile.hear_about_us = post_vars.get('hear_about_us_free')
    else:
        cme_user_profile.hear_about_us = post_vars.get('hear_about_us')

    cme_user_profile.mailing_list = post_vars.get('mailing_list') if 'mailing_list' in post_vars else 0

    try:
        cme_user_profile.save()

    except Exception:
        log.exception("UserProfile creation failed for user {0}.".format(user.id))
    return (user, cme_user_profile, registration)

def validate_required_fields(required_post_vars, post_vars):
    
    error = {}
    for var in required_post_vars:
        if len(post_vars[var]) < 2:
            error_str = {'username': 'Username must be minimum of two characters long.',
                         'email': 'A properly formatted e-mail is required.',
                         'name': 'Your legal name must be a minimum of two characters long.',
                         'password': 'A valid password is required.',
 #                        'terms_of_service': 'Accepting Terms of Service is required.',
 #                        'honor_code': 'Agreeing to the Honor Code is required.',
                         'profession': 'Choose your profession.',
                         'license_number': 'Enter your license number.',
                         'patient_population': 'Choose your patient population',
                         'specialty': 'Choose your specialty',
                         'address_1': 'Enter your Address 01',
                         'city': 'Enter your city',
                         'state_province': "Choose your state/Province",
                         'postal_code': 'Enter your postal code',
                         'country': 'Choose your country',
                         'phone_number': 'Enter your phone number',
                         'hear_about_us': 'Choose how you heard about us'}
            error['success'] = False
            error['value'] = error_str[var]
            error['field'] = var
            return error
        
        
def validate_required_boxes(post_vars, tos_not_required):
    
    REQUIRED_BOXES_DICT = {'terms_of_service': ("You must accept the terms of service.", 'terms_of_service'),
                           'honor_code': ("To enroll, you must follow the honor code.", 'honor_code'),
                           }
    
    error = {}
    for k, v in REQUIRED_BOXES_DICT.items():
        if not (tos_not_required and k == 'terms_of_service'):
            if post_vars.get(k, 'false') != u'true':
                error['success'] = False
                error['value'] = v[0]
                error['field'] = v[1]
                return error
 
def validate_required_secondaries(post_vars):
    
    REQUIRED_SECONDARIES_DICT = {'stanford_affiliated': ('1', 'how_stanford_affiliated', 'Choose how you are affiliated with Stanford.'),
                                 'how_stanford_affiliated': ('Other', 'how_stanford_affiliated_free', 'Enter how you are affiliated with Stanford.'),
                                 'specialty': ('Other', 'specialty_free','Enter your specialty.'),
                                 'sub_specialty': ('Other', 'sub_specialty_free', 'Enter your sub-specialty.'),
                                 'hear_about_us': ('Other', 'hear_about_us_free', 'Enter how you heard about us.')
                                 }
    
    error = {}
    for k, v in REQUIRED_SECONDARIES_DICT.items():
        if post_vars.get(k) == v[0] and len(post_vars.get(v[1])) < 2:
            error['success'] = False
            error['value'] = v[2]
            error['field'] = k
            return error
        
def validate_required_radios(post_vars):
    
    REQUIRED_RADIOS_DICT = {'stanford_affiliated': 'Select whether, or not, you are affiliated with Stanford.'
                           }
    
    error = {}
    for k, v in REQUIRED_RADIOS_DICT.items():
        if k not in post_vars:
            error['success'] = False
            error['value'] = v
            error['field'] = k
            return error
