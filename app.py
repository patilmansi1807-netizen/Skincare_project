import os
import sqlite3
from datetime import datetime

try:
    from flask import Flask, render_template, request, redirect, url_for, flash
except ImportError as exc:
    raise RuntimeError(
        "Flask is required. Install the project dependencies with 'pip install -r requirements.txt'."
    ) from exc

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'glowcare_secret_key_2026_dev')

DB_NAME = 'skincare.db'

# Skin Concern Constants
FINE_LINES_ANTI_AGING = 'Fine Lines & Anti-Aging'


def get_db_connection():
    """Establish connection to SQLite database with dictionary-like row access."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables and seed default products if empty or outdated."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            skin_type TEXT,
            concern TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            routine_time TEXT,
            notes TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            reminder_time TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            amount REAL,
            date TEXT,
            category TEXT,
            image TEXT
        )
    ''')

    # Ensure backward compatibility for expenses columns
    try:
        cursor.execute('ALTER TABLE expenses ADD COLUMN category TEXT')
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute('ALTER TABLE expenses ADD COLUMN image TEXT')
    except sqlite3.OperationalError:
        pass

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT,
            reason TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT,
            category TEXT,
            price REAL NOT NULL,
            image TEXT,
            description TEXT,
            stock INTEGER DEFAULT 10,
            skin_type TEXT DEFAULT 'All Skin Types',
            concern TEXT DEFAULT 'Glow & Maintenance',
            rating REAL DEFAULT 4.8
        )
    ''')

    # Ensure backward compatibility for products columns
    for col in [('skin_type', "TEXT DEFAULT 'All Skin Types'"), ('concern', "TEXT DEFAULT 'Glow & Maintenance'"), ('rating', 'REAL DEFAULT 4.8')]:
        try:
            cursor.execute(f'ALTER TABLE products ADD COLUMN {col[0]} {col[1]}')
        except sqlite3.OperationalError:
            pass

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            pincode TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            total_amount REAL NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT DEFAULT 'Order Placed'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    # 30 Curated Skincare Products with High-Resolution Verified Skin & Skincare Images
    catalog_30_products = [
        # --- Cleansers ---
        (
            'Gentle Hydrating Cream Cleanser',
            'Cetaphil',
            'Cleanser',
            499.00,
            'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=600&q=80',
            'Non-foaming cream cleanser infused with Niacinamide, Panthenol, and hydrating Glycerin that preserves the natural skin lipid barrier.',
            25,
            'Dry / Sensitive',
            'Dryness & Barrier Support',
            4.8
        ),
        (
            '2% Salicylic Acid Acne Control Cleanser',
            'CeraVe',
            'Cleanser',
            749.00,
            'https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?auto=format&fit=crop&w=600&q=80',
            'Formulated with 3 essential ceramides and purifying BHA to target active breakouts and unclog pores without causing dryness.',
            20,
            'Oily / Acne-Prone',
            'Acne & Blemishes',
            4.9
        ),
        (
            'Centella Light Cleansing Oil',
            'SKIN1004',
            'Cleanser',
            1199.00,
            'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=600&q=80',
            'Ultra-gentle botanical cleansing oil crafted with pure Madagascar Centella to dissolve stubborn waterproof sunscreen and sebum plugs.',
            15,
            'All Skin Types',
            'Healthy Glow & Maintenance',
            4.9
        ),
        (
            'Rice & Ceramide Hydrating Foaming Cleanser',
            'The Face Shop',
            'Cleanser',
            599.00,
            'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=600&q=80',
            'Velvety whipped face wash infused with natural rice bran extract and rice water to brighten dull texture and replenish hydration.',
            22,
            'Normal / Dull',
            'Healthy Glow & Maintenance',
            4.7
        ),

        # --- Toners & Essences ---
        (
            'AHA/BHA Clarifying Treatment Toner',
            'COSRX',
            'Toner',
            890.00,
            'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=600&q=80',
            'Mineral water and willow bark clarifying mist designed to gently sweep away dead surface flakes, refine skin texture, and prevent blackheads.',
            30,
            'Oily / Combination',
            'Acne & Blemishes',
            4.8
        ),
        (
            'Green Plum Refreshing Calming Toner',
            'Beauty of Joseon',
            'Toner',
            1050.00,
            'https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?auto=format&fit=crop&w=600&q=80',
            'Slightly acidic daily soothing toner with 25% green plum water and 2% mung bean extract to rebalance skin pH and relieve redness.',
            18,
            'Sensitive / Reactive',
            'Redness & Irritation',
            4.9
        ),
        (
            'Hyaluronic Acid Deep Moisture Toner',
            'Isntree',
            'Toner',
            950.00,
            'https://images.unsplash.com/photo-1615397349754-cfa2066a298e?auto=format&fit=crop&w=600&q=80',
            '5 types of concentrated low-to-high molecular hyaluronic acid to flood parched cells with intense moisture and prevent dehydration.',
            24,
            'Dry / Dehydrated',
            'Dryness & Barrier Support',
            4.8
        ),

        # --- Serums & Actives ---
        (
            '10% Niacinamide + 1% Zinc Blemish Serum',
            'The Ordinary',
            'Serum',
            699.00,
            'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=600&q=80',
            'High-strength clinical blemish formula engineered to regulate excess sebum activity, soothe active inflammation, and visibly tighten enlarged pores.',
            40,
            'Oily / Acne-Prone',
            'Acne & Blemishes',
            4.9
        ),
        (
            '15% Vitamin C + Ferulic Brightening Serum',
            'Minimalist',
            'Serum',
            699.00,
            'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?auto=format&fit=crop&w=600&q=80',
            'Stabilized Ethyl Ascorbic Acid enriched with Ferulic Acid and Centella Asiatica to fade stubborn dark spots and shield against photoaging.',
            28,
            'All Skin Types',
            'Hyperpigmentation & Sun Spots',
            4.9
        ),
        (
            'Hyaluronic Acid 2% + B5 Multi-Depth Hydrator',
            'The Ordinary',
            'Serum',
            750.00,
            'https://images.unsplash.com/photo-1617897903246-719242758050?auto=format&fit=crop&w=600&q=80',
            'Next-generation cross-polymer Hyaluronic Acid combined with Pro-Vitamin B5 to instantly plump dehydrated fine lines and fortify dermal elasticity.',
            35,
            'All / Dehydrated',
            'Dryness & Barrier Support',
            4.8
        ),
        (
            '2% Alpha Arbutin Dark Spot Correction Serum',
            'Minimalist',
            'Serum',
            549.00,
            'https://images.unsplash.com/photo-1616683693504-3ea7e9ad6fec?auto=format&fit=crop&w=600&q=80',
            'Advanced depigmenting serum featuring 2% ultra-purified Alpha Arbutin and Hyaluronic Acid to fade sun tan, melasma, and post-acne pigmentation.',
            22,
            'All Skin Types',
            'Hyperpigmentation & Sun Spots',
            4.8
        ),
        (
            '0.3% Retinol in Squalane Night Renewal Elixir',
            'Minimalist',
            'Serum',
            599.00,
            'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=600&q=80',
            'Pure Retinol in a skin-mimicking olive squalane base to accelerate overnight cellular turnover, soften fine lines, and boost collagen density.',
            18,
            'Aging / Normal',
            'Fine Lines & Anti-Aging',
            4.9
        ),
        (
            '3% Tranexamic Acid + 5% Mandelic Acid Serum',
            'GlowCare Pro',
            'Serum',
            849.00,
            'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=600&q=80',
            'Clinical dermal brightening solution pairing Tranexamic Acid with Mandelic Acid to treat deep hormonal melasma and stubborn dark patches.',
            14,
            'Pigmentation Prone',
            'Hyperpigmentation & Sun Spots',
            4.8
        ),
        (
            'Advanced Snail 96 Mucin Power Essence',
            'COSRX',
            'Serum',
            1290.00,
            'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?auto=format&fit=crop&w=600&q=80',
            '96.3% filtered Snail Secretion Filtrate that delivers the coveted dewy "glass skin" finish, soothes flare-ups, and accelerates healing.',
            30,
            'All Skin Types',
            'Healthy Glow & Maintenance',
            5.0
        ),
        (
            'Multi-Peptide + Copper Peptides 1% Serum',
            'The Ordinary',
            'Serum',
            1850.00,
            'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?auto=format&fit=crop&w=600&q=80',
            'Comprehensive multi-technology peptide complex with direct copper tripeptide-1 to support structural skin matrix, firm sagging tissue, and revitalize tone.',
            12,
            'Aging / Mature',
            'Fine Lines & Anti-Aging',
            4.9
        ),
        (
            '10% Azelaic Acid Suspension Brightening Cream',
            'The Ordinary',
            'Serum',
            890.00,
            'https://images.unsplash.com/photo-1576426863848-c21f53c60b19?auto=format&fit=crop&w=600&q=80',
            'Multi-functional brightening cream-gel with pure Azelaic acid to visibly diminish redness, soothe rosacea-prone skin, and even skin tone.',
            16,
            'Sensitive / Rosacea',
            'Redness & Irritation',
            4.7
        ),

        # --- Moisturizers & Barrier Care ---
        (
            'Ceramide Barrier Repair Cream 0.3%',
            'Minimalist',
            'Moisturizer',
            449.00,
            'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=600&q=80',
            'Intensive barrier-restoring daily moisturizer with 5 essential ceramides, Madecassoside, and Ursolic acid to heal damaged skin barrier.',
            35,
            'Dry / Compromised',
            'Dryness & Barrier Support',
            4.9
        ),
        (
            'Hydro Boost Oil-Free Hyaluronic Water Gel',
            'Neutrogena',
            'Moisturizer',
            799.00,
            'https://images.unsplash.com/photo-1573461160327-b450ce3d8e7f?auto=format&fit=crop&w=600&q=80',
            'Ultra-refreshing, non-comedogenic water gel that drenches skin in 72-hour continuous hydration without leaving an oily residue.',
            28,
            'Oily / Combination',
            'Dryness & Barrier Support',
            4.8
        ),
        (
            'Cicaplast Baume B5+ Soothing Repair Balm',
            'La Roche-Posay',
            'Moisturizer',
            1150.00,
            'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=600&q=80',
            'Multi-purpose emergency soothing balm enriched with Tribioma probiotic complex, 5% Panthenol, and Madecassoside for irritated, sensitive skin.',
            20,
            'Sensitive / Damaged',
            'Redness & Irritation',
            5.0
        ),
        (
            'Midnight Recovery Botanical Night Cream',
            'GlowCare Pro',
            'Moisturizer',
            1499.00,
            'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=600&q=80',
            'Velvety overnight lipid repair cream rich in squalane, evening primrose oil, and peptide complex to restore radiant skin bounce by morning.',
            15,
            'Dry / Normal',
            'Fine Lines & Anti-Aging',
            4.8
        ),
        (
            'Green Tea Seed Hyaluronic Cream',
            'Innisfree',
            'Moisturizer',
            1200.00,
            'https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?auto=format&fit=crop&w=600&q=80',
            'Jeju green tea biotics and 5-layer hyaluronic acid provide a moisture shield to lock hydration into deeper epidermal layers.',
            18,
            'Combination / Normal',
            'Healthy Glow & Maintenance',
            4.7
        ),

        # --- Sunscreens (SPF Defense) ---
        (
            'Ultra-Light Fluid Sunscreen SPF 50+ PA++++',
            'Derma Co',
            'Sunscreen',
            499.00,
            'https://images.unsplash.com/photo-1599305090598-fe179d501227?auto=format&fit=crop&w=600&q=80',
            'Feather-light broad-spectrum fluid sunscreen enriched with 1% Hyaluronic acid and Vitamin E. Zero white cast, non-sticky, completely invisible.',
            50,
            'All Skin Types',
            'Sun Protection & Anti-Aging',
            4.9
        ),
        (
            'Ultra Matte Dry-Touch Gel Sunscreen SPF 50',
            'Re\'equil',
            'Sunscreen',
            695.00,
            'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=600&q=80',
            'Water and sweat-resistant physical/chemical sunscreen with a velvety matte primer finish that controls excess midday oil shine.',
            35,
            'Oily / Acne-Prone',
            'Sun Protection & Anti-Aging',
            4.9
        ),
        (
            'UV Aqua Rich Watery Essence SPF 50+ PA++++',
            'Biore UV',
            'Sunscreen',
            980.00,
            'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=600&q=80',
            'World-renowned Japanese water capsule formula that glides like fresh water, giving instant dewy glow and high UV defense.',
            30,
            'Normal / Dry',
            'Sun Protection & Anti-Aging',
            5.0
        ),

        # --- Targeted Exfoliants & Treatments ---
        (
            '2% Salicylic Acid BHA Liquid Exfoliant',
            'Paula\'s Choice',
            'Treatment',
            1200.00,
            'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=600&q=80',
            'Iconic leave-on chemical exfoliant that dissolves pore-clogging debris, shrinks enlarged pores, and smooths rough skin texture.',
            25,
            'Oily / Acne-Prone',
            'Acne & Blemishes',
            4.9
        ),
        (
            'AHA 30% + BHA 2% Peeling Solution Mask',
            'The Ordinary',
            'Treatment',
            950.00,
            'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=600&q=80',
            '10-minute exfoliating facial peeling mask with glycolic, lactic, and salicylic acids to reveal dazzling radiant and clear skin.',
            22,
            'Resilient Skin',
            'Healthy Glow & Maintenance',
            4.8
        ),
        (
            'Hydrocolloid Master Pimple Patch (36 Patches)',
            'COSRX',
            'Treatment',
            399.00,
            'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=600&q=80',
            'Invisible protective stickers that draw out whitehead exudate overnight, reduce inflammation, and prevent acne picking scars.',
            60,
            'Acne-Prone',
            'Acne & Blemishes',
            4.9
        ),

        # --- Eye Care & Masks ---
        (
            'Caffeine 5% + EGCG Under-Eye Depuffing Serum',
            'The Ordinary',
            'Eye Care',
            650.00,
            'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?auto=format&fit=crop&w=600&q=80',
            'Concentrated green tea epigallocatechin gallate and caffeine to drain puffy fluids, constrict under-eye capillaries, and brighten dark rings.',
            30,
            'All Skin Types',
            'Dark Circles & Eye Fatigue',
            4.8
        ),
        (
            'Multi-Peptide Youth Eye Cream with Retinol',
            'GlowCare Pro',
            'Eye Care',
            899.00,
            'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=600&q=80',
            'Firming and smoothing eye treatment formulated with palmitoyl peptides and micro-encapsulated retinol to reduce fine lines and crow\'s feet.',
            20,
            'Aging / Fine Lines',
            'Dark Circles & Eye Fatigue',
            4.9
        ),
        (
            'Pink Clay Pore Detox & Glow Mask',
            'GlowCare Pro',
            'Face Mask',
            599.00,
            'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=600&q=80',
            'Australian mineral pink clay blended with Aloe Vera and Centella to gently detoxify congested pores and refine texture without tightening skin.',
            25,
            'Oily / Congested',
            'Acne & Blemishes',
            4.7
        )
    ]

    # Re-sync products catalog to ensure latest valid URLs & details
    cursor.execute('SELECT COUNT(*) FROM products')
    product_count = cursor.fetchone()[0]

    if product_count != 30:
        cursor.execute('DELETE FROM products')
        cursor.executemany('''
            INSERT INTO products (name, brand, category, price, image, description, stock, skin_type, concern, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', catalog_30_products)
    else:
        # Update existing records with verified images
        for item in catalog_30_products:
            cursor.execute('''
                UPDATE products 
                SET brand = ?, category = ?, price = ?, image = ?, description = ?, stock = ?, skin_type = ?, concern = ?, rating = ?
                WHERE name = ?
            ''', (item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[0]))

    conn.commit()
    conn.close()


@app.context_processor
def inject_globals():
    """Make current year and user profile globally available to all templates."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM profile ORDER BY id DESC LIMIT 1')
    user_prof = cursor.fetchone()
    conn.close()
    return {
        'now_year': datetime.now().year,
        'global_profile': user_prof
    }


def get_clinical_recommendations(skin_type, concern):
    """Generate tailored clinical skincare recommendations based on skin type and primary concern."""
    recs = []

    # Concern-specific guidance
    if concern == 'Acne':
        recs.append("🫧 Cleanse twice daily using a gentle foaming or 1.5-2% Salicylic Acid (BHA) cleanser to clear sebum without stripping the protective mantle.")
        recs.append("✨ Apply 5%–10% Niacinamide with Zinc PCA in the morning to soothe inflammatory redness and regulate active sebum secretion.")
        recs.append("🧪 Incorporate an oil-free gel moisturizer formulated with Ceramides and Centella Asiatica to heal the skin barrier.")
        recs.append("🌙 Use targeted spot treatments (such as Azelaic Acid 10% or Benzoyl Peroxide 2.5%) on active lesions at bedtime.")
        recs.append("☀️ Never skip daily broad-spectrum SPF 50 — post-acne dark marks (PIH) darken dramatically with UV exposure.")

    elif concern == 'Dryness':
        recs.append("💧 Cleanse with a non-foaming hydrating milk or cream cleanser; avoid hot water which dissolves essential lipids.")
        recs.append("🌾 Apply multi-molecular Hyaluronic Acid or Panthenol (Pro-Vitamin B5) serum directly onto damp skin to lock in deep hydration.")
        recs.append("🛡️ Layer a barrier-repair moisturizer rich in Ceramides NP/EOP, Cholesterol, and Fatty Acids twice daily.")
        recs.append("🥑 At night, seal in moisture with 2-3 drops of pure plant Squalane or a nourishing overnight barrier mask.")
        recs.append("☀️ Use a hydrating, dewy chemical or mineral SPF 50 sunscreen enriched with Vitamin E.")

    elif concern == 'Pigmentation':
        recs.append("🍊 Apply a stabilized 10%–15% Vitamin C (L-Ascorbic or Ethyl Ascorbic Acid) serum each morning under SPF to block melanin formation.")
        recs.append("🌸 Layer Alpha Arbutin (2%) or Tranexamic Acid (3%) in your evening ritual to fade stubborn sun spots and post-inflammatory marks.")
        recs.append("✨ Gently exfoliate 1–2 times weekly with Lactic Acid (5-10%) to accelerate cellular renewal and buff away dull hyperpigmented cells.")
        recs.append("☀️ Strictly apply 2 finger-lengths of broad-spectrum SPF 50+ UVA/UVB sunscreen every morning and reapply if outdoors.")
        recs.append("🌿 Pair your brightening actives with soothing Niacinamide and Licorice Root extract to prevent rebound pigment flares.")

    elif concern == 'Dark Circles':
        recs.append("👁️ Apply an eye fluid formulated with Caffeine (5%) and EGCG morning and night to constrict capillaries and drain puffy fluid.")
        recs.append("🧬 Gently pat a peptide-rich eye cream with Hyaluronic Acid around the orbital bone to plump thin, delicate under-eye skin.")
        recs.append("✨ In the evening, use a low-concentration encapsulated Retinol or Vitamin K eye serum to boost collagen and firm skin.")
        recs.append("☀️ Always extend your daily mineral sunscreen up to the orbital bone, and wear UV400 polarized sunglasses outdoors.")
        recs.append("😴 Prioritize 7-8 hours of restful sleep and hydrate consistently (2.5L water daily) to reduce vascular discoloration.")

    elif concern == 'Aging':
        recs.append("⏳ Introduce encapsulated Retinol or Retinaldehyde (0.1%-0.3%) 2–3 evenings per week to accelerate cellular turnover and collagen synthesis.")
        recs.append("🧬 Apply a multi-peptide firming complex (Copper Peptides / Matrixyl 3000) every morning to reinforce structural dermal elasticity.")
        recs.append("🛡️ Neutralize oxidative environmental stressors with Vitamin C + Ferulic Acid antioxidant serum every morning.")
        recs.append("🧴 Nourish with an intensely restorative Peptide & Ceramide night cream to combat transepidermal moisture loss.")
        recs.append("☀️ Apply broad-spectrum SPF 50+ religiously 365 days a year — 80% of visible skin aging is UV-induced photoaging.")

    else:  # No Major Concern / Maintenance
        recs.append("🌿 Maintain healthy homeostasis with a gentle pH-balanced (5.5) daily cleanser morning and night.")
        recs.append("💧 Keep skin plump and hydrated with daily Hyaluronic Acid, Centella Asiatica, and Green Tea extract serum.")
        recs.append("🧴 Apply a weightless barrier cream containing essential ceramides to protect against environmental pollution.")
        recs.append("☀️ Wear broad-spectrum SPF 50 every single day as your primary preventive anti-aging and skin health ritual.")
        recs.append("✨ Perform a gentle mild chemical exfoliation (AHA/PHA) once weekly to maintain radiant texture.")

    # Skin type specific nuance
    if skin_type == 'Sensitive':
        recs.append("🌸 Sensitive Skin Rule: Always patch-test active products on your inner forearm for 24h, and avoid synthetic fragrances and essential oils.")
    elif skin_type == 'Oily':
        recs.append("🫧 Oily Skin Rule: Look for labels marked 'Non-Comedogenic' and lightweight gel/water-cream textures.")
    elif skin_type == 'Dry':
        recs.append("🌵 Dry Skin Rule: Apply hydrating toners in multiple thin layers ('7-skin method') before locking with rich cream.")
    elif skin_type == 'Combination':
        recs.append("⚖️ Combination Skin Rule: Zone-treat your face: apply lightweight gel to the T-zone and richer cream to drier cheeks.")

    return recs


# ----------------------------------------------------
# Routes
# ----------------------------------------------------

@app.route('/')
def home():
    """Landing page with AI skin diagnostic analyzer."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM profile ORDER BY id DESC LIMIT 1')
    user_profile = cursor.fetchone()
    conn.close()
    return render_template('index.html', profile=user_profile)


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Process skin diagnostic, generate recommendations, and fetch matched dispensary products."""
    if request.method == 'POST':
        skin_type = request.form.get('skin_type', 'Normal')
        concern = request.form.get('concern', 'No Major Concern')
    else:
        # Support GET with query params or fallback to user profile
        skin_type = request.args.get('skin_type')
        concern = request.args.get('concern')
        if not skin_type or not concern:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM profile ORDER BY id DESC LIMIT 1')
            user_profile = cursor.fetchone()
            conn.close()
            if user_profile:
                skin_type = user_profile['skin_type']
                concern = user_profile['concern']
            else:
                return redirect(url_for('home'))

    recommendations = get_clinical_recommendations(skin_type, concern)

    # Fetch top matched products from catalog
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query products matching skin_type, concern, or general
    cursor.execute('''
        SELECT * FROM products
        WHERE skin_type LIKE ? OR concern LIKE ? OR skin_type LIKE '%All%'
        ORDER BY rating DESC
        LIMIT 6
    ''', (f'%{skin_type}%', f'%{concern}%'))
    matched_products = cursor.fetchall()
    conn.close()

    return render_template(
        'result.html',
        skin_type=skin_type,
        concern=concern,
        recommendations=recommendations,
        matched_products=matched_products
    )


@app.route('/routine', methods=['GET', 'POST'])
def routine():
    """Manage daily AM/PM skincare routine steps."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        product = request.form.get('product', '').strip()
        routine_time = request.form.get('routine_time', 'Morning')
        notes = request.form.get('notes', '').strip()

        if product:
            cursor.execute(
                'INSERT INTO routine (product, routine_time, notes) VALUES (?, ?, ?)',
                (product, routine_time, notes)
            )
            conn.commit()
            flash(f"🧴 Added '{product}' to your {routine_time} routine!", "success")
        conn.close()
        return redirect(url_for('routine'))

    cursor.execute('SELECT * FROM routine ORDER BY id DESC')
    routines = cursor.fetchall()
    conn.close()
    return render_template('routine.html', routines=routines)


@app.route('/delete_routine/<int:id>')
def delete_routine(id):
    """Delete a step from the skincare routine."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM routine WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("🗑️ Step removed from your routine.", "info")
    return redirect(url_for('routine'))


@app.route('/reminder', methods=['GET', 'POST'])
def reminder():
    """Manage daily skincare reminders and application alarms."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        reminder_time = request.form.get('reminder_time', '').strip()

        if title and reminder_time:
            cursor.execute(
                'INSERT INTO reminders (title, reminder_time) VALUES (?, ?)',
                (title, reminder_time)
            )
            conn.commit()
            flash(f"⏰ Reminder '{title}' scheduled for {reminder_time}!", "success")
        conn.close()
        return redirect(url_for('reminder'))

    cursor.execute('SELECT * FROM reminders ORDER BY reminder_time ASC, id DESC')
    reminders = cursor.fetchall()
    conn.close()
    return render_template('reminder.html', reminders=reminders)


@app.route('/delete_reminder/<int:id>')
def delete_reminder(id):
    """Delete a skincare reminder."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reminders WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("🗑️ Reminder deleted successfully.", "info")
    return redirect(url_for('reminder'))


@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    """Track skincare expenditures, product purchases, and category breakdown."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        product = request.form.get('product', '').strip()
        amount_raw = request.form.get('amount', '0').strip()
        category = request.form.get('category', 'Skincare').strip()
        image = request.form.get('image', '').strip()

        try:
            amount = float(amount_raw)
        except ValueError:
            amount = 0.0

        if product and amount >= 0:
            date_today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                'INSERT INTO expenses (product, amount, date, category, image) VALUES (?, ?, ?, ?, ?)',
                (product, amount, date_today, category, image)
            )
            conn.commit()
            flash(f"💳 Logged ₹{amount:.2f} for '{product}' in your skincare investment tracker!", "success")

        conn.close()
        return redirect(url_for('expenses'))

    cursor.execute('SELECT * FROM expenses ORDER BY id DESC')
    expenses_list = cursor.fetchall()
    total = sum(item['amount'] for item in expenses_list)

    # Calculate category-wise breakdown
    category_totals = {}
    for item in expenses_list:
        cat = item['category'] or 'General'
        category_totals[cat] = category_totals.get(cat, 0.0) + (item['amount'] or 0.0)

    # Fetch all catalog products for quick expense logging & selling picker
    cursor.execute('SELECT * FROM products ORDER BY category ASC, name ASC')
    all_products = cursor.fetchall()

    conn.close()
    return render_template(
        'expenses.html',
        expenses=expenses_list,
        total=total,
        category_totals=category_totals,
        catalog_products=all_products
    )


@app.route('/delete_expense/<int:id>')
def delete_expense(id):
    """Delete a tracked expense item."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("🗑️ Expense item removed successfully.", "info")
    return redirect(url_for('expenses'))


@app.route('/buy_product/<int:id>', methods=['GET', 'POST'])
def buy_product(id):
    """Instant one-click product purchase & log to expenses tracker."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()

    if not product:
        conn.close()
        flash("Product not found.", "danger")
        return redirect(url_for('products'))

    # Record into expenses
    date_today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute(
        'INSERT INTO expenses (product, amount, date, category, image) VALUES (?, ?, ?, ?, ?)',
        (product['name'], product['price'], date_today, product['category'], product['image'])
    )

    # Also log to orders table
    cursor.execute('''
        INSERT INTO orders (customer_name, phone, email, address, city, pincode, payment_method, total_amount, order_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('GlowCare Member', '9876543210', 'member@glowcare.skin', 'Online Direct Purchase', 'Mumbai', '400001', 'Direct Checkout', product['price'], date_today, 'Order Confirmed'))
    order_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO order_items (order_id, product_id, product_name, price, quantity)
        VALUES (?, ?, ?, ?, ?)
    ''', (order_id, product['id'], product['name'], product['price'], 1))

    conn.commit()
    conn.close()

    flash(f"✨ Successfully purchased & logged '{product['name']}' (₹{product['price']:.2f}) into your expenses!", "success")
    return redirect(url_for('expenses'))


@app.route('/quick_add_routine/<int:id>', methods=['GET', 'POST'])
def quick_add_routine(id):
    """Quickly add a curated shelf product to user's AM/PM routine."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()

    if product:
        routine_time = 'Morning' if product['category'] in ['Sunscreen', 'Cleanser'] else 'Night'
        notes = f"{product['brand']} ({product['category']}) - {product['skin_type']}"
        cursor.execute(
            'INSERT INTO routine (product, routine_time, notes) VALUES (?, ?, ?)',
            (product['name'], routine_time, notes)
        )
        conn.commit()
        flash(f"🧴 Added '{product['name']}' to your {routine_time} routine!", "success")

    conn.close()
    return redirect(url_for('routine'))


@app.route('/api/products')
def api_products():
    """Return JSON catalog of all 30 products for live UI search & filtering."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()
    return {'products': [dict(r) for r in rows]}


@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    """Schedule and manage dermatologist and clinical clinic appointments."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        date = request.form.get('date', '').strip()
        time = request.form.get('time', '').strip()
        reason = request.form.get('reason', '').strip()

        if name and date and time:
            cursor.execute(
                'INSERT INTO appointments (name, date, time, reason) VALUES (?, ?, ?, ?)',
                (name, date, time, reason)
            )
            conn.commit()
            flash("🩺 Clinical appointment booked successfully!", "success")
        conn.close()
        return redirect(url_for('appointment'))

    cursor.execute('SELECT * FROM appointments ORDER BY date ASC, time ASC')
    appointments_list = cursor.fetchall()
    conn.close()
    return render_template('appointment.html', appointments=appointments_list)


@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    """Delete or cancel a dermatologist appointment."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM appointments WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("🗑️ Appointment cancelled successfully.", "info")
    return redirect(url_for('appointment'))


@app.route('/products')
def products():
    """Display curated skincare product shelf with 30 items, filtering, and direct purchasing."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products ORDER BY id ASC')
    rows = cursor.fetchall()

    # Get unique categories and their counts
    cursor.execute('SELECT category, COUNT(*) as count FROM products GROUP BY category ORDER BY count DESC')
    cat_counts = cursor.fetchall()
    conn.close()

    product_list = []
    for r in rows:
        p_dict = dict(r)
        p_dict['desc'] = p_dict.get('description', '')
        product_list.append(p_dict)

    return render_template('products.html', products=product_list, cat_counts=cat_counts)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Display and manage user skin ID profile."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age_raw = request.form.get('age', '0').strip()
        skin_type = request.form.get('skin_type', 'Normal')
        concern = request.form.get('concern', 'No Major Concern')

        try:
            age = int(age_raw)
        except ValueError:
            age = 0

        # Check if profile already exists
        cursor.execute('SELECT id FROM profile ORDER BY id DESC LIMIT 1')
        existing = cursor.fetchone()

        if existing:
            cursor.execute('''
                UPDATE profile
                SET name = ?, age = ?, skin_type = ?, concern = ?
                WHERE id = ?
            ''', (name, age, skin_type, concern, existing['id']))
        else:
            cursor.execute('''
                INSERT INTO profile (name, age, skin_type, concern)
                VALUES (?, ?, ?, ?)
            ''', (name, age, skin_type, concern))

        conn.commit()
        conn.close()
        flash("✨ Skin ID Profile updated successfully!", "success")
        return redirect(url_for('profile'))

    cursor.execute('SELECT * FROM profile ORDER BY id DESC LIMIT 1')
    user_profile = cursor.fetchone()
    conn.close()
    return render_template('profile.html', profile=user_profile)


# Initialize DB on module load / startup
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)