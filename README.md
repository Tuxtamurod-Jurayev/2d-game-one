# 2D Game Development Series — 12 Projects Roadmap

Ushbu repozitoriy 12 ta ketma-ket murakkablashib boruvchi 2D o‘yin loyihalarini o‘z ichiga oladi.

## 🕹️ 01-Loyiha: Pixel Runner

Roadmap'dagi 1-loyiha — **Pixel Runner** (Cyberpunk/Retro uslubidagi cheksiz yugurish va to‘siqlardan sakrash o‘yini).

### ✨ Xususiyatlari:
* **Physics & Controls:**
  * `SPACE` yoki `UP` / `W`: Sakrash (sakrash kuchi va dinamik havo fizikasi).
  * `DOWN` yoki `S`: Sirpanish / egilish (pastlab uchuvchi dronlar ostidan o‘tish).
  * `ESC`: O‘yinni pauza qilish.
* **Protsedurali to‘siqlar:** Kichik/katta yer to‘siqlari hamda havodan uchuvchi kiber-dronlar.
* **Bonus Tizimi:** Oltin tangalar (Coins) yig‘ish (+100 ball har bir tangaga).
* **Tezlik progressiyasi:** Masofa oshgan sari o‘yin tezligi silliq oshib boradi.
* **8-bit Sintezlangan Ovoz:** Hech qanday tashqi audio fayllarsiz, Python ichida avtomatik sintezlanadigan ovoz effektlari (sakrash, tanga olish, urilish, checkpoint).
* **Parallax Background:** Neon ufq chizig‘i, siluet binolar va yulduzli osmon.
* **Saqlash tizimi:** Eng yuqori rekord (`saves/highscore.json`) avtomatik saqlanadi.
* **HTML5 Versiya:** Brauzerda to‘g‘ridan-to‘g‘ri o‘ynash uchun `index.html` ham mavjud.

---

### 🚀 Kompyuterda ishga tushirish (Run):

1. **Python orqali ishga tushirish:**
```bash
pip install pygame
python main.py
```

2. **Brauzerda ishga tushirish:**
`index.html` faylini istalgan brauzerda (Chrome, Edge, Firefox) ochishingiz mumkin.

---

## 🗺️ 12 Loyihali Master Roadmap

1. **01 — Pixel Runner** (2D scene, input, collision, spawn, UI)
2. **02 — Dungeon Escape** (Platformer physics, TileMap, puzzle)
3. **03 — Neon Breaker** (2D physics, bounce, power-up)
4. **04 — Shadow Tactics 2D** (AI state machine, raycast, stealth)
5. **05 — Farm & Craft 2D** (Simulation, inventory, crafting, save)
6. **06 — Rogue Cells** (ProcGen, combat, meta progression)
7. **07 — Tower Defense: Last Grid** (Pathfinding, wave manager)
8. **08 — Chrono Shift** (State history, rewind, deterministic)
9. **09 — Arena Clash 2D** (Networking, server authority)
10. **10 — Metro Manager 2D** (Graph algorithms, simulation)
11. **11 — Echoes of the Forest** (Metroidvania, ability gating, boss AI)
12. **12 — Mythic Realms** *(Capstone)* (Procedural multiplayer sandbox, anti-dupe database)

Barcha texnik topshiriqlar va hujjatlar: [MASTER_TZ.md](MASTER_TZ.md) va [docs/](docs/) papkasida joylashgan.
