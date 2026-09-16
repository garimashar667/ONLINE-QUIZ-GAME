import streamlit as st
import time

# Page Configuration
st.set_page_config(page_title="🎮 Ultimate Game Quiz", page_icon="⚡", layout="centered")

# Custom CSS for Game-like Attractive UI (Background, Cards, Fonts)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a0845 100%);
        color: #ffffff;
    }
    .question-card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff4b2b 0%, #ff416c 100%);
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Epic Arcade Quiz Challenge")
st.write("Jaldi kijiye! Har question ke liye sirf **15 Seconds** hain! ⏱️")

# Naye aur Mazedaar Questions (Aap inhein apne hisaab se change kar sakte hain)
quiz_data = [
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": 1
    },
    {
        "question": "What is the capital city of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
        "answer": 2
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"],
        "answer": 2
    },
    {
        "question": "Which of these is a programming language named after a snake?",
        "options": ["C++", "Python", "Java", "Ruby"],
        "answer": 1
    }
]

QUESTION_TIME = 15  # Har question ke liye seconds

# Initialize Session State
if "step" not in st.session_state:
    st.session_state.step = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False
if "last_correct" not in st.session_state:
    st.session_state.last_correct = False
if "correct_ans_text" not in st.session_state:
    st.session_state.correct_ans_text = ""

total_questions = len(quiz_data)

# Quiz On-going Screen
if st.session_state.step < total_questions:
    # Progress Bar
    st.progress(st.session_state.step / total_questions)
    
    current_q = quiz_data[st.session_state.step]
    
    # Timer Logic Calculation
    elapsed_time = int(time.time() - st.session_state.start_time)
    time_left = QUESTION_TIME - elapsed_time
    
    # Agar time khatam ho gaya
    if time_left <= 0 and not st.session_state.show_feedback:
        st.session_state.show_feedback = True
        st.session_state.last_correct = False
        st.session_state.correct_ans_text = current_q["options"][current_q["answer"]]
        st.rerun()

    # Timer display and UI card
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### Level {st.session_state.step + 1} of {total_questions}")
    with col2:
        if time_left > 5:
            st.markdown(f"⏳ **00:{time_left:02d}s**")
        else:
            st.markdown(f"🔴 <span style='color:red; font-weight:bold;'>00:{time_left:02d}s</span>", unsafe_allow_html=True)

    with st.container():
        st.markdown(f'<div class="question-card"><h4>{current_q["question"]}</h4></div>', unsafe_allow_html=True)
        
        user_choice = st.radio(
            "Choose your option:", 
            current_q["options"], 
            key=f"q_{st.session_state.step}"
        )
        
        if st.session_state.show_feedback:
            if st.session_state.last_correct:
                st.success("🎉 Boom!correct!")
            else:
                st.error(f"⏰ Time Out or wrong answer! Right answer: **{st.session_state.correct_ans_text}**")
                
            if st.button("Next Level ➔"):
                st.session_state.show_feedback = False
                st.session_state.step += 1
                st.session_state.start_time = time.time()
                st.rerun()
        else:
            if st.button("Lock Answer 🔒"):
                selected_index = current_q["options"].index(user_choice)
                st.session_state.correct_ans_text = current_q["options"][current_q["answer"]]
                
                if selected_index == current_q["answer"]:
                    st.session_state.score += 1
                    st.session_state.last_correct = True
                else:
                    st.session_state.last_correct = False
                    
                st.session_state.show_feedback = True
                st.rerun()
                
    # Auto refresh page every 1 second to update the timer smoothly
    time.sleep(1)
    st.rerun()

else:
    # Quiz Finished Screen
    st.progress(1.0)
    st.markdown("<h2 style='text-align: center;'>🏆 Game Over! 🏆</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Your Final Score: {st.session_state.score} / {total_questions}</h3>", unsafe_allow_html=True)
    
    percentage = (st.session_state.score / total_questions) * 100
    if percentage == 100:
        st.balloons()
        st.markdown("<p style='text-align: center; color: #00ffcc;'>Legend! You cleared everything with a 100% score!</p>", unsafe_allow_html=True)
    elif percentage >= 50:
        st.markdown("<p style='text-align: center; color: #ffcc00;'>Great job! You played well.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align: center; color: #ff4d4d;'>Nice try! Try again to beat your score.</p>", unsafe_allow_html=True)
        
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Play Again 🔄"):
            st.session_state.step = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.show_feedback = False
            st.rerun()