const express = require('express');
const fs = require('fs-extra');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, 'productos.json');

app.use(express.json());

// Leer todos los productos
async function leerProductos() {
  try {
    const data = await fs.readFile(DATA_FILE, 'utf-8');
    return JSON.parse(data);
  } catch {
    return [];
  }
}

// Guardar productos
async function guardarProductos(productos) {
  await fs.writeFile(DATA_FILE, JSON.stringify(productos, null, 2));
}

// ➕ Añadir un producto
app.post('/productos', async (req, res) => {
  const { id, nombre, precio } = req.body;
  if (!id || !nombre || !precio) {
    return res.status(400).json({ error: 'Faltan campos obligatorios' });
  }

  const productos = await leerProductos();
  if (productos.find(p => p.id === id)) {
    return res.status(409).json({ error: 'Producto ya existe' });
  }

  productos.push({ id, nombre, precio });
  await guardarProductos(productos);
  res.status(201).json({ mensaje: 'Producto añadido' });
});

// 🔍 Consultar el precio de un producto por ID
app.get('/productos/:id/precio', async (req, res) => {
  const { id } = req.params;
  const productos = await leerProductos();
  const producto = productos.find(p => p.id === id);

  if (!producto) {
    return res.status(404).json({ error: 'Producto no encontrado' });
  }

  res.json({ id: producto.id, nombre: producto.nombre, precio: producto.precio });
});

// ✏️ Modificar un producto
app.put('/productos/:id', async (req, res) => {
  const { id } = req.params;
  const { nombre, precio } = req.body;

  const productos = await leerProductos();
  const index = productos.findIndex(p => p.id === id);

  if (index === -1) {
    return res.status(404).json({ error: 'Producto no encontrado' });
  }

  if (nombre !== undefined) productos[index].nombre = nombre;
  if (precio !== undefined) productos[index].precio = precio;

  await guardarProductos(productos);
  res.json({ mensaje: 'Producto actualizado' });
});

// 🏁 Iniciar servidor
app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});
