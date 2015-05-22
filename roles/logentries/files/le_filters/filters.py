# Example
#
# # filter celery events
# def filter_celery_events(events):
#     filtered_events = []
#     for event in events.split('\n')[:-1]:
#         if event.find('Attempt to decode JSON with unexpected mimetype: text/html; charset=utf-8') == -1:
#             filtered_events.append(event)
#     return ''.join(x + '\n' for x in filtered_events)
#
#
# # filter server events
# def filter_server_events(events):
#     filtered_events = []
#     for event in events.split('\n')[:-1]:
#         if event.find('[INFO][tornado.access]: 200 GET /status') == -1:
#             filtered_events.append(event)
#     return ''.join(x + '\n' for x in filtered_events)
#
#
# filters = {
#     'waterbutler_celery_1.log': filter_celery_events,
#     'waterbutler_server_1.log': filter_server_events,
#     'waterbutler_server_2.log': filter_server_events,
# }
