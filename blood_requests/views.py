from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import BloodRequest, DonorResponse
import json


def request_list(request):
    """Public emergency request board"""
    blood_group = request.GET.get("blood_group", "")
    rh_factor = request.GET.get("rh_factor", "")
    urgency = request.GET.get("urgency", "")
    
    requests_qs = BloodRequest.objects.filter(status="open").order_by("-created_at")
    if blood_group:
        requests_qs = requests_qs.filter(blood_group=blood_group)
    if rh_factor:
        requests_qs = requests_qs.filter(rh_factor=rh_factor)
    if urgency:
        requests_qs = requests_qs.filter(urgency_level=urgency)
    
    return render(request, "requests/list.html", {
        "requests_list": requests_qs,
        "blood_group": blood_group,
        "rh_factor": rh_factor,
    })


def request_detail(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    responses = blood_request.donor_responses.all().select_related("donor")
    ranked_donors = blood_request.get_ranked_donors(radius_km=50)

    # Determine whether the currently logged-in hospital can fulfill this request.
    can_hospital_fulfill = False
    hospital_stock_for_type = 0
    if (
        request.user.is_authenticated
        and request.user.role == "hospital"
        and blood_request.linked_hospital is not None
    ):
        try:
            hospital = request.user.hospital_profile
            if hospital.pk == blood_request.linked_hospital_id and blood_request.status == "open":
                from hospitals.services import get_stock_field_name
                blood_stock = getattr(hospital, "blood_stock", None)
                if blood_stock:
                    field_name = get_stock_field_name(
                        blood_request.blood_group, blood_request.rh_factor
                    )
                    if field_name:
                        hospital_stock_for_type = getattr(blood_stock, field_name, 0)
                        can_hospital_fulfill = hospital_stock_for_type >= blood_request.units_remaining
        except Exception:
            # Never crash the detail page due to missing profile data.
            pass

    return render(request, "requests/detail.html", {
        "blood_request": blood_request,
        "responses": responses,
        "ranked_donors": ranked_donors,
        "can_hospital_fulfill": can_hospital_fulfill,
        "hospital_stock_for_type": hospital_stock_for_type,
    })


def requests_json(request):
    """API endpoint for map markers"""
    requests_qs = BloodRequest.objects.filter(status="open").values(
        "id", "blood_group", "rh_factor", "hospital_name",
        "urgency_level", "latitude", "longitude", "city"
    )
    return JsonResponse(list(requests_qs), safe=False)
