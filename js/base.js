// create a console
let body = document.getElementsByTagName('body')[0];
let cons = document.createElement('div');
cons.className = 'console';
body.appendChild(cons);

let lg = document.getElementsByClassName('console')[0];

// output log
function log(msg) {
	lg.className = "exist console";
	lg.innerHTML = msg;
}

function disLog(e) {
	e.target.className="dis";
}

lg.addEventListener('click', disLog, false);

// observer error
function onErrorListener(message, source, lineno, colno, error) {
	let res = '<b>Error msg:</b> ' + message + '<br>';
	res += '<b>Source file: </b>' + source + '<br>';
	res += '<b>Line number:</b> ' + lineno + '<br>';
	res += '<b>Column number: </b> ' + colno + '<br>';
	log(res);
}
window.onerror = onErrorListener;


