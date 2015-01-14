/* global $ */

$(document).ready(function(){
	$('.url-input').val('');

	var hideDialog = true;

	var qtipError = $('.url-input').qtip({
	    content: {
	    	prerender: true,
	    	text: 'Please enter a URL.',

	    },
	    show: '',
	    hide: 'unfocus',
	    position: {
	    	viewport: $(window),
	    	my: 'bottom left',
	    	at: 'top center',
	    	target: $('.url-input'),
	    	adjust: {
	    		x: 40
	    	}
	    },
	    style: {
	    	classes: 'qtip-tipsy'
	    }
	}).qtip('api');

	var qtipCopy = $('.short-code').qtip({
	    content: {
	    	prerender: true,
	    	text: 'CTRL-C to copy.',
	    },
	    show: '',
	    hide: 'unfocus',
	    position: {
	    	viewport: $(window),
	    	my: 'bottom center',
	    	at: 'top center',
	    	target: $('.short-code'),
		    adjust: {
		    	y: 10
		    }
	    },
	    style: {
	    	classes: 'qtip-tipsy'
	    }
	}).qtip('api');

	$('#url-form').submit(function(event){
		event.preventDefault();
		
		var request_url = $('.url-input').val();

		if(request_url === ''){
			$('.form-group').addClass('has-error');
			qtipError.set('content.text', 'Please enter a URL.');
			qtipError.show();
			return;
		} else {
			$('.form-group').removeClass('has-error');
			$('.form-group').addClass('has-success');
		}

		
		$('#url-form').append('<img class="center-block" src="static/pictures/spinner.gif">');

		$.getJSON('/generate/', { url: request_url }, function( data ){
			if(data.hasError === true){
				$('img').remove();
				qtipError.set('content.text', 'This URL is invalid.');
				qtipError.show();
			}
			$('img').fadeOut('slow', function(){
				$(this).remove();
				$('.short-code').fadeIn().css('display', 'block');
				$('.short-code').val('http://localhost:5000/url/' + data.shortURL);
				$('.short-code').focus();
				$('.short-code').select();
				hideDialog = false;
				qtipCopy.show();
			});
		});
	});

	$('.short-code').click(function(){
		this.focus();
		this.select();
		if(hideDialog){
			qtipCopy.show();
		} else {
			qtipCopy.hide();
		}
		hideDialog = !hideDialog;
	});
});