from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import SignUpForm, ContactForm, RegistrationForm

# Create your views here.

def home(request):
	#message = "What's Up {0}".format(str(request.user))
	message = 'Welcome '
	user = 'stranger'
	
	# if request.method == 'POST':
	# 	print request.POST

	form = SignUpForm(request.POST or None)

	if request.user.is_authenticated():
		message = "What's Up "
		user = request.user
	context = {
		'wish': message,
		'username': user,
		'form': form
	}
	# it's safer to do most of the validation inside SignUp class in forms.py instead
	if form.is_valid():
		instance = form.save(commit=False)
		full_name = form.cleaned_data.get('full_name')
		if not full_name:
			full_name = 'Anonymous'
		instance.full_name = full_name
		instance.save()
		context = {
			'wish': 'thank you for your time'
		}

	return render(request, "home.html", context)

def contact(request):
	form = ContactForm(request.POST or None)
	headline = "Contact Us"
	aligned_center = False
	if form.is_valid():
		for key, value in form.cleaned_data.iteritems():
			print key, value

		#mailing the contact form data	
		form_full_name = form.cleaned_data.get('full_name')
		form_email = form.cleaned_data.get('email')
		form_message = form.cleaned_data.get('message')
		form_subject = "Contact form details"

		#data to be sent as the mail
		sending_message = "{0} with {1} mail id says {2}".format(form_full_name, form_email, form_message)
		host_email = settings.EMAIL_HOST_USER
		sending_email = [settings.EMAIL_HOST_USER]

		send_mail(form_subject, sending_message, host_email,
    	sending_email, fail_silently=False)
    	
	context = {
		"form" : form,
		"headline": headline,
		"aligned_center": aligned_center
	}

	return render(request, 'contact.html', context)

def register(request):
	form = RegistrationForm(request.POST or None)
	# headline = "Contact Us"
	# aligned_center = False
	if form.is_valid():
		for key, value in form.cleaned_data.iteritems():
			print key, value
		form.save()	
		#mailing the contact form data	
		# form_full_name = form.cleaned_data.get('full_name')
		# form_email = form.cleaned_data.get('email')
		# form_message = form.cleaned_data.get('message')
		# form_subject = "Contact form details"

		#data to be sent as the mail
		# sending_message = "{0} with {1} mail id says {2}".format(form_full_name, form_email, form_message)
		# host_email = settings.EMAIL_HOST_USER
		# sending_email = [settings.EMAIL_HOST_USER]

		# send_mail(form_subject, sending_message, host_email,
  #   	sending_email, fail_silently=False)
    	
	context = {
		"cust_form" : form,
		"headline": "from views",
		# "aligned_center": aligned_center
	}

	return render(request, 'registration/registration_form.html', context)