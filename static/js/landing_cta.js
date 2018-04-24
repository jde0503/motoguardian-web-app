// jQuery for call-to action on landing page for email

$(document).ready( function() {

	$(".submit").click( function() {
        if (this.id == "submit1") {
		    var email = $("#email1").val();
        }
        else {
            var email = $("#email2").val();
        }

        $.ajax({
            type: "POST",
            url: "/landing",
            data: JSON.stringify({email_address: email}),
            success: (function(){alert("Submission success.");}),
            error: (function(){alert("Submission failed.");})
        });

		$("div.form-row").replaceWith(
			"<span id=\"cta-ty\"> Thank you! </span>"
		);

	});

});
