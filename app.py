import random
from fractions import Fraction

import streamlit as st

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Limit Practice",
    page_icon="📐",
    layout="centered",
)

# ─── Styling ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .block-container { max-width: 680px; padding-top: 2rem; }
    .limit-display   { text-align: center; margin: 1.8rem 0; }

    .feedback-correct {
        color: #1a7f37;
        font-size: 1.15rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    .feedback-incorrect {
        color: #cf222e;
        font-size: 1.15rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    .feedback-encourage {
        color: #7d4e00;
        font-size: 1rem;
        margin-top: 0.3rem;
    }
    .step-card {
        background: #f6f8fa;
        border: 1px solid #d0d7de;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0 0.9rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─── Problem generation ───────────────────────────────────────────────────────
def generate_problem() -> dict:
    """
    Generates a limit of the form:
        lim_{x → -1}  sqrt( (x + 1) / (x² + cx + b) )

    Pick integer a in [2, 7], then:
        b = a² + 1,  c = a² + 2
    so the denominator factors as (x+1)(x+b) and the limit equals 1/a.
    """
    a = random.randint(2, 7) # range 2–7 keeps problems non-trivial but manageable
    b = a * a + 1            # constant term of denominator
    c = a * a + 2            # linear coefficient of denominator
    return dict(a=a, b=b, c=c, answer=Fraction(1, a))




def parse_answer(text: str) -> Fraction | None:
    """Accept '1/3', '0.333', '2', etc."""
    text = text.strip()
    try:
        if "/" in text:      # Split on the slash and parse each side as an integer
            num_s, den_s = text.split("/", 1)
            return Fraction(int(num_s.strip()), int(den_s.strip())) # For decimals and integers, Fraction() handles the conversion
        return Fraction(text).limit_denominator(100_000)            # limit_denominator snaps floating-point noise to the nearest simple fraction
    except Exception:
        return None


# ─── Session state ────────────────────────────────────────────────────────────
if "problem" not in st.session_state:
    st.session_state.problem    = generate_problem()
    st.session_state.submitted  = False  # tracks whether the student has hit Submit
    st.session_state.correct    = None   # True / False / None
    st.session_state.attempts   = 0      # counts how many times they've submitted
    st.session_state.widget_key = 0


def new_problem():
    st.session_state.problem    = generate_problem()
    st.session_state.submitted  = False
    st.session_state.correct    = None
    st.session_state.attempts   = 0
    st.session_state.widget_key += 1


def try_again():
    """Keep the same problem, just clear the input and feedback."""
    st.session_state.submitted  = False
    st.session_state.correct    = None
    st.session_state.widget_key += 1


p = st.session_state.problem
a, b, c = p["a"], p["b"], p["c"]
answer: Fraction = p["answer"]

# ─── Header ───────────────────────────────────────────────────────────────────
st.title("Solve the limit:")

# ─── Limit display ────────────────────────────────────────────────────────────
st.markdown('<div class="limit-display">', unsafe_allow_html=True)
st.latex(
    r"\lim_{x \to -1} \sqrt{\dfrac{x + 1}{x^2 + "
    + str(c) + r"x + " + str(b) + r"}}"
)
st.markdown("</div>", unsafe_allow_html=True)

# ─── Input + submit ───────────────────────────────────────────────────────────
st.markdown("**Your answer:**")
col_input, col_submit = st.columns([3, 1])

with col_input:
    user_text = st.text_input(
        label="answer",
        label_visibility="collapsed",
        placeholder='e.g. "1/3" or "0.333"',
        key=f"ans_{st.session_state.widget_key}",
    )
with col_submit:
    submit_clicked = st.button("Submit", type="primary", use_container_width=True)

if submit_clicked:
    st.session_state.submitted = True
    st.session_state.attempts += 1

# ─── Feedback ────────────────────────────────────────────────────────────────
# Only show feedback once the student has clicked Submit
if st.session_state.submitted:
    raw = user_text.strip()
    
    if not raw:     # Edge case: they hit Submit without typing anything
        st.warning("Please enter an answer above, then press Submit.")

    else:
        parsed = parse_answer(raw)

        if parsed is None:    # Edge case: input was typed but couldn't be parsed as a number
            st.warning(
                "Couldn't read that input. Try a fraction like `1/3`, "
                "a decimal like `0.333`, or a whole number."
            )

        elif parsed == answer:
            # ── Correct ──────────────────────────────────────────────────────
            st.session_state.correct = True
            st.markdown(
                f'<p class="feedback-correct">✓ Correct! '
                f'The limit is $\\dfrac{{{answer.numerator}}}{{{answer.denominator}}}$. '
                f'Great work! </p>',
                unsafe_allow_html=True,
            )

            # New problem button
            st.markdown("")
            if st.button("➡️ Try a new problem", type="primary", use_container_width=True):
                new_problem()
                st.rerun()

        else:
            # ── Incorrect ────────────────────────────────────────────────────
            st.session_state.correct = False
            attempts = st.session_state.attempts

            st.markdown(
                '<p class="feedback-incorrect">✗ Not quite — give it another shot!</p>',
                unsafe_allow_html=True,
            )

            # Escalating encouragement based on number of attempts
            if attempts == 1:
                msg = "💡 Hint: try factoring the denominator first."
            elif attempts == 2:
                msg = "💡 Remember: both numerator and denominator share a common factor of $(x + 1)$."
            else:
                msg = "💡 Check the step-by-step solution below — it walks through every step."
             # After 3+ attempts, point them to the full walkthrough
            st.markdown(
                f'<p class="feedback-encourage">{msg}</p>',
                unsafe_allow_html=True,
            )

            # Two options: retry the same problem, or move on to a new one
            col_retry, col_new = st.columns(2)
            with col_retry:
                if st.button("🔁 Try Again", type="primary", use_container_width=True):
                    try_again()
                    st.rerun()
            with col_new:
                if st.button("➡️ New Problem", use_container_width=True):
                    new_problem()
                    st.rerun()

        # ── Step-by-step solution (bonus — always available after submitting) ─
        # Only shown when a valid answer was submitted (not on empty or
        # unparseable input) so it doesn't appear prematurely
        st.markdown("---")
        with st.expander("📖 Show step-by-step solution", expanded=False):

            st.markdown("**Step 1 — Direct substitution reveals 0/0**")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.latex(
                r"\text{At } x = -1: \quad "
                r"\frac{(-1)+1}{(-1)^2 + " + str(c) + r"(-1) + " + str(b) + r"}"
                r" = \frac{0}{1 - " + str(c) + r" + " + str(b) + r"} = \frac{0}{0}"
            )
            st.markdown(
                "Both numerator **and** denominator equal 0, giving an indeterminate "
                "$\\frac{0}{0}$ form. We need to simplify before evaluating."
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("**Step 2 — Factor the denominator**")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown(
                f"Since $x = -1$ is a root of $x^2 + {c}x + {b}$, "
                f"$(x+1)$ must be a factor:"
            )
            st.latex(
                r"x^2 + " + str(c) + r"x + " + str(b)
                + r" = (x + 1)(x + " + str(b) + r")"
            )
            st.markdown(
                f"Check: $(x+1)(x+{b}) = x^2 + {b+1}x + {b} = x^2 + {c}x + {b}$ ✓"
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("**Step 3 — Cancel the common $(x+1)$ factor**")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.latex(
                r"\sqrt{\frac{x+1}{(x+1)(x+" + str(b) + r")}}"
                r" = \sqrt{\frac{1}{x+" + str(b) + r"}}"
                r"\qquad (x \neq -1)"
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(r"**Step 4 — Evaluate as** $x \to -1$")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            inner_val = b - 1  # = a²
            ans_latex = (
                r"\dfrac{1}{" + str(answer.denominator) + r"}"
                if answer.denominator != 1
                else str(answer.numerator)
            )
            st.latex(
                r"\lim_{x \to -1}\sqrt{\frac{1}{x+" + str(b) + r"}}"
                r" = \sqrt{\frac{1}{-1+" + str(b) + r"}}"
                r" = \sqrt{\frac{1}{" + str(inner_val) + r"}}"
                r" = \frac{1}{\sqrt{" + str(inner_val) + r"}}"
                r" = \frac{1}{" + str(a) + r"}"
                r" = " + ans_latex
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.success(
                f"**Answer: $\\dfrac{{1}}{{{a}}}$** — factor out the shared "
                f"$(x+1)$, cancel it, then substitute $x = -1$."
            )