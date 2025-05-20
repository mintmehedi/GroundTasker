from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.http import Http404
from .models import Task, Offer

# TEMPORARY SAMPLE DATA
sample_tasks = [
    {
        'id': 1,
        'title': 'Weed backyard',
        'username': 'Mark',
        'description': 'Remove weeds and tidy the backyard.',
        'location': 'Parramatta, NSW',
        'budget': 100,
        'preferred_date': 'Before Fri, 11 Apr',
        'preferred_time': 'Midday',
    },
    {
        'id': 2,
        'title': 'Fix sink',
        'username': 'Sarah',
        'description': 'Leaking pipe under kitchen sink.',
        'location': 'Wollongong, NSW',
        'budget': 150,
        'preferred_date': 'On Mon, 15 Apr',
        'preferred_time': 'Morning',
    },
    {
        'id': 3,
        'title': 'Dog walking',
        'username': 'John',
        'description': 'Walk my dog for an hour.',
        'location': 'Sydney, NSW',
        'budget': 50,
        'preferred_date': 'Flexible',
        'preferred_time': 'Anytime',
    },
    {
        'id': 4,
        'title': 'Grocery shopping',
        'username': 'Emily',
        'description': 'Buy groceries for the week.',
        'location': 'Bondi, NSW',
        'budget': 80,
        'preferred_date': 'Before Sun, 14 Apr',
        'preferred_time': 'Afternoon',
    },
    {
        'id': 5,
        'title': 'Car wash',
        'username': 'Michael',
        'description': 'Wash and vacuum my car.',
        'location': 'Wollongong, NSW',
        'budget': 30,
        'preferred_date': 'On Sat, 13 Apr',
        'preferred_time': 'Morning',
    },
    # ... (Add more if needed)
]

@login_required
def post_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.posted_by = request.user
            task.save()
            return redirect('job_list')  # Redirect to job list after posting
    else:
        form = TaskForm()
    
    return render(request, 'post_task.html', {'form': form})


def job_list(request):
    # Use real Task model later — for now use sample_tasks
    tasks = sample_tasks

    # Extract unique locations
    locations = sorted(set(task['location'] for task in tasks))

    return render(request, 'job_list.html', {
        'tasks': tasks,
        'locations': locations  # sent to template
    })



def job_detail(request, task_id):
    # TEMP: Sample tasks used for frontend development
    task_dict = {task['id']: task for task in sample_tasks}

    # Try to find the task by its ID
    task = task_dict.get(task_id)
    if not task:
        # Swap with raise Http404 or redirect if real task not found
        raise Http404("Task not found")

    return render(request, 'job_detail.html', {
        'task': task
    })

# BACKEND note:
# Later, replace this with:
# from .models import Task
# task = get_object_or_404(Task, id=task_id)

### -------------------- Manage Tasks View -------------------- #
@login_required
def manage_tasks(request):
    # MOCKED tab data
    posted_tasks = sample_tasks[:3]
    applied_offers = [
        {'task': sample_tasks[1], 'amount': 90, 'message': "Can fix this Thursday", 'status': 'pending'},
        {'task': sample_tasks[3], 'amount': 75, 'message': "Available Sunday", 'status': 'rejected'},
    ]
    engaged_offers = [
        {'task': sample_tasks[0], 'amount': 100, 'message': "Booked in", 'status': 'accepted'},
    ]
    bookmarked_tasks = [sample_tasks[2], sample_tasks[4]]

    return render(request, 'manage_tasks.html', {
        'posted_tasks': posted_tasks,
        'applied_offers': applied_offers,
        'engaged_offers': engaged_offers,
        'bookmarked_tasks': bookmarked_tasks,
    })


# TEMP: Simulated posted/applied/bookmarked/engaged task structure
posted_tasks = sample_tasks[:3]  # First 3 as posted
applied_offers = [
    {'task': sample_tasks[1], 'amount': 90, 'message': "Can fix this Thursday", 'status': 'pending'},
    {'task': sample_tasks[3], 'amount': 75, 'message': "Available Sunday", 'status': 'rejected'},
]
engaged_offers = [
    {'task': sample_tasks[0], 'amount': 100, 'message': "Booked in", 'status': 'accepted'},
    {'task': sample_tasks[1], 'amount': 90, 'message': "Can fix this Thursday", 'status': 'pending'},
]
bookmarked_tasks = [sample_tasks[2], sample_tasks[4]]  # Just simulate a couple
