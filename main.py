from jira import JIRA
import re
from datetime import datetime
from pytz import timezone
from database import insert_on_conflict


def convert_inserted(line):
    utc_time = datetime.strptime(line, '%Y-%m-%dT%H:%M:%S.%f%z')\
        .replace(tzinfo=timezone('utc')).strftime('%Y-%m-%d %H:%M:%S')
    return utc_time


sql = '''
insert into {} as t ({}) values ({}) on conflict (key)
do update set
    created = excluded.created,
    creator = excluded.creator,
    assignee = excluded.assignee,
    duedate = excluded.duedate,
    issuelinks = excluded.issuelinks,
    issuetype = excluded.issuetype,
    labels = excluded.labels,
    lastViewed = excluded.lastViewed,
    priority = excluded.priority,
    project_name = excluded.project_name,
    reporter = excluded.reporter,
    status = excluded.status,
    subtasks = excluded.subtasks,
    summary = excluded.summary,
    updated = excluded.updated
'''


token = 'mi2aUfOpvGmsvMvhvPgo106C'
jiraOptions = {'server': "https://ksitemp.atlassian.net"}

jira = JIRA(options=jiraOptions, basic_auth=("tega85338@gmail.com", token))

jql = "project = 'KBP'"
jira_list = jira.search_issues(jql, maxResults=0)
# print(jira_list)
# print(dir(jira_list))
# print(jira_list.total)
#
# print(dir(jira))
# users = jira.search_users(jql)
# print(users)
lst = []
for i in jira_list:
    data = {
        'key': i.key,
        'created': convert_inserted(i.fields.created),
        'creator': i.fields.creator.displayName,
        'assignee': i.fields.assignee.displayName if i.fields.assignee else None,
        'duedate': i.fields.duedate,
        'issuelinks': ','.join([i.id for i in i.fields.issuelinks]),
        'issuetype': i.fields.issuetype.name,
        'labels': ','.join(i.fields.labels),
        'lastViewed': i.fields.lastViewed,
        'priority': i.fields.priority.name,
        'project_name': i.fields.project.name,
        'reporter': i.fields.reporter.displayName,
        'status': i.fields.status.name,
        'subtasks': ','.join([i.key for i in i.fields.subtasks]),
        'summary': i.fields.summary,
        'updated': convert_inserted(i.fields.updated),
    }
    print(data)
    lst.append(data)

insert_on_conflict('home.jira_issues', lst, sql)

'''
data = {
        'key': i.key,
        'created': convert_inserted(i.fields.created),
        'creator': i.fields.creator.displayName,
        # 'aggregateprogress': i.fields.aggregateprogress.progress,
        # 'aggregateprogress_t': i.fields.aggregateprogress.total,
        # 'aggregatetimeestimate': i.fields.aggregatetimeestimate,
        # 'aggregatetimeoriginalestimate': i.fields.aggregatetimeoriginalestimate,
        # 'aggregatetimespent': i.fields.aggregatetimespent,
        'assignee': i.fields.assignee.displayName if i.fields.assignee else None,
        # 'components': i.fields.components,

        # 'customfield_10000': i.fields.customfield_10000,
        # 'customfield_10001': i.fields.customfield_10001,
        # 'customfield_10002': i.fields.customfield_10002,
        # 'customfield_10010': i.fields.customfield_10010,
        # 'customfield_10014': i.fields.customfield_10014,
        # 'customfield_10015': i.fields.customfield_10015,
        # 'customfield_10016': i.fields.customfield_10016,
        # 'customfield_10017': i.fields.customfield_10017,
        # 'customfield_10018': i.fields.customfield_10018.hasEpicLinkFieldDependency,
        # 'customfield_10018_sf': i.fields.customfield_10018.showField,
        # 'customfield_10018_er': i.fields.customfield_10018.nonEditableReason,
        # 'customfield_10019': i.fields.customfield_10019,
        # 'customfield_10020': i.fields.customfield_10020,
        # 'customfield_10021': i.fields.customfield_10021,
        # 'customfield_10022': i.fields.customfield_10022,
        # 'customfield_10023': i.fields.customfield_10023,
        # 'customfield_10029': i.fields.customfield_10029,
        # 'customfield_10033': i.fields.customfield_10033,
        # 'customfield_10034': i.fields.customfield_10034,
        # 'customfield_10035': i.fields.customfield_10035,
        # 'customfield_10036': i.fields.customfield_10036,
        # 'customfield_10040': i.fields.customfield_10040,
        # 'description': i.fields.description,
        'duedate': i.fields.duedate,
        # 'environment': i.fields.environment,
        # 'fixVersions': i.fields.fixVersions,
        'issuelinks': i.fields.issuelinks,
        'issuetype': i.fields.issuetype.name,
        'labels': i.fields.labels,
        'lastViewed': i.fields.lastViewed,
        'priority': i.fields.priority.name,
        # 'progress': i.fields.progress.progress,
        # 'project_key': i.fields.project.key,
        'project_name': i.fields.project.name,
        'reporter': i.fields.reporter.displayName,
        # 'reporter_id': i.fields.reporter.accountId,
        # 'resolution': i.fields.resolution,
        # 'resolutiondate': i.fields.resolutiondate,
        # 'security': i.fields.security,
        'status': i.fields.status.name,
        # 'statuscategorychangedate': convert_inserted(i.fields.statuscategorychangedate),
        'subtasks': i.fields.subtasks,
        'summary': i.fields.summary,
        # 'timeestimate': i.fields.timeestimate,
        # 'timeoriginalestimate': i.fields.timeoriginalestimate,
        'timespent': i.fields.timespent,
        'updated': convert_inserted(i.fields.updated),
        # 'versions': i.fields.versions,
        # 'votes': i.fields.votes.votes,
        # 'watches': i.fields.watches,
        # 'workratio': i.fields.workratio,
    }
'''