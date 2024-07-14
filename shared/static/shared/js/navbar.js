document
  .getElementById("hamburger-icon")
  .addEventListener("click", function (event) {
    var menu = document.getElementById("menu");
    var style = getComputedStyle(menu); // get the computed style of #menu
    if (style.right === "0px") {
      menu.style.right = "-100%";
    } else {
      menu.style.right = "0px";
    }
    event.stopPropagation(); // Prevent click from immediately propagating to document
  });

document.addEventListener("click", function (event) {
  var menu = document.getElementById("menu");
  if (menu.style.right === "0px") {
    menu.style.right = "-100%";
  }
});

// Prevent menu close when clicking inside the menu
document.getElementById("menu").addEventListener("click", function (event) {
  event.stopPropagation();
});

// working basic version of the hamburger menu below
// document
//   .getElementById("hamburger-icon")
//   .addEventListener("click", function () {
//     var menu = document.getElementById("menu");
//     var style = getComputedStyle(menu); // get the computed style of #menu
//     if (style.right === "0px") {
//       menu.style.right = "-100%";
//     } else {
//       menu.style.right = "0px";
//     }
//   });
