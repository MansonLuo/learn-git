$(function() {	

	$.ajax({
		type: "get",
		url: "http://127.0.0.1:5000/test.json",
		contentType: "application/json;charset=utf-8",
		dataType: "json",
	}).done(function() {
		alert('success');
	}).fail(function() {
		alert('fail');
	});
});
