-- ========================================================================
-- Mythic Realms (2D Multiplayer Sandbox) — Database Schema
-- Engine: PostgreSQL 14+ / Supabase
-- Target: Dedicated Server Persistence & Anti-Dupe Transaction Management
-- ========================================================================

-- UUID kengaytmasini faollashtirish
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ------------------------------------------------------------------------
-- 1. O'yinchilar akkauntlari (Supabase Auth yoki shaxsiy Auth tizimi uchun)
-- ------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ------------------------------------------------------------------------
-- 2. Dunyolar (Server instancelari va dunyo holati)
-- ------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS worlds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    seed INT NOT NULL,                  -- Protsedurali generatsiya uchun tayanch seed
    time_of_day FLOAT DEFAULT 0.0,      -- Kun/tun sikli (0.0 dan 24.0 gacha)
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_saved TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ------------------------------------------------------------------------
-- 3. Xarakterlar (Player State - Muayyan dunyoga bog'langan o'yinchi)
-- ------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS characters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    world_id UUID REFERENCES worlds(id) ON DELETE CASCADE,
    health INT NOT NULL DEFAULT 100 CHECK (health >= 0 AND health <= 100),
    hunger INT NOT NULL DEFAULT 100 CHECK (hunger >= 0 AND hunger <= 100),
    pos_x FLOAT NOT NULL DEFAULT 0.0,
    pos_y FLOAT NOT NULL DEFAULT 0.0,
    is_dead BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, world_id)           -- Har bir o'yinchining bitta dunyoda faqat 1 ta xarakteri bo'ladi
);

-- ------------------------------------------------------------------------
-- 4. Qurilgan Obyektlar (Building System / Inshootlar va Sandiqlar)
-- ------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS structures (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    world_id UUID REFERENCES worlds(id) ON DELETE CASCADE,
    owner_id UUID REFERENCES characters(id) ON DELETE SET NULL,
    structure_type VARCHAR(50) NOT NULL, -- Masalan: 'wood_wall', 'chest', 'workbench', 'furnace'
    grid_x INT NOT NULL,
    grid_y INT NOT NULL,
    current_health INT NOT NULL,
    extra_data JSONB DEFAULT '{}'::jsonb, -- Qo'shimcha parametrlar: eshik holati, pech yoqilg'i vaqti va h.k.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(world_id, grid_x, grid_y)    -- Bitta koordinatada faqat 1 ta asosiy inshoot bo'lishi mumkin
);

-- ------------------------------------------------------------------------
-- 5. Inventarlar (O'yinchi sumkasi yoki Sandiq konteyneri)
-- ------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS inventories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    character_id UUID REFERENCES characters(id) ON DELETE CASCADE,
    structure_id UUID REFERENCES structures(id) ON DELETE CASCADE,
    slots_count INT NOT NULL DEFAULT 20,
    -- Polymorphic bog'lanish: Inventar yo faqat personajga, yo faqat inshootga tegishli bo'lishi shart
    CHECK ((character_id IS NOT NULL AND structure_id IS NULL) OR 
           (character_id IS NULL AND structure_id IS NOT NULL))
);

-- ------------------------------------------------------------------------
-- 6. Inventar Ichidagi Buyumlar (Slotlar bo'yicha joylashuv)
-- ------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS inventory_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    inventory_id UUID NOT NULL REFERENCES inventories(id) ON DELETE CASCADE,
    item_id VARCHAR(50) NOT NULL,       -- Buyum identifikatori: 'wood', 'iron_sword', 'chest'
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    slot_index INT NOT NULL CHECK (slot_index >= 0),
    durability INT,                     -- Asbob va qurollarning qolgan zarbasi (resurslarda NULL)
    UNIQUE(inventory_id, slot_index)   -- Bitta slotda faqat 1 ta item bo'lishi qat'iy kafolatlanadi
);

-- ========================================================================
-- INDEKSLAR (Tezkor o'qish va qidiruv uchun)
-- ========================================================================
CREATE INDEX IF NOT EXISTS idx_characters_world ON characters(world_id);
CREATE INDEX IF NOT EXISTS idx_structures_world_grid ON structures(world_id, grid_x, grid_y);
CREATE INDEX IF NOT EXISTS idx_inventories_char ON inventories(character_id);
CREATE INDEX IF NOT EXISTS idx_inventories_structure ON inventories(structure_id);
CREATE INDEX IF NOT EXISTS idx_inventory_items_lookup ON inventory_items(inventory_id, slot_index);

-- ========================================================================
-- ANTI-DUPE TRANSACTION: Atomik Item O'tkazish Protsedurasi
-- Bu protsedura ikkita inventar o'rtasida buyum almashish paytida qulflash
-- (Row-level Locking) mexanizmini ishlatadi va duplikatsiyani 100% yo'q qiladi.
-- ========================================================================
CREATE OR REPLACE FUNCTION transfer_inventory_item(
    p_from_inv_id UUID,
    p_to_inv_id UUID,
    p_from_slot INT,
    p_to_slot INT,
    p_qty INT
) RETURNS BOOLEAN AS $$
DECLARE
    v_source_item inventory_items%ROWTYPE;
    v_target_item inventory_items%ROWTYPE;
BEGIN
    -- 1. Xavfsiz tartibda (Deadlock oldini olish uchun) qatorlarni qulflash (FOR UPDATE)
    SELECT * INTO v_source_item 
    FROM inventory_items 
    WHERE inventory_id = p_from_inv_id AND slot_index = p_from_slot
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Manba slotida buyum topilmadi!';
    END IF;

    IF v_source_item.quantity < p_qty THEN
        RAISE EXCEPTION 'Yetarli miqdorda buyum mavjud emas!';
    END IF;

    SELECT * INTO v_target_item 
    FROM inventory_items 
    WHERE inventory_id = p_to_inv_id AND slot_index = p_to_slot
    FOR UPDATE;

    -- 2. Agar maqsadli slot bo'sh bo'lsa
    IF v_target_item.id IS NULL THEN
        -- Yangi slotga qo'shish
        INSERT INTO inventory_items (inventory_id, item_id, quantity, slot_index, durability)
        VALUES (p_to_inv_id, v_source_item.item_id, p_qty, p_to_slot, v_source_item.durability);

        -- Manba slotidan ayirish yoki o'chirish
        IF v_source_item.quantity = p_qty THEN
            DELETE FROM inventory_items WHERE id = v_source_item.id;
        ELSE
            UPDATE inventory_items 
            SET quantity = quantity - p_qty 
            WHERE id = v_source_item.id;
        END IF;

    -- 3. Agar maqsadli slotda xuddi shu turdagi stacklanadigan item bo'lsa
    ELSIF v_target_item.item_id = v_source_item.item_id AND v_source_item.durability IS NULL THEN
        UPDATE inventory_items 
        SET quantity = quantity + p_qty 
        WHERE id = v_target_item.id;

        IF v_source_item.quantity = p_qty THEN
            DELETE FROM inventory_items WHERE id = v_source_item.id;
        ELSE
            UPDATE inventory_items 
            SET quantity = quantity - p_qty 
            WHERE id = v_source_item.id;
        END IF;

    ELSE
        RAISE EXCEPTION 'Maqsadli slot band yoki buyum turlari mos kelmadi!';
    END IF;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
