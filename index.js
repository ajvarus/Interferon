function messageBoxToggle(clickedButtonId, boxToHideId) {
  const clickedButton = document.getElementById(clickedButtonId);
  const boxToHide = document.getElementById(boxToHideId);

  // Add click event listener to the button
  clickedButton.addEventListener("click", function () {
    // Toggle the visibility of the target element
    boxToHide.classList.toggle("is-hidden");
  });
}
console.log("hello");
messageBoxToggle("indexMessageDeleteButton", "indexMessageBox");
console.log("hello");
messageBoxToggle("indexKeygenButton", "indexMessageBox");
console.log("hello");
