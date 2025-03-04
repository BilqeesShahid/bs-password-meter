import re
import streamlit as st
import random
import string


# Sidebar with project information
st.sidebar.title("📌 About This Project")
st.sidebar.markdown(
    """
    **💪 Password Strength Meter**
    
    - ✅ **Objective:** Evaluate password strength based on security rules.
    - ✅ **Features:**
      - Analyze password length, character types, and patterns.
      - Assign a strength score (Weak, Moderate, Strong).
      - Provide feedback for weak passwords.
      - Generate strong passwords.
    - ✅ **Password Criteria:**
      - At least 8 characters long.
      - Contains uppercase & lowercase letters.
      - Includes at least one digit (0-9).
      - Has one special character (!@#$%^&*).
    
    **📝 Scoring System:**
    - ✅ Weak (1-2): Short, missing key elements.
    - ✅ Moderate (3-4): Good but missing some security features.
    - ✅ Strong (5): Meets all criteria.
    
    **💡 Feedback System**
    - ✅ If the password is **weak**, it suggests improvements.
    - ✅ If the password is **moderate**, it provides additional recommendations.
    - ✅ If the password is **strong**, it displays a success message.
    """
)


# Apply Custom CSS for Enhanced UI
st.markdown(
    """
    <style>
        /* Title Styling */
       .custom-title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: #211C84; /* Blue Color */
        }
        /* Subtitle Styling */
        .subtitle {
            font-size: 20px;
            font-weight: bold;
            color: #0056b3; /* Dark Blue */
        }
        /* Button Styling */
        .stButton > button {
            background-color: #007BFF;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px 20px;
            transition: 0.3s;
            border: none;
             width: 100% !important;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
        /* Password Input Field */
        .password-box {
            border: 2px solid #007BFF;
            border-radius: 8px;
            padding: 10px;
            display: flex;
            align-items: center;
        }
        .password-box input {
            flex: 1;
            border: none;
            font-size: 18px;
            outline: none;
        }
        .password-box .icon {
            color: #007BFF;
            font-size: 22px;
            margin-right: 10px;
        }
        /* Custom Slider */
        div[data-baseweb="slider"] {
            padding: 10px 0;
        }
        div[data-baseweb="slider"] .css-1dp5vir {
            background: #007BFF !important;
        }
        div[data-baseweb="slider"] .css-13b4uab {
            background: #007BFF !important;
            border: 2px solid white;
            width: 16px;
            height: 16px;
            border-radius: 50%;
        }
        .custom-text {
        color:  #0056b3;
        font-weight: bold;
    }
        
        /* Success, Warning, Error Messages */
        .stSuccess { color: #388E3C !important; font-weight: bold; }
        .stWarning { color: #E65100 !important; font-weight: bold; }
        .stError { color: #D32F2F !important; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

# List of weak passwords to reject
COMMON_PASSWORDS = {"password", "123456", "qwerty", "password123", "admin", "letmein", "welcome"}

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Check if password is in the common password list
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("📖 This password is too common. Choose a unique one.")
        return 1, feedback

    # Check password length (minimum 8 characters)
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("📖 Password should be at least 8 characters long.")

    # Check for uppercase and lowercase letters
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("📖 Include both uppercase and lowercase letters.")

    # Check for at least one digit
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("📖 Add at least one number (0-9).")

    # Check for at least one special character
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("📖 Include at least one special character (!@#$%^&*).")

    return score, feedback

# Function to generate a strong password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Streamlit UI
st.markdown('<h1 class="custom-title">🛡️ Password Strength Meter</h1>', unsafe_allow_html=True)
st.markdown("""This app helps you evaluate your password strength and generate secure passwords.
    """)
# Slider to choose password length with improved design
st.markdown('<p class="subtitle">📏 Choose Password Length:</p>', unsafe_allow_html=True)
password_length = st.slider("", min_value=8, max_value=20, value=12)

# Input field for password with custom styling
st.markdown('<p class="subtitle">🔑 Enter Your Password:</p>', unsafe_allow_html=True)
password = st.text_input("", type="password")

# Live length validation (BEFORE checking strength)
if password:
    if len(password) < password_length:
        st.warning(f"⚠️ Your password is **too short**! You selected {password_length}, but entered {len(password)}.")
    elif len(password) > password_length:
        st.warning(f"⚠️ Your password is **too long**! You selected {password_length}, but entered {len(password)}.")
    else:
        st.success("✅ Password length is correct!")


# Button to check password strength (only if length matches)
if st.button("🔍 Check Strength"):
    if password:
        if len(password) != password_length:
            st.error("❌ Fix password length first!")
        else:
            score, feedback = check_password_strength(password)
            if score == 5:
                st.success("🎉 Excellent password! Your digital security is in good hands.")
                st.balloons()  # 🎈 Balloons for strong password
            elif score in [3, 4]:
                st.warning("📝 Moderate Password - Improve it with extra security measures.")
            else:
                st.error("❌ Weak Password - Improve it using the suggestions below.")

            # Display feedback with notebook icon
            for msg in feedback:
                st.write(f" {msg}")
    else:
        st.error("❌ Please enter a password to check its strength.")


# Button to generate a strong password
if st.button("⚡ Generate Strong Password"):
    strong_password = generate_password(password_length)
    st.success(f"🔑 Suggested Strong Password: **{strong_password}**")
    
# Styled heading
st.markdown('<p class="custom-text">💡 Password Security Tips</p>', unsafe_allow_html=True)

# Expander with plain text title
with st.expander("Click to view security tips"):
    st.markdown(
        """
        ### Tips for Creating Secure Passwords
        
        - **Use Long Passwords**: Aim for at least 12 characters  
        - **Mix Character Types**: Include uppercase, lowercase, numbers, and symbols  
        - **Avoid Personal Information**: Don't use names, birthdates, or common words  
        - **Use Different Passwords**: Each account should have a unique password  
        - **Consider a Password Manager**: Tools like LastPass, 1Password, or Bitwarden can help  
        - **Change Passwords Regularly**: Update important passwords every 3-6 months  

        Remember, the strongest passwords are random and not based on predictable patterns!  
        """,
        unsafe_allow_html=True
    )
