from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from ghctags.lib import RepoMeta


@view_config(route_name='home', renderer='index.mako')
def my_view(request):
    return {'project': 'ghctags'}


@view_config(route_name='lookup.html', renderer='lookup.mako')
@view_config(route_name='lookup.json', renderer='json')
def lookup(request):
    repo_meta = RepoMeta(request.GET["username"], request.GET["reponame"])
    results = repo_meta.lookup(request.GET["symbol"])
    if results.status == "ok":
        if len(results) == 0:
            return {
                'status': 'ok',
                'message': 'no results found',
                'results': [],
                'repository': {
                    'username': repo_meta.username,
                    'reponame': repo_meta.reponame,
                },
            }
        elif len(results) == 1:
            return HTTPFound("https://github.com/%s/%s/blob/master/%s#L%d" % (repo_meta.username, repo_meta.reponame, results[0].filename, results[0].line_number))
        else:
            return {
                'status': 'ok',
                'message': 'multiple results found',
                'results': [{"filename": loc.filename, "line_number": loc.line_number} for loc in results],
                'repository': {
                    'username': repo_meta.username,
                    'reponame': repo_meta.reponame,
                },
            }
            return HTTPFound("https://github.com/%s/%s/blob/master/%s#L%d" % (repo_meta.username, repo_meta.reponame, filename, line_number))
    elif results.status == "no repo":
        repo_meta.queue_for_update()
        return {
            'status': 'ok',
            'message': 'This repository has been queued for indexing, please try again in a minute',
            'results': [],
            'repository': {
                'username': repo_meta.username,
                'reponame': repo_meta.reponame,
            },
        }


