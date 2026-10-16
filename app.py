import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="JE Global Logistics LLC - TMS Portal", page_icon="🚛", layout="wide")

# High-Contrast Professional Styling (JE Global Logistics LLC Branding)
st.markdown("""
<style>
    /* Page Background & Font Contrast */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    /* Header Banner */
    .brand-header {
        background-color: #0F172A;
        padding: 22px 25px;
        border-radius: 10px;
        border-left: 8px solid #EAB308;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }
    .brand-header h1 {
        color: #FFFFFF !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: 0.5px;
    }
    .brand-header p {
        color: #E2E8F0 !important;
        font-size: 14px !important;
        margin-top: 6px !important;
        margin-bottom: 0 !important;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-top: 4px solid #0F172A !important;
        padding: 16px !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-weight: 700 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border: 1px solid #0F172A !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #1E293B !important;
        color: #EAB308 !important;
        border-color: #EAB308 !important;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: #E2E8F0;
        border-radius: 6px 6px 0 0;
        color: #334155 !important;
        font-weight: 600;
        padding: 10px 18px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
    }

    /* RateCon Box */
    .ratecon-box {
        border: 2px solid #0F172A;
        padding: 20px;
        border-radius: 8px;
        background-color: #FFFFFF;
        color: #0F172A;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .ratecon-header {
        color: #0F172A;
        margin: 0;
        font-weight: 800;
    }
    .ratecon-clause {
        color: #DC2626;
        font-weight: 700;
        background-color: #FEF2F2;
        padding: 8px 12px;
        border-radius: 4px;
        border-left: 4px solid #DC2626;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session Database
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

# Sidebar Authentication
st.sidebar.title("🔐 Corporate Login")
user_emails = [u['email'] for u in st.session_state.users]

if not user_emails:
    st.error("No users registered in system.")
    st.stop()

sel_email = st.sidebar.selectbox("Select Active Account", user_emails)
curr_u = next((u for u in st.session_state.users if u['email'] == sel_email), st.session_state.users[0])

st.sidebar.write(f"**Logged User:** {curr_u['name']}")
st.sidebar.write(f"**Access Level:** `{curr_u['role'].upper()}`")

if curr_u['role'] == 'admin':
    admin_mode = st.sidebar.radio("Admin Operating Mode", ["Company Overview (All Brokers)", "My Active Book (Owner Broker)"])
else:
    admin_mode = "Broker Mode"

st.sidebar.markdown("---")
st.sidebar.info("**JE Global Logistics LLC**\n7901 4th St N STE 300\nSt. Petersburg FL 33702\n\n*Special Terms: We dont pay detention, delays or tonu.*")

# Header Section
st.markdown("""
<div class="brand-header">
    <h1>JE GLOBAL LOGISTICS LLC</h1>
    <p>Enterprise Transportation Management System & Multi-Freight Dispatch Portal</p>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tabs_list = ["📊 Dashboard", "📦 Load Dispatch", "👥 Customers (CRM)", "🛡️ Carriers & Documents", "📝 RateCon & Signature Hub"]
if curr_u['role'] == 'admin':
    tabs_list.append("⚙️ User Management")

tabs = st.tabs(tabs_list)

# TAB 1: DASHBOARD
with tabs[0]:
    st.subheader("Brokerage Financial Dashboard")
    loads_v = st.session_state.loads if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [l for l in st.session_state.loads if l['broker_id'] == curr_u['id']]
    rev = sum(l['client_total'] for l in loads_v)
    dpay = sum(l['driver_pay'] for l in loads_v)
    profit = sum(l['broker_fee'] for l in loads_v)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Client Revenue", f"${rev:,.2f}")
    c2.metric("Total Driver / Carrier Pay", f"${dpay:,.2f}")
    c3.metric("Net Brokerage Profit", f"${profit:,.2f}")
    st.markdown("---")
    if loads_v:
        st.dataframe(pd.DataFrame(loads_v)[['id', 'customer', 'commodity', 'trailer', 'client_total', 'driver_pay', 'broker_fee', 'status']], use_container_width=True)
    else:
        st.info("No active loads in current view.")

# TAB 2: LOAD DISPATCH
with tabs[1]:
    st.subheader("Dispatch & Order Entry (All Freight Types)")
    with st.expander("➕ Create New Load Order", expanded=False):
        with st.form("new_load_form"):
            st.markdown("#### 1. Customer Information")
            col1, col2, col3 = st.columns(3)
            ctype = col1.selectbox("Customer Status", ["Repeated Customer", "New Customer"])
            cname = col2.text_input("Customer Name*")
            cphone = col3.text_input("Customer Phone*")
            cemail = st.text_input("Customer Email*")
            cbill = st.text_input("Billing Address*")
            
            st.markdown("#### 2. Route & Contacts")
            p_addr = st.text_input("Pick-Up Address*")
            d_addr = st.text_input("Delivery Address*")
            
            st.markdown("#### 3. Financial Breakdown")
            f1, f2 = st.columns(2)
            ctot = f1.number_input("Client Total ($)*", min_value=0.0, step=100.0)
            dpay_in = f2.number_input("Driver / Carrier Pay ($)*", min_value=0.0, step=100.0)
            st.info(f"Calculated Broker Fee: **${ctot - dpay_in:,.2f}**")
            
            st.markdown("#### 4. Freight Specs")
            s1, s2 = st.columns(2)
            comm = s1.text_input("Commodity Description*")
            trailer = s2.selectbox("Trailer Type*", ["Dry Van", "Reefer", "Car Hauler / Enclosed", "Car Hauler / Open", "Flatbed", "Stepdeck", "Lowboy / RGN", "LTL / Partial", "Hotshot"])
            weight = st.text_input("Weight (lbs)*")
            
            st.markdown("#### 5. Carrier Information")
            cmc = st.text_input("Carrier MC# / DOT#*")
            car_name = st.text_input("Carrier Name*")
            car_email = st.text_input("Carrier Email (for Ratecon)*")
            disp_contact = st.text_input("Dispatch Contact Name*")
            drv_phone = st.text_input("Driver Phone Number")
            p_date = st.date_input("Pick Up Date", datetime.date.today())
            d_date = st.date_input("Delivery Date", datetime.date.today() + datetime.timedelta(days=3))
            
            submit = st.form_submit_button("Save Load & Prepare Ratecon")
            if submit:
                new_id = f"JE-2026-{len(st.session_state.loads)+1001}"
                st.session_state.loads.append({
                    'id': new_id, 'broker_id': curr_u['id'], 'customer': cname, 'type': ctype, 'phone': cphone, 'email': cemail, 'billing': cbill, 'pickup': p_addr, 'delivery': d_addr,
                    'client_total': float(ctot), 'driver_pay': float(dpay_in), 'broker_fee': float(ctot - dpay_in), 'commodity': comm, 'year': '', 'make': '', 'model': '', 'dims': '', 'weight': weight, 'trailer': trailer,
                    'mc': cmc, 'carrier': car_name, 'dispatch': disp_contact, 'driver_phone': drv_phone, 'car_email': car_email, 'c_pay_meth': 'QuickPay', 'p_date': str(p_date), 'd_date': str(d_date),
                    'status': 'Awaiting Carrier Signature', 'signed_by': None, 'signed_date': None
                })
                st.success(f"Load {new_id} Created Successfully!")
                st.rerun()

    st.markdown("### Active Dispatch Orders")
    l_disp = st.session_state.loads if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [l for l in st.session_state.loads if l['broker_id'] == curr_u['id']]
    for ld in l_disp:
        st.write(f"📦 **{ld['id']}** | {ld['customer']} | {ld['commodity']} ({ld['trailer']}) | Carrier Pay: **${ld['driver_pay']:,.2f}** | Broker Margin: **${ld['broker_fee']:,.2f}** | Status: **{ld['status']}**")

# TAB 3: CUSTOMERS
with tabs[2]:
    st.subheader("Customers Directory (Isolated by Broker)")
    cust_v = st.session_state.clients if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [c for c in st.session_state.clients if c['broker_id'] == curr_u['id']]
    st.dataframe(pd.DataFrame(cust_v), use_container_width=True)

# TAB 4: CARRIERS & DOCUMENTS
with tabs[3]:
    st.subheader("Carrier Directory & Document Vault")
    st.caption("Required Certificate Holder: JE Global Logistics LLC | 7901 4th St N STE 300 St. Petersburg FL 33702")
    with st.expander("📥 Upload Carrier Compliance Documents (W9, COI, Authority)", expanded=False):
        with st.form("doc_upload_form"):
            mc_in = st.text_input("MC# / DOT#*")
            car_in = st.text_input("Carrier Name*")
            ph_in = st.text_input("Phone*")
            em_in = st.text_input("Email*")
            w9_f = st.file_uploader("Upload W9 Form", type=['pdf', 'png', 'jpg'])
            coi_f = st.file_uploader("Upload COI", type=['pdf', 'png', 'jpg'])
            auth_f = st.file_uploader("Upload Authority Certificate", type=['pdf', 'png', 'jpg'])
            drv_in = st.text_input("Driver First/Last Name & Phone Number*")
            sub_doc = st.form_submit_button("Upload Documents to Database")
            if sub_doc:
                st.session_state.carriers.append({
                    'mc': mc_in, 'name': car_in, 'phone': ph_in, 'email': em_in, 'w9': w9_f is not None, 'coi': coi_f is not None, 'auth': auth_f is not None, 'driver': drv_in, 'safer': False, 'motus': False, 'scam_call': False, 'status': 'Pending Admin Review'
                })
                st.success("Carrier documents uploaded successfully!")
                st.rerun()

    st.markdown("### Carrier Directory & Verification Queue")
    for car in st.session_state.carriers:
        with st.expander(f"🚛 {car['name']} ({car['mc']}) - Status: {car['status']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Phone:** {car['phone']} | **Email:** {car['email']}")
                st.write(f"**Driver Info:** {car['driver']}")
                st.write(f"- W9: {'✅ Uploaded' if car['w9'] else '❌ Missing'}")
                st.write(f"- COI: {'✅ Uploaded' if car['coi'] else '❌ Missing'}")
                st.write(f"- Authority Cert: {'✅ Uploaded' if car['auth'] else '❌ Missing'}")
            with col2:
                if curr_u['role'] == 'admin':
                    st.write("**Admin Verification Controls:**")
                    s_chk = st.checkbox("SAFER Active Status Verified", value=car['safer'], key=f"s_{car['mc']}")
                    m_chk = st.checkbox("Motus Safety Rating Verified", value=car['motus'], key=f"m_{car['mc']}")
                    c_chk = st.checkbox("Anti-Scam Phone Call Check (Official SAFER Number)", value=car['scam_call'], key=f"c_{car['mc']}")
                    if st.button(f"Approve Carrier {car['mc']}", key=f"btn_{car['mc']}"):
                        car['safer'] = s_chk
                        car['motus'] = m_chk
                        car['scam_call'] = c_chk
                        car['status'] = "Approved"
                        st.success("Carrier Approved!")
                        st.rerun()

# TAB 5: RATECON & E-SIGNATURE HUB
with tabs[4]:
    st.subheader("Rate Confirmation & E-Signature Hub")
    if st.session_state.loads:
        sel_id = st.selectbox("Select Order to View Ratecon", [l['id'] for l in st.session_state.loads])
        ld_t = next(l for l in st.session_state.loads if l['id'] == sel_id)
        
        st.markdown(f'''
        <div class="ratecon-box">
            <h3 class="ratecon-header">JE GLOBAL LOGISTICS LLC - RATE CONFIRMATION</h3>
            <p style="margin:2px 0; font-size:13px; color:#475569;">7901 4th St N STE 300 St. Petersburg FL 33702 | Phone: (800) 555-0199</p>
            <hr style="border-top:1px solid #CBD5E1; margin:12px 0;">
            <p><b>Order ID:</b> {ld_t['id']} | <b>Pickup Date:</b> {ld_t['p_date']} | <b>Delivery Date:</b> {ld_t['d_date']}</p>
            <p><b>Carrier:</b> {ld_t['carrier']} ({ld_t['mc']}) | <b>Dispatch Contact:</b> {ld_t['dispatch']}</p>
            <p><b>Driver Phone:</b> {ld_t['driver_phone']}</p>
            <p><b>Route:</b> {ld_t['pickup']} ➔ {ld_t['delivery']}</p>
            <p><b>Commodity:</b> {ld_t['commodity']} ({ld_t['trailer']}) | Weight: {ld_t['weight']}</p>
            <p style="font-size:20px; color:#0F172A; margin-top:10px;"><b>CARRIER PAY: ${ld_t['driver_pay']:,.2f} USD</b></p>
            <div class="ratecon-clause">*** SPECIAL TERMS: We dont pay detention, delays or tonu. ***</div>
            <hr style="border-top:1px solid #CBD5E1; margin:12px 0;">
            <p><b>E-Signature Status:</b> <b>{ld_t['status']}</b></p>
        </div>
        ''', unsafe_allow_html=True)
        
        if ld_t['signed_date']:
            st.success(f"Signed By: {ld_t['signed_by']} on {ld_t['signed_date']}")
        else:
            st.warning("Awaiting Carrier Signature...")
            
        st.markdown("---")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button("📧 Email Ratecon to Carrier for E-Signature"):
                ld_t['status'] = 'Awaiting Carrier Signature'
                st.success(f"Ratecon sent to {ld_t['car_email']}!")
        with col_s2:
            signer = st.text_input("Carrier Representative Name", value=ld_t['dispatch'])
            if st.button("✍️ Simulate Carrier E-Sign"):
                ld_t['status'] = 'Signed & Confirmed'
                ld_t['signed_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                ld_t['signed_by'] = f"{signer} ({ld_t['carrier']})"
                st.balloons()
                st.success("✅ Ratecon E-Signed and confirmed! Admin & Broker notified.")
                st.rerun()

# TAB 6: USER MANAGEMENT (ADMIN ONLY)
if curr_u['role'] == 'admin':
    with tabs[5]:
        st.subheader("⚙️ User & Access Management")
        st.caption("Manage corporate accounts and active broker permissions for @jegloballogistics.com")
        
        col_u1, col_u2 = st.columns(2)
        
        # Add User Form
        with col_u1:
            st.markdown("### ➕ Add New User / Broker")
            with st.form("add_user_form"):
                u_name = st.text_input("Full Name*")
                u_email = st.text_input("Corporate Email (@jegloballogistics.com)*")
                u_role = st.selectbox("Role", ["broker", "admin"])
                add_sub = st.form_submit_button("Add User to System")
                
                if add_sub:
                    if u_email in [u['email'] for u in st.session_state.users]:
                        st.error("User with this email already exists!")
                    elif not u_name or not u_email:
                        st.error("Please fill in both Name and Email.")
                    else:
                        new_u_id = f"b{len(st.session_state.users)+1}"
                        st.session_state.users.append({
                            'id': new_u_id,
                            'name': u_name,
                            'email': u_email,
                            'role': u_role
                        })
                        st.success(f"User {u_name} ({u_email}) added successfully!")
                        st.rerun()

        # Remove User Form
        with col_u2:
            st.markdown("### 🗑️ Remove User / Broker")
            removable_users = [u for u in st.session_state.users if u['email'] != curr_u['email']]
            if removable_users:
                user_to_remove = st.selectbox("Select User to Remove", [f"{u['name']} ({u['email']})" for u in removable_users])
                rem_email = user_to_remove.split("(")[1].replace(")", "").strip()
                
                if st.button("❌ Delete Selected User", type="primary"):
                    st.session_state.users = [u for u in st.session_state.users if u['email'] != rem_email]
                    st.success(f"User {rem_email} has been removed from the platform.")
                    st.rerun()
            else:
                st.info("No other users available to remove.")

        st.markdown("---")
        st.markdown("### Current Active Users Directory")
        st.dataframe(pd.DataFrame(st.session_state.users), use_container_width=True)
