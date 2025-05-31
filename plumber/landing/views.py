from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Owner
from django.contrib import messages
from .forms import ServiceBookingForm
from .models import ServiceBooking
import stripe
from django.conf import settings
from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail

# Home page view
def home(request):
    return render(request, 'landing/home.html')

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"Message from {name}"
        full_message = f"From: {name} <{email}>\n\nMessage:\n{message}"

        send_mail(
            subject,
            full_message,
            email,  # From email
            [settings.SITE_OWNER_EMAIL],  # To email (you should define this in settings.py)
            fail_silently=False,
        )
        return redirect('home')

    return render(request, 'landing/contact.html')

# Login view for user authentication
'''
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Get the user from the form
            login(request, user)  # Log the user in
            return redirect('dashboard')  # Redirect to the dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'landing/login.html', {'form': form})
'''
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Optional: redirect to "next" if provided in GET or POST
            next_url = request.GET.get('next') or request.POST.get('next')
            return redirect(next_url or 'dashboard')  # Default to dashboard

        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'landing/login.html', {'form': form})


# Dashboard view for authenticated users
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'landing/dashboard.html')

# Service booking form view
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ServiceBookingForm
from django.conf import settings  # Make sure your email settings are configured

def book_service(request):
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # Customize the email content
            subject = 'New Service Booking Received'
            message = f'''
            A new service booking has been received.

            Name: {booking.name}
            Email: {booking.email}
            Service: {booking.service}
            Preferred Date: {booking.preferred_date}

            Please follow up with the customer.
            '''
            recipient_list = ['akpaejike72@gmail.com']  # Replace with your actual email

            # Send the email
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

            messages.success(request, 'Your booking has been received! We will contact you soon.')
            return redirect('home')
    else:
        form = ServiceBookingForm()
    return render(request, 'landing/book_service.html', {'form': form})

# Stripe payment view for service bookings
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def payment(request, booking_id):
    booking = ServiceBooking.objects.get(id=booking_id)
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=5000,  # Amount in cents (5000 cents = $50)
                currency="usd",
                description="Plumbing Service Payment",
                source=token,
            )
            booking.paid = True
            booking.save()
            return render(request, 'landing/payment_success.html')
        except stripe.error.StripeError:
            return render(request, 'landing/payment_error.html')
    
    return render(request, 'landing/payment.html', {'booking': booking})

# Twilio chat service creation view
'''
def chat(request):
    client = Client('your_twilio_sid', 'your_twilio_auth_token')
    channel = client.chat.services('your_service_sid') \
                .channels.create(friendly_name='Plumbing Chat')
    return render(request, 'landing/chat.html', {'channel_sid': channel.sid})
'''
from twilio.rest import Client
from django.conf import settings
from django.shortcuts import render

def chat(request):
    try:
        # Initialize Twilio client with your Twilio SID and Auth Token
        client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

        # Create a new chat channel
        channel = client.chat.services(settings.TWILIO_SERVICE_SID) \
                            .channels.create(friendly_name='Plumbing Chat')

        return render(request, 'landing/chat.html', {'channel_sid': channel.sid})
    except Exception as e:
        return render(request, 'landing/chat.html', {'error': str(e)})
