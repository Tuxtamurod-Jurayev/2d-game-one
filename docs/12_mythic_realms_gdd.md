# Game Design Document (GDD) — Mythic Realms

> **Loyiha:** 12-Loyiha (Capstone)  
> **O‘yin nomi:** Mythic Realms  
> **Janr:** 2D Multiplayer Survival & Crafting Sandbox  
> **Platforma:** PC (Windows Desktop / Web HTML5)  
> **Arxitektura:** Server-Authoritative Dedicated Server + Web/Desktop Client  
> **Kamera:** 2D Top-down (Zoom va Screen Shake qo‘llab-quvvatlaydi)  

---

## 1. Asosiy o‘yin sikli (Core Gameplay Loop)

O‘yin jarayoni 4 bosqichli uzluksiz siklga asoslanadi:

```text
[1. Explore & Gather] ──► [2. Craft & Build] ──► [3. Survive & Defend] ──► [4. Progression & Conquer]
         ▲                                                                                 │
         └─────────────────────────────────────────────────────────────────────────────────┘
```

1. **Explore & Gather (Kashf qilish va yig‘ish):** O‘yinchilar dunyoni o‘rganadi, daraxt kesadi, tosh/ruda qaziydi, oziq-ovqat va noyob materiallarni yig‘adi.
2. **Craft & Build (Yasash va qurish):** Yig‘ilgan xomashyolardan dastgohlar (workbench, furnace), qurol-yarog‘, devorlar, eshiklar va mustahkam baza quriladi.
3. **Survive & Defend (Omon qolish va himoya):** Ochlikni qondirish, ekstremal iqlim (sovuq/issiq) ta’sirini kamaytirish, tunda paydo bo‘ladigan dushmanlar va davriy reydlardan bazani himoyalash.
4. **Progression & Conquer (Rivojlanish va yengish):** Yangi texnologik bosqichlarga (tier) o‘tish, g‘orlar tubiga tushish, global altarlarni faollashtirish va dunyo bosslarini birgalikda yengish.

---

## 2. Biomlar spetsifikatsiyasi (Kamida 3 ta)

Dunyoda seed asosida kamida 3 ta bir-biridan farq qiluvchi biom shakllanadi:

| Biom | Iqlim va Atrof-muhit | Asosiy resurslar | Maxsus mexanika |
|---|---|---|---|
| **Yashil O‘rmon (Forest)** | Mo‘tadil, boshlang‘ich xavfsiz zona. Daraxtzor va daryolar. | Wood, Stone, Fiber, Berries, Raw Meat. | Boshlang‘ich spawn hududi; xavf darajasi past. |
| **Qaqragan Sahro (Desert)** | Quruq, jazirama issiq. Kaktuslar va qum barxanlari. | Sand, Coal, Gold Ore, Cactus, Bone. | Suv tanqisligi (Water Flask talab etiladi), tezroq ochqash. |
| **Muzlik / Tundra (Snow)** | Sovuq qahraton, muz va qattiq jinslar. | Ice, Iron Ore, Hardwood, Leather. | Gipodermiya (sovuq qotish); olov (Campfire/Torch) yonida turmasa HP kamayadi. |

---

## 3. Dushmanlar va Bosslar (Bestiary)

### 3.1. Oddiy Dushmanlar
1. **Slime (Shilliqurt):**
   * *Biom:* Yashil O‘rmon (kunduz va kechasi).
   * *Harakat:* Sakrab-sakrab yaqinlashadi, yaqin masofadan kontakt zarba beradi.
   * *Drop:* Slime Gel (mash'ala va yelim uchun).
2. **Skeleton (Skelet):**
   * *Biom:* O‘rmon va Tundra (faqat tunda va g‘orlarda).
   * *Harakat:* Yoy bilan masofadan o‘q otadi, o‘yinchidan masofa saqlashga intiladi.
   * *Drop:* Bone, Arrow.
3. **Desert Scorpion (Sahro Chayoni):**
   * *Biom:* Qaqragan Sahro.
   * *Harakat:* Tezkor yuguradi, dumi bilan zaharli zarba beradi (DoT — vaqtinchalik zahar zarari).
   * *Drop:* Leather, Chitin, Poison Gland.
4. **Ice Wolf (Muz Bo‘risi):**
   * *Biom:* Muzlik/Tundra.
   * *Harakat:* Gala bo‘lib (pack AI) harakatlanadi, o‘yinchini o‘rab olishga harakat qiladi.
   * *Drop:* Leather, Raw Meat, Wolf Fang.

### 3.2. Dunyo Bosslari
1. **Golem of the Depths (Tosh Golem):**
   * *Joylashuvi:* Yer osti g‘orlarining eng pastki qavatidagi qadimiy zal.
   * *Xususiyatlari:* Juda yuqori HP va zirh.
   * *Fazalari:*
     * *1-Faza:* Og‘ir musht zarbalari va tosh otish.
     * *2-Faza (HP < 50%):* Erga zarba berib hududiy (AoE) silkinish to‘lqini hosil qiladi va shiplardan toshlar yog‘diradi.
   * *Mukofot:* Ancient Core, Gold Ingot, Tier 3 Crafting retseptlari.
2. **Shadow Dragon (Soya Ajdari — Yakuniy Boss):**
   * *Chaqirilishi:* Sahro va Tundra chegarasidagi maxsus qurbonlik altari orqali tunda chaqiriladi.
   * *Xususiyatlari:* Havoda uchadi, o‘yinchilar va qurilgan bazalarni nishonga oladi.
   * *Fazalari:*
     * *1-Faza:* Havodan olov/soya sharlari bilan bombardimon qilish va sho‘ng‘ish (dive attack).
     * *2-Faza (HP < 40%):* Yerga qo‘nib, skeletlar to‘lqinini chaqiradi va o‘yinchilar bazasidagi devorlarni buzib o‘tuvchi qora quyun chaqiradi.
   * *Mukofot:* Dragon Scale, Mythic Essence (O‘yinni g‘alaba bilan yakunlash artefakti).

---

## 4. Resurslar va Iqtisodiyot (30 ta Asosiy Item)

| ID | Nomi | Toifa | Max Stack | Durability | Qisqacha tavsif |
|---|---|---|---|---|---|
| `wood` | Wood | Xomashyo | 99 | — | Daraxtlardan olinadi; asosiy qurilish materiali |
| `stone` | Stone | Xomashyo | 99 | — | Tosh konlaridan olinadi |
| `iron_ore` | Iron Ore | Xomashyo | 99 | — | Yer ostidan qazib olinadi |
| `gold_ore` | Gold Ore | Xomashyo | 99 | — | Noyob kon |
| `coal` | Coal | Xomashyo | 99 | — | Pechda yoqilg‘i va mash'ala uchun |
| `fiber` | Fiber | Xomashyo | 99 | — | O‘tlardan yig‘iladi |
| `sand` | Sand | Xomashyo | 99 | — | Sahrodan olinadi, shisha uchun |
| `ice` | Ice | Xomashyo | 99 | — | Muzlikdan olinadi |
| `leather` | Leather | Xomashyo | 99 | — | Hayvonlar terisi |
| `bone` | Bone | Xomashyo | 99 | — | Skeletlardan tushadi |
| `slime_gel` | Slime Gel | Xomashyo | 99 | — | Shilliqurtdan tushadi |
| `berries` | Berries | Oziq-ovqat | 50 | — | +10 Hunger |
| `raw_meat` | Raw Meat | Oziq-ovqat | 50 | — | Xom go‘sht (+5 Hunger, zahar xavfi) |
| `cooked_meat`| Cooked Meat | Oziq-ovqat | 50 | — | Pechda pishirilgan (+35 Hunger, +10 HP) |
| `water_flask`| Water Flask | Oziq-ovqat | 10 | — | Sahroda suvsizlanishdan saqlaydi |
| `mushroom` | Mushroom | Oziq-ovqat | 50 | — | G‘orlardan topiladi |
| `bread` | Bread | Oziq-ovqat | 50 | — | Bug‘doydan yasaladi (+25 Hunger) |
| `health_pot` | Health Potion| Oziq-ovqat | 20 | — | Darhol +50 HP tiklaydi |
| `planks` | Planks | Material | 99 | — | Taxtalar (qurilish uchun) |
| `stone_bricks`| Stone Bricks| Material | 99 | — | Tosh g‘ishtlar |
| `iron_ingot` | Iron Ingot | Material | 99 | — | Eritilgan temir |
| `gold_ingot` | Gold Ingot | Material | 99 | — | Eritilgan oltin |
| `cloth` | Cloth | Material | 99 | — | Fiberdan to‘qilgan mato |
| `glass` | Glass | Material | 99 | — | Qumni eritish orqali olinadi |
| `wood_axe` | Wooden Axe | Asbob/Qurol | 1 | 100 | Boshlang‘ich bolta |
| `stone_pick` | Stone Pickaxe| Asbob/Qurol | 1 | 150 | Tosh va temir qazishga mos |
| `iron_sword` | Iron Sword | Asbob/Qurol | 1 | 250 | O‘rta darajadagi jangovar qilich |
| `hunter_bow` | Hunter Bow | Asbob/Qurol | 1 | 180 | Masofadan o‘q otish yoyi |
| `arrow` | Arrow | O‘q-dori | 99 | — | Yoy uchun o‘qlar |
| `iron_armor` | Iron Armor Set| Asbob/Qurol| 1 | 300 | Zirh (+40% zararni qaytarish) |

---

## 5. Qurilish va Crafting Tizimi (25 ta Retsept)

### 5.1. Tier 1 — Qo‘lda yasaladigan (Handcrafting)
1. **Torch:** 1x `wood` + 1x `coal` (yoki `slime_gel`) ──► 4x `torch`
2. **Campfire:** 5x `wood` + 3x `stone` ──► 1x `campfire` (Isinish va oddiy pishirish)
3. **Wooden Axe:** 4x `wood` ──► 1x `wood_axe`
4. **Wooden Pickaxe:** 5x `wood` ──► 1x `wood_pick`
5. **Planks (4x):** 1x `wood` ──► 4x `planks`
6. **Cloth (1x):** 3x `fiber` ──► 1x `cloth`
7. **Workbench (Tier 2 Dastgoh):** 10x `planks` + 4x `stone` ──► 1x `workbench`

### 5.2. Tier 2 — Workbench talab qilinadigan retseptlar
8. **Stone Axe:** 3x `planks` + 3x `stone` ──► 1x `stone_axe`
9. **Stone Pickaxe:** 3x `planks` + 4x `stone` ──► 1x `stone_pick`
10. **Wooden Wall:** 4x `planks` ──► 1x `wood_wall`
11. **Wooden Floor:** 2x `planks` ──► 1x `wood_floor`
12. **Wooden Door:** 6x `planks` ──► 1x `wood_door`
13. **Chest (Sandiq - 20 slot):** 8x `planks` ──► 1x `chest`
14. **Hunter Bow:** 3x `wood` + 2x `fiber` ──► 1x `hunter_bow`
15. **Arrows (10x):** 1x `wood` + 1x `stone` + 1x `fiber` ──► 10x `arrow`
16. **Furnace (Eritish pechi):** 10x `stone` + 2x `coal` ──► 1x `furnace`
17. **Water Flask:** 2x `leather` + 1x `fiber` ──► 1x `water_flask`

### 5.3. Tier 3 — Furnace va Anvil (Temirchilik) orqali
18. **Iron Ingot:** 1x `iron_ore` + 1x `coal` (Furnace'da) ──► 1x `iron_ingot`
19. **Gold Ingot:** 1x `gold_ore` + 1x `coal` (Furnace'da) ──► 1x `gold_ingot`
20. **Glass:** 2x `sand` + 1x `coal` ──► 1x `glass`
21. **Iron Sword:** 2x `iron_ingot` + 1x `planks` ──► 1x `iron_sword`
22. **Iron Armor Set:** 8x `iron_ingot` + 4x `leather` ──► 1x `iron_armor`
23. **Steel Pickaxe:** 4x `iron_ingot` + 2x `planks` ──► 1x `steel_pick`
24. **Stone Brick Wall:** 4x `stone_bricks` ──► 1x `stone_brick_wall`
25. **Health Potion:** 1x `glass` + 2x `berries` + 1x `slime_gel` ──► 1x `health_pot`

---

## 6. Server va Tarmoq Qoidalari (Multiplayer Spec)

1. **Server-Authoritative Physics & Movement:**
   * O‘yinchi mijozi faqat yo‘nalish vektorini yuboradi. Server pozitsiyani, tezlikni va devorlar bilan to‘qnashuvlarni tekshiradi. Tezlik chegarasidan oshib ketgan (Speedhack) paketlar darhol rad etiladi.
2. **Server-Side Mining & Placing:**
   * O‘yinchi "qurish" yoki "qazish" so‘rovini yuborganda, server o‘yinchining nishongacha bo‘lgan masofasini (Reach distance $\le 3.5$ metr), inventarida kerakli resurs yoki asbob borligini tekshiradi va tranzaksiyani tasdiqlaydi.
3. **Session & Capacity:**
   * Har bir dunyo instansi 2 dan 8 tagacha o‘yinchini qabul qiladi.
4. **Persistent World State:**
   * Dunyodagi barcha o‘zgarishlar (qurilgan inshootlar, yer rel’efi o‘zgarishlari, sandiqlar ichi) PostgreSQL bazasida saqlanadi va server har 30–60 soniyada xotiradagi o‘zgarishlarni bazaga batch tarzda commit qiladi.
