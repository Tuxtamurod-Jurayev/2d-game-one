# 2D Game Development Series — 12 Projects Roadmap

Ushbu repozitoriy 12 ta ketma-ket murakkablashib boruvchi 2D o‘yin loyihalarini o‘z ichiga oladi.

## 🕹️ 01-Loyiha: Pixel Runner (Modern Humanoid Edition)

Roadmap'dagi 1-loyiha — **Pixel Runner** zamonaviy inson qahramoni va shaffof (glassmorphism) interfeysi bilan yangilandi.

### ✨ Yangilangan va Optimallashtirilgan Xususiyatlar:
* **Humanoid Personaj & Harakat:**
  * O‘yinchi to‘liq odam qiyofasiga (bosh, soch, yuz, kiber-kostyum/jaket, oyoq va qo‘llar) o‘tkazildi.
  * Odam anatomiyasiga mos yugurish sikli (oyoqlar bo‘g‘inlari, tizzalar bukilishi, qo‘llarning qadamga teskari fazada tebranishi).
  * Dinamik sakrash (havoda oyoqlar yig‘ilishi, shamolda soch tebranishi, yerga tushganda chang effekti).
  * Zamonaviy sirpanish/egilish (Slide: pastki qavatga tushish, dronlar ostidan xavfsiz sirpanib o‘tish va uchqunlar).
* **Zamonaviy Qo‘lda Chizilgan Ikonalar (No AI):**
  * 🏆 **Trophy Icon:** Rekord uchun oltin kubok nishoni.
  * 🪙 **Coin Icon:** Oltin tangalar shaffof pill-panellar ichida.
  * ⚡ **Speed Icon:** O‘yin tezligi dinamik indikatori.
  * 🏃 **Runner Icon:** Chopuvchi inson silueti.
  * ⏸️ **Pause Icon:** Minimalist pauza belgisi.
* **Minimalist Glassmorphism UI:**
  * Quti-quti eski dizayndan voz kechilib, zamonaviy shaffof xiralashtirilgan (frosted glass) panellar va nozik neon hoshiyalar qo‘llandi.
  * Oltin tanga yig‘ilganda uchqunli chaqnash effektlari.
* **Physics & Controls:**
  * `SPACE` yoki `UP` / `W`: Sakrash.
  * `DOWN` yoki `S`: Sirpanish / Egilish.
  * `ESC`: Pauza / Davom ettirish.
* **8-bit Sintezlangan Ovoz:** Tashqi audio fayllarsiz toza matematik to‘lqinlar.
* **HTML5 Versiya:** Brauzerda to‘liq inson qiyofasi va yangi UI bilan o‘ynash uchun `index.html`.

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
