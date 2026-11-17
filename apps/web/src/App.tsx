import { useState, type FormEvent } from 'react'
import { supabase } from './lib/supabase'
import CameraStudio from './CameraStudio'

type Screen = 'splash' | 'signin' | 'signup' | 'recovery' | 'dashboard' | 'camera'
type Category = 'All effects' | 'Funny' | 'Beauty' | 'Animals' | 'Distortion' | 'Fantasy'

const categories: Category[] = ['All effects', 'Funny', 'Beauty', 'Animals', 'Distortion', 'Fantasy']
const effects: { name: string; creator: string; category: Exclude<Category, 'All effects'>; emoji: string; className: string; tag?: string }[] = [
  { name: 'Soft glow', creator: 'IRIS Originals', category: 'Beauty', emoji: '✦', className: 'effect-glow', tag: 'TRENDING' },
  { name: 'Big mood', creator: 'Mia K.', category: 'Funny', emoji: '😎', className: 'effect-mood' },
  { name: 'Puppy eyes', creator: 'IRIS Originals', category: 'Animals', emoji: '🐶', className: 'effect-puppy', tag: 'POPULAR' },
  { name: 'Bubble face', creator: 'Noah B.', category: 'Distortion', emoji: '🫧', className: 'effect-bubble' },
  { name: 'Dreamscape', creator: 'IRIS Originals', category: 'Fantasy', emoji: '🪩', className: 'effect-dream' },
  { name: 'Tiny mouth', creator: 'Mia K.', category: 'Distortion', emoji: '🤏', className: 'effect-tiny' },
]

function Brand({ light = false }: { light?: boolean }) {
  return <a className={`brand ${light ? 'brand-light' : ''}`} href="#" aria-label="IRIS home"><span className="brand-symbol" aria-hidden="true"><i /></span><span>iris<span className="brand-period">.</span></span></a>
}

function VisualPanel({ mode }: { mode: 'welcome' | 'signup' }) {
  return <aside className={`visual-panel visual-${mode}`}><div className="visual-grain" /><div className="visual-orbit orbit-a" /><div className="visual-orbit orbit-b" /><div className="visual-copy"><span className="visual-kicker"><span /> YOUR FACE. YOUR CANVAS.</span><p className="visual-statement">{mode === 'welcome' ? <>There's more<br />to <em>you.</em></> : <>Your world.<br />Your <em>rules.</em></>}</p><p className="visual-description">{mode === 'welcome' ? 'Step into a world made for self-expression.' : 'Join the creative side. Your next favorite look is one tap away.'}</p></div><div className="visual-bottom"><span>IRIS STUDIO</span><span>01 — 04</span></div><div className="visual-sticker">✳<small>PLAY<br />MORE.</small></div></aside>
}

function Splash({ onNavigate }: { onNavigate: (screen: Screen) => void }) {
  return <main className="splash-screen"><div className="splash-top"><Brand /><span className="top-note">A CREATIVE CAMERA EXPERIENCE</span></div><div className="splash-content"><div className="splash-copy"><span className="eyebrow"><span className="eyebrow-dot" /> YOUR CREATIVE PLAYGROUND</span><h1>See beyond<br /><em>yourself.</em></h1><p>Little moments. Big personality. Discover playful effects, try a new side of you and share the fun with your people.</p><div className="splash-actions"><button className="button button-primary" onClick={() => onNavigate('signup')}>Create your account <span>↗</span></button><button className="button button-quiet" onClick={() => onNavigate('signin')}>I already have an account <span>→</span></button></div><button className="preview-link" onClick={() => onNavigate('dashboard')}>Just looking? Explore IRIS first →</button><div className="splash-footnote"><span className="avatar-stack"><i>A</i><i>M</i><i>J</i></span><span>MADE FOR EXPRESSION. <b>SHARED WITH EVERYONE.</b></span></div></div><div className="splash-art" aria-label="Abstract colorful IRIS visual"><div className="art-ring ring-one" /><div className="art-ring ring-two" /><div className="art-disc"><div className="disc-inner"><span>i</span></div></div><span className="art-spark spark-one">✳</span><span className="art-spark spark-two">✦</span><div className="art-caption"><span className="live-dot" /> REAL-TIME MAGIC</div><div className="art-label">YOUR LOOK,<br /><b>REMIXED.</b></div></div></div><footer className="splash-footer"><span>IRIS © 2026</span><span>SEE YOURSELF DIFFERENTLY</span><span>MADE FOR THE MOMENT ✳</span></footer></main>
}

function AuthLayout({ mode, onNavigate }: { mode: 'signin' | 'signup'; onNavigate: (screen: Screen) => void }) {
  const isSignup = mode === 'signup'
  const [showPassword, setShowPassword] = useState(false)
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)
  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setMessage('')
    if (!supabase) {
      setMessage('Authentication is not configured yet. Add VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY to apps/web/.env.local, then restart the development server.')
      return
    }
    const form = new FormData(event.currentTarget)
    const email = String(form.get('email') ?? '').trim()
    const password = String(form.get('password') ?? '')
    setBusy(true)
    try {
      if (isSignup) {
        const name = String(form.get('name') ?? '').trim()
        const { data, error } = await supabase.auth.signUp({ email, password, options: { data: { full_name: name } } })
        if (error) throw error
        setMessage(data.session ? 'Your IRIS account has been created. Welcome!' : 'Account created. Check your email to confirm your address before signing in.')
        if (data.session) onNavigate('dashboard')
      } else {
        const { error } = await supabase.auth.signInWithPassword({ email, password })
        if (error) throw error
        onNavigate('dashboard')
      }
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Something went wrong. Please try again.')
    } finally {
      setBusy(false)
    }
  }
  return <main className="auth-screen"><VisualPanel mode={isSignup ? 'signup' : 'welcome'} /><section className="auth-side"><div className="auth-top"><Brand /><button className="text-button" onClick={() => onNavigate('splash')}>← Back to home</button></div><div className="auth-content"><span className="eyebrow">{isSignup ? 'JOIN THE PLAYGROUND' : 'WELCOME BACK'}</span><h1>{isSignup ? <>Let's make<br /><em>some magic.</em></> : <>Good to see<br />you <em>again.</em></>}</h1><p className="form-intro">{isSignup ? 'Create your free IRIS account.' : 'Sign in to pick up where your creativity left off.'}</p>{!isSignup && <button className="google-button" type="button" onClick={() => setMessage('Google sign-in will be connected when authentication is implemented.')}><span className="google-g">G</span> Continue with Google</button>}{!isSignup && <div className="form-divider"><span>OR CONTINUE WITH EMAIL</span></div>}<form className="auth-form" onSubmit={handleSubmit}>{isSignup && <label>Your name<input name="name" type="text" placeholder="What should we call you?" autoComplete="name" required /></label>}<label>Email address<input name="email" type="email" placeholder="you@example.com" autoComplete="email" required /></label><label>Password<div className="password-field"><input name="password" type={showPassword ? 'text' : 'password'} placeholder={isSignup ? 'At least 8 characters' : 'Enter your password'} minLength={isSignup ? 8 : undefined} autoComplete={isSignup ? 'new-password' : 'current-password'} required /><button type="button" onClick={() => setShowPassword(!showPassword)}>{showPassword ? 'Hide' : 'Show'}</button></div></label>{!isSignup && <div className="form-options"><label className="checkbox-label"><input type="checkbox" /> Remember me</label><button className="inline-button" type="button" onClick={() => onNavigate('recovery')}>Forgot password?</button></div>}{isSignup && <label className="checkbox-label terms-check"><input type="checkbox" required /> I agree to the Terms of Service and Privacy Policy.</label>}<button className="button button-primary submit-button" type="submit" disabled={busy}>{busy ? 'Please wait…' : isSignup ? 'Create account' : 'Sign in'} <span>→</span></button>{message && <div className="form-message" role="status">{message}<button className="inline-button" type="button" onClick={() => onNavigate('dashboard')}>Explore preview →</button></div>}</form><p className="auth-switch">{isSignup ? 'Already have an account?' : 'New to IRIS?'} <button onClick={() => onNavigate(isSignup ? 'signin' : 'signup')}>{isSignup ? 'Sign in' : 'Create an account'}</button></p><p className="legal-note">{isSignup ? 'No spam. Just good vibes and great effects.' : 'By continuing, you agree to our Terms of Service and Privacy Policy.'}</p></div><div className="auth-footer"><span>IRIS © 2026</span><span>SEE BEYOND YOURSELF.</span></div></section></main>
}

function Recovery({ onNavigate }: { onNavigate: (screen: Screen) => void }) {
  const [sent, setSent] = useState(false)
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)
  return <main className="recovery-screen"><div className="recovery-top"><Brand /><button className="text-button" onClick={() => onNavigate('signin')}>← Back to sign in</button></div><section className="recovery-card"><div className="recovery-icon">✉</div><span className="eyebrow">ACCOUNT RECOVERY</span><h1>{sent ? <>Check your<br /><em>inbox.</em></> : <>Forgot your<br /><em>password?</em></>}</h1><p>{sent ? `If an account exists for ${email}, you'll receive a reset link shortly.` : "It happens. Enter your email and we'll help you get back in."}</p>{!sent && <form className="auth-form" onSubmit={async (event) => { event.preventDefault(); setMessage(''); if (!supabase) { setMessage('Password recovery is unavailable until Supabase is configured.'); return } setBusy(true); const { error } = await supabase.auth.resetPasswordForEmail(email, { redirectTo: `${window.location.origin}/` }); setBusy(false); if (error) setMessage(error.message); else setSent(true) }}><label>Email address<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" required /></label><button className="button button-primary submit-button" type="submit" disabled={busy}>{busy ? 'Sending…' : 'Send reset link'} <span>→</span></button>{message && <p className="form-message" role="alert">{message}</p>}</form>}{sent && <button className="button button-primary submit-button" onClick={() => onNavigate('signin')}>Back to sign in <span>→</span></button>}<p className="privacy-note">Your camera stays off until you choose to open Studio. Face tracking will run on your device whenever possible.</p></section><footer className="recovery-footer">IRIS © 2026 <span>MADE FOR EXPRESSION ✳</span></footer></main>
}

function Dashboard({ onNavigate }: { onNavigate: (screen: Screen) => void }) {
  const [category, setCategory] = useState<Category>('All effects')
  const [query, setQuery] = useState('')
  const filtered = effects.filter((effect) => (category === 'All effects' || effect.category === category) && `${effect.name} ${effect.creator} ${effect.category}`.toLowerCase().includes(query.toLowerCase()))
  return <main className="dashboard-shell">
    <aside className="dashboard-sidebar"><div className="sidebar-brand"><Brand /></div><div className="sidebar-label">WORKSPACE</div><nav className="side-nav" aria-label="Main navigation"><button className="side-link active" aria-current="page"><span>⌂</span> Explore</button><button className="side-link" onClick={() => onNavigate('camera')}><span>◎</span> Camera Studio <i className="nav-new">NEW</i></button><button className="side-link" onClick={() => setCategory('All effects')}><span>✧</span> Effects</button><button className="side-link" onClick={() => setCategory('All effects')}><span>▧</span> My creations</button></nav><div className="sidebar-bottom"><div className="creator-card"><span className="creator-icon">✳</span><b>Have an idea?</b><p>Create a filter of your own and share it with the world.</p><button onClick={() => onNavigate('camera')}>Start creating ↗</button></div><button className="side-link profile-link"><span className="profile-avatar">G</span> Guest account <span className="guest-pill">PREVIEW</span></button></div></aside>
    <section className="dashboard-main"><header className="dashboard-header"><div className="breadcrumb">Workspace <span>/</span> <b>Explore</b></div><div className="header-actions"><span className="preview-badge"><i /> PREVIEW MODE</span><button className="icon-button" aria-label="Notifications">♧<i /></button><button className="header-avatar" aria-label="Guest profile">G</button></div></header><div className="dashboard-content"><section className="welcome-banner"><div className="welcome-text"><span className="eyebrow"><span className="eyebrow-dot" /> YOUR CREATIVE PLAYGROUND</span><h1>Make a little<br /><em>more you.</em></h1><p>Find your next favorite look. Play with effects, make something unexpected and share the moment.</p><button className="button button-dark" onClick={() => onNavigate('camera')}>Open Camera Studio <span>↗</span></button></div><div className="welcome-art" aria-hidden="true"><div className="welcome-orbit" /><div className="welcome-orbit second" /><div className="welcome-sphere">✳</div><span className="welcome-float float-top">YOUR<br />MOMENT</span><span className="welcome-float float-bottom">✨ JUST FOR FUN</span></div><span className="banner-index">IRIS / 001</span></section>
      <section className="quick-section"><div className="section-heading"><div><span className="eyebrow">FIND YOUR VIBE</span><h2>Explore effects</h2></div><label className="effect-search"><span>⌕</span><input aria-label="Search effects" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search effects..." /></label></div><div className="category-row" aria-label="Filter effects by category">{categories.map((item) => <button key={item} className={category === item ? 'category-chip selected' : 'category-chip'} aria-pressed={category === item} onClick={() => setCategory(item)}>{item}</button>)}</div><div className="effects-grid">{filtered.map((effect) => <article className="effect-card" key={effect.name}><button className="effect-visual" onClick={() => onNavigate('camera')} aria-label={`Try ${effect.name} in Camera Studio`}><div className={`effect-art ${effect.className}`}><span>{effect.emoji}</span><i>✦</i></div>{effect.tag && <span className="effect-tag">{effect.tag}</span>}<span className="effect-open">↗</span></button><div className="effect-meta"><div><h3>{effect.name}</h3><p>by {effect.creator}</p></div><span className="effect-category">{effect.category}</span></div></article>)}</div>{filtered.length === 0 && <div className="empty-effects">No effects match that search. Try another name or category.</div>}</section>
      <section className="community-strip"><div className="community-symbol">✳</div><div><b>Good things look better shared.</b><p>Your creations, your friends, your little corner of the internet.</p></div><button onClick={() => onNavigate('camera')}>Make your first creation →</button></section>
      <footer className="dashboard-footer"><span>IRIS © 2026</span><span>SEE YOURSELF DIFFERENTLY ✳</span></footer></div></section>
  </main>
}

function App() {
  const [screen, setScreen] = useState<Screen>('splash')
  return <div className="app-root">{screen === 'splash' && <Splash onNavigate={setScreen} />}{(screen === 'signin' || screen === 'signup') && <AuthLayout mode={screen} onNavigate={setScreen} />}{screen === 'recovery' && <Recovery onNavigate={setScreen} />}{screen === 'dashboard' && <Dashboard onNavigate={setScreen} />}{screen === 'camera' && <CameraStudio onBack={() => setScreen('dashboard')} />}</div>
}

export default App
