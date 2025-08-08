from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# ✅ Modelos
class Producto(BaseModel):
    nombre: str
    precio: float
    categoria: str  # Ej: "alimento", "juguetes", "accesorios"
    stock: int

class ProductoParcial(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    categoria: Optional[str] = None
    stock: Optional[int] = None

# ✅ Base de datos simulada con productos reales de mascotas
productos = [
    {"id": 1, "nombre": "Croquetas premium para perro", "precio": 42.5, "categoria": "alimento", "stock": 100},
    {"id": 2, "nombre": "Rascador para gatos", "precio": 35.0, "categoria": "accesorios", "stock": 25},
    {"id": 3, "nombre": "Juguete interactivo para gato", "precio": 18.0, "categoria": "juguetes", "stock": 40},
    {"id": 4, "nombre": "Comedero automático", "precio": 55.9, "categoria": "accesorios", "stock": 15},
    {"id": 5, "nombre": "Alpiste para canarios", "precio": 9.5, "categoria": "alimento", "stock": 60},
    {"id": 6, "nombre": "Collar luminoso para perro", "precio": 12.75, "categoria": "accesorios", "stock": 35},
    {"id": 7, "nombre": "Pelota de goma para perro", "precio": 6.0, "categoria": "juguetes", "stock": 50},
    {"id": 8, "nombre": "Arena sanitaria para gatos", "precio": 14.3, "categoria": "alimento", "stock": 45},
]

# ✅ GET: Listar productos, con filtros opcionales por nombre y categoría
@app.get("/productos/")
def obtener_productos(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría")
):
    resultado = productos
    if nombre:
        resultado = [p for p in resultado if nombre.lower() in p["nombre"].lower()]
    if categoria:
        resultado = [p for p in resultado if categoria.lower() == p["categoria"].lower()]
    return {"productos": resultado}

# ✅ GET: Obtener producto por ID
@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# ✅ POST: Crear nuevo producto
@app.post("/productos/", status_code=201)
def crear_producto(producto: Producto):
    nuevo_id = max((p["id"] for p in productos), default=0) + 1
    nuevo_producto = {
        "id": nuevo_id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "categoria": producto.categoria,
        "stock": producto.stock
    }
    productos.append(nuevo_producto)
    return {"mensaje": "Producto creado correctamente", "producto": nuevo_producto}


# ✅ PUT: Actualizar todos los campos de un producto
@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto: Producto):
    for p in productos:
        if p["id"] == producto_id:
            p.update({
                "nombre": producto.nombre,
                "precio": producto.precio,
                "categoria": producto.categoria,
                "stock": producto.stock
            })
            return {"mensaje": "Producto actualizado", "producto": p}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# ✅ PATCH: Actualizar parcialmente un producto
@app.patch("/productos/{producto_id}")
def actualizar_parcial(producto_id: int, datos: ProductoParcial):
    for p in productos:
        if p["id"] == producto_id:
            if datos.nombre is not None:
                p["nombre"] = datos.nombre
            if datos.precio is not None:
                p["precio"] = datos.precio
            if datos.categoria is not None:
                p["categoria"] = datos.categoria
            if datos.stock is not None:
                p["stock"] = datos.stock
            return {"mensaje": "Producto actualizado parcialmente", "producto": p}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# ✅ DELETE: Eliminar producto
@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            productos.remove(producto)
            return {"mensaje": "Producto eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")
