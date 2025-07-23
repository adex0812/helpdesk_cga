from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.db.models import Count, Case, When, IntegerField, Sum
from complain.models import Complaint
import json
from django.core.serializers.json import DjangoJSONEncoder

def dashboard_view(request):
    """Main dashboard view"""
    # Get summary statistics
    summary_data = get_complaint_summary()
    recent_complaints = Complaint.objects.order_by('-created_at')[:10]
    
    # Calculate totals for stats cards
    totals = calculate_status_totals(summary_data)
    
    # Serialize summary_data for JavaScript
    summary_data_json = json.dumps(list(summary_data), cls=DjangoJSONEncoder)
    
    context = {
        'summary_data': summary_data,
        'summary_data_json': summary_data_json,
        'recent_complaints': recent_complaints,
        'total_complaints': Complaint.objects.count(),
        'total_pending': totals['pending'],
        'total_in_progress': totals['in_progress'],
        'total_done': totals['done'],
        'total_rejected': totals['rejected'],
    }
    return render(request, 'index.html', context)

def calculate_status_totals(summary_data):
    """Calculate total counts for each status"""
    totals = {
        'pending': 0,
        'in_progress': 0,
        'done': 0,
        'rejected': 0
    }
    
    for item in summary_data:
        totals['pending'] += item.get('pending', 0)
        totals['in_progress'] += item.get('in_progress', 0)
        totals['done'] += item.get('done', 0)
        totals['rejected'] += item.get('rejected', 0)
    
    return totals

def get_complaint_summary():
    """Get complaint summary using Django ORM"""
    summary = Complaint.objects.values('username').annotate(
        pending=Count(Case(When(status='Pending', then=1), output_field=IntegerField())),
        in_progress=Count(Case(When(status='In Progress', then=1), output_field=IntegerField())),
        done=Count(Case(When(status='Done', then=1), output_field=IntegerField())),
        rejected=Count(Case(When(status='Rejected', then=1), output_field=IntegerField())),
        total=Count('id')
    ).order_by('username')
    
    return list(summary)

def get_complaint_summary_raw_sql():
    """Alternative: Get complaint summary using raw SQL"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                ROW_NUMBER() OVER (ORDER BY USERNAME) AS no,
                USERNAME as username,
                SUM(CASE WHEN STATUS = 'Pending' THEN 1 ELSE 0 END) AS pending,
                SUM(CASE WHEN STATUS = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
                SUM(CASE WHEN STATUS = 'Done' THEN 1 ELSE 0 END) AS done,
                SUM(CASE WHEN STATUS = 'Rejected' THEN 1 ELSE 0 END) AS rejected
            FROM BOT_COMPLAINTS_DEV
            GROUP BY USERNAME
            ORDER BY USERNAME;
        """)
        
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    return results

def api_complaint_data(request):
    """API endpoint for AJAX requests"""
    summary_data = get_complaint_summary()
    totals = calculate_status_totals(summary_data)
    
    return JsonResponse({
        'summary': summary_data,
        'total': Complaint.objects.count(),
        'totals': totals
    })

def complaint_detail_view(request, complaint_id):
    """View for individual complaint details"""
    complaint = Complaint.objects.get(id=complaint_id)
    return render(request, 'dashboard/complaint_detail.html', {'complaint': complaint})



