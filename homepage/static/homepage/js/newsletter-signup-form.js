// function getCookie(name) {
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== "") {
//     const cookies = document.cookie.split(";");
//     for (let i = 0; i < cookies.length; i++) {
//       const cookie = cookies[i].trim();
//       // Does this cookie string begin with the name we want?
//       if (cookie.substring(0, name.length + 1) === name + "=") {
//         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//         break;
//       }
//     }
//   }
//   return cookieValue;
// }

// const csrftoken = getCookie("csrftoken");

$(document).ready(function () {
  $("#newsletter").on("submit", function (e) {
    e.preventDefault();

    var formData = {
      email: $("#email").val(),
      csrfmiddlewaretoken: csrftoken,
    };

    $("#loading").fadeIn("slow");
    $("#sent-message").hide();
    $("#error-message").hide();

    $.ajax({
      url: "/newsletter/signup/",
      type: "POST",
      data: formData,
      dataType: "json",
      success: function (response) {
        $("#loading").hide();
        if (response.status === "success") {
          $("#sent-message").text(response.message).fadeIn("slow");
          $("#newsletter").trigger("reset");

          setTimeout(function () {
            $("#sent-message").fadeOut("slow");
          }, 3000);
        } else {
          $("#error-message").text(response.message).show();
        }
      },
      error: function (response) {
        $("#loading").hide();
        $("#error-message")
          .text("خطایی رخ داده است. لطفا دوباره تلاش کنید.")
          .show();
      },
    });
  });
});
