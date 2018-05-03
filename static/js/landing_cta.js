$(document).on('submit','#email-form', function(e){
	e.preventDefault();

	$.ajax({
		type:'POST',
		url: 'email/',
		data:{
			email: $('#email-input').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
		
	});
	$("div.form-row").replaceWith(
		"<span id=\"cta-ty\">Thank you for subscribing!</span>"
		);
});

