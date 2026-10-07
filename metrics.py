from prometheus_client import Counter


TICKETS_CREATED = Counter(
    "helpdesk_tickets_created_total",
    "Total number of created tickets",
    ["category"]
)