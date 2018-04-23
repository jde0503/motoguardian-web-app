// jQuery for call-to action on landing page for email

$(document).ready( function() {

	$(".submit").click( function() {
		var email = $("#email").val();

        $.ajax({
            type: "POST",
            url: "/landing",
            data: JSON.stringify({email_address: email}),
            success: alert("Submission success."),
        });

		$("div.form-row").replaceWith(
			"<span id=\"cta-ty\"> Thank you! </span>"
		);

	});

});
