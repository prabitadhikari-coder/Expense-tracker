const form = document.getElementById("expense-form");
const list = document.getElementById("expense-list");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const category = document.getElementById("category").value;
  const amount = document.getElementById("amount").value;

  const item = document.createElement("li");
  item.textContent = `${category}: $${amount}`;
  list.appendChild(item);

  form.reset();
});
