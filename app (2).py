import streamlit as st
import math


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Kraftcure Products Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .stApp {
        background: #f5f7fb;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* Top Header */
    .top-header {
        background: linear-gradient(135deg, #172554, #1e3a8a);
        border-radius: 16px;
        padding: 22px 28px;
        margin-bottom: 28px;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.15);
    }

    .header-badge {
        color: #93c5fd;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }

    .header-title {
        color: white;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 7px;
    }

    .header-subtitle {
        color: #dbeafe;
        font-size: 14px;
    }

    /* Section Styling */
    .step-label {
        color: #2563eb;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-top: 12px;
        margin-bottom: 5px;
    }

    .section-title {
        color: #1e293b;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 12px;
        margin-bottom: 14px;
    }

    /* Streamlit Inputs */
    .stSelectbox label,
    .stMultiSelect label,
    .stNumberInput label {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #334155 !important;
    }

    /* Divider */
    hr {
        margin-top: 24px !important;
        margin-bottom: 24px !important;
    }

    /* KPI Cards */
    .metric-card {
        border-radius: 16px;
        padding: 20px;
        min-height: 145px;
        color: white;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.12);
    }

    .metric-label {
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.3px;
        opacity: 0.85;
        margin-bottom: 20px;
    }

    .metric-value {
        font-size: 27px;
        font-weight: 800;
        margin-bottom: 16px;
    }

    .metric-note {
        font-size: 11px;
        opacity: 0.82;
    }

    .purple-card {
        background: linear-gradient(135deg, #3730a3, #6366f1);
    }

    .teal-card {
        background: linear-gradient(135deg, #0f766e, #14b8a6);
    }

    .orange-card {
        background: linear-gradient(135deg, #c2410c, #f97316);
    }

    .dark-card {
        background: linear-gradient(135deg, #1e293b, #475569);
    }

    /* Final Result */
    .final-card {
        background: linear-gradient(135deg, #1e40af, #2563eb);
        border-radius: 18px;
        padding: 28px;
        text-align: center;
        color: white;
        margin-top: 24px;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.22);
    }

    .final-label {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.8px;
        opacity: 0.9;
    }

    .final-value {
        font-size: 44px;
        font-weight: 800;
        margin-top: 10px;
    }

    .final-note {
        font-size: 12px;
        opacity: 0.85;
        margin-top: 8px;
    }

    /* Product Card */
    .product-name {
        font-size: 17px;
        font-weight: 750;
        color: #1e293b;
        padding-top: 8px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# BACKEND PRODUCT DATA
# ============================================================

GST_RATE = 18.0


PRODUCTS = {

    "PA": {
        "type": "insurer",
        "rates": {
            "Care": 12.00,
            "Aditya Birla": 21.186440677966104,
            "Cigna Manipal": 24.00,
        },
    },

    "Hospicash": {
        "type": "insurer",
        "rates": {
            "ZUNO": 150.00,
        },
    },

    "PA Hospicash": {
        "type": "insurer",
        "rates": {
            "Magma": 424.00,
            "Tata": 169.00,
        },
    },

    "PA + Cancer Specific": {
        "type": "fixed",
        "rates": {
            "Cigna Manipal": 180.00,
        },
    },

    "Cancer Specific": {
        "type": "fixed",
        "rates": {
            "Cigna Manipal": 156.00,
        },
    },

    "GTL": {
        "type": "insurer",
        "rates": {
            "IPRU": 450.00,
            "Aviva": 320.30,
        },
    },

    "PA + CI": {
        "type": "insurer",
        "rates": {
            "Magma": 270.00,
            "Cigna Manipal": 368.00,
        },
    },

    "CI": {
        "type": "fixed",
        "rates": {
            "Cigna Manipal": 344.00,
        },
    },

    "Health": {
        "type": "tier",
        "insurer": "Aditya Birla",
        "rates": {
            "Plan 1": 1879.00,
            "Plan 2": 2699.00,
            "Plan 3": 3369.00,
        },
    },
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def round_half_up(value):
    if value >= 0:
        return math.floor(value + 0.5)
    return math.ceil(value - 0.5)


def format_currency(value):

    value = round_half_up(value)

    return "₹{:,.0f}".format(value)


def get_sorted_insurers(rates):

    return sorted(
        rates.items(),
        key=lambda item: item[1]
    )


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="top-header">

    <div class="header-badge">
        POLICYGRACE • INTERNAL PRICING TOOL
    </div>

    <div class="header-title">
        Kraftcure Products Calculator
    </div>

    <div class="header-subtitle">
        Select products, configure insurers and calculate the final premium instantly.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# STEP 01 - SELECT PRODUCTS
# ============================================================

st.markdown("""
<div class="step-label">
STEP 01
</div>

<div class="section-title">
Select Products
</div>

<div class="section-subtitle">
Choose one or more insurance products to include in the quotation.
</div>
""", unsafe_allow_html=True)


selected_products = st.multiselect(
    "Which product(s) do you want to quote?",
    options=list(PRODUCTS.keys()),
    placeholder="Choose products"
)


product_choices = {}


# ============================================================
# STEP 02 - PRODUCT CONFIGURATION
# ============================================================

if selected_products:

    st.divider()

    st.markdown("""
    <div class="step-label">
        STEP 02
    </div>

    <div class="section-title">
        Product Configuration
    </div>

    <div class="section-subtitle">
        Select the insurer or available option for each product.
    </div>
    """, unsafe_allow_html=True)


    for product_name in selected_products:

        product = PRODUCTS[product_name]

        col1, col2 = st.columns([1, 2])


        with col1:

            st.markdown(
                f'<div class="product-name">{product_name}</div>',
                unsafe_allow_html=True
            )


        with col2:

            # ----------------------------------------
            # INSURER SELECTION
            # ----------------------------------------

            if product["type"] == "insurer":

                sorted_insurers = get_sorted_insurers(
                    product["rates"]
                )

                insurer_names = [
                    insurer
                    for insurer, rate in sorted_insurers
                ]


                selected_insurer = st.selectbox(
                    f"Select insurer for {product_name}",
                    insurer_names,
                    key=f"insurer_{product_name}"
                )


                selected_rate = product["rates"][
                    selected_insurer
                ]


                product_choices[product_name] = {
                    "insurer": selected_insurer,
                    "rate": selected_rate,
                    "option": "Standard"
                }


            # ----------------------------------------
            # FIXED PRODUCT
            # ----------------------------------------

            elif product["type"] == "fixed":

                insurer = list(
                    product["rates"].keys()
                )[0]

                rate = product["rates"][insurer]


                st.selectbox(
                    f"Insurer for {product_name}",
                    [insurer],
                    key=f"fixed_{product_name}"
                )


                product_choices[product_name] = {
                    "insurer": insurer,
                    "rate": rate,
                    "option": "Standard"
                }


            # ----------------------------------------
            # TIER PRODUCT
            # ----------------------------------------

            elif product["type"] == "tier":

                tier_options = list(
                    product["rates"].keys()
                )


                selected_tier = st.selectbox(
                    f"Select option for {product_name}",
                    tier_options,
                    key=f"tier_{product_name}"
                )


                rate = product["rates"][
                    selected_tier
                ]


                product_choices[product_name] = {
                    "insurer": product["insurer"],
                    "rate": rate,
                    "option": selected_tier
                }


# ============================================================
# STEP 03 - LOADING
# ============================================================

loading_percentage = 0.0


if selected_products:

    st.divider()

    st.markdown("""
    <div class="step-label">
        STEP 03
    </div>

    <div class="section-title">
        Enter Loading
    </div>

    <div class="section-subtitle">
        Add the required loading or partner commission percentage.
    </div>
    """, unsafe_allow_html=True)


    loading_percentage = st.number_input(
        "Loading Percentage (%)",
        min_value=0.0,
        max_value=99.0,
        value=0.0,
        step=0.5
    )


# ============================================================
# CALCULATE BUTTON
# ============================================================

if selected_products:

    calculate = st.button(
        "Calculate Premium",
        type="primary",
        use_container_width=True
    )

else:

    calculate = False

    st.info(
        "Select at least one product to calculate the premium."
    )


# ============================================================
# CALCULATION RESULTS
# ============================================================

if calculate:

    # --------------------------------------------------------
    # BASE PREMIUM
    # --------------------------------------------------------

    total_base_premium = sum(
        product_choices[product]["rate"]
        for product in selected_products
    )


    # --------------------------------------------------------
    # LOADING CALCULATION
    #
    # Loading is calculated by grossing up the base premium.
    #
    # Example:
    # Base = 100
    # Loading = 20%
    #
    # Final Before GST = 100 / 0.80 = 125
    # Partner Payout = 25
    # --------------------------------------------------------

    if loading_percentage < 100:

        premium_before_gst = (
            total_base_premium /
            (1 - loading_percentage / 100)
        )

    else:

        premium_before_gst = total_base_premium


    loading_amount = (
        premium_before_gst -
        total_base_premium
    )


    partner_payout = loading_amount


    # --------------------------------------------------------
    # GST
    # --------------------------------------------------------

    gst_amount = (
        premium_before_gst *
        GST_RATE / 100
    )


    final_premium = (
        premium_before_gst +
        gst_amount
    )


    # ========================================================
    # RESULTS HEADER
    # ========================================================

    st.divider()


    st.markdown("""
    <div class="step-label">
        STEP 04
    </div>

    <div class="section-title">
        Calculation Results
    </div>

    <div class="section-subtitle">
        Your calculated premium quotation.
    </div>
    """, unsafe_allow_html=True)


    # ========================================================
    # KPI CARDS
    # ========================================================

    card1, card2, card3, card4 = st.columns(4)


    with card1:

        st.markdown(
            f"""
            <div class="metric-card purple-card">

                <div class="metric-label">
                    BASE PREMIUM
                </div>

                <div class="metric-value">
                    {format_currency(total_base_premium)}
                </div>

                <div class="metric-note">
                    Combined selected product premium
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with card2:

        st.markdown(
            f"""
            <div class="metric-card teal-card">

                <div class="metric-label">
                    LOADING AMOUNT
                </div>

                <div class="metric-value">
                    {format_currency(loading_amount)}
                </div>

                <div class="metric-note">
                    Additional amount generated through loading
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with card3:

        st.markdown(
            f"""
            <div class="metric-card orange-card">

                <div class="metric-label">
                    PARTNER PAYOUT
                </div>

                <div class="metric-value">
                    {format_currency(partner_payout)}
                </div>

                <div class="metric-note">
                    Calculated partner commission amount
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with card4:

        st.markdown(
            f"""
            <div class="metric-card dark-card">

                <div class="metric-label">
                    GST AMOUNT
                </div>

                <div class="metric-value">
                    {format_currency(gst_amount)}
                </div>

                <div class="metric-note">
                    GST calculated at 18%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # FINAL PREMIUM
    # ========================================================

    st.markdown(
        f"""
        <div class="final-card">

            <div class="final-label">
                FINAL PREMIUM INCLUDING GST
            </div>

            <div class="final-value">
                {format_currency(final_premium)}
            </div>

            <div class="final-note">
                Premium before GST: {format_currency(premium_before_gst)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # SELECTED PRODUCT SUMMARY
    # ========================================================

    st.divider()


    st.markdown("""
    <div class="section-title" style="font-size:18px;">
        Selected Product Rates
    </div>

    <div class="section-subtitle">
        Product-wise backend premium configuration.
    </div>
    """, unsafe_allow_html=True)


    summary_data = []


    for product_name in selected_products:

        product_info = product_choices[product_name]


        summary_data.append({
            "Product": product_name,
            "Insurer": product_info["insurer"],
            "Rate": format_currency(
                product_info["rate"]
            )
        })


    st.dataframe(
        summary_data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<br>
<div style="
    text-align:center;
    color:#94a3b8;
    font-size:11px;
    font-weight:600;
">
    KRAFTCURE PRODUCTS CALCULATOR • POWERED BY POLICYGRACE
</div>
""", unsafe_allow_html=True)
