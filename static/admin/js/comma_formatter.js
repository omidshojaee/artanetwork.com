document.addEventListener("DOMContentLoaded", function () {
  // Select all input fields that might need comma formatting
  const inputs = document.querySelectorAll('input[type="text"]');

  inputs.forEach((input) => {
    // Add event listeners for formatting
    input.addEventListener("input", formatNumber);
    input.addEventListener("blur", formatNumber);
  });

  function formatNumber(e) {
    let value = e.target.value;

    // Remove existing commas and non-numeric characters
    value = value.replace(/[,\D]/g, "");

    // Convert to number and back to string to remove leading zeros
    const numberValue = parseInt(value, 10);

    // Skip formatting if value is empty or not a valid number
    if (isNaN(numberValue)) {
      e.target.value = "";
      return;
    }

    // Format with commas
    e.target.value = numberValue.toLocaleString("en-US");
  }
});
