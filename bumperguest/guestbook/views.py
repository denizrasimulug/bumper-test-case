from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from bumperguest.guestbook.dtos.EntryDetailDto import EntryDetailDTO
from bumperguest.guestbook.models import Entry, Guest
from bumperguest.guestbook.requests import CreateEntryRequest, GetEntriesRequest
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.db.models import F, Max

class EntryView(View):
    ENTRY_PER_PAGE = 3
    def post(self, request):
        request_data = CreateEntryRequest(request.POST)

        if not request_data.is_valid():
            return JsonResponse({"errors": request_data.errors}, status=400)

        guest, created = Guest.objects.get_or_create(name=request_data.name)
        entry = Entry.objects.create(
            subject=request_data.subject,
            message=request_data.message,
            guest=guest
        )
        
        entry_dto = EntryDetailDTO(entry)
        return JsonResponse(entry_dto.to_dict())

    def get(self, request):
        request_data = GetEntriesRequest(request.GET)
        if not request_data.is_valid():
            return JsonResponse({"errors": request_data.errors}, status=400)
        entries = Entry.objects.all().order_by('-created_date').annotate(guest_name=F('guest__name')).values('guest_name', 'subject', 'message')
        paginator = Paginator(entries, self.ENTRY_PER_PAGE)
        page_obj = paginator.get_page(request_data.page)

        entries_list = [
            {
                "user": entry.guest_name,
                "subject": entry.subject,
                "message": entry.message,
            }
            for entry in page_obj
        ]

        response_data = {
            "count": paginator.count,
            "page_size": paginator.per_page,
            "total_pages": paginator.num_pages,
            "current_page_number": page_obj.number,
            "links": {
                "next": page_obj.next_page_number() if page_obj.has_next() else None,
                "previous": (
                    page_obj.previous_page_number() if page_obj.has_previous() else None
                ),
            },
            "entries": entries_list,
        }

        return JsonResponse(response_data)


@require_GET
def get_user_data(request):
    # Query the Entry table, grouping by guest, and selecting the latest entry per guest
    latest_entries = (
        Entry.objects.annotate(latest_date=Max("created_date"))
        .filter(created_date=F("latest_date"))
        .select_related("guest")  # Fetch guest data in the same query
        .only(
            "guest__name", "subject", "message", "created_date"
        )  # Limit fields to save memory
    )

    # Prepare response data from the latest entries
    users_data = [
        {
            "username": entry.guest.name,
            "last_entry": f"{entry.subject} | {entry.message}",
        }
        for entry in latest_entries
    ]

    response_data = {"users": users_data}

    return JsonResponse(response_data)