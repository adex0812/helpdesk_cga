from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import Complaint
from .forms import UpdateStatusForm
import requests
from django.utils.html import escape
from django.contrib.auth.decorators import login_required

@login_required
def complaint_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'ALL')
    
    complaints = Complaint.objects.all()

    if search_query:
        complaints = complaints.filter(
            Q(username__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    if status_filter != 'ALL':
        complaints = complaints.filter(status=status_filter)

    complaints = complaints.order_by('-created_at')

    paginator = Paginator(complaints, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'list.html', context)

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'detail.html', {'complaint': complaint})

@login_required
def complaint_update_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.method == 'POST':
        form = UpdateStatusForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.update_date = timezone.now()
            complaint.save()

            token = '7780641652:AAHuJbouT-Y5IKvJRwcqjG5WtBJix3NY9yA'
            chat_id = complaint.user_id  
            description = escape(complaint.description)
            status = escape(complaint.status)
            keterangan = escape(complaint.keterangan)
            
            message = f"Komplain atau permintaan Anda dengan deskripsi {description} telah diproses dengan status {status} dan keterangannya {keterangan}"
            api_url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message
            }

            try:
                requests.post(api_url, data=payload)
            except requests.exceptions.RequestException as e:
                print("Gagal kirim Telegram:", e)

            messages.success(request, 'Status updated successfully!')
            return redirect('complaint_detail', pk=pk)
    else:
        form = UpdateStatusForm(instance=complaint)
    
    return render(request, 'update_status.html', {
        'form': form,
        'complaint': complaint,
        'user': request.user, 
        'complaint': complaint
    })

def complaint_api(request):
    complaints = Complaint.objects.all().values(
        'id', 'username', 'user_id', 'description', 'complaint_type',
        'status', 'created_at', 'update_status_by', 'keterangan'
    )
    return JsonResponse(list(complaints), safe=False)