// ==UserScript== 
// @name Ctags for GitHub 
// @namespace http://ghctags.shishnet.org/
// @description Click on identifiers in github code browser to see the definition
// @include https://github.com/*
// ==/UserScript==

/*
 * Disclaimer: I don't know how to do anything without jQuery.
 */
function bindAll(names) {
	for(var j=0; j<names.length; j++) {
		var name = names[j];
		name.onclick = lookup;
		name.onmouseover = hover;
		name.onmouseout = unhover;
	}
}

function main() {
	var highlights = document.querySelectorAll(".highlight");

/*
	if(highlights.length) {
		if(window.console) console.log("Hooking GHCtags links into source viewer");
	}
*/
	for(var i=0; i<highlights.length; i++) {
		var highlight = highlights[i];
		if(highlight.className.indexOf("ghctagged") > 0) {
			continue;
		}
		highlight.className += " ghctagged";

		bindAll(highlight.querySelectorAll(".n"));   // name
		bindAll(highlight.querySelectorAll(".nx"));  // name executable
		// nb = builtin? nv = variable?
	}
}

function lookup() {
	var path_parts = window.location.pathname.split("/");
	var username = path_parts[1];
	var reponame = path_parts[2];
	var lookup_url = "http://ghctags.shishnet.org/lookup.html?username="+username+"&reponame="+reponame+"&symbol="+this.innerHTML;
	console.log(lookup_url);
	window.location.href = lookup_url;
}

function hover() {
	this.style.textDecoration = "underline";
}

function unhover() {
	this.style.textDecoration = null;
}

// new content is ajax-loaded every now and then...
//main();
setInterval(main, 1000);
