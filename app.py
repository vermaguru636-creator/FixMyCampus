import streamlit as st
import sqlite3
import random

# ==================================================
# DATABASE
# ==================================================

conn = sqlite3.connect("complaints.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id TEXT PRIMARY KEY,
    category TEXT,
    location TEXT,
    description TEXT,
    status TEXT
)
""")

conn.commit()

# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="FixMyCampus",
    page_icon="🏫",
    layout="wide"
)

# ==================================================
# SESSION STATE
# ==================================================

if "admin" not in st.session_state:
    st.session_state.admin = False

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# ==================================================
# LIGHT THEME / VISIBILITY FIX
# ==================================================

st.markdown("""
<style>

/* Main page */
.stApp {
    background-color: #f5f7fb;
    color: #172033;
}

/* Normal text */
p, label, span, div {
    color: #172033;
}

/* Headings */
h1, h2, h3, h4 {
    color: #102a43 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #d9e2ec;
}

section[data-testid="stSidebar"] * {
    color: #172033 !important;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #155eef, #0b4f9c);
    padding: 35px;
    border-radius: 20px;
    margin-bottom: 25px;
}

.hero h1,
.hero p {
    color: white !important;
}

/* Cards */
.card {
    background-color: #ffffff;
    border: 1px solid #d9e2ec;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 15px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

.card h2,
.card h3,
.card p {
    color: #172033 !important;
}

/* Input boxes */
input,
textarea {
    background-color: #ffffff !important;
    color: #172033 !important;
    border: 1px solid #9fb3c8 !important;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #172033 !important;
    border-color: #9fb3c8 !important;
}

div[data-baseweb="select"] span {
    color: #172033 !important;
}

/* File uploader */
section[data-testid="stFileUploader"] {
    background-color: #ffffff;
    border-radius: 12px;
}

/* Buttons */
.stButton > button {
    background-color: #155eef;
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #0b4f9c;
    color: white !important;
}

/* Metrics */
div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #d9e2ec;
    padding: 15px;
    border-radius: 12px;
}

div[data-testid="stMetric"] label {
    color: #52606d !important;
}

div[data-testid="stMetricValue"] {
    color: #102a43 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #52606d !important;
    padding: 30px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🏫 FixMyCampus")

st.sidebar.caption(
    "Smart Campus Complaint System"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "👨‍🎓 Student Portal",
        "🔐 Admin Portal"
    ],
    index=[
        "🏠 Home",
        "👨‍🎓 Student Portal",
        "🔐 Admin Portal"
    ].index(st.session_state.page)
)

st.session_state.page = page

st.sidebar.divider()

st.sidebar.info("Report • Track • Resolve")

# ==================================================
# HOME
# ==================================================

if page == "🏠 Home":

    st.markdown("""
    <div class="hero">
        <h1>🏫 FixMyCampus</h1>
        <p>Smart Campus Complaint Management System</p>
        <p>Report problems. Track progress. Improve your campus.</p>
    </div>
    """, unsafe_allow_html=True)

    st.header("Choose your portal")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="card">
            <h2>👨‍🎓 Student Portal</h2>
            <p>
            Report campus problems, upload photos,
            and track complaint progress.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Student Portal →",
            use_container_width=True
        ):
            st.session_state.page = "👨‍🎓 Student Portal"
            st.rerun()

    with col2:

        st.markdown("""
        <div class="card">
            <h2>🔐 Admin Portal</h2>
            <p>
            View complaints, manage issues,
            and update their status.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Admin Portal →",
            use_container_width=True
        ):
            st.session_state.page = "🔐 Admin Portal"
            st.rerun()

    st.divider()

    st.header("How FixMyCampus works")

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="card">
            <h3>📝 1. Report</h3>
            <p>Submit a campus issue with its location and description.</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card">
            <h3>🔎 2. Track</h3>
            <p>Use your complaint ID to check its current status.</p>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="card">
            <h3>✅ 3. Resolve</h3>
            <p>Admins update the issue until it is resolved.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        FixMyCampus • Smart Campus Management
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# STUDENT PORTAL
# ==================================================

elif page == "👨‍🎓 Student Portal":

    st.title("👨‍🎓 Student Portal")

    st.caption(
        "Report a campus issue or track an existing complaint."
    )

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Reported'"
    )
    reported = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='In Progress'"
    )
    progress = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Resolved'"
    )
    resolved = cursor.fetchone()[0]

    a, b, c, d = st.columns(4)

    with a:
        st.metric("Total", total)

    with b:
        st.metric("🟡 Reported", reported)

    with c:
        st.metric("🔵 In Progress", progress)

    with d:
        st.metric("🟢 Resolved", resolved)

    st.divider()

    st.header("📝 Report a Problem")

    with st.container(border=True):

        category = st.selectbox(
            "What is the problem?",
            [
                "Cleanliness",
                "Electricity",
                "Water",
                "Wi-Fi",
                "Classroom",
                "Other"
            ]
        )

        location = st.text_input(
            "📍 Location",
            placeholder="Example: Block A, Room 204"
        )

        description = st.text_area(
            "Describe the problem",
            placeholder="Explain what needs to be fixed..."
        )

        photo = st.file_uploader(
            "📸 Upload a photo",
            type=["jpg", "jpeg", "png"]
        )

        if photo:
            st.image(
                photo,
                caption="Uploaded Problem Photo",
                width=400
            )

        if st.button(
            "🚀 Submit Complaint",
            use_container_width=True
        ):

            if location and description:

                complaint_id = "FMC" + str(
                    random.randint(1000, 9999)
                )

                cursor.execute(
                    """
                    INSERT INTO complaints
                    (id, category, location, description, status)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        complaint_id,
                        category,
                        location,
                        description,
                        "Reported"
                    )
                )

                conn.commit()

                st.success(
                    "Complaint submitted successfully! 🎉"
                )

                st.info(
                    "Your Complaint ID: "
                    + complaint_id
                )

            else:

                st.warning(
                    "Please enter the location and description."
                )

    st.divider()

    st.header("🔎 Track Your Complaint")

    with st.container(border=True):

        track_id = st.text_input(
            "Complaint ID",
            placeholder="Example: FMC1234"
        )

        if st.button(
            "Track Complaint",
            use_container_width=True
        ):

            cursor.execute(
                """
                SELECT category, location, description, status
                FROM complaints
                WHERE id=?
                """,
                (track_id,)
            )

            complaint = cursor.fetchone()

            if complaint:

                category, location, description, status = complaint

                st.success("Complaint found! ✅")

                st.write("**Category:**", category)
                st.write("**Location:**", location)
                st.write("**Description:**", description)

                if status == "Reported":
                    st.warning("🟡 Status: Reported")

                elif status == "In Progress":
                    st.info("🔵 Status: In Progress")

                else:
                    st.success("🟢 Status: Resolved")

            else:

                st.error(
                    "Complaint ID not found."
                )


# ==================================================
# ADMIN PORTAL
# ==================================================

elif page == "🔐 Admin Portal":

    if not st.session_state.admin:

        st.title("🔐 Admin Portal")

        st.caption(
            "Authorized personnel only."
        )

        password = st.text_input(
            "Admin Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if password == "admin123":

                st.session_state.admin = True
                st.rerun()

            else:

                st.error(
                    "Incorrect password."
                )

    else:

        st.title("🛠️ Admin Dashboard")

        st.caption(
            "Manage and resolve campus complaints."
        )

        if st.button("Logout"):
            st.session_state.admin = False
            st.rerun()

        cursor.execute(
            "SELECT COUNT(*) FROM complaints"
        )
        total = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM complaints WHERE status='Reported'"
        )
        reported = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM complaints WHERE status='In Progress'"
        )
        progress = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM complaints WHERE status='Resolved'"
        )
        resolved = cursor.fetchone()[0]

        a, b, c, d = st.columns(4)

        with a:
            st.metric("Total", total)

        with b:
            st.metric("🟡 Reported", reported)

        with c:
            st.metric("🔵 In Progress", progress)

        with d:
            st.metric("🟢 Resolved", resolved)

        st.divider()

        cursor.execute(
            """
            SELECT id, category, location,
                   description, status
            FROM complaints
            ORDER BY rowid DESC
            """
        )

        complaints = cursor.fetchall()

        if complaints:

            for complaint in complaints:

                complaint_id, category, location, description, status = complaint

                with st.container(border=True):

                    st.subheader(
                        "🎫 " + complaint_id
                    )

                    left, right = st.columns(2)

                    with left:

                        st.write(
                            "**Category:**",
                            category
                        )

                        st.write(
                            "**Location:**",
                            location
                        )

                    with right:

                        if status == "Reported":
                            st.warning("🟡 Reported")

                        elif status == "In Progress":
                            st.info("🔵 In Progress")

                        else:
                            st.success("🟢 Resolved")

                    st.write(
                        "**Description:**",
                        description
                    )

                    new_status = st.selectbox(
                        "Change Status",
                        [
                            "Reported",
                            "In Progress",
                            "Resolved"
                        ],
                        index=[
                            "Reported",
                            "In Progress",
                            "Resolved"
                        ].index(status),
                        key=complaint_id
                    )

                    if st.button(
                        "Update Status",
                        key="update_" + complaint_id,
                        use_container_width=True
                    ):

                        cursor.execute(
                            """
                            UPDATE complaints
                            SET status=?
                            WHERE id=?
                            """,
                            (
                                new_status,
                                complaint_id
                            )
                        )

                        conn.commit()

                        st.success(
                            "Status updated successfully! ✅"
                        )

                        st.rerun()

        else:

            st.info(
                "No complaints have been submitted yet."
            )

        st.markdown("""
        <div class="footer">
            FixMyCampus Admin • Complaint Management
        </div>
        """, unsafe_allow_html=True)
