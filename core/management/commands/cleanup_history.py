"""
Management command to clean up contact messages and chatbot history older than specified days.
Default: 30 days.

Usage:
    python manage.py cleanup_history
    python manage.py cleanup_history --days 15
"""
from django.core.management.base import BaseCommand
from contact.models import ContactMessage
from chatbot.models import ChatMessage


class Command(BaseCommand):
    help = 'Deletes contact messages and chatbot conversation history older than N days (default 30)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days of history to retain (default: 30)'
        )

    def handle(self, *args, **options):
        days = options['days']
        self.stdout.write(f'Running history cleanup (retaining past {days} days)...')

        contact_deleted = ContactMessage.prune_old_messages(days=days)
        chat_deleted = ChatMessage.prune_old_messages(days=days)

        self.stdout.write(
            self.style.SUCCESS(
                f'Cleanup complete: Deleted {contact_deleted} contact message(s) and {chat_deleted} chatbot log(s) older than {days} days.'
            )
        )
