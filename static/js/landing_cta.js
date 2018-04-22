// jQuery for call-to action on landing page for email

$(document).ready( function() {

	$("#submit").click( function() {
		alert("Submitted.");
		var email = $("#email").val();
		console.log(email);

		$.post( "/landing", {
			email
		});

		$("div.form-row").replaceWith(
			"<span id=\"cta-ty\"> Thank you! </span>"
		);

	});

});

