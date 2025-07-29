const express = require('express');
const fs = require('fs-extra');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Ruta al archivo JSON que guarda los productos
const DATA_FILE = path.join(__dirname, 'productos.json');

// Middleware para parsear JSON
app.use(express.json());

// Servir archivos estáticos desde la carpeta public
app.use(express.static(path.join(__dirname, 'public')));

// Ruta raíz que entrega index.html directamente (opcional si usas archivos estáticos bien)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// === Funciones para leer y guardar productos ===

async function leerProductos() {
  try {
    const data = await fs.readFile(DATA_FILE, 'utf-8');
    return JSON.parse(data);
  } catch {
    return [];
  }
}

async function guardarProductos(productos) {
  await fs.writeFile(DATA_FILE, JSON.stringify(productos, null, 2));
}

// === Rutas del API REST ===

// Añadir o sobrescribir producto
app.post('/api/productos', async (req, res) => {
  const { id, nombre, precio } = req.body;

  if (!id || !nombre || precio === undefined) {
    return res.status(400).json({ error: 'Faltan campos: id, nombre o precio' });
  }

  const productos = await leerProductos();
  const index = productos.findIndex(p => p.id === id);

  if (index !== -1) {
    // Ya existe → sobrescribir
    productos[index] = { id, nombre, precio };
  } else {
    // Nuevo producto
    productos.push({ id, nombre, precio });
  }

  await guardarProductos(productos);
  res.status(201).json({ mensaje: 'Producto guardado correctamente' });
});


// 🔍 Obtener precio por ID
app.get('/api/productos/:id/precio', async (req, res) => {
  const { id } = req.params;
  const productos = await leerProductos();
  const producto = productos.find(p => p.id === id);

  if (!producto) {
    return res.status(404).json({ error: 'Producto no encontrado' });
  }

  res.json({ id: producto.id, nombre: producto.nombre, precio: producto.precio });
});

// ✏️ Modificar un producto
app.put('/api/productos/:id', async (req, res) => {
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
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
