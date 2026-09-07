from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def projects(request):
    # Dummy data: In the future, you can pull this from a Model
    project_list = [
        {
            'title': 'Django Project',
            'description': 'A web application built with Django framework to manage and showcase projects.',
            'tech_stack': 'Python, Django, HTML, CSS, JavaScript',
            'github_url':'https://github.com/Sonisah-013/Django.git'
        },
        {
            'title': 'RAG-based Q&A System',
            'description': 'A Retrieval-Augmented Generation system using LangChain and Vector Databases to provide context-aware answers.',
            'tech_stack': 'Python, LangChain, Pinecone, OpenAI API',
            'github_url': 'https://github.com/Sonisah-013/RAG_QA_System.git'
        },
        {
            'title': 'Tesla Stock Price Predictor',
            'description': 'Time-series forecasting model using LSTM networks to predict market trends based on historical data.',
            'tech_stack': 'TensorFlow, Pandas, Matplotlib, Scikit-learn',
            'github_url': 'https://github.com/Sonisah-013/TSLA_Stock_System.git'
        },
        {
            'title': 'Laptop Price Regressor',
            'description': 'A Machine Learning application that estimates the price of laptops based on hardware specifications.',
            'tech_stack': 'Flask, Scikit-learn, Seaborn, NumPy',
            'github_url': 'https://github.com/Sonisah-013/Laptop_Price_Predictor.git'
        },
    ]
    return render(request, 'projects.html', {'projects': project_list})

import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm  # Adjust this import to match your app

logger = logging.getLogger(__name__)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # 1. Save to Database
            contact_instance = form.save()

            # 2. Prepare the Email
            subject = f"New Portfolio Message from {contact_instance.name}"
            body = f"""
            You have a new message from your portfolio website:
            
            Name: {contact_instance.name}
            Email: {contact_instance.email}
            
            Message:
            {contact_instance.message}
            """
            
            sender_email = settings.DEFAULT_FROM_EMAIL  
            recipient_list = ['sonisah013@gmail.com'] 

            # 3. Send the Email
            try:
                # Attempt to send FIRST
                send_mail(subject, body, sender_email, recipient_list)
                
                # Only show success if the line above does NOT throw an error
                messages.success(request, "Success! Your message was sent to Soni's inbox.")
                print("✅ Email sent successfully.")
                
                
                return redirect('contact')
                
            except Exception as e:
                print("EMAIL ERROR:", repr(e))
                logger.exception("Email sending failed")

                messages.error(
                    request,
                    "Email failed, but your message was saved."
                )

                return redirect("contact")
    else:
        form = ContactForm() 
    
    return render(request, 'contact.html', {'form': form})