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
from django.db.models import Max, F, Count


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
            .order_by("-created_at")
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

    # Step 1: Annotate each Guest with the count of entries and the maximum ULID value for their latest entry
    guest_entry_details = Guest.objects.annotate(
        entry_count=Count("entry"), latest_entry_ulid=Max("entry__ulid")
    ).order_by("-latest_entry_ulid")

    # Step 2: Retrieve the latest entries using the maximum ULIDs
    latest_ulids = [
        guest.latest_entry_ulid
        for guest in guest_entry_details
        if guest.latest_entry_ulid
    ]
    latest_entries = {
        entry.ulid: entry for entry in Entry.objects.filter(ulid__in=latest_ulids)
    }

    # Step 3: Compute the user data by matching guests to their latest entry
    users_data = [
        {
            "username": guest.name,
            "last_entry": f"{latest_entries[guest.latest_entry_ulid].subject} | {latest_entries[guest.latest_entry_ulid].message}",
            "last_entry_id": latest_entries[guest.latest_entry_ulid].id,
            "entry_count": guest.entry_count,
        }
        for guest in guest_entry_details
        if guest.latest_entry_ulid in latest_entries
    ]

    response_data = {"users": users_data}
    return JsonResponse(response_data)
