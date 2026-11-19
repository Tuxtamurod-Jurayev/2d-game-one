# 12-Loyiha: Mythic Realms (Capstone Project) — Yangilangan Yakuniy TZ

> **Loyiha turi:** Capstone / Yakuniy loyiha  
> **Murakkablik darajasi:** Ekspert  
> **Janr:** 2D Multiplayer Survival & Crafting Sandbox  
> **Dvigatel:** Godot 4.x / Web Client (Node.js/PostgreSQL Server-authoritative backend bilan)  
> **Maqsadli platforma:** PC (Windows Desktop va Web)  

---

## 1. Vizual Uslub va Art-Dizayn Talablari (Yangi & Qat'iy)

### 1.1. Asosiy Qahramon (Odam qiyofasi — Humanoid)
* **Anatomiya va Proporsiya:** O‘yinchi boshqaradigan personaj **100% odam qiyofasida (humanoid)** bo‘lishi shart. Noaniq geometrik shakllar yoki g‘ayritabiiy mavjudotlar boshqariladigan personaj sifatida ishlatilmaydi. Proporsiyalar zamonaviy 2D uslubida (realistik yoki estetik stilizatsiyalangan, masalan 32x48 / 48x64 piksel yoki vektorli 2D) shakllantiriladi.
* **Animatsiyalar:** Inson harakatlariga xos silliq sikllar talab etiladi:
  * *Idle:* Erkin nafas olish va tayyorgarlik holati.
  * *Walk / Run:* 8 yo‘nalishli odam qadam tashlash anatomiyasi.
  * *Chop / Mine:* Bolta yoki cho‘kich bilan zarba berish harakati.
  * *Attack:* Qilich bilan siltash yoki kamondan o‘q tortish holati.
  * *Hurt / Die:* Zarba qabul qilish va yiqilish.
* **Boshlang‘ich Kastomizatsiya (Character Customization):** O‘yinga kirishdan oldin o‘yinchi o‘z insoniy qiyofasini sozlashi shart:
  * Teri rangi (Skin tones: kamida 5 xil).
  * Soch turmagi va rangi (Hairstyles: kamida 4 xil + rang palitrasi).
  * Boshlang‘ich kiyim rangi (Ko‘ylak va shim ranglari).

### 1.2. Ikonalar va UI Elementlari (AI aralashuvisiz — 100% Handcrafted Art)
* **Sun'iy Intellektdan Foydalanish Taqiqlanadi:** Midjourney, DALL-E, Stable Diffusion va boshqa generativ AI vositalari orqali vizual assetlar yaratish **qat’iyan man etiladi**.
* **Mualliflik Kafolati (Art Provenance):** Barcha ikonalar (resurslar, qurollar, asboblar, mebellar, UI tugmalari) dizayner/rassom tomonidan qo‘lda (Pixel-art yoki Vector) chizilgan bo‘lishi va buni tasdiqlovchi manba fayllar (`.psd`, `.ai` yoki `.aseprite` qatlamlari bilan) taqdim etilishi shart.
* **Tipografiya va O‘qilishi Osonlik:** Har bir ikona o‘z funksiyasini bir qarashda bildiradi. Matnlar zamonaviy, toza sans-serif shriftlarda bo‘lib, kichik va yuqori zichlikdagi ekranlarda ham (HiDPI) tiniq o‘qiladi.

---

## 2. UI/UX Dizayn (Zamonaviy Standartlar)

### 2.1. Minimalistik va Shaffof Interfeys (Modern Glassmorphism)
* Eski "og‘ir qutili" (chunky/retro-box) interfeyslardan butunlay voz kechiladi.
* Zamonaviy indie survival o‘yinlari (Rust, V Rising) standartlariga mos, yengil qoraytirilgan, yarim shaffof (translucent blur/frosted glass) va o‘yin ekranini to‘sib qo‘ymaydigan nozik panellar ishlatiladi.

### 2.2. Dinamik HUD (Context-Aware HUD)
* **Avtomatik Fade:** Qahramon xavfsiz va xotirjam holatda turganda Jon (Health), Ochlik (Hunger) va Stamina ko‘rsatkichlari ekranni chalg‘itmaslik uchun xira (fade out, 20-30% opacity) holatga o‘tadi.
* **Faollashuv:** O‘yinchi yugurganda (Stamina sarflanganda), ochqaganda (Hunger < 30%) yoki jang qilganda (HP o‘zgarganda) HUD paneli darhol yorqinlashadi (100% opacity) va xavf signallari beradi.

### 2.3. Zamonaviy Inventar va Crafting
* **Markazni to‘smaydigan ergonomika:** O‘yinchi inventari ekranning chap qismida, crafting yoki sandiq oynasi esa o‘ng qismida joylashadi; ekran markazidagi gameplay doimo ko‘rinib turadi.
* **Qidiruv qatori (Search bar):** Crafting oynasida kerakli buyumni nomidan darhol topish imkoniyati.
* **Kategoriya filtrlari:** Barcha, Qurollar, Asboblar, Oziq-ovqat, Qurilish materiallari, Resurslar.
* **Ergonomik boshqaruv:** Shift + Click orqali itemlarni sandiq yoki hotbarga bir zumda o‘tkazish (Quick Transfer).

### 2.4. Boshqaruv sxemasi (Controls)
* **WASD:** Odam qahramonining 8 yo‘nalishli harakati.
* **Mouse (Sichqoncha):** Nishonga olish / Qurilmalarni joylashtirish.
* **Left Click:** Asbob/qurol bilan zarba berish yoki qazish.
* **Right Click:** Grid bo‘yicha inshootni joylashtirish.
* **E:** Interaksiya (Obyektlarni olish, sandiq/eshikni ochish).
* **Tab yoki I:** Zamonaviy yarim shaffof inventarni ochish/yopish.
* **C:** Crafting menyusini chaqirish.
* **Esc:** Minimalistik pauza va sozlamalar menyusi.

---

## 3. Asosiy Mexanikalar va Tizimlar

### 3.1. Protsedurali Dunyo (Procedural World Generation)
* **Seed asosidagi yaratilish:** FastNoiseLite orqali biomlar, yer relyefi, daryolar va yer osti g‘orlari generatsiya qilinadi.
* **Biomlar:** Yashil O‘rmon (Forest), Qaqragan Sahro (Desert), Muzli Qor Tog‘lari (Snow/Mountains).
* **Resurs tugunlari (Nodes):** Daraxtlar, tosh qatlamlari, temir, oltin va ko‘mir rudalari tarmoq bo‘ylab tabiiy guruhlanadi.

### 3.2. Omon qolish (Survival)
* **Kun va Tun Sikli:** Real vaqtda 24 daqiqalik to‘liq sikl.
* **Insoniy Ehtiyojlar:** 
  * Tunda havo keskin soviydi; inson qahramon sovuqdan muzlab qolmasligi uchun mash’ala (Torch), o‘choq (Campfire) yoki mustahkam boshpana (Baza) ichida bo‘lishi shart.
  * Ochlik (Hunger) vaqti-vaqti bilan oziqlanishni talab qiladi; to‘yimli ovqatlar (Cooked meat) jarohatlarni tezroq tiklaydi.

### 3.3. Qurilish (Grid-based Building System)
* **Silliq va Aniq Snapping:** Devorlar, pollar, eshiklar, ish stollari va sandiqlar sichqoncha yordamida kataklar (grid) bo‘yicha joylashadi.
* **Gologramma Preview:** Joylashtirishdan oldin obyekt shaffof ko‘rinadi:
  * *Yashil gologramma:* Qurishga ruxsat bor.
  * *Qizil gologramma:* O‘rin band yoki poydevor (pol) yo‘q.

### 3.4. Multiplayer (Server-Authoritative Co-op)
* **O‘yinchilar (Insonlar) Kooperatsiyasi:** 2 dan 8 tagacha odam bir serverda birlashib baza quradi va resurslarni birgalikda boshqaradi.
* **Dushmanlar:** Odamlarga qarshi faqat g‘ayriinsoniy dushmanlar (klonlar, kabus maxluqlar, skeletlar, ajdarlar) jang qiladi.
* **Server Avtoriteti & Anti-Dupe:** Barcha harakatlar, qazish, qurish va inventardagi buyum o‘tkazishlari faqat serverdagi atomik tranzaksiyalar (SQL `transfer_inventory_item`) orqali tasdiqlanadi.

---

## 4. Ishlab Chiqish Bosqichlari va Qat'iy Qoidalar

1. **Art-Dastur (Art Bible):** Inson qahramoni proporsiyalari, kastomizatsiya qismlari, ranglar palitrasi va UI shablonlari (Figma'da) chizib olinadi. AI vositalari to‘liq bloklanadi.
2. **UI Prototipi (Frontend):** Zamonaviy, nozik, yarim shaffof va animatsiyali interfeys (HUD, inventar, crafting) yig‘iladi.
3. **Core Gameplay:** Inson personaji kontrolleri, 8 yo‘nalishli harakat, animatsiya daraxti, silliq kamera va interaksiya kodlanadi.
4. **Tizimlar Integratsiyasi:** Qo‘lda chizilgan original ikonalar bilan inventar, crafting va grid-building tizimi birlashtiriladi.
5. **Multiplayer & Backend:** Dedicated Server (Node.js/PostgreSQL yoki Godot Headless) ulanadi. Anti-duplication va dunyo persistence joriy etiladi.
6. **QA va Sayqallash:** UI turli ekran o‘lchamlari va aspekt nisbatlarida sinovdan o‘tkaziladi; UX tiqilib qolishlari tuzatiladi.

---

## 5. Yakuniy Topshiriq (MVP Qabul Mezonlari / DoD)

* [ ] **100% Inson Qahramoni:** Boshqariladigan personaj to‘liq inson qiyofasida bo‘lishi, odam anatomiyasi animatsiyalariga ega bo‘lishi va boshlang‘ich ko‘rinishi (soch, teri, kiyim) o‘yin boshida sozlanishi shart.
* [ ] **Zamonaviy Shaffof UI/UX:** Quti-quti dizaynlardan xoli, zamonaviy indie survival standartlariga mos, dinamik (auto-fade) HUD, qidiruv va filtrlarga ega inventar.
* [ ] **Nol AI (0% AI Art):** O‘yindagi birorta ham ikona yoki vizual element AI tomonidan generatsiya qilinmaganligi, barchasi mualliflik ishi ekanligi manba fayllar (`.psd`, `.ai`, `.aseprite`) orqali isbotlanishi shart.
* [ ] **Ko‘p O‘yinchili Muhit:** Server-authoritative arxitekturada 2–8 nafar o‘yinchi birgalikda uzilishlarsiz va dupe-xatolarsiz o‘ynay olishi.
* [ ] **Dunyo Saqlanishi (Persistence):** Server restart bo‘lganda yoki o‘yinchi qayta kirganda dunyo, bazalar va inventar yo‘qolmasdan to‘liq tiklanishi.
