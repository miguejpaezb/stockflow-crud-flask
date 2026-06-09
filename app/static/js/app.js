// =========================
// ELEMENTOS DEL DOM
// =========================

const productForm = document.querySelector(".product-form");
const formTitle = document.querySelector(".form-title");
const productNameInput = document.getElementById("product-name");
const productCategoryInput = document.getElementById("product-category");
const productStockInput = document.getElementById("product-stock");
const minimumStockInput = document.getElementById("minimum-stock");
const productPriceInput = document.getElementById("product-price");
const searchInput = document.getElementById("search-input");
const tableBody = document.querySelector(".inventory-table tbody");
const stockModal = document.getElementById("stock-modal");
const stockAmountInput = document.getElementById("stock-amount");
const modalForm = document.querySelector(".modal-form");
const closeModalBtn = document.getElementById("close-stock-modal");
const resetBtn = document.querySelector('input[type="reset"]');

let editingProductId = null;
let currentStockProductId = null;
let allProducts = [];

// =========================
// RENDERIZAR TABLA
// =========================

function renderTable(products) {
  tableBody.innerHTML = "";

  if (products.length === 0) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 4;
    td.textContent = "No se encontraron productos";
    td.style.textAlign = "center";
    td.style.padding = "2rem";
    tr.appendChild(td);
    tableBody.appendChild(tr);
    return;
  }

  products.forEach(function (p) {
    const tr = document.createElement("tr");
    const priceFormatted = Number(p.price).toLocaleString("es-CO", {
      style: "currency",
      currency: "COP",
      minimumFractionDigits: 0,
    });

    tr.innerHTML =
      "<td>" + escapeHtml(p.name) + "</td>" +
      "<td>" + p.stock + "</td>" +
      "<td>" + priceFormatted + "</td>" +
      '<td class="actions-cell">' +
        '<a href="#" class="add-stock-link" data-id="' + p.id + '">Agregar</a>' +
        '<a href="#" class="edit-link" data-id="' + p.id + '">Editar</a>' +
        '<a href="#" class="delete-link" data-id="' + p.id + '">Eliminar</a>' +
      "</td>";

    tableBody.appendChild(tr);
  });

  document.querySelectorAll(".add-stock-link").forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      currentStockProductId = parseInt(link.dataset.id);
      stockModal.classList.add("show");
    });
  });

  document.querySelectorAll(".edit-link").forEach(function (link) {
    link.addEventListener("click", async function (e) {
      e.preventDefault();
      var id = parseInt(link.dataset.id);
      try {
        var product = await getProductById(id);
        editingProductId = id;
        formTitle.textContent = "Editar Producto";
        productNameInput.value = product.name;
        productCategoryInput.value = product.category;
        productStockInput.value = product.stock;
        minimumStockInput.value = product.minimum_stock;
        productPriceInput.value = product.price;
        productForm.querySelector('input[type="submit"]').value = "Actualizar";
      } catch (err) {
        alert("Error al cargar producto: " + err.message);
      }
    });
  });

  document.querySelectorAll(".delete-link").forEach(function (link) {
    link.addEventListener("click", async function (e) {
      e.preventDefault();
      if (!confirm("\u00bfEliminar este producto?")) return;
      var id = parseInt(link.dataset.id);
      try {
        await deleteProduct(id);
        await loadProducts();
      } catch (err) {
        alert("Error al eliminar: " + err.message);
      }
    });
  });
}

function escapeHtml(text) {
  var div = document.createElement("div");
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}

// =========================
// CARGAR PRODUCTOS
// =========================

async function loadProducts() {
  try {
    allProducts = await getAllProducts();
    renderTable(allProducts);
  } catch (err) {
    alert("Error al cargar productos: " + err.message);
  }
}

// =========================
// RESETEAR FORMULARIO
// =========================

function resetForm() {
  editingProductId = null;
  formTitle.textContent = "Agregar Nuevo Producto";
  productForm.reset();
  productForm.querySelector('input[type="submit"]').value = "Guardar";
}

// =========================
// ENVIAR FORMULARIO (CREAR / ACTUALIZAR)
// =========================

productForm.addEventListener("submit", async function (e) {
  e.preventDefault();

  var data = {
    name: productNameInput.value.trim(),
    category: productCategoryInput.value.trim(),
    stock: parseInt(productStockInput.value) || 0,
    minimum_stock: parseInt(minimumStockInput.value) || 1,
    price: parseFloat(productPriceInput.value) || 0,
  };

  try {
    if (editingProductId) {
      await updateProduct(editingProductId, data);
    } else {
      await createProduct(data);
    }
    resetForm();
    await loadProducts();
  } catch (err) {
    alert("Error: " + err.message);
  }
});

// =========================
// MODAL: ENVIAR STOCK
// =========================

modalForm.addEventListener("submit", async function (e) {
  e.preventDefault();
  var amount = parseInt(stockAmountInput.value);

  if (!amount || amount <= 0) {
    alert("Ingrese una cantidad v\u00e1lida");
    return;
  }

  try {
    await addStock(currentStockProductId, amount);
    stockModal.classList.remove("show");
    modalForm.reset();
    await loadProducts();
  } catch (err) {
    alert("Error: " + err.message);
  }
});

// =========================
// MODAL: CERRAR (click botón cerrar)
// =========================

closeModalBtn.addEventListener("click", function () {
  stockModal.classList.remove("show");
  modalForm.reset();
});

// =========================
// BÚSQUEDA
// =========================

searchInput.addEventListener("input", function () {
  var query = searchInput.value.toLowerCase();
  var filtered = allProducts.filter(function (p) {
    return p.name.toLowerCase().indexOf(query) !== -1;
  });
  renderTable(filtered);
});

// =========================
// BOTÓN LIMPIAR FORMULARIO
// =========================

resetBtn.addEventListener("click", resetForm);

// =========================
// INICIALIZAR AL CARGAR LA PÁGINA
// =========================

document.addEventListener("DOMContentLoaded", loadProducts);
