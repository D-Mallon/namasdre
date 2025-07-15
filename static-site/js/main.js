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

    // Check for popup trigger
    const popupOverlay = document.querySelector(".popup-overlay");
    const closePopupButton = document.querySelector(".close-popup-button");

    if (popupOverlay) {
      console.log("Popup overlay detected");
      const successMessage = document.querySelector(
        ".popup-message-content"
      ).innerText;
      if (successMessage) {
        popupOverlay.style.display = "flex"; // Show the popup if there's a message
        console.log("Showing popup with message:", successMessage);
      }

      if (closePopupButton) {
        console.log("Close button detected");
        closePopupButton.addEventListener("click", function () {
          popupOverlay.style.display = "none"; // Hide the popup
          location.reload(); // Refresh the page after closing the popup
        });
      } else {
        console.log("Close button not found");
      }
    }

    // Handle contact form submission with Formspree
    const contactForm = document.getElementById("contact-form");
    if (contactForm) {
      contactForm.addEventListener("submit", function (event) {
        // Form will be handled by Formspree
        // This is just for any additional JS functionality
        console.log("Form submitted to Formspree");
      });
    }
  });
})(jQuery);
