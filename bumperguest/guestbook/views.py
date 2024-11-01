import json
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from guestbook.dtos.EntryDetailDto import EntryDetailDTO
from guestbook.models import Entry, Guest
from guestbook.requests.GetEntriesRequest import GetEntriesRequest
from guestbook.requests.CreateEntryRequest import CreateEntryRequest
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.db.models import Max, F, OuterRef, Subquery


class EntryView(View):
    ENTRY_PER_PAGE = 3

    def post(self, request):
        request_data = CreateEntryRequest(json.loads(request.body))

        if not request_data.is_valid():
            return JsonResponse({"errors": request_data.errors}, status=400)

        guest, created = Guest.objects.get_or_create(name=request_data.name)
        entry = Entry.objects.create(
            subject=request_data.subject, message=request_data.message, guest=guest
        )

        entry_dto = EntryDetailDTO(entry)
        return JsonResponse(entry_dto.to_dict(), status=201)

    def get(self, request):
        entries = (
            Entry.objects.all()
            .order_by("-created_date")
            .annotate(guest_name=F("guest__name"))
            .values("guest_name", "subject", "message")
        )
        paginator = Paginator(entries, self.ENTRY_PER_PAGE)
        request_data = GetEntriesRequest(
            request.GET.get("page", 1),
            paginator.num_pages,
        )
        if not request_data.is_valid():
            return JsonResponse({"errors": request_data.errors}, status=400)
        page_obj = paginator.get_page(request_data.page)

        entries_list = [
            {
                "user": entry["guest_name"],
                "subject": entry["subject"],
                "message": entry["message"],
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
    # Annotate each guest with the ID of their latest entry
    latest_entry_ids = (
        Entry.objects.filter(guest=OuterRef("pk"))
        .order_by("-created_date")
        .values("id")[:1]
    )

    # Now we fetch the latest entry for each guest using this annotation
    guests_with_latest_entries = Guest.objects.annotate(
        latest_entry_id=Subquery(latest_entry_ids)
    ).filter(latest_entry_id__isnull=False)

    # Query the latest entries using these IDs
    latest_entries = Entry.objects.filter(
        id__in=[guest.latest_entry_id for guest in guests_with_latest_entries]
    ).order_by("-created_date")

    # Construct your response
    users_data = [
        {
            "username": entry.guest.name,
            "last_entry": f"{entry.subject} | {entry.message}",
            "entry_id": entry.id,
        }
        for entry in latest_entries
    ]

    response_data = {"users": users_data}

    return JsonResponse(response_data)
