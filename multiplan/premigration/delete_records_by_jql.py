from library.customers.multiplan.server import multiplan_server

jql = 'project = MARS AND issuetype = Test AND fixVersion is EMPTY AND created < 2020-01-01 ORDER BY created DESC'

# Logic Below
issues_to_delete = multiplan_server.search(jql)
for issue in issues_to_delete:
    multiplan_server.delete(issue['self'])
