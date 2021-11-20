# main.py for katalog modul

# import Library
import json
from fastapi import FastAPI, Body, Depends
from app.model import UserLoginSchema
from app.auth.auth_handler import signJWT
from app.auth.auth_bearer import JWTBearer

# membuka file admin.json dan produk.json
with open("admin.json", "r") as read_file: 
    data_user = json.load(read_file)

with open("produk.json", "r") as read_file: 
    data = json.load(read_file)

app = FastAPI() 

# root
@app.get('/')
def root():
    return{'Deploy your previous APIs in a public cloud service. Explain the steps and provide the API URLs to access. '}


# menampilkan semua data dalam produk.json
@app.get('/produk', dependencies=[Depends(JWTBearer())], tags=['CRUD Katalog Produk']) 
async def read_all_produk() -> dict: 
    return data
 

# membaca 1 data dalam produk.json
@app.get('/produk/{item_id}', dependencies=[Depends(JWTBearer())], tags=['CRUD Katalog Produk'])
async def read_produk(item_id: int) -> dict:
    
    if item_id > len(data['produk']):
        return {
            "error": "Tidak ada menu dengan ID tersebut. Permintaan gagal diproses."
        }
    for product_item in data['produk']:
        if product_item["idProduk"] == (item_id):
            return product_item

# menambahkan katalog produk
@app.post('/produk/{name}', dependencies=[Depends(JWTBearer())], tags=['CRUD Katalog Produk'])
async def Add_produk(name: str, harga: str , quantity: int, berat: str, deskripsi:str) ->dict :
    for produk_item in data['produk']:
        if produk_item['namaProduk'] == name:
            return {"error":"Terjadi duplikasi nama produk. Permintaan gagal diproses."}
    else :
        id = 1
        if(len(data['produk']) > 0):
            id = data['produk'][len(data['produk']) - 1]['idProduk'] + 1
        new_data={'idProduk':id,'namaProduk':name, "harga": harga, "quantity": quantity , "berat": berat, "deskripsi": deskripsi}
        data['produk'].append(dict(new_data))
    
        #melakukan rewrite
        read_file.close()
        with open("produk.json","w") as write_file:
            json.dump(data,write_file,indent=4)
        write_file.close()
        return {
            "message": "Produk berhasil ditambahkan."
        }


# mengupdate katalog produk
@app.put('/produk/{item_id}', dependencies=[Depends(JWTBearer())], tags=['CRUD Katalog Produk'])
async def update_produk(item_id: int, name: str, harga: str , quantity: int, berat: str, deskripsi:str): 
    for produk_item in data['produk']:
        if produk_item['idProduk'] == item_id:
            produk_item['namaProduk']= name
            produk_item['harga']= harga
            produk_item['quantity']= quantity
            produk_item['berat']= berat
            produk_item['deskripsi']= deskripsi
            read_file.close()
            with open("produk.json","w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()
            return{"message":"Data telah berhasil disunting."}
    else :
        return{"error":"Data tidak ditemukan. Permintaan gagal diproses."}

# menghapus salah satu produk
@app.delete('/produk/{item_id}', dependencies=[Depends(JWTBearer())], tags=['CRUD Katalog Produk'])
async def delete_produk(name: str): 
    for produk_item in data['produk']:
        if produk_item['namaProduk'] == name:
               # id = data['produk'][len(data['produk'])-1]['idProduk']+1
                remove_data={'idProduk':produk_item['idProduk'] ,'namaProduk':name, "harga": produk_item['harga'] , "quantity": produk_item['quantity']  , "berat": produk_item['berat'] , "deskripsi": produk_item['deskripsi'] }
                data['produk'].remove(dict(remove_data))
                # rewrite menu.json
                read_file.close()
                with open("produk.json","w") as write_file:
                    json.dump(data,write_file,indent=4)
                write_file.close()
                return{"message":"Data berhasil dihapus"}
        else :
            return {"error":"Data tidak ditemukan. Permintaan gagal diproses."}

# Mengecek kesesuaian data login
def check_user(data: UserLoginSchema):
    for user in data_user['admin']:
        if user["username"] == data.username and user["password"] == data.password:
            return True
    return False

# Melakukan autentikasi dan return pesan
@app.post("/user/login", tags=["User"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.username)
    return {
        "error": "Username atau password salah. Permintaan login gagal diproses."
    }