document.addEventListener("DOMContentLoaded", function () {
  const priceInput = document.querySelector("#id_price"); // Target the 'price' field input
  if (priceInput) {
    priceInput.addEventListener("input", function (e) {
      // Remove commas first, then format the value with commas
      const value = priceInput.value.replace(/,/g, "");
      if (!isNaN(value)) {
        priceInput.value = Number(value).toLocaleString("en-US");
      }
    });

    // Ensure the commas are removed before submitting the form
    priceInput.form.addEventListener("submit", function () {
      priceInput.value = priceInput.value.replace(/,/g, "");
    });
  }
});
