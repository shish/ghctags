<!DOCTYPE html>
<html>
	<head>
		<title>GHCTags - Ctags for GitHub</title>
		<style>
.ss {
	border: 1px solid #888;
	box-shadow: 2px 2px 4px #888;
}
TABLE {
	max-width: 1200px;
	width: 100%;
	margin: auto;
}
TD {
	vertical-align: top;
	text-align: center;
}
.col {
	width: 450px;
	text-align: left;
	margin: auto;
}
		</style>
	</head>
	<body>
		<table>
			<tr><td colspan="2">

				<h1>GHCtags - Ctags for GitHub</h1>
				<p>(No official relation to either Ctags or GitHub)

			</td></tr>

			<tr><td width="50%"><div class="col">

				<h2>Step 1: Install User Script</h2>
				<p><a href="/static/ghctags.user.js">User script</a> (See right)

				<h2>Step 2: Click on Symbol</h2>
				<p><img class="ss" src="${request.static_url('ghctags:static/click-on-symbol.png')}" />

				<h2>Step 3: Get Definition</h2>
				<p><img class="ss" src="${request.static_url('ghctags:static/get-definition.png')}" />
	
				<h2>Step 4: <a href="https://news.ycombinator.com/item?id=6689060">Complain on HN</a></h2>
				<p><img class="ss" src="${request.static_url('ghctags:static/bitch.png')}" />
	
			</div></td><td><div class="col">

				<h2>Installing a User Script</h2>
				<h3>Firefox:</h3>
				<ol>
					<li>Install <a href="https://addons.mozilla.org/firefox/addon/748">Greasemonkey</a>
					<li>Click on the "user script" link to the left
				</ol>
				<h3>Chrome:</h3>
				<ol>
					<li>Install <a href="https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo">Tampermonkey</a>
					<li>Click on the "user script" link to the left
				</ol>
				<!--
				<p>(Or I could jump through google's hoops to get into their app store, but eh)
				-->

				<p>&nbsp;
				<h2>TODO</h2>
				<ul>
					<li>AJAX lookup rather than HTTP redirect so that the multiple-results menu can appear in the page
					<ul><li>(GitHub's well-implemented security policy makes this a pain v_v May need to write
					a low-level plugin for each browser instead of a user script &gt;_&lt;<!-- Or GitHub could hire me
					so that I can do a properly integrated version ^_^ -->)</ul>
					<li>Add a "refresh tags" button to the repo browser
					<li>Re-attach event handlers after content is AJAX-loaded, instead of on a 1-second loop
				</ul>

				<p>&nbsp;
				<h2>Contact</h2>
				<ul>
					<li><a href="webmaster+ghctags@shishnet.org">webmaster+ghctags@shishnet.org</a>
					<li><a href="http://code.shishnet.org/">Check out my other stuff</a>
				</ul>

			</div></td></tr>
		</table>
	</body>
</html>
