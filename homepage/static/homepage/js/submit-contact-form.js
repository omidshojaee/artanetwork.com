$(document).ready(function () {
  $("#contact-form").on("submit", function (e) {
    e.preventDefault();

    var formData = {
      name: $("#name").val(),
      tel: $("#tel").val(),
      subject: $("#subject").val(),
      message: $("#message").val(),
      csrfmiddlewaretoken: csrftoken,
    };

    $("#contact-loading").fadeIn("slow");
    $("#contact-sent-message").hide();
    $("#contact-error-message").hide();

    $.ajax({
      url: "/contact/",
      type: "POST",
      data: formData,
      dataType: "json",
      success: function (response) {
        $("#contact-loading").hide();
        if (response.status === "success") {
          $("#contact-sent-message").text(response.message).fadeIn("slow");
          $("#contact-form").trigger("reset");

          setTimeout(function () {
            $("#contact-sent-message").fadeOut("slow");
          }, 3000);
        } else {
          $("#contact-error-message").text(response.message).show();
        }
      },
      error: function (response) {
        $("#contact-loading").hide();
        $("#contact-error-message")
          .text("خطایی رخ داده است. لطفا دوباره تلاش کنید.")
          .show();
      },
    });
  });
});
