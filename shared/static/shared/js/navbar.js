// function toggleMenu() {
//   const menu = document.getElementById("menu");
//   if (menu.style.right === "-100%") {
//     menu.style.right = "0";
//   } else {
//     menu.style.right = "-100%";
//   }
// }

document
  .getElementById("hamburger-icon")
  .addEventListener("click", function () {
    var menu = document.getElementById("menu");
    var style = getComputedStyle(menu); // get the computed style of #menu
    if (style.right === "0px") {
      menu.style.right = "-100%";
    } else {
      menu.style.right = "0px";
    }
  });
