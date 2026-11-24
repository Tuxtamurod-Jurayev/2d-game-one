# 2D Game Development Series — 12 Projects Roadmap

Ushbu repozitoriy 12 ta ketma-ket murakkablashib boruvchi 2D o‘yin loyihalarini o‘z ichiga oladi.

## 🕹️ 01-Loyiha: Pixel Runner (Multi-Stage Humanoid Edition)

Roadmap'dagi 1-loyiha — **Pixel Runner** zamonaviy inson qahramoni, ikki bosqichli sakrash (Double Jump) va dinamik bosqichlar (Multi-Stage) bilan yangilandi.

### ✨ Yangilangan va Optimallashtirilgan Xususiyatlar:
* **Ikki Bosqichli Baland Sakrash (Double Jump):**
  * `SPACE` yoki `W` / `UP` tugmasi 1-marta bosilganda yerdan sakraydi.
  * Havodalik paytida 2-marta bosilganda **Double Jump** ishga tushadi: qahramon havoda akrobatik 360° salto (somersault) aylanib, yanada balandroqqa ko'tariladi!
  * Oyoq ostida energiyali zarba to'lqini (shockwave ring) va sintezlangan maxsus double-jump ovoz effekti.
  * Tugmani tez qo'yib yuborish orqali balandlikni boshqarish (variable jump height).
* **Dinamik Bosqichli Tizim (Multi-Stage Progression):**
  * **1-bosqich: Cyber Dawn (0 - 1200):** Moviy neon ufq, binafsha osmon va sokin shahar.
  * **2-bosqich: Sunset Metropolis (1200 - 3000):** Oltin/olovrang quyosh botishi, qizg'ish grid va tezlashgan sur'at.
  * **3-bosqich: Neon Nightfall (3000 - 5500):** To'q binafsha va yorqin fuksiya neon nurlari.
  * **4-bosqich: Apex Overdrive (5500+):** Giper-yashil kiber tezyurar rejim.
* **Bosqichga Mos Dinamik O'zgaruvchan UI:**
  * Har bir bosqichda barcha HUD nishonlari va hoshiyalari o'sha bosqich ranglariga moslashadi.
  * Yangi bosqichga yetganda ekranda animatsiyali daraja burchagi (Stage Banner) va tantanali ovoz yangraydi.
  * Yangi Stage indikatori va bosqich to'lish progress-bari.
* **Barqaror Shahar Chiroqlari (Zero-Flicker Windows):**
  * Binolar chiroqlarining ochib-yonishi va o'chib qolishi to'liq bartaraf etildi. Barcha deraza yoritgichlari binolarga nisbatan statik va realistik tarzda saqlanadi.
* **Humanoid Personaj & Harakat:**
  * O‘yinchi to‘liq odam qiyofasida (bosh, shamolda tebranuvchi soch, sport kiber-jaketi, ikki bo'g'inli tizza va tirsak kinematikasi).
  * O'yinchining yerga tushayotgan soyasi (altitude shadow) balandlikka qarab o'zgaradi.
  * Sirpanish (Slide): pastki qavatga tushish, dronlar ostidan xavfsiz sirpanib o‘tish va uchqunlar.
* **Physics & Controls:**
  * `SPACE` / `UP` / `W`: Sakrash (havoda yana bosa — Double Jump).
  * `DOWN` / `S`: Sirpanish / Egilish.
  * `ESC`: Pauza / Davom ettirish.
* **HTML5 Versiya:** Brauzerda to‘liq inson qiyofasi, double jump va bosqichlar bilan o‘ynash uchun `index.html`.

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
