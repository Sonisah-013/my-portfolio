import logging
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm
 
logger = logging.getLogger(__name__)
 
 
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
            'github_url': 'https://github.com/Sonisah-013/Django.git'
        },
        {
            'title': 'RAG_QA_System_Base',
            'description': 'A Retrieval-Augmented Generation (RAG) pipeline for grounded Q&A over PDF and text documents, built with LangChain, ChromaDB, and Groq.',
            'tech_stack': 'Python, LangChain, Pinecone, OpenAI API',
            'github_url': 'https://github.com/Sonisah-013/RAG_QA_System_Base.git'
        },
        {
            'title': 'Tesla Stock Price Predictor',
            'description': 'Time-series forecasting model using LSTM networks to predict market trends based on historical data.',
            'tech_stack': 'TensorFlow, Pandas, Matplotlib, Scikit-learn',
            'github_url': 'https://github.com/Sonisah-013/TSLA_Stock_System.git'
        },
        {
            'title': 'Student-Lead-Analysis',
            'description': 'Analysis of student leads: demand by course and area, student groups, and interest prediction.',
            'tech_stack': 'Python, Pandas, Matplotlib, Scikit-learn',
            'github_url': 'https://github.com/Sonisah-013/Student-Lead-Analysis.git'
        },
        {
            'title': 'insurance-charges-analysis',
            'description': 'EDA and machine learning models predicting health insurance charges based on age, BMI, smoking status, and other factors',
            'tech_stack': 'Python, Pandas, Matplotlib, Scikit-learn',
            'github_url': 'https://github.com/Sonisah-013/insurance-charges-analysis.git'
        },
    ]
    return render(request, 'projects.html', {'projects': project_list})
 
 
def send_email_via_resend(subject, body, recipient_email):
    """
    Sends an email using Resend's HTTP API instead of SMTP.
    This works on Render's free tier because it uses HTTPS (port 443),
    which is NOT blocked, unlike SMTP ports 25/465/587.
    """
    url = "https://api.resend.com/emails"
 
    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }
 
    payload = {
        "from": "Portfolio Contact <onboarding@resend.dev>",  # Resend's free test sender
        "to": [recipient_email],
        "subject": subject,
        "text": body,
    }
 
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()  # raises an exception if Resend returns an error
    return response
 
 
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
 
            recipient_email = 'sonisah013@gmail.com'  # your Gmail, unchanged
 
            # 3. Send the Email via Resend (HTTP API, not SMTP)
            try:
                send_email_via_resend(subject, body, recipient_email)
 
                messages.success(request, "Success! Your message was sent to Soni's inbox.")
                print("✅ Email sent successfully via Resend.")
 
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