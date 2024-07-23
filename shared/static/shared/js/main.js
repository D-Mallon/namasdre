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

  // Function to book class and handle response
  window.bookClass = function (classId) {
    const csrftoken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;
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
    popup.innerText = message;
    popup.classList.add("show");
    setTimeout(function () {
      popup.classList.remove("show");
    }, 3000);

    document.addEventListener("click", function () {
      popup.classList.remove("show");
    });
  }
})(jQuery);
