import streamlit as st
import pandas as pd
import datetime

# Page Configuration
st.set_page_config(
    page_title="JE Global Logistics LLC - TMS Portal",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Brand Identity (Yellow/Gold #FFC000 & Charcoal Black #111827)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Brand Header Banner */
    .brand-header {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        padding: 22px 28px;
        border-radius: 12px;
        border-left: 8px solid #FFC000;
        margin-bottom: 22px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .brand-title {
        color: #FFFFFF;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin: 0;
    }
    
    .brand-title span {
        color: #FFC000;
    }
    
    .brand-subtitle {
        color: #D1D5DB;
        font-size: 13.5px;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #FFC000;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 800 !important;
    }

    /* Custom Buttons */
    .stButton > button {
        background-color: #FFC000 !important;
        color: #111827 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #E6B000 !important;
        box-shadow: 0 4px 12px rgba(255, 192, 0, 0.3) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #F3F4F6 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label {
        color: #FFC000 !important;
        font-weight: 700;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #E2E8F0;
        padding: 5px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 7px;
        color: #374151;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #111827 !important;
        color: #FFC000 !important;
        font-weight: 700;
    }

    /* Ratecon Card */
    .ratecon-card {
        background-color: #FFFFFF;
        border: 2px solid #FFC000;
        border-radius: 12px;
        padding: 22px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .legal-badge {
        background-color: #FEF2F2;
        border-left: 4px solid #DC2626;
        padding: 10px 14px;
        color: #991B1B;
        font-weight: 700;
        font-size: 13px;
        margin: 12px 0;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Database State Initialization
if 'db' not in st.session_state:
    st.session_state.db = True
    st.session_state.users = [
        {'id': 'admin', 'name': 'Admin (Owner)', 'email': 'admin@jegloballogistics.com', 'role': 'admin'},
        {'id': 'b1', 'name': 'John Doe (Broker 1)', 'email': 'jdoe@jegloballogistics.com', 'role': 'broker'},
        {'id': 'b2', 'name': 'Sarah Smith (Broker 2)', 'email': 'ssmith@jegloballogistics.com', 'role': 'broker'},
        {'id': 'b3', 'name': 'Mike Johnson (Broker 3)', 'email': 'mjohnson@jegloballogistics.com', 'role': 'broker'},
        {'id': 'b4', 'name': 'Alex Rivera (Broker 4)', 'email': 'arivera@jegloballogistics.com', 'role': 'broker'},
        {'id': 'b5', 'name': 'Emily Davis (Broker 5)', 'email': 'edavis@jegloballogistics.com', 'role': 'broker'},
        {'id': 'b6', 'name': 'Carlos Gomez (Broker 6)', 'email': 'cgomez@jegloballogistics.com', 'role': 'broker'},
    ]
    st.session_state.clients = [
        {'id': 'C101', 'name': 'Caterpillar Midwest', 'contact': 'David Miller', 'phone': '(312) 555-0199', 'email': 'dmiller@cat.com', 'address': 'Peoria, IL', 'broker_id': 'admin', 'type': 'Repeated'},
        {'id': 'C102', 'name': 'Apex Auto Haulers', 'contact': 'Robert Chen', 'phone': '(404) 555-0143', 'email': 'logistics@apex.com', 'address': 'Atlanta, GA', 'broker_id': 'b1', 'type': 'Repeated'},
        {'id': 'C103', 'name': 'Titan Steel & General Freight', 'contact': 'Amanda Ross', 'phone': '(713) 555-0188', 'email': 'aross@titan.com', 'address': 'Houston, TX', 'broker_id': 'b2', 'type': 'New'},
    ]
    st.session_state.carriers = [
        {'mc': 'MC-987654', 'name': 'Eagle Express Logistics', 'phone': '(800) 555-8822', 'email': 'dispatch@eagle.com', 'w9': True, 'coi': True, 'auth': True, 'driver': 'James Wilson - (800) 555-8823', 'safer': True, 'motus': True, 'scam_call': True, 'status': 'Approved'},
        {'mc': 'MC-456123', 'name': 'Reliable Freight Lines', 'phone': '(888) 555-3344', 'email': 'pete@reliable.com', 'w9': True, 'coi': False, 'auth': True, 'driver': 'Pending', 'safer': True, 'motus': False, 'scam_call': False, 'status': 'Pending Admin Review'},
    ]
    st.session_state.loads = [
        {'id': 'JE-2026-1001', 'broker_id': 'admin', 'customer': 'Caterpillar Midwest', 'type': 'Repeated', 'phone': '(312) 555-0199', 'email': 'dmiller@cat.com', 'billing': 'Peoria, IL', 'pickup': 'Peoria, IL', 'delivery': 'Tampa, FL', 'client_total': 4500.0, 'driver_pay': 3600.0, 'broker_fee': 900.0, 'commodity': 'Heavy Equipment CAT D6', 'year': '2022', 'make': 'CAT', 'model': 'D6T', 'dims': 'L:22ft W:8.5ft H:10ft', 'weight': '42000 lbs', 'trailer': 'Lowboy / RGN', 'mc': 'MC-987654', 'carrier': 'Eagle Express', 'dispatch': 'Mark Stevens', 'driver_phone': '(800) 555-8823', 'car_email': 'dispatch@eagle.com', 'c_pay_meth': 'QuickPay', 'p_date': '2026-10-18', 'd_date': '2026-10-21', 'status': 'Signed & Confirmed', 'signed_by': 'Mark Stevens (Eagle Express)', 'signed_date': '2026-10-16 10:15 AM'},
        {'id': 'JE-2026-1002', 'broker_id': 'b1', 'customer': 'Apex Auto Haulers', 'type': 'Repeated', 'phone': '(404) 555-0143', 'email': 'logistics@apex.com', 'billing': 'Atlanta, GA', 'pickup': 'Atlanta, GA', 'delivery': 'Dallas, TX', 'client_total': 2800.0, 'driver_pay': 2200.0, 'broker_fee': 600.0, 'commodity': 'Automobiles (3 Sedans)', 'year': '2024', 'make': 'Toyota', 'model': 'Camry', 'dims': '45ft Enclosed', 'weight': '11500 lbs', 'trailer': 'Car Hauler / Enclosed', 'mc': 'MC-456123', 'carrier': 'Reliable Freight', 'dispatch': 'Pete Taylor', 'driver_phone': '(888) 555-3344', 'car_email': 'pete@reliable.com', 'c_pay_meth': 'Check on Delivery', 'p_date': '2026-10-20', 'd_date': '2026-10-22', 'status': 'Awaiting Carrier Signature', 'signed_by': None, 'signed_date': None},
    ]

# Sidebar Brand Header
st.sidebar.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <div style="background: #FFC000; color: #111827; font-weight: 900; font-size: 22px; padding: 10px; border-radius: 8px; letter-spacing: 1px;">
            JE GLOBAL
        </div>
        <div style="color: #FFFFFF; font-weight: 700; font-size: 14px; margin-top: 4px; letter-spacing: 2px;">
            LOGISTICS LLC
        </div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.title("🔐 Corporate Portal Login")
sel_email = st.sidebar.selectbox("Select User (@jegloballogistics.com)", [u['email'] for u in st.session_state.users])
curr_u = next(u for u in st.session_state.users if u['email'] == sel_email)

st.sidebar.markdown(f"""
    <div style="background: #1F2937; padding: 12px; border-radius: 8px; border-left: 4px solid #FFC000; margin-bottom: 15px;">
        <p style="margin:0; font-size:12px; color:#9CA3AF;">Logged User:</p>
        <p style="margin:0; font-weight:700; color:#FFFFFF;">{curr_u['name']}</p>
        <p style="margin:0; font-size:12px; color:#FFC000; font-weight:700;">ROLE: {curr_u['role'].upper()}</p>
    </div>
""", unsafe_allow_html=True)

if curr_u['role'] == 'admin':
    admin_mode = st.sidebar.radio("Admin Operating View", ["Company Overview (All Brokers)", "My Active Book (Owner Broker)"])
else:
    admin_mode = "Broker Mode"

st.sidebar.markdown("---")
st.sidebar.info("**JE Global Logistics LLC**\n7901 4th St N STE 300\nSt. Petersburg FL 33702\n*We dont pay detention, delays or tonu.*")

# Top Header Banner
st.markdown("""
    <div class="brand-header">
        <div class="brand-title">
            🚚 JE GLOBAL <span>LOGISTICS</span> TMS
        </div>
        <div class="brand-subtitle">
            Enterprise Freight Brokerage Platform — Black & Gold Edition | Cars, General Freight, Partials & Heavy Equipment
        </div>
    </div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
t1, t2, t3, t4, t5, t6 = st.tabs([
    "📊 Financial Dashboard", 
    "📦 Load Dispatch", 
    "👥 Customers (CRM)", 
    "🛡️ Carrier Vault", 
    "📝 RateCon & Signature", 
    "⚙️ User Management"
])

# TAB 1: DASHBOARD
with t1:
    st.subheader("Brokerage Financial & Operational Performance")
    loads_v = st.session_state.loads if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [l for l in st.session_state.loads if l['broker_id'] == curr_u['id']]
    
    rev = sum(l['client_total'] for l in loads_v)
    dpay = sum(l['driver_pay'] for l in loads_v)
    profit = sum(l['broker_fee'] for l in loads_v)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Client Revenue", f"${rev:,.2f}")
    c2.metric("Total Carrier / Driver Pay", f"${dpay:,.2f}")
    c3.metric("Broker Net Profit", f"${profit:,.2f}")
    
    st.markdown("---")
    st.markdown("### Active Shipments Summary")
    if loads_v:
        df_l = pd.DataFrame(loads_v)[['id', 'customer', 'commodity', 'trailer', 'client_total', 'driver_pay', 'broker_fee', 'status']]
        df_l.columns = ['Load ID', 'Customer', 'Commodity', 'Trailer Type', 'Client Total ($)', 'Driver Pay ($)', 'Broker Fee ($)', 'Status']
        st.dataframe(df_l, use_container_width=True)

# TAB 2: LOAD DISPATCH
with t2:
    st.subheader("Dispatch & Order Entry (Multi-Freight Support)")
    with st.expander("➕ Create & Dispatch New Load", expanded=False):
        with st.form("new_load_form"):
            st.markdown("#### 1. Customer Details")
            col1, col2, col3 = st.columns(3)
            ctype = col1.selectbox("Customer Type", ["Repeated Customer", "New Customer"])
            cname = col2.text_input("Customer Name*")
            cphone = col3.text_input("Customer Phone*")
            cemail = st.text_input("Customer Email*")
            cbill = st.text_input("Billing Address*")
            
            st.markdown("#### 2. Route Specification")
            r1, r2 = st.columns(2)
            p_addr = r1.text_input("Pick-Up Address*")
            d_addr = r2.text_input("Delivery Address*")
            
            st.markdown("#### 3. Financial Agreement")
            f1, f2 = st.columns(2)
            ctot = f1.number_input("Client Total ($)*", min_value=0.0, step=100.0)
            dpay_in = f2.number_input("Carrier / Driver Pay ($)*", min_value=0.0, step=100.0)
            st.info(f"Auto-Calculated Broker Profit: **${ctot - dpay_in:,.2f}**")
            
            st.markdown("#### 4. Cargo & Equipment Specs")
            s1, s2, s3 = st.columns(3)
            comm = s1.text_input("Commodity Description*")
            trailer = s2.selectbox("Trailer Type*", [
                "Dry Van", "Reefer", "Car Hauler / Enclosed", "Car Hauler / Open", 
                "Flatbed", "Stepdeck", "Lowboy / RGN", "LTL / Partial", "Hotshot"
            ])
            weight = s3.text_input("Weight (lbs)*")
            
            st.markdown("#### 5. Assigned Carrier")
            c1_car, c2_car = st.columns(2)
            cmc = c1_car.text_input("Carrier MC# / DOT#*")
            car_name = c2_car.text_input("Carrier Company Name*")
            car_email = c1_car.text_input("Carrier Dispatch Email*")
            disp_contact = c2_car.text_input("Dispatch Contact Name*")
            drv_phone = st.text_input("Driver Direct Phone Number")
            
            p_date = st.date_input("Pick Up Date", datetime.date.today())
            d_date = st.date_input("Delivery Date", datetime.date.today() + datetime.timedelta(days=3))
            
            submit = st.form_submit_button("🚀 Submit Load & Create Order")
            if submit:
                new_id = f"JE-2026-{len(st.session_state.loads)+1001}"
                st.session_state.loads.append({
                    'id': new_id, 'broker_id': curr_u['id'], 'customer': cname, 'type': ctype, 'phone': cphone, 'email': cemail, 'billing': cbill, 'pickup': p_addr, 'delivery': d_addr,
                    'client_total': float(ctot), 'driver_pay': float(dpay_in), 'broker_fee': float(ctot - dpay_in), 'commodity': comm, 'year': '', 'make': '', 'model': '', 'dims': '', 'weight': weight, 'trailer': trailer,
                    'mc': cmc, 'carrier': car_name, 'dispatch': disp_contact, 'driver_phone': drv_phone, 'car_email': car_email, 'c_pay_meth': 'QuickPay', 'p_date': str(p_date), 'd_date': str(d_date),
                    'status': 'Awaiting Carrier Signature', 'signed_by': None, 'signed_date': None
                })
                st.success(f"Load Order {new_id} Successfully Created!")
                st.rerun()

    st.markdown("### Active Load Queue")
    l_disp = st.session_state.loads if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [l for l in st.session_state.loads if l['broker_id'] == curr_u['id']]
    for ld in l_disp:
        st.write(f"📦 **{ld['id']}** | {ld['customer']} | {ld['commodity']} ({ld['trailer']}) | Carrier Pay: **${ld['driver_pay']:,.2f}** | Broker Margin: **${ld['broker_fee']:,.2f}** | Status: `{ld['status']}`")

# TAB 3: CUSTOMERS
with t3:
    st.subheader("Customer Relationship Directory (Broker Isolated)")
    cust_v = st.session_state.clients if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [c for c in st.session_state.clients if c['broker_id'] == curr_u['id']]
    st.dataframe(pd.DataFrame(cust_v), use_container_width=True)

# TAB 4: CARRIERS & DOCUMENTS
with t4:
    st.subheader("Carrier Directory & Compliance Document Vault")
    st.caption("Mandatory Certificate Holder: **JE Global Logistics LLC | 7901 4th St N STE 300 St. Petersburg FL 33702**")
    
    with st.expander("📥 Register Carrier & Upload Compliance Files (W9, COI, Authority)", expanded=False):
        with st.form("doc_upload_form"):
            mc_in = st.text_input("MC# / DOT#*")
            car_in = st.text_input("Carrier Name*")
            ph_in = st.text_input("Phone Number*")
            em_in = st.text_input("Email Address*")
            w9_f = st.file_uploader("Upload W9 Form", type=['pdf', 'png', 'jpg'])
            coi_f = st.file_uploader("Upload COI (Certificate of Insurance)", type=['pdf', 'png', 'jpg'])
            auth_f = st.file_uploader("Upload Authority Certificate", type=['pdf', 'png', 'jpg'])
            drv_in = st.text_input("Driver Name & Phone Number*")
            
            sub_doc = st.form_submit_button("Save Carrier Documents")
            if sub_doc:
                st.session_state.carriers.append({
                    'mc': mc_in, 'name': car_in, 'phone': ph_in, 'email': em_in, 'w9': w9_f is not None, 'coi': coi_f is not None, 'auth': auth_f is not None, 'driver': drv_in, 'safer': False, 'motus': False, 'scam_call': False, 'status': 'Pending Admin Review'
                })
                st.success("Carrier documents uploaded successfully!")
                st.rerun()

    st.markdown("### Compliance Audit Queue")
    for car in st.session_state.carriers:
        with st.expander(f"🚛 {car['name']} ({car['mc']}) — Status: {car['status']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Contact:** {car['phone']} | {car['email']}")
                st.write(f"**Driver Assigned:** {car['driver']}")
                st.write(f"- W9 Form: {'✅ Verified' if car['w9'] else '❌ Missing'}")
                st.write(f"- COI (Cert Holder Verified): {'✅ Verified' if car['coi'] else '❌ Missing'}")
                st.write(f"- Authority Certificate: {'✅ Verified' if car['auth'] else '❌ Missing'}")
            with col2:
                if curr_u['role'] == 'admin':
                    st.write("**Admin Anti-Scam Security Checks:**")
                    s_chk = st.checkbox("SAFER Active Status Verified", value=car['safer'], key=f"s_{car['mc']}")
                    m_chk = st.checkbox("Motus Safety Rating Verified", value=car['motus'], key=f"m_{car['mc']}")
                    c_chk = st.checkbox("Anti-Scam Phone Call Check (Official SAFER Number)", value=car['scam_call'], key=f"c_{car['mc']}")
                    if st.button(f"Approve Carrier {car['mc']}", key=f"btn_{car['mc']}"):
                        car['safer'] = s_chk
                        car['motus'] = m_chk
                        car['scam_call'] = c_chk
                        car['status'] = "Approved"
                        st.success("Carrier Approved for Dispatch!")
                        st.rerun()

# TAB 5: RATECON & E-SIGNATURE HUB
with t5:
    st.subheader("Rate Confirmation & E-Signature Hub")
    sel_id = st.selectbox("Select Order ID", [l['id'] for l in st.session_state.loads])
    ld_t = next(l for l in st.session_state.loads if l['id'] == sel_id)
    
    st.markdown(f"""
    <div class="ratecon-card">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #FFC000; padding-bottom:10px;">
            <div>
                <h2 style="color:#111827; margin:0; font-weight:800;">JE GLOBAL LOGISTICS LLC</h2>
                <p style="margin:0; font-size:12px; color:#4B5563;">7901 4th St N STE 300 St. Petersburg FL 33702 | Phone: (800) 555-0199</p>
            </div>
            <div style="background:#111827; color:#FFC000; padding:8px 16px; border-radius:6px; font-weight:800;">
                RATE CONFIRMATION
            </div>
        </div>
        <br>
        <p><b>Order ID:</b> {ld_t['id']} | <b>Pick Up Date:</b> {ld_t['p_date']} | <b>Delivery Date:</b> {ld_t['d_date']}</p>
        <p><b>Carrier Name:</b> {ld_t['carrier']} ({ld_t['mc']}) | <b>Dispatch Contact:</b> {ld_t['dispatch']}</p>
        <p><b>Driver Phone:</b> {ld_t['driver_phone']}</p>
        <p><b>Route:</b> {ld_t['pickup']} ➔ {ld_t['delivery']}</p>
        <p><b>Commodity Specs:</b> {ld_t['commodity']} ({ld_t['trailer']}) | Weight: {ld_t['weight']}</p>
        <hr>
        <h3 style="color:#111827; margin:5px 0;">AGREED CARRIER PAY: <span style="color:#D97706;">${ld_t['driver_pay']:,.2f} USD</span></h3>
        
        <div class="legal-badge">
            ⚠️ SPECIAL MANDATORY TERMS: We dont pay detention, delays or tonu.
        </div>
        
        <p><b>E-Signature Status:</b> <span style="font-weight:700;">{ld_t['status']}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    if ld_t['signed_date']:
        st.success(f"✅ Signed By: {ld_t['signed_by']} on {ld_t['signed_date']}")
    else:
        st.warning("⏳ Status: Awaiting Carrier Representative Signature")
        
    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("📧 Email Ratecon to Carrier"):
            ld_t['status'] = 'Awaiting Carrier Signature'
            st.success(f"Ratecon emailed to {ld_t['car_email']}!")
    with col_s2:
        signer = st.text_input("Representative Full Name", value=ld_t['dispatch'])
        if st.button("✍️ Execute Carrier E-Sign"):
            ld_t['status'] = 'Signed & Confirmed'
            ld_t['signed_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            ld_t['signed_by'] = f"{signer} ({ld_t['carrier']})"
            st.balloons()
            st.success("✅ Ratecon E-Signed and confirmed! Admin and Broker notified.")
            st.rerun()

# TAB 6: USER MANAGEMENT
with t6:
    st.subheader("⚙️ Corporate User & Broker Management")
    st.caption("Manage corporate access for `@jegloballogistics.com` team members.")
    
    if curr_u['role'] == 'admin':
        with st.form("add_user_form"):
            st.markdown("#### Add New Team Member")
            u_col1, u_col2, u_col3 = st.columns(3)
            new_u_name = u_col1.text_input("Full Name*")
            new_u_email = u_col2.text_input("Corporate Email (@jegloballogistics.com)*")
            new_u_role = u_col3.selectbox("Role*", ["broker", "admin"])
            
            sub_u = st.form_submit_button("➕ Add User to Platform")
            if sub_u:
                if new_u_email and "@jegloballogistics.com" in new_u_email:
                    new_u_id = f"b{len(st.session_state.users)}"
                    st.session_state.users.append({
                        'id': new_u_id, 'name': new_u_name, 'email': new_u_email, 'role': new_u_role
                    })
                    st.success(f"User {new_u_name} ({new_u_email}) added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a valid corporate email ending in @jegloballogistics.com")
        
        st.markdown("### Active Platform Users")
        st.dataframe(pd.DataFrame(st.session_state.users), use_container_width=True)
    else:
        st.warning("User Management is restricted to Admin accounts.")
