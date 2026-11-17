import { useState, type FormEvent } from 'react'

type Screen = 'splash' | 'signin' | 'signup' | 'recovery'

function Brand({ light = false }: { light?: boolean }) {
  return (
    <a className={`brand ${light ? 'brand-light' : ''}`} href="#" aria-label="IRIS home">
      <span className="brand-symbol" aria-hidden="true"><i /></span>
      <span>iris<span className="brand-period">.</span></span>
    </a>
  )
}

function VisualPanel({ mode }: { mode: 'welcome' | 'signup' }) {
  return (
    <aside className={`visual-panel visual-${mode}`}>
      <div className="visual-grain" />
      <div className="visual-orbit orbit-a" />
      <div className="visual-orbit orbit-b" />
      <div className="visual-copy">
        <span className="visual-kicker"><span /> YOUR FACE. YOUR CANVAS.</span>
        <p className="visual-statement">
          {mode === 'welcome' ? <>There's more<br />to <em>you.</em></> : <>Your world.<br />Your <em>rules.</em></>}
        </p>
        <p className="visual-description">
          {mode === 'welcome'
            ? 'Step into a world made for self-expression.'
            : 'Join the creative side. Your next favorite look is one tap away.'}
        </p>
      </div>
      <div className="visual-bottom"><span>IRIS STUDIO</span><span>01 — 04</span></div>
      <div className="visual-sticker">✳<small>PLAY<br />MORE.</small></div>
    </aside>
  )
}

function Splash({ onNavigate }: { onNavigate: (screen: Screen) => void }) {
  return (
    <main className="splash-screen">
      <div className="splash-top"><Brand /><span className="top-note">A CREATIVE CAMERA EXPERIENCE</span></div>
      <div className="splash-content">
        <div className="splash-copy">
          <span className="eyebrow"><span className="eyebrow-dot" /> YOUR CREATIVE PLAYGROUND</span>
          <h1>See beyond<br /><em>yourself.</em></h1>
          <p>Little moments. Big personality. Discover playful effects, try a new side of you and share the fun with your people.</p>
          <div className="splash-actions">
            <button className="button button-primary" onClick={() => onNavigate('signup')}>Create your account <span>↗</span></button>
            <button className="button button-quiet" onClick={() => onNavigate('signin')}>I already have an account <span>→</span></button>
          </div>
          <div className="splash-footnote"><span className="avatar-stack"><i>A</i><i>M</i><i>J</i></span><span>MADE FOR EXPRESSION. <b>SHARED WITH EVERYONE.</b></span></div>
        </div>
        <div className="splash-art" aria-label="Abstract colorful IRIS visual">
          <div className="art-ring ring-one" /><div className="art-ring ring-two" />
          <div className="art-disc"><div className="disc-inner"><span>i</span></div></div>
          <span className="art-spark spark-one">✳</span><span className="art-spark spark-two">✦</span>
          <div className="art-caption"><span className="live-dot" /> REAL-TIME MAGIC</div>
          <div className="art-label">YOUR LOOK,<br /><b>REMIXED.</b></div>
        </div>
      </div>
      <footer className="splash-footer"><span>IRIS © 2026</span><span>SEE YOURSELF DIFFERENTLY</span><span>MADE FOR THE MOMENT ✳</span></footer>
    </main>
  )
}

function AuthLayout({ mode, onNavigate }: { mode: 'signin' | 'signup'; onNavigate: (screen: Screen) => void }) {
  const isSignup = mode === 'signup'
  const [showPassword, setShowPassword] = useState(false)
  const [message, setMessage] = useState('')
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setMessage(isSignup
      ? 'Your account form is ready. Authentication will be connected in a later step.'
      : 'Your sign-in form is ready. Authentication will be connected in a later step.')
  }

  return (
    <main className="auth-screen">
      <VisualPanel mode={isSignup ? 'signup' : 'welcome'} />
      <section className="auth-side">
        <div className="auth-top"><Brand /><button className="text-button" onClick={() => onNavigate('splash')}>← Back to home</button></div>
        <div className="auth-content">
          <span className="eyebrow">{isSignup ? 'JOIN THE PLAYGROUND' : 'WELCOME BACK'}</span>
          <h1>{isSignup ? <>Let's make<br /><em>some magic.</em></> : <>Good to see<br />you <em>again.</em></>}</h1>
          <p className="form-intro">{isSignup ? 'Create your free IRIS account.' : 'Sign in to pick up where your creativity left off.'}</p>
          {!isSignup && <button className="google-button" type="button" onClick={() => setMessage('Google sign-in will be connected when authentication is implemented.')}><span className="google-g">G</span> Continue with Google</button>}
          {!isSignup && <div className="form-divider"><span>OR CONTINUE WITH EMAIL</span></div>}
          <form className="auth-form" onSubmit={handleSubmit}>
            {isSignup && <label>Your name<input name="name" type="text" placeholder="What should we call you?" autoComplete="name" required /></label>}
            <label>Email address<input name="email" type="email" placeholder="you@example.com" autoComplete="email" required /></label>
            <label>Password<div className="password-field"><input name="password" type={showPassword ? 'text' : 'password'} placeholder={isSignup ? 'At least 8 characters' : 'Enter your password'} minLength={isSignup ? 8 : undefined} autoComplete={isSignup ? 'new-password' : 'current-password'} required /><button type="button" onClick={() => setShowPassword(!showPassword)}>{showPassword ? 'Hide' : 'Show'}</button></div></label>
            {!isSignup && <div className="form-options"><label className="checkbox-label"><input type="checkbox" /> Remember me</label><button className="inline-button" type="button" onClick={() => onNavigate('recovery')}>Forgot password?</button></div>}
            {isSignup && <label className="checkbox-label terms-check"><input type="checkbox" required /> I agree to the Terms of Service and Privacy Policy.</label>}
            <button className="button button-primary submit-button" type="submit">{isSignup ? 'Create account' : 'Sign in'} <span>→</span></button>
            {message && <p className="form-message" role="status">{message}</p>}
          </form>
          <p className="auth-switch">{isSignup ? 'Already have an account?' : 'New to IRIS?'} <button onClick={() => onNavigate(isSignup ? 'signin' : 'signup')}>{isSignup ? 'Sign in' : 'Create an account'}</button></p>
          <p className="legal-note">{isSignup ? 'No spam. Just good vibes and great effects.' : 'By continuing, you agree to our Terms of Service and Privacy Policy.'}</p>
        </div>
        <div className="auth-footer"><span>IRIS © 2026</span><span>SEE BEYOND YOURSELF.</span></div>
      </section>
    </main>
  )
}

function Recovery({ onNavigate }: { onNavigate: (screen: Screen) => void }) {
  const [sent, setSent] = useState(false)
  const [email, setEmail] = useState('')
  return (
    <main className="recovery-screen">
      <div className="recovery-top"><Brand /><button className="text-button" onClick={() => onNavigate('signin')}>← Back to sign in</button></div>
      <section className="recovery-card">
        <div className="recovery-icon">✉</div>
        <span className="eyebrow">ACCOUNT RECOVERY</span>
        <h1>{sent ? <>Check your<br /><em>inbox.</em></> : <>Forgot your<br /><em>password?</em></>}</h1>
        <p>{sent ? `If an account exists for ${email}, you'll receive a reset link shortly.` : "It happens. Enter your email and we'll help you get back in."}</p>
        {!sent && <form className="auth-form" onSubmit={(event) => { event.preventDefault(); setSent(true) }}><label>Email address<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" required /></label><button className="button button-primary submit-button" type="submit">Send reset link <span>→</span></button></form>}
        {sent && <button className="button button-primary submit-button" onClick={() => onNavigate('signin')}>Back to sign in <span>→</span></button>}
        <p className="privacy-note">Your camera stays off until you choose to open Studio. Face tracking will run on your device whenever possible.</p>
      </section>
      <footer className="recovery-footer">IRIS © 2026 <span>MADE FOR EXPRESSION ✳</span></footer>
    </main>
  )
}

function App() {
  const [screen, setScreen] = useState<Screen>('splash')

  return (
    <div className="app-root">
      {screen === 'splash' && <Splash onNavigate={setScreen} />}
      {(screen === 'signin' || screen === 'signup') && <AuthLayout mode={screen} onNavigate={setScreen} />}
      {screen === 'recovery' && <Recovery onNavigate={setScreen} />}
    </div>
  )
}

export default App
