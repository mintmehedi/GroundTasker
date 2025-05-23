
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Profile 
from tasks.views import engaged_offers  
from django.shortcuts import render, redirect
from adminpanel.models import Ticket

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



@login_required
def support_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        category = request.POST.get('category')
        message = request.POST.get('issue')
        file = request.FILES.get('attachment')

        Ticket.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            category=category,
            message=message,
            attachment=file
        )
        return redirect('support')  # or 'ticket_submitted' if you have one

    return render(request, 'support.html')

