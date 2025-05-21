
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile 
from tasks.views import engaged_offers  # import from your task app

def messages_view(request):
    selected_task_id = request.GET.get('task_id')
    
    # Prepare sidebar data from engaged offers
    sidebar_conversations = []
    for offer in engaged_offers:
        task = offer['task']
        sidebar_conversations.append({
            'task_id': task['id'],
            'title': task['title'],
            'username': task['username'],  # Placeholder until linked with real user
            'active': str(task['id']) == str(selected_task_id)
        })

    return render(request, 'messages.html', {
        'conversations': sidebar_conversations,
        'selected_task_id': selected_task_id
    })

def notifications_view(request):
    notifications = [
        {
            'sender': 'Emily',
            'message': 'sent you a message on "Fix sink".',
            'timestamp': '2 minutes ago',
            'status': 'unread'
        },
        {
            'sender': 'Mark',
            'message': 'made an offer on "Car wash".',
            'timestamp': '10 minutes ago',
        },
        {
            'sender': 'System',
            'message': 'Your task "Grocery shopping" was marked as completed.',
            'timestamp': 'Yesterday',
        },
        # Add more as needed
    ]
    return render(request, 'notifications.html', {'notifications': notifications})


def support_view(request):
    return render(request, 'support.html')