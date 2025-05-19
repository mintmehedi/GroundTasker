from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TaskForm


# TEMPORARY SAMPLE DATA
sample_tasks = [
    {
        'id': 1,
        'title': 'Weed backyard',
        'description': 'Remove weeds and tidy the backyard.',
        'location': 'Parramatta, NSW',
        'budget': 100,
        'preferred_date': 'Before Fri, 11 Apr',
        'preferred_time': 'Midday',
    },
    {
        'id': 2,
        'title': 'Fix sink',
        'description': 'Leaking pipe under kitchen sink.',
        'location': 'Wollongong, NSW',
        'budget': 150,
        'preferred_date': 'On Mon, 15 Apr',
        'preferred_time': 'Morning',
    },
    {
        'id': 3,
        'title': 'Dog walking',
        'description': 'Walk my dog for an hour.',
        'location': 'Sydney, NSW',
        'budget': 50,
        'preferred_date': 'Flexible',
        'preferred_time': 'Anytime',
    },
    {
        'id': 4,
        'title': 'Grocery shopping',
        'description': 'Buy groceries for the week.',
        'location': 'Bondi, NSW',
        'budget': 80,
        'preferred_date': 'Before Sun, 14 Apr',
        'preferred_time': 'Afternoon',
    },
    {
        'id': 5,
        'title': 'Car wash',
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
    # Reformat sample_tasks into dict for lookup
    task_dict = {task['id']: task for task in sample_tasks}
    
    task = task_dict.get(task_id)
    if not task:
        return render(request, '404.html')

    return render(request, 'job_detail.html', {
        'task': task,
        'tasks': sample_tasks
    })
