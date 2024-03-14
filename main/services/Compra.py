from main.repositories import CompraRepository

compra_repository = CompraRepository()

class CompraService:
    def obtener_compra_con_descuento(self, id):
        compra = compra_repository.find_one(id)
        
        #aqui podria ir la logica
        
        return compra
    def agregar_compra(self, compra):
        #agregar  logica antes de guardar en la base de datos
        compra = compra_repository.create(compra)
        return compra