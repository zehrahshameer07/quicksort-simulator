"""
Quick Sort Simulator  |  DAA CIA 3(b)
A step-by-step visual simulator built with Streamlit.
Run locally:  streamlit run app.py
"""
import random
import time

import streamlit as st

st.set_page_config(page_title="Quick Sort Simulator", layout="wide")

# ----------------------------------------------------------------------------
# 1. COLOURS AND STYLE
# ----------------------------------------------------------------------------
C = {
    "unchecked": "#D8D1BE",   # inside the current sub-array, not looked at yet
    "small": "#6FA8DC",       # small zone: numbers <= pivot
    "big": "#F2B84B",         # big zone: numbers > pivot
    "cur": "#1F2A37",         # the number being checked right now
    "pivot": "#E4572E",       # the pivot
    "done": "#4C956C",        # in its final sorted position
    "faded": "#EEE9DA",       # outside the current sub-array
}
LEGEND = [("unchecked", "Not checked yet"), ("small", "Small zone (less than or equal to pivot)"),
          ("big", "Big zone (greater than pivot)"), ("cur", "Being checked now"),
          ("pivot", "Pivot"), ("done", "Final sorted position")]

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stMarkdown, button, input { font-family: 'Inter', sans-serif !important; }
.stApp { background: #FBF8F1; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #F3EDDC; }
.block-container { padding-top: 2rem; max-width: 1100px; }
.hero { border-bottom: 3px solid #F2B84B; padding-bottom: 14px; margin-bottom: 18px; }
.hero h1 { margin: 0; font-size: 2rem; color: #1F2A37; font-weight: 700; }
.hero p { margin: 4px 0 0; color: #5F6B7A; }
.steps3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 18px; }
.steps3 div { background: #fff; border: 1px solid #E8E0CC; border-radius: 12px; padding: 12px 14px; color: #3A4656; font-size: .92rem; }
.steps3 b { display: block; color: #1F2A37; margin-bottom: 2px; }
.steps3 span { display: inline-block; background: #1F2A37; color: #fff; border-radius: 50%; width: 22px; height: 22px;
               text-align: center; line-height: 22px; font-size: .75rem; margin-right: 6px; }
.card { background: #fff; border: 1px solid #E8E0CC; border-radius: 14px; padding: 16px 18px; margin-bottom: 14px; }
.card h3 { margin: 0 0 10px; font-size: .78rem; letter-spacing: .08em; text-transform: uppercase; color: #8A7A55; }
.phase { display: inline-block; background: #1F2A37; color: #fff; border-radius: 999px; padding: 3px 12px;
         font-size: .78rem; font-weight: 600; margin-bottom: 8px; }
.say { background: #fff; border: 1px solid #E8E0CC; border-left: 6px solid #F2B84B; border-radius: 12px;
       padding: 14px 18px; font-size: 1.08rem; color: #1F2A37; min-height: 92px; }
.sub { font-size: .9rem; color: #5F6B7A; margin-bottom: 4px; }
.stage { display: flex; align-items: flex-end; gap: 6px; height: 270px; padding-top: 26px; }
.bar { flex: 1; min-width: 18px; border-radius: 8px 8px 3px 3px; position: relative; transition: all .3s; }
.bar b { position: absolute; top: -22px; left: 0; right: 0; text-align: center; font-size: .82rem; color: #1F2A37; font-weight: 600; }
.idx { display: flex; gap: 6px; margin-top: 6px; }
.idx div { flex: 1; min-width: 18px; text-align: center; font-size: .72rem; color: #8B93A0; min-height: 34px; line-height: 1.3; }
.idx div b { font-size: .68rem; }
.legend { display: flex; flex-wrap: wrap; gap: 8px 18px; margin-top: 10px; font-size: .8rem; color: #5F6B7A; }
.legend i { display: inline-block; width: 12px; height: 12px; border-radius: 3px; margin-right: 6px; vertical-align: -2px; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.stat { background: #fff; border: 1px solid #E8E0CC; border-radius: 12px; padding: 8px 14px; }
.stat span { display: block; font-size: .72rem; color: #8A7A55; text-transform: uppercase; letter-spacing: .06em; }
.stat b { font-size: 1.4rem; color: #1F2A37; }
.code { font-family: 'Courier New', monospace; font-size: .84rem; line-height: 1.75; }
.code div { padding: 1px 10px; border-radius: 6px; white-space: pre; color: #5F6B7A; }
.code div.on { background: #FCE8B2; font-weight: 700; color: #1F2A37; }
.stk { display: flex; flex-direction: column-reverse; gap: 6px; }
.stk div { background: #FBF8F1; border: 1px solid #E8E0CC; border-radius: 8px; padding: 4px 12px; font-family: 'Courier New', monospace; font-size: .84rem; }
.stk div:last-child { border-color: #E4572E; background: #FDECE6; font-weight: 700; }
.note { font-size: .8rem; color: #5F6B7A; margin-top: 8px; }
div.stButton > button { border-radius: 10px; border: 1px solid #D8D1BE; background: #fff; color: #1F2A37; font-weight: 600; width: 100%; }
div.stButton > button:hover { border-color: #1F2A37; color: #1F2A37; }
div.stButton > button[kind="primary"] { background: #1F2A37; color: #fff; border-color: #1F2A37; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# 2. ALGORITHM  (records a snapshot after every step so we can play and rewind)
# ----------------------------------------------------------------------------
PSEUDO = [
    "QuickSort(A, lo, hi):",
    "  if lo < hi:",
    "    p = Partition(A, lo, hi)",
    "    QuickSort(A, lo, p - 1)",
    "    QuickSort(A, p + 1, hi)",
    "Partition(A, lo, hi):",
    "  pivot = A[hi];  i = lo - 1",
    "  for j = lo to hi - 1:",
    "    if A[j] <= pivot:  i++; swap(A[i], A[j])",
    "  swap(A[i + 1], A[hi]);  return i + 1",
]


def build_steps(arr, mode):
    a = list(arr)
    steps, stack, done = [], [], set()
    n_ = {"cmp": 0, "swp": 0}
    rng = lambda x, y: set(range(x, y))

    def snap(phase, msg, line=0, lo=None, hi=None, piv=None, cur=None, small=(), big=(), sw=()):
        sub = ""
        if lo is not None and lo <= hi:
            sub = "Working on: " + ", ".join(str(v) for v in a[lo:hi + 1]) + f"   (positions {lo} to {hi})"
        steps.append(dict(a=list(a), lo=lo, hi=hi, piv=piv, cur=cur, small=set(small), big=set(big),
                          sw=list(sw), done=set(done), cmp=n_["cmp"], swp=n_["swp"], stack=list(stack),
                          line=line, phase=phase, msg=msg, sub=sub))

    def pick(lo, hi):
        if mode == "First element":
            return lo
        if mode == "Middle element":
            return (lo + hi) // 2
        if mode == "Random element":
            return random.randint(lo, hi)
        if mode == "Median of three":
            m = (lo + hi) // 2
            return sorted([lo, m, hi], key=lambda k: a[k])[1]
        return hi

    def qs(lo, hi):
        stack.append(f"QuickSort({lo}, {hi})")
        if lo < hi:
            snap("Current sub-array",
                 f"We now sort positions {lo} to {hi}, which holds {hi - lo + 1} numbers.", 1, lo, hi)
            p = pick(lo, hi)
            if p != hi:
                a[p], a[hi] = a[hi], a[p]
                n_["swp"] += 1
                snap("Choose the pivot",
                     f"Strategy: {mode.lower()}. The pivot is {a[hi]}. It is swapped to the last position "
                     f"({hi}) so it stays out of the way while we scan.", 6, lo, hi, piv=hi, sw=(p, hi))
            else:
                snap("Choose the pivot", f"The pivot is the last number, {a[hi]}.", 6, lo, hi, piv=hi)
            pivot, i = a[hi], lo - 1
            snap("Get ready to scan",
                 f"We will check every number from left to right and compare it with the pivot {pivot}. "
                 f"Small numbers go to the left (blue zone), big ones stay on the right (yellow zone).",
                 6, lo, hi, piv=hi)
            for j in range(lo, hi):
                n_["cmp"] += 1
                ok = a[j] <= pivot
                snap("Compare",
                     f"Compare {a[j]} with the pivot {pivot}. Is {a[j]} less than or equal to {pivot}?",
                     7, lo, hi, piv=hi, cur=j, small=rng(lo, i + 1), big=rng(i + 1, j))
                if ok:
                    i += 1
                    same = i == j
                    a[i], a[j] = a[j], a[i]
                    n_["swp"] += 1
                    snap("Move to small zone",
                         (f"Yes. {a[j]} is already next to the small zone, so it simply joins it."
                          if same else
                          f"Yes. {a[i]} is small, so it joins the small zone. It swaps places with {a[j]}, "
                          f"the first number of the big zone."),
                         8, lo, hi, piv=hi, small=rng(lo, i + 1), big=rng(i + 1, j + 1),
                         sw=() if same else (i, j))
                else:
                    snap("Stays in big zone",
                         f"No. {a[j]} is greater than {pivot}, so it stays in the big zone.",
                         8, lo, hi, piv=hi, small=rng(lo, i + 1), big=rng(i + 1, j + 1))
            a[i + 1], a[hi] = a[hi], a[i + 1]
            n_["swp"] += 1
            p = i + 1
            done.add(p)
            snap("Place the pivot",
                 f"Scan finished. The pivot {a[p]} swaps into position {p}, exactly between the small and big "
                 f"zones. It is now in its final sorted position.",
                 9, lo, hi, piv=p, small=rng(lo, p), big=rng(p + 1, hi + 1), sw=(p, hi))
            snap("Sort the left side",
                 f"Repeat the whole process on the left side (positions {lo} to {p - 1})."
                 + (" It is empty, so there is nothing to do." if p - 1 < lo else ""), 3, lo, hi)
            qs(lo, p - 1)
            snap("Sort the right side",
                 f"Left side finished. Now repeat on the right side (positions {p + 1} to {hi})."
                 + (" It is empty, so there is nothing to do." if p + 1 > hi else ""), 4, lo, hi)
            qs(p + 1, hi)
        elif lo == hi:
            done.add(lo)
            snap("Single number", f"Only one number ({a[lo]}) is left here, so it is already sorted.", 1, lo, hi)
        stack.pop()

    snap("Start", "This is the starting array. Press Play, or use Next to go one step at a time.")
    qs(0, len(a) - 1)
    done.update(range(len(a)))
    snap("Finished", f"The array is sorted. It took {n_['cmp']} comparisons and {n_['swp']} swaps.")
    return steps


# ----------------------------------------------------------------------------
# 3. DRAWING HELPERS
# ----------------------------------------------------------------------------
def bars_html(s):
    a = s["a"]
    mn, mx = min(min(a), 0), max(max(a), 1)
    bars, idx = [], []
    for k, v in enumerate(a):
        in_range = s["lo"] is not None and s["lo"] <= k <= s["hi"]
        tag = ""
        if k == s["piv"] and k not in s["done"]:
            col, tag = C["pivot"], "pivot"
        elif k in s["done"]:
            col = C["done"]
            tag = "pivot" if k == s["piv"] else ""
        elif k == s["cur"]:
            col, tag = C["cur"], "checking"
        elif k in s["small"]:
            col = C["small"]
        elif k in s["big"]:
            col = C["big"]
        elif in_range:
            col = C["unchecked"]
        else:
            col = C["faded"]
        ring = "box-shadow:0 0 0 3px #1F2A37;" if k in s["sw"] else ""
        h = 12 + (v - mn) / (mx - mn or 1) * 88
        bars.append(f'<div class="bar" style="height:{h:.0f}%;background:{col};{ring}"><b>{v}</b></div>')
        tag_html = f'<br><b style="color:{col if col != C["faded"] else "#8B93A0"}">{tag}</b>' if tag else ""
        idx.append(f"<div>{k}{tag_html}</div>")
    legend = "".join(f'<span><i style="background:{C[k]}"></i>{t}</span>' for k, t in LEGEND)
    return (f'<div class="sub">{s["sub"] or "&nbsp;"}</div><div class="stage">{"".join(bars)}</div>'
            f'<div class="idx">{"".join(idx)}</div><div class="legend">{legend}</div>'
            f'<div class="note">A dark outline means the two numbers were just swapped. Numbers under the bars are positions.</div>')


def code_html(line):
    rows = "".join(f'<div class="{"on" if k == line else ""}">{t.replace("<", "&lt;")}</div>'
                   for k, t in enumerate(PSEUDO))
    return f'<div class="code">{rows}</div>'


def stack_html(stack):
    if not stack:
        return '<div class="stk"><div>(empty)</div></div>'
    return '<div class="stk">' + "".join(f"<div>{t}</div>" for t in stack) + "</div>"


# ----------------------------------------------------------------------------
# 4. STATE + SIDEBAR
# ----------------------------------------------------------------------------
if "inp" not in st.session_state:
    st.session_state.inp = "38, 27, 43, 3, 9, 82, 10, 55, 21, 64"
    st.session_state.idx = 0
    st.session_state.sig = None
    st.session_state.arr = [38, 27, 43, 3, 9, 82, 10, 55, 21, 64]


def random_array():
    st.session_state.inp = ", ".join(str(random.randint(1, 99)) for _ in range(random.randint(8, 12)))


def go(delta=None, to=None):
    n = len(st.session_state.steps)
    if to is not None:
        st.session_state.idx = to if to >= 0 else n - 1
    else:
        st.session_state.idx = max(0, min(n - 1, st.session_state.idx + delta))


with st.sidebar:
    st.markdown("### Setup")
    st.text_input("Numbers to sort (separate with commas, then press Enter)", key="inp")
    st.button("Random numbers", on_click=random_array)
    mode = st.selectbox("Pivot strategy", ["Last element", "First element", "Middle element",
                                           "Random element", "Median of three"])
    speed = st.slider("Play speed", 1, 10, 5)
    st.caption("Tip: enter 1, 2, 3, 4, 5, 6, 7, 8 with the last-element strategy to see the worst case. "
               "Then switch to median of three and compare the recursion depth.")

try:
    parsed = [int(x) for x in st.session_state.inp.replace(",", " ").split()]
    if not 2 <= len(parsed) <= 20:
        raise ValueError
    st.session_state.arr = parsed
except ValueError:
    st.sidebar.error("Please enter 2 to 20 whole numbers.")

sig = (tuple(st.session_state.arr), mode)
if sig != st.session_state.sig:
    st.session_state.steps = build_steps(st.session_state.arr, mode)
    st.session_state.sig = sig
    st.session_state.idx = 0
steps = st.session_state.steps

# ----------------------------------------------------------------------------
# 5. PAGE
# ----------------------------------------------------------------------------
st.markdown('<div class="hero"><h1>Quick Sort Simulator</h1>'
            '<p>See how Quick Sort arranges numbers, one small step at a time.</p></div>'
            '<div class="steps3">'
            '<div><b><span>1</span>Pick a pivot</b>Choose one number to compare everything against.</div>'
            '<div><b><span>2</span>Split into small and big</b>Numbers less than or equal to the pivot go left, the rest go right. The pivot lands in its final spot.</div>'
            '<div><b><span>3</span>Repeat on each side</b>Do the same on the left group and the right group until every number is placed.</div>'
            '</div>', unsafe_allow_html=True)

phase_ph = st.empty()
say = st.empty()
st.write("")
viz = st.empty()
c1, c2, c3, c4, c5 = st.columns(5)
c1.button("Reset", on_click=go, kwargs=dict(to=0))
c2.button("Back", on_click=go, kwargs=dict(delta=-1))
play = c3.button("Play", type="primary")
c4.button("Next", on_click=go, kwargs=dict(delta=1))
c5.button("End", on_click=go, kwargs=dict(to=-1))
st.caption("Press any button while playing to pause.")
prog = st.empty()
stats = st.empty()
st.write("")
left, right = st.columns([3, 2])
code_ph, stack_ph = left.empty(), right.empty()


def draw(k):
    s = steps[k]
    say.markdown(f'<div class="phase">{s["phase"]}</div><div class="say">{s["msg"]}</div>', unsafe_allow_html=True)
    viz.markdown(f'<div class="card">{bars_html(s)}</div>', unsafe_allow_html=True)
    prog.progress(k / (len(steps) - 1), text=f"Step {k} of {len(steps) - 1}")
    stats.markdown(
        '<div class="stats">'
        f'<div class="stat"><span>Comparisons</span><b>{s["cmp"]}</b></div>'
        f'<div class="stat"><span>Swaps</span><b>{s["swp"]}</b></div>'
        f'<div class="stat"><span>Recursion depth</span><b>{len(s["stack"])}</b></div></div>',
        unsafe_allow_html=True)
    code_ph.markdown(
        f'<div class="card"><h3>Pseudocode</h3>{code_html(s["line"])}'
        '<div class="note">The highlighted line is the one being executed. '
        'i is the last position of the small zone. j is the number being checked.</div></div>',
        unsafe_allow_html=True)
    stack_ph.markdown(
        f'<div class="card"><h3>Recursion call stack</h3>{stack_html(s["stack"])}'
        '<div class="note">Each line is a QuickSort call that is still waiting to finish. '
        'The top one (red) is the call running now.</div></div>', unsafe_allow_html=True)


draw(st.session_state.idx)

if play:
    if st.session_state.idx >= len(steps) - 1:
        st.session_state.idx = 0
    for k in range(st.session_state.idx, len(steps)):
        st.session_state.idx = k
        draw(k)
        time.sleep(1.25 - speed * 0.11)

with st.expander("Complexity"):
    st.markdown("""
| Case | Time | When it happens |
|---|---|---|
| Best | O(n log n) | The pivot splits the numbers into two nearly equal halves |
| Average | O(n log n) | Typical, mixed-up input |
| Worst | O(n²) | Already sorted input with a first or last pivot (very uneven splits) |

Space: O(log n) on average for the recursion stack. Quick Sort sorts in place and is not stable.
""")
with st.expander("Why the pivot choice matters"):
    st.markdown("""
The pivot decides how even each split is. If the pivot is always the smallest or largest number, one side
is empty and the other side holds almost everything, so the recursion goes about n levels deep. A pivot near
the middle value keeps the recursion about log n levels deep. This is why median of three and random pivots
exist. Watch the Recursion depth counter to see the difference.
""")