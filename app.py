import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="JE Global Logistics LLC - TMS Portal", page_icon="🚛", layout="wide")

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
st.sidebar.title("🔐 Corporate User Login")
sel_email = st.sidebar.selectbox("Email (@jegloballogistics.com)", [u['email'] for u in st.session_state.users])
curr_u = next(u for u in st.session_state.users if u['email'] == sel_email)
st.sidebar.write(f"**User:** {curr_u['name']}")
st.sidebar.write(f"**Role:** `{curr_u['role'].upper()}`")

if curr_u['role'] == 'admin':
    admin_mode = st.sidebar.radio("Admin Operating View", ["Company Overview (All Brokers)", "My Active Book (Owner Broker)"])
else:
    admin_mode = "Broker Mode"

st.sidebar.markdown("---")
st.sidebar.info("**JE Global Logistics LLC**\n7901 4th St N STE 300\nSt. Petersburg FL 33702\n*We dont pay detention, delays or tonu.*")

st.title("JE Global Logistics LLC - Management Portal")
st.caption("Multi-Freight Transportation Management System (Cars, General Freight, Partials, Heavy Machinery)")

t1, t2, t3, t4, t5 = st.tabs(["📊 Dashboard", "📦 Load Dispatch", "👥 Customers (CRM)", "🛡️ Carriers & Documents", "📝 RateCon & Signature Hub"])

# TAB 1: DASHBOARD
with t1:
    st.subheader("Brokerage Financial Dashboard")
    loads_v = st.session_state.loads if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [l for l in st.session_state.loads if l['broker_id'] == curr_u['id']]
    rev = sum(l['client_total'] for l in loads_v)
    dpay = sum(l['driver_pay'] for l in loads_v)
    profit = sum(l['broker_fee'] for l in loads_v)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Client Revenue", f"${rev:,.2f}")
    c2.metric("Total Driver / Carrier Pay", f"${dpay:,.2f}")
    c3.metric("Broker Net Profit", f"${profit:,.2f}")
    st.markdown("---")
    if loads_v:
        st.dataframe(pd.DataFrame(loads_v)[['id', 'customer', 'commodity', 'trailer', 'client_total', 'driver_pay', 'broker_fee', 'status']], use_container_width=True)

# TAB 2: LOAD DISPATCH
with t2:
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
            st.markdown("#### 4. Freight Specs (Cars, General Freight, LTL, Heavy Equipment)")
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
                st.success(f"Load {new_id} Created!")
                st.rerun()
    st.markdown("### Active Orders")
    l_disp = st.session_state.loads if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [l for l in st.session_state.loads if l['broker_id'] == curr_u['id']]
    for ld in l_disp:
        st.write(f"📦 **{ld['id']}** | {ld['customer']} | {ld['commodity']} ({ld['trailer']}) | Carrier Pay: ${ld['driver_pay']:,.2f} | Broker Fee: ${ld['broker_fee']:,.2f} | Status: **{ld['status']}**")

# TAB 3: CUSTOMERS
with t3:
    st.subheader("Customers Directory (Isolated by Broker)")
    cust_v = st.session_state.clients if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [c for c in st.session_state.clients if c['broker_id'] == curr_u['id']]
    st.dataframe(pd.DataFrame(cust_v), use_container_width=True)

# TAB 4: CARRIERS & DOCUMENTS
with t4:
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
                st.success("Documents uploaded successfully!")
                st.rerun()
    st.markdown("### Carrier Directory & Verification Queue")
    for car in st.session_state.carriers:
        with st.expander(f"🚛 {car['name']} ({car['mc']}) - Status: {car['status']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Phone:** {car['phone']} | **Email:** {car['email']}")
                st.write(f"**Driver Info:** {car['driver']}")
                st.write(f"- W9: {'✅ Uploaded' if car['w9'] else '❌ Missing'}")
                st.write(f"- COI (Certificate Holder Verified): {'✅ Uploaded' if car['coi'] else '❌ Missing'}")
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
with t5:
    st.subheader("Rate Confirmation & E-Signature Hub")
    sel_id = st.selectbox("Select Order", [l['id'] for l in st.session_state.loads])
    ld_t = next(l for l in st.session_state.loads if l['id'] == sel_id)
    
    st.markdown(f'''
    <div style="border:2px solid #1E3A8A; padding:15px; border-radius:8px; background:#FFFFFF;">
        <h3 style="color:#1E3A8A; margin:0;">JE GLOBAL LOGISTICS LLC - RATE CONFIRMATION</h3>
        <p style="margin:0; font-size:12px;">7901 4th St N STE 300 St. Petersburg FL 33702 | Phone: (800) 555-0199</p>
        <hr>
        <p><b>Order ID:</b> {ld_t['id']} | <b>Pickup Date:</b> {ld_t['p_date']}</p>
        <p><b>Carrier:</b> {ld_t['carrier']} ({ld_t['mc']}) | <b>Dispatch Contact:</b> {ld_t['dispatch']}</p>
        <p><b>Driver Phone:</b> {ld_t['driver_phone']}</p>
        <p><b>Route:</b> {ld_t['pickup']} ➔ {ld_t['delivery']}</p>
        <p><b>Commodity:</b> {ld_t['commodity']} ({ld_t['trailer']}) | Weight: {ld_t['weight']}</p>
        <p style="font-size:18px; color:#1E3A8A;"><b>CARRIER PAY: ${ld_t['driver_pay']:,.2f} USD</b></p>
        <p style="color:red; font-weight:bold;">*** SPECIAL TERMS: We dont pay detention, delays or tonu. ***</p>
        <hr>
        <p><b>E-Signature Status:</b> <b>{ld_t['status']}</b></p>
    </div>
    ''', unsafe_allow_html=True)
    
    if ld_t['signed_date']:
        st.success(f"Signed By: {ld_t['signed_by']} on {ld_t['signed_date']}")
    else:
        st.warning("Awaiting Signature...")
        
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
