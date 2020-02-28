$(function() {
	var $headings = $('h2');
	var $paragraphs = $('p');
	//setup
	$paragraphs.not(':first').hide();

	// bind click for headings
	$('body').on('click','h2', function() {
		var $this = $(this);
		var $curP = $this.next();
		
		// show par if it's hidden
		if (!$curP.is(':visible')) {
			$curP.trigger('showParagraph');
		}else {
			// hide par if it's visible
			$curP.trigger('hideParagraph');
		}

	});
		
	// bind click for each p
	$('body').on('click', 'p', function() {
		//we can only click p when it's visible
		$(this).trigger('hideParagraph');
	});

	// bind showParagraph event for each p
	$('body').on('showParagraph', 'p', function() {
		$paragraphs.slideUp('normal');
		$(this).slideDown('normal');
	});

	// bind hideParagraph event for each p
	$('body').on('hideParagraph', 'p', function() {
		$paragraphs.slideUp('normal');
	});

});





