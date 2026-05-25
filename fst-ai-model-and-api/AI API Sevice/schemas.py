from pydantic import BaseModel
from typing import List, Optional

class Item(BaseModel):
    name: str
    price: Optional[float] = 0.0 # Kasih default 0.0 biar gak error kalau harga gak kebaca
    category: Optional[str] = "Lainnya"

class OCRResponse(BaseModel):
    store_name: Optional[str] = "Tidak Diketahui"
    date: Optional[str] = None
    total_amount: Optional[float] = 0.0 # Optional biar gak error 500 kalau Llama gagal hitung total
    items: List[Item] = [] # Default list kosong
    category_summary: Optional[str] = None
    confidence_score: Optional[float] = 0.0