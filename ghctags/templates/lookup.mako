<html>
	<head>
		<title>Results</title>
	</head>
	<body>
	% if results:
		Multiple results found:
		<ul>
			% for r in results:
				<li>
					<a
						href="${
							'https://github.com/%s/%s/blob/master/%s#L%d' % (
								repository['username'], repository['reponame'], r['filename'], r['line_number']
							)
						}"
					>${r['filename']}:${r['line_number']}</a>
				</li>
			% endfor
		</ul>
	% else:
		${message}
	% endif
	</body>
</html>
