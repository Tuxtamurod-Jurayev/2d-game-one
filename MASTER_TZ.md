# 12 ta 2D O'yin Loyihasi — Master Texnik Topshiriq (TZ)

## 1. Umumiy konsept va maqsad

Ushbu dastur 12 ta ketma-ket murakkablashib boruvchi 2D o‘yin loyihasidan iborat amaliy o‘quv va ishlab chiqish tizimidir. Maqsad — oddiy 2D mexanikalardan tortib, murakkab AI, protsedurali generatsiya va server-avtoritar multiplayer arxitekturasigacha bo‘lgan to‘liq GameDev siklini (GDD → Prototype → Production → QA → Release) o‘zlashtirish.

* **Asosiy dvigatel (Engine):** Godot 4.x (yoki Unity 2D)
* **Arxitektura tamoyili:** Component-based / Modular Scene Architecture (Autoload/Singleton menedjerlar bilan)
* **Nazorat tizimi:** Git (Feature-branch workflow)

---

## 2. Loyihalar matritsasi (12 bosqichli Roadmap)

Loyihalar qat’iy ketma-ketlikda bajariladi. Keyingi loyihaga o‘tish uchun joriy loyiha MVP qabul mezonlaridan to‘liq o‘tishi shart.

| # | Loyiha nomi | Asosiy texnik fokus va o‘zlashtiriladigan ko‘nikma | Talab etiladigan maxsus tizimlar |
|---|---|---|---|
| **01** | **Pixel Runner** | 2D scene, input, collision, spawn va bazaviy UI | Level/Scene Manager |
| **02** | **Dungeon Escape** | Platformer physics, TileMap, level design va puzzle | Camera System, Level Manager |
| **03** | **Neon Breaker** | 2D physics, bounce, power-up va level data | Level/Scene Manager |
| **04** | **Shadow Tactics 2D** | AI state machine, raycast, stealth va mission logic | AI State Machine |
| **05** | **Farm & Craft 2D** | Simulation, inventory, crafting, economy va save | Inventory/Item DB |
| **06** | **Rogue Cells** | Procedural generation, combat, loot va meta progression | AI State Machine, Inventory, ProcGen |
| **07** | **Tower Defense: Last Grid** | Pathfinding, target selection, wave va strategy balance | AI/Wave Manager, Grid System |
| **08** | **Chrono Shift** | State history, rewind, deterministic gameplay va puzzle | Command/State History System |
| **09** | **Arena Clash 2D** | Networking, server authority, matchmaking va sync | Camera System, Networking |
| **10** | **Metro Manager 2D** | Graph algorithms, simulation, pathfinding va economy | Graph/Pathfinding System |
| **11** | **Echoes of the Forest** | World design, ability gating, boss AI va narrative | Camera System, AI State Machine |
| **12** | **Mythic Realms** *(Capstone)* | Procedural sandbox, multiplayer persistence, server arch. | Inventory, ProcGen, Server Save, Networking |

> **12-loyiha (Mythic Realms) uchun maxsus qabul mezoni:** Oldingi 11 loyiha yakunlangach boshlanadi. World state serverda saqlanishi, item duplikatsiyasi (dupe) server tomonidan bloklanishi, uzilishdan (disconnect) keyin progress tiklanishi hamda multiplayer harakat/jang to‘liq sinxron ishlashi shart.

---

## 3. Yagona loyiha arxitekturasi (Godot Standarti)

Barcha 12 ta loyiha yagona papka va kod tuzilmasi standartiga bo‘ysunadi. Bitta katta skriptga barcha mantiqni yozish (God Object) qat’iyan man etiladi.

```text
game-project/
├── project.godot
├── scenes/          # Barcha .tscn fayllar (main, menus, levels, player, enemies, objects, ui)
├── scripts/         # Barcha .gd fayllar
│   ├── managers/    # Autoload/Singleton (GameState, Audio, Input, Save, Network)
│   ├── systems/     # Qayta ishlatiluvchi tizimlar (Camera, Inventory, ProcGen, StateMachine)
│   ├── gameplay/    # O'yin mexanikalari va obyekt kontrollerlari
│   ├── ai/          # Dushman va NPC xulq-atvori
│   └── data/        # Custom Resource klasslar va ma'lumot strukturalari
├── assets/          # Sprites, tilesets, animations, backgrounds, audio (music/sfx), fonts, ui
├── data/            # JSON/Resource fayllar (levels, items, enemies, quests)
├── saves/           # Lokal test save fayllari (.gitignore ga qo'shiladi)
├── tests/           # Unit va integratsion test sahnalari
├── docs/            # GDD.md, controls.md, changelog.md
├── export/          # Yakuniy build fayllari (.gitignore ga qo'shiladi)
└── README.md
```

---

## 4. Majburiy yadro tizimlari (Core Systems Spec)

### Barcha o‘yinlarda bo‘lishi shart bo‘lgan bazaviy tizimlar (Core Baseline):
* **Game State Manager:** Menu, Playing, Paused, Victory, Game Over holatlarini markazlashgan holda boshqarish.
* **Input Manager:** Klaviatura, sichqoncha, gamepad va mobil touch boshqaruvini abstraksiya qilish.
* **Audio Manager:** Music va SFX kanallari (AudioBus), ovozni o‘chirish (mute) va balandlikni sozlash.
* **Save/Load System:** Progress, sozlamalar, rekordlar va inventarni lokal (multiplayerda esa serverda) xavfsiz saqlash.

### Loyiha turiga qarab qo‘shiladigan modullar:
* **Camera System:** Follow, chegaralar (limits), screen shake, zoom va smooth transition.
* **Level/Scene Manager:** Sahnalarni asinxron yuklash, qayta ishga tushirish va o‘tish effektlari.
* **AI State Machine:** Patrol, Chase, Attack, Search, Flee holatlari va ular orasidagi o‘tish mantiqi.
* **Inventory/Item DB:** Item ma’lumotlar bazasi, stack, equipment va crafting tizimi.
* **Procedural Generator:** Seed asosida xarita, xona, resurs va eventlarni generatsiya qilish.
* **Networking Module:** Lobby, Server Authority, State Synchronization, Reconnect va Lag Compensation.

---

## 5. Ishlab chiqish sikli (10 bosqichli Pipeline)

Har bir o‘yin quyidagi qat’iy ketma-ketlikda ishlab chiqiladi:

1. **GDD (Game Design Document):** O‘yin maqsadi, Core Loop, boshqaruv sxemasi, mexanikalar, yutish/yutqazish shartlari va qiyinlik jadvalini (`docs/GDD.md`) yozish.
2. **Pre-production:** Reference, wireframe, kerakli assetlar ro‘yxati, texnik risklar va MVP chegarasini (scope) belgilash.
3. **Prototype (Greybox):** Grafikaga chalg‘imasdan eng muhim 1–2 mexanikani oddiy shakllarda yaratish va "game feel"ni tekshirish.
4. **Core Gameplay:** Player controller, fizika/collision, kamera, dushman/obyekt interaksiyasi va to‘liq gameplay loopni (Boshlash → O‘ynash → Maqsad/Yutqazish → Natija → Qayta boshlash) yig‘ish.
5. **Content Production:** Level, xarita, dushman turlari, itemlar, missiya va dialoglarni yaratish.
6. **UI/UX:** Main Menu, HUD, Pause, Settings, Tutorial, Game Over, Victory va Accessibility ekranlarini ulash.
7. **Art & Audio Integration:** Sprite, tileset, animatsiya, VFX, fon musiqasi va SFX larni yagona nomlash standarti asosida integratsiya qilish.
8. **Save & Progression:** Checkpoint, unlock, rekordlar va inventarni saqlash/yuklash tizimini ulash.
9. **QA & Balance:** Chek-list asosida testlash, buglarni tuzatish va o‘yin balansini sozlash.
10. **Build & Release:** Export preset sozlash, icon/splash screen qo‘shish, hujjatlarni yakunlash va toza build chiqarish.

---

## 6. Jarayon qoidalari (Engineering Rules)

1. **Ketma-ketlik:** Bir vaqtda faqat bitta loyiha ishlanadi. MVP qabul mezonidan o‘tmaguncha keyingisiga o‘tilmaydi.
2. **Hujjat birlamchiligi:** Kod yozishdan oldin GDD va boshqaruv sxemasi tasdiqlanadi.
3. **Modullilik:** Har bir mexanika alohida mustaqil sahna (Scene) yoki skript moduli sifatida yoziladi.
4. **Git intizomi:** Har bir mantiqiy o‘zgarish alohida commit qilinadi; katta tizimlar alohida `feature/` branchda ishlanadi.
5. **Uzluksiz testlash (Continuous QA):** Har bir tizim yoki level qo‘shilishi bilan darhol test qilinadi; xatolarni loyiha oxiriga yig‘ib qo‘yish taqiqlanadi.
6. **Multiplayer qoidasi:** Onlayn o‘yinlarda (09 va 12-loyihalar) rivojlantirish 3 bosqichda boradi: *Offline Gameplay → Local Multiplayer → Online/Dedicated Server Multiplayer*.

---

## 7. QA Testlash chek-listi va Topshirish (DoD)

### Har bir reliz oldidan tekshiriladigan QA chek-listi:
* Menyudan o‘yinga kirish, Pause, Resume va Main Menuga qaytish xatosiz ishlaydi.
* Victory va Game Over ekranlari barcha belgilangan shartlarda to‘g‘ri chaqiriladi.
* Collision, trigger, hitbox/hurtbox va obyektlar interaksiyasi aniq ishlaydi.
* O‘yinchi xaritadan tushib ketishi (out of bounds), devorga tiqilib qolishi yoki softlock holatlari yo‘q.
* O‘yinni yopib ochganda Save/Load barcha progress, item va sozlamalarni to‘liq tiklaydi.
* Audio sozlamalari (Mute, Volume) sahna almashganda yoki pauzada buzilmaydi.
* Turli ekran o‘lchamlari (Aspect Ratio) va FPS o‘zgarishlarida UI va fizika buzilmaydi (mobil bo‘lsa — touch va safe area ishlaydi).
* *(Multiplayer uchun)* Yuqori ping (latency), uzilish (disconnect/reconnect), server restart va noto‘g‘ri/buzilgan client paketlari (anti-cheat/validation) tekshirilgan.
* Yakuniy build boshqa toza qurilmada `README.md` ko‘rsatmasi asosida muammosiz ishga tushadi.

### Yakuniy topshiriladigan artefaktlar (Deliverables):
1. **GitHub Repository:** Toza source code, `.gitignore` sozlangan.
2. **Hujjatlar (`/docs` va `README.md`):** GDD, boshqaruv sxemasi, ishlatilgan assetlar va ularning litsenziyalari ro‘yxati, bugfix changelog, engine versiyasi va build ko‘rsatmasi.
3. **Backend (09 va 12-loyihalar uchun):** Server source code, DB sxemasi, deploy skriptlari va tarmoq/API hujjatlari.
4. **Executable Build & Media:** Belgilangan platforma uchun tayyor o‘yin fayli hamda to‘liq gameplay loop aks etgan demo video.

---

## 8. Baholash mezonlari (KPI)

* **Gameplay va mexanika (25%):** O‘yin to‘liq o‘ynaladi, boshqaruv (controls) sezgir va barcha mexanikalar xatosiz ishlaydi.
* **Level va kontent dizayni (15%):** Bosqichlarning murakkablashuv balansi va kontent sifati.
* **Kod arxitekturasi (15%):** Modullilik, DRY tamoyili, papka va skriptlarning standartga mosligi.
* **UI/UX va Audio-vizual sifat (15%):** Interfeys qulayligi, animatsiya, VFX va ovoz uyg‘unligi.
* **Save va Progression (10%):** Ma’lumotlarni saqlash va yuklash tizimining ishonchliligi.
* **QA va Performance (10%):** FPS barqarorligi, turli ekranlarga moslashuv va buglarning yo‘qligi.
* **Hujjatlashtirish va Release (10%):** GDD, README, Git tarixi, tayyor build va demo video sifati.
