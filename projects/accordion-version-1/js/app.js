$(function() {
	var $headings = $('h2');
	var $paragraphs = $('p');
	//setup
	$paragraphs.not(':first').hide();

	$headings.on('click', function() {
		var $this = $(this);
		var $curP = $this.next();
		
		// not work if current p is visible
		if ($curP.is(':visible')) {
			return;
		}

		// show current p and hide the others
		$paragraphs.slideUp('normal');
		$curP.slideDown('normal');
		
	});
});





