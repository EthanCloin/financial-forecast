/**
 * finds all input elements with a validationType attribute set to 'currency'
 */
console.log("we running");
  const currencyElements = document.querySelectorAll(
    "input[validationType='currency']"
  );
  console.log(currencyElements);
  for (const el of currencyElements) {
    el.addEventListener("input", (e) => {
      inputChar = e.data;
      if (isNaN(Number(inputChar)) && inputChar !== ".") {
        // e.preventDefault();
        console.log("bad fkn input");
        previousValue = el.value.slice(0, -1);
        el.value = previousValue;
      }
    });

    el.addEventListener("blur", (e) => {
      const value = parseFloat(el.value.replace(/[^0-9.]/g, "")) || 0;
      console.log(value);
      const formatter = new Intl.NumberFormat("en-us", {
        style: "currency",
        currency: "USD",
      });

      el.value = formatter.format(value);
    });

    el.addEventListener("keydown", (e) => {
      const isEnterKeypress = e.keyCode === 13;
      if (isEnterKeypress) e.preventDefault();
    });
  }