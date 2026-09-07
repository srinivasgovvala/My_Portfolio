"""Seed initial data for the portfolio."""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings.development')
django.setup()

from core.models import PersonalProfile, HeroRole, SEOSettings, SiteSettings
from profile_app.models import Skill, Technology
from education.models import Education
from experience.models import Experience
from projects.models import Project, ProjectTechnology, FutureProject
from chatbot.models import ChatbotSettings


def seed():
    print("Seeding portfolio data...")

    # Site settings
    site = SiteSettings.get()
    site.site_name = 'Nagasrinivas Govvala'
    site.tagline = 'Building practical software with Python, Django, AI and modern web technologies.'
    site.save()

    # Personal profile
    p = PersonalProfile.get()
    p.full_name = 'Nagasrinivas Govvala'
    p.title = 'Fresher Software Developer'
    p.location = 'Hyderabad, Telangana, India'
    p.email = 'nagasrinivas@email.com'
    p.github_url = 'https://github.com/NagasrinivasGovvala'
    p.linkedin_url = 'https://linkedin.com/in/nagasrinivas-govvala'
    p.about_short = 'A fresher software developer from Hyderabad building real applications with Python, Django, and AI.'
    p.about_long = """I'm Nagasrinivas Govvala — a fresher software developer from Hyderabad, Telangana.

I graduated with a B.Tech in Computer Science and Engineering in 2025. My development journey has been defined not by years in industry, but by shipping real applications that solve actual problems.

I build with Python and Django as my primary stack, experiment with machine learning and NLP, and create production-oriented websites. I use modern AI-assisted development workflows — Claude, ChatGPT, OpenCode, and Antigravity — as collaborative tools in my development process.

My approach: build and learn by shipping real projects. Every project in this portfolio was built to work, not just to demonstrate skills."""
    p.available_for_work = True
    p.resume = 'resume/resume.pdf'
    p.save()

    # SEO
    seo = SEOSettings.get()
    seo.page_title = 'Nagasrinivas Govvala | Fresher Software Developer — Python, Django, AI/ML'
    seo.meta_description = 'Nagasrinivas Govvala — Fresher Software Developer from Hyderabad. Python, Django, Machine Learning, AI, Full-Stack web development. ResumeAI, Toxic Comment Classification, PID Controls.'
    seo.save()

    # Hero roles
    HeroRole.objects.all().delete()
    roles = [
        'Fresher Software Developer',
        'Python Developer',
        'Django Developer',
        'AI & Machine Learning Enthusiast',
        'Full-Stack Developer',
    ]
    for i, role in enumerate(roles):
        HeroRole.objects.create(role=role, order=i, is_active=True)
    print(f"  Created {len(roles)} hero roles")

    # Education
    Education.objects.all().delete()
    Education.objects.create(
        degree='B.Tech',
        field='Computer Science and Engineering',
        institution='Srinivasa Institute of Engineering and Technology',
        year=2025,
        grade='CGPA: 7.17',
        order=0,
    )
    Education.objects.create(
        degree='Diploma',
        field='Computer Engineering',
        institution='BVC Institute of Technology and Science',
        year=2022,
        grade='Percentage: 70%',
        order=1,
    )
    print("  Created 2 education entries")

    # Experience
    Experience.objects.all().delete()
    from datetime import date
    Experience.objects.create(
        title='AWS Cloud Foundations Training',
        organization='AWS / Training Program',
        exp_type='internship',
        start_date=date(2024, 1, 1),
        end_date=date(2024, 6, 30),
        description='Completed AWS Cloud Foundations and AWS Cloud Practitioner training. Gained knowledge of cloud computing fundamentals, AWS core services, security, architecture, and pricing models.',
        technologies='AWS, Cloud Computing',
        order=0,
    )
    Experience.objects.create(
        title='Data Annotation Specialist',
        organization='Data Annotation Platform',
        exp_type='part_time',
        start_date=date(2024, 7, 1),
        is_current=True,
        description='Part-time data annotation work — labeling and reviewing AI training data to improve machine learning model quality.',
        technologies='AI, Data Labeling, NLP',
        order=1,
    )
    print("  Created 2 experience entries")

    # Skills
    Skill.objects.all().delete()
    skills_data = [
        ('Python', 'programming', 'primary'),
        ('SQL', 'programming', 'working'),
        ('HTML', 'web', 'primary'),
        ('CSS', 'web', 'primary'),
        ('JavaScript', 'web', 'working'),
        ('Django', 'web', 'primary'),
        ('Scikit-learn', 'data_ml', 'working'),
        ('Pandas', 'data_ml', 'working'),
        ('NumPy', 'data_ml', 'working'),
        ('Matplotlib', 'data_ml', 'familiar'),
        ('NLP', 'data_ml', 'working'),
        ('Machine Learning', 'data_ml', 'working'),
        ('MySQL', 'database', 'working'),
        ('PostgreSQL', 'database', 'working'),
        ('AWS Cloud', 'cloud', 'familiar'),
        ('Visual Studio Code', 'tools', 'primary'),
        ('PyCharm', 'tools', 'working'),
        ('Git / GitHub', 'tools', 'working'),
        ('Microsoft Office', 'tools', 'familiar'),
        ('Claude', 'ai_tools', 'primary'),
        ('ChatGPT', 'ai_tools', 'primary'),
        ('OpenCode', 'ai_tools', 'working'),
        ('Antigravity', 'ai_tools', 'working'),
    ]
    for i, (name, cat, prof) in enumerate(skills_data):
        Skill.objects.create(name=name, category=cat, proficiency=prof, order=i)
    print(f"  Created {len(skills_data)} skills")

    # Technologies with descriptions
    Technology.objects.all().delete()
    techs_data = [
        ('Python', 'programming', 'Primary backend language for web development and ML projects', 'ResumeAI, Toxic Comment Classification', '#3776ab'),
        ('SQL', 'programming', 'Database querying and management', 'All Django projects', '#f29111'),
        ('Django', 'web', 'Backend web framework for ResumeAI and Toxic Comment Classification', 'ResumeAI, Toxic Comment Classification', '#092e20'),
        ('HTML', 'web', 'Markup for all web projects', 'All web projects', '#e34f26'),
        ('CSS', 'web', 'Styling for all web projects', 'All web projects', '#1572b6'),
        ('JavaScript', 'web', 'Frontend interactivity and animations', 'PID Controls, Portfolio', '#f7df1e'),
        ('Next.js', 'web', 'React framework used for PID Controls corporate website', 'PID Controls', '#000000'),
        ('Django REST Framework', 'web', 'API endpoint development', 'ResumeAI', '#a30000'),
        ('Scikit-learn', 'data_ml', 'Machine learning pipeline — TF-IDF + Logistic Regression', 'Toxic Comment Classification', '#f89939'),
        ('Pandas', 'data_ml', 'Data manipulation and analysis', 'Toxic Comment Classification', '#150458'),
        ('NumPy', 'data_ml', 'Numerical computing for ML preprocessing', 'Toxic Comment Classification', '#013243'),
        ('Matplotlib', 'data_ml', 'Data visualization for ML results', 'Toxic Comment Classification', '#11557c'),
        ('NLP', 'data_ml', 'Text preprocessing, TF-IDF vectorization for toxicity detection', 'Toxic Comment Classification', '#9333ea'),
        ('OpenRouter API', 'data_ml', 'LLM access for AI career assistant and chatbot features', 'ResumeAI', '#7c3aed'),
        ('PostgreSQL', 'database', 'Production database for Django applications', 'ResumeAI', '#336791'),
        ('MySQL', 'database', 'Relational database management', 'Various projects', '#00618a'),
        ('AWS Cloud', 'cloud', 'Cloud computing fundamentals and core AWS services (Practitioner level)', '', '#ff9900'),
        ('Git / GitHub', 'tools', 'Version control for all projects', 'All projects', '#f05032'),
        ('ReportLab', 'tools', 'PDF generation for resume export feature', 'ResumeAI', '#cc0000'),
        ('Google OAuth', 'tools', 'Authentication via Google for ResumeAI', 'ResumeAI', '#4285f4'),
    ]
    for i, (name, cat, desc, proj, color) in enumerate(techs_data):
        Technology.objects.create(name=name, category=cat, description=desc, related_project=proj, color=color, order=i)
    print(f"  Created {len(techs_data)} technologies")

    # Project technologies
    tech_map = {}
    tech_names = ['Python', 'Django', 'Django REST Framework', 'PostgreSQL', 'OpenRouter API', 'ReportLab',
                  'django-allauth', 'Google OAuth', 'Google Drive API', 'WhiteNoise', 'Vercel',
                  'Scikit-learn', 'TF-IDF', 'Logistic Regression', 'Pandas', 'NumPy', 'HTML', 'CSS',
                  'JavaScript', 'Next.js', 'React', 'Tailwind CSS', 'Machine Learning', 'NLP']
    for name in tech_names:
        obj, _ = ProjectTechnology.objects.get_or_create(name=name)
        tech_map[name] = obj

    # Projects
    Project.objects.all().delete()

    p1 = Project.objects.create(
        title='ResumeAI',
        slug='resumeai',
        category='AI / Career Technology / Django',
        short_description='An AI-powered Django web application for creating ATS-friendly resumes, analyzing resumes against job descriptions, and improving them with AI.',
        full_description="""ResumeAI is a production-grade Django web application that helps job seekers create, analyze, and improve their resumes using artificial intelligence.

Built with Django REST Framework and integrated with OpenRouter LLMs, the application provides real-time ATS scoring, keyword analysis, and AI-powered improvement suggestions tailored to specific job descriptions.""",
        problem='Job seekers struggle to optimize resumes for ATS (Applicant Tracking Systems). Generic resume templates fail to highlight the right keywords, resulting in qualified candidates being filtered before human review.',
        solution='ResumeAI combines a structured resume builder with AI analysis. Users can build resumes, check their ATS compatibility score, receive keyword and formatting feedback, and get AI-powered improvement suggestions — all in one Django application.',
        features="""Resume builder with live preview
PDF export via ReportLab
ATS score checker
Keyword analysis
Section-by-section analysis
Formatting analysis
Readability analysis
AI career assistant
Job-specific resume improvement
Google OAuth authentication
Google Drive integration
Django Admin dashboard
AI model and settings management
Usage limits per user""",
        architecture='Django monolith with REST API endpoints for analysis features. PostgreSQL for user data and resumes. OpenRouter API for LLM calls. ReportLab for PDF generation. django-allauth for Google OAuth. WhiteNoise for static file serving.',
        challenges='Implementing reliable PDF generation that matches the live preview. Handling Google Drive API OAuth flow within Django. Rate-limiting OpenRouter API calls to control costs. Designing a resume data model flexible enough for varied resume structures.',
        result='A functional, production-deployed Django application with full authentication, AI integration, and PDF export capabilities.',
        learning='Learned to integrate multiple third-party APIs within a single Django application. Gained experience with PDF generation, OAuth flows, and LLM prompt engineering for structured output.',
        github_url='https://github.com/NagasrinivasGovvala/ResumeAI',
        live_url='',
        is_featured=True,
        is_completed=True,
        order=0,
    )
    for name in ['Python', 'Django', 'Django REST Framework', 'PostgreSQL', 'OpenRouter API', 'ReportLab', 'Google OAuth']:
        if name in tech_map:
            p1.technologies.add(tech_map[name])

    p2 = Project.objects.create(
        title='Toxic Comment Classification',
        slug='toxic-comment-classification',
        category='Machine Learning / NLP',
        short_description='A Django web application that detects and classifies comments across six toxicity categories using a TF-IDF + Logistic Regression ML pipeline.',
        full_description="""Toxic Comment Classification is a machine learning web application built with Django that analyzes text comments and classifies them across six toxicity categories: Toxic, Severe Toxic, Obscene, Threat, Insult, and Identity Hate.

The ML pipeline uses TF-IDF vectorization combined with multi-output Logistic Regression classification, implemented with Scikit-learn and deployed within a Django application.""",
        problem='Online platforms struggle with automated moderation at scale. Manual review is slow and inconsistent. Existing solutions are often black boxes without interpretable category breakdowns.',
        solution='A Django application that wraps a trained TF-IDF + Logistic Regression pipeline. Users can submit comments and receive category-level toxicity scores with visualizations. The application includes a REST API for programmatic access.',
        features="""User authentication and dashboard
Comment toxicity prediction
Multi-label classification (6 categories)
API-based prediction endpoint
Analytics and usage statistics
Visualization of toxicity scores
Model training pipeline
Batch comment processing""",
        architecture='Django web application with a trained Scikit-learn pipeline (TF-IDF vectorizer + multi-output Logistic Regression). Model is serialized with joblib and loaded at application startup. REST API for programmatic prediction access.',
        challenges='Building a multi-output classifier that handles the correlation between toxicity categories. Creating meaningful visualizations for multi-label prediction results. Optimizing model loading time at Django startup.',
        result='A working ML web application with multi-label toxicity classification, visualization, and API access.',
        learning='Gained hands-on experience with NLP preprocessing, TF-IDF vectorization, multi-output classification, and deploying ML models within a Django application.',
        github_url='https://github.com/NagasrinivasGovvala/Toxic-Comment-Classification',
        live_url='',
        is_featured=True,
        is_completed=True,
        order=1,
    )
    for name in ['Python', 'Django', 'Scikit-learn', 'TF-IDF', 'Logistic Regression', 'Pandas', 'NumPy', 'HTML', 'CSS', 'JavaScript', 'Machine Learning', 'NLP']:
        if name in tech_map:
            p2.technologies.add(tech_map[name])

    p3 = Project.objects.create(
        title='PID Controls — Corporate Website',
        slug='pid-controls',
        category='Production Website / BMS / Automation',
        short_description='A professional corporate website developed for a Hyderabad-based Building Management System and automation company, built with Next.js and deployed on Vercel.',
        full_description="""PID Controls is a professional corporate website built for a real Hyderabad-based Building Management System (BMS) and automation company.

Built with Next.js App Router, React, and Tailwind CSS, this is a production-deployed website with real SEO implementation, structured data, and business contact integration.""",
        problem='The company needed a professional web presence that accurately communicated their BMS and automation services to potential clients, with proper SEO and contact functionality.',
        solution='A production-grade Next.js corporate website with full page structure, SEO metadata, Google Maps, WhatsApp integration, and structured data for local business discovery.',
        features="""Responsive multi-page website
Home, About, Services, Industries pages
Process and Why Choose Us sections
Interactive project-process dashboard
Scroll animations
WhatsApp and call buttons
Consultation contact form
Google Maps integration
SEO metadata and Open Graph
XML Sitemap
robots.txt
LocalBusiness structured data""",
        architecture='Next.js App Router with server-side rendering. Tailwind CSS for styling. Deployed on Vercel with CI/CD. Inter and Montserrat typography. SVG custom graphics.',
        challenges='Implementing LocalBusiness structured data correctly for local SEO. Ensuring scroll animations work cross-browser. Optimizing Core Web Vitals on the Vercel deployment.',
        result='A live, production-deployed corporate website for a real client, demonstrating the ability to build and deliver business-oriented web projects.',
        learning='Learned Next.js App Router architecture, production SEO implementation, and the workflow of delivering a complete website to a real client.',
        github_url='https://github.com/NagasrinivasGovvala/pid-controls',
        live_url='https://pid-controls.vercel.app',
        is_featured=True,
        is_completed=True,
        order=2,
    )
    for name in ['Next.js', 'React', 'Tailwind CSS', 'JavaScript', 'HTML', 'CSS']:
        if name in tech_map:
            p3.technologies.add(tech_map[name])

    print("  Created 3 projects")

    # Future projects
    FutureProject.objects.all().delete()
    FutureProject.objects.create(
        title='Apartment Operating System',
        slug='apartment-operating-system',
        concept='A unified digital platform for managing apartment communities — residents, maintenance, payments, and communications.',
        description='A comprehensive web application designed to streamline apartment community management. Residents can submit maintenance requests, make payments, receive announcements, and communicate with management through a single platform. Administrators get a real-time dashboard of community operations.',
        status='concept',
        technologies_planned='Python, Django, PostgreSQL, WebSockets, React, Payment Gateway',
        order=0,
        is_active=True,
    )
    FutureProject.objects.create(
        title='Voice AI for Farmers',
        slug='voice-ai-for-farmers',
        concept='A voice-driven AI assistant that answers agricultural questions in local languages, accessible via basic smartphones.',
        description='A voice-first AI application designed for Indian farmers with limited digital literacy. Farmers can ask questions about crops, weather, prices, and government schemes in Telugu or Hindi using voice input. The system processes speech, queries relevant agricultural data, and responds in natural language.',
        status='research',
        technologies_planned='Python, Django, Speech-to-Text API, OpenRouter LLM, Hindi/Telugu NLP',
        order=1,
        is_active=True,
    )
    FutureProject.objects.create(
        title='AI Skill-to-Job Engine',
        slug='ai-skill-to-job-engine',
        concept='An AI system that analyzes a developer\'s skill profile and recommends specific learning paths to reach target job roles.',
        description='A data-driven career navigation tool. Developers input their current skills, desired role, and timeline. The AI analyzes skill gaps, recommends a prioritized learning roadmap, and tracks progress. Integrates job market data to ensure recommendations reflect actual hiring requirements.',
        status='concept',
        technologies_planned='Python, Django, OpenRouter LLM, PostgreSQL, Data Visualization, Job APIs',
        order=2,
        is_active=True,
    )
    print("  Created 3 future projects")

    # Chatbot settings
    cfg = ChatbotSettings.get()
    cfg.model = 'google/gemini-2.0-flash-001'
    cfg.max_tokens = 1024
    cfg.temperature = 0.4
    cfg.is_enabled = True
    cfg.save()
    print("  Chatbot set to google/gemini-2.0-flash-001")

    print("Seeding complete.")


if __name__ == '__main__':
    seed()
