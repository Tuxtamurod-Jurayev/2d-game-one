# 2D Game Development Series — 12 Projects Roadmap

Ushbu repozitoriy 12 ta ketma-ket murakkablashib boruvchi 2D o‘yin loyihalarini o‘z ichiga oladi.

## 🕹️ 01-Loyiha: Pixel Runner (Subway Heroes & Multi-Stage Edition)

Roadmap'dagi 1-loyiha — **Pixel Runner** Subway Surfers qahramonlari (Jake, Tricky, Fresh, Yutani) tanlovi, ikki bosqichli sakrash (Double Jump), dinamik bosqichlar va yangilangan shahar manzarasi bilan yangilandi.

### ✨ Yangilangan va Optimallashtirilgan Xususiyatlar:
* **4 ta Tanlanadigan Subway Qahramonlari:**
  * 🧢 **JAKE:** Orqaga kiyilgan oq-qizil kepka, jinsi jilet, oq xudi va ko'k jinsi shim.
  * 🎀 **TRICKY:** Qizil bini bosh kiyimi, sarg'ish pigtail kokillari, qora ko'zoynak, oq top va keng 90-yillar jinsi shimi.
  * 🎵 **FRESH:** Baland klassik flat-top soch turmagi, katta qora ko'zoynak, yashil mayka, qizil shortik va chiziqli uzun paypoqlar.
  * 👽 **YUTANI:** Gigant ko'zli yashil o'zga sayyoralik kombinezoni (alien onesie), binafsha soch tugunlari va 4 ta qo'li bilan!
  * **Tanlash boshqaruvi:** Bosh menyuda `Q` / `E` (yoki Chap / O'ng tugma) orqali personajlarni tanlash mumkin.
* **Ikki Bosqichli Baland Sakrash (Double Jump):**
  * `SPACE` yoki `W` 1-marta bosilganda yerdan sakraydi.
  * Havodalik paytida 2-marta bosilganda **Double Jump** ishga tushadi: qahramon havoda akrobatik 360° salto (somersault) aylanib, yanada balandroqqa ko'tariladi!
  * Personajning aksent rangidagi zarba to'lqini (shockwave ring) va ovoz effekti.
* **Chiroyli Multi-Layer Orqa Fon (Gorgeous Cityscape):**
  * Yumshoq nurlanuvchi Kiber-Oy / Quyosh va uning atmosferaviy nurlari.
  * Havoda suzuvchi volumetrik bulutlar.
  * Bino tomlarida yonib turuvchi neon bannerlar (`SUBWAY`, `RUN`, `CYBER`, `NEON`).
  * Ufq bo'ylab harakatlanuvchi relslar va temir yo'l shpallari (sleepers).
  * Mutlaqo miltillamaydigan, statik va realistik deraza chiroqlari.
* **4 Bosqichli Dinamik O'yin (Multi-Stage):**
  * **1-bosqich: Cyber Dawn (0 - 1200):** Moviy neon ufq.
  * **2-bosqich: Sunset Metropolis (1200 - 3000):** Oltin quyosh botishi.
  * **3-bosqich: Neon Nightfall (3000 - 5500):** Qizg'ish neon shahar.
  * **4-bosqich: Apex Overdrive (5500+):** Giper-yashil tezyurar rejim.
* **Boshqaruv (Controls):**
  * `Q` / `E` yoki `A` / `D`: Qahramonni almashtirish (Menyuda).
  * `SPACE` / `UP` / `W`: Sakrash (Havoda 2x bosilsa — Double Jump).
  * `DOWN` / `S`: Sirpanish (Slide).
  * `ESC`: Pauza / Davom ettirish.
* **HTML5 Versiya:** Brauzerda to‘liq 4 ta qahramon, double jump va yangi fon bilan o‘ynash uchun `index.html`.

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
