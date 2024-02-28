from library.customers.multiplan.server import multiplan_server

field_from = 'customfield_10620'  # Epic Link
field_to = 'customfield_14622'  # Legacy Epic Key

jql = 'key = PMS-124'

# Logic Below
for issue in multiplan_server.search(jql):
    multiplan_server.update_issue(issue['key'], {field_to: issue['fields'][field_from]})
