(function ($) {
  skel.breakpoints({
    xlarge: "(max-width: 1680px)",
    large: "(max-width: 1280px)",
    medium: "(max-width: 980px)",
    small: "(max-width: 736px)",
    xsmall: "(max-width: 480px)",
    xxsmall: "(max-width: 360px)",
  });

  $(function () {
    var $window = $(window),
      $body = $("body");

    // Disable animations/transitions until the page has loaded.
    $body.addClass("is-loading");

    $window.on("load", function () {
      window.setTimeout(function () {
        $body.removeClass("is-loading");
      }, 100);
    });

    // Fix: Placeholder polyfill.
    $("form").placeholder();

    // Prioritize "important" elements on medium.
    skel.on("+medium -medium", function () {
      $.prioritize(
        ".important\\28 medium\\29",
        skel.breakpoint("medium").active
      );
    });

    // Items.
    $(".item").each(function () {
      var $this = $(this),
        $header = $this.find("header"),
        $a = $header.find("a"),
        $img = $header.find("img");

      // Set background.
      $a.css("background-image", "url(" + $img.attr("src") + ")");

      // Remove original image.
      $img.remove();
    });
  });

  // Function to get CSRF token
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Function to book class and handle response
  window.bookClass = function (classId) {
    const csrftoken = getCookie("csrftoken");
    fetch("/add_class_to_profile/" + classId + "/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({}),
    })
      .then((response) => response.json())
      .then((data) => {
        showPopupMessage(data.message);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  // Function to show popup message
  function showPopupMessage(message) {
    const popup = document.getElementById("popup-message");
    if (popup) {
      popup.innerText = message;
      popup.classList.add("show");
      setTimeout(function () {
        popup.classList.remove("show");
      }, 3000);

      document.addEventListener("click", function () {
        popup.classList.remove("show");
      });
    }
  }

  // cancelBooking function
  window.cancelBooking = function (bookingId) {
    // console.log("Cancel button clicked for booking ID:", bookingId); // Debugging line

    if (confirm("Are you sure you want to cancel this booking?")) {
      const csrftoken = getCookie("csrftoken"); // Use the correct function to get the CSRF token
      fetch(`/remove_class_from_profile/${bookingId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            document.getElementById(`class-item-${bookingId}`).remove();
            showPopupMessage(data.message);
          } else {
            showPopupMessage("Failed to remove the booking.");
          }
        })
        .catch((error) => console.error("Error:", error));
    }
  };
})(jQuery);
