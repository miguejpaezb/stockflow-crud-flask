// =========================
// ELEMENTOS DEL DOM
// =========================

const openModalButton = document.getElementById("open-stock-modal");
const closeModalButton = document.getElementById("close-stock-modal");
const stockModal = document.getElementById("stock-modal");

// =========================
// ABRIR MODAL
// =========================

openModalButton.addEventListener("click", (event) => {
  event.preventDefault();
  stockModal.classList.add("show");
});

// =========================
// CERRAR MODAL
// =========================

closeModalButton.addEventListener("click", () => {
  stockModal.classList.remove("show");
});