// =========================
// CONFIGURACIÓN BASE
// =========================

const API_BASE_URL = "http://localhost:5000/api";


// =========================
// PRODUCTOS — CRUD
// =========================

/**
 * GET /api/products
 * Obtiene todos los productos
 * @returns {Promise<Array>}
 */
async function getAllProducts() {
  const response = await fetch(`${API_BASE_URL}/products`);
  if (!response.ok) throw new Error("Error al obtener los productos");
  return await response.json();
}


/**
 * GET /api/products/:id
 * Obtiene un producto por ID
 * @param {number} id
 * @returns {Promise<Object>}
 */
async function getProductById(id) {
  const response = await fetch(`${API_BASE_URL}/products/${id}`);
  if (!response.ok) throw new Error("Producto no encontrado");
  return await response.json();
}


/**
 * POST /api/products
 * Crea un nuevo producto
 * @param {{ name: string, category: string, stock: number, minimum_stock: number, price: number }} productData
 * @returns {Promise<Object>}
 */
async function createProduct(productData) {
  const response = await fetch(`${API_BASE_URL}/products`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(productData),
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.error || "Error al crear el producto");
  }
  return await response.json();
}


/**
 * PUT /api/products/:id
 * Actualiza los datos de un producto
 * @param {number} id
 * @param {Object} productData — campos a actualizar
 * @returns {Promise<Object>}
 */
async function updateProduct(id, productData) {
  const response = await fetch(`${API_BASE_URL}/products/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(productData),
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.error || "Error al actualizar el producto");
  }
  return await response.json();
}


/**
 * PUT /api/products/:id/stock
 * Agrega unidades al stock de un producto (modal de stock)
 * @param {number} id
 * @param {number} amount — cantidad a sumar
 * @returns {Promise<Object>}
 */
async function addStock(id, amount) {
  const response = await fetch(`${API_BASE_URL}/products/${id}/stock`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount }),
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.error || "Error al agregar stock");
  }
  return await response.json();
}


/**
 * DELETE /api/products/:id
 * Elimina un producto por ID
 * @param {number} id
 * @returns {Promise<Object>}
 */
async function deleteProduct(id) {
  const response = await fetch(`${API_BASE_URL}/products/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.error || "Error al eliminar el producto");
  }
  return await response.json();
}


// =========================
// EXPORTS (para uso modular)
// =========================

// Si usas módulos ES6 en el frontend, descomenta esto:
// export { getAllProducts, getProductById, createProduct, updateProduct, addStock, deleteProduct };
