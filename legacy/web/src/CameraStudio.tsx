import { useCallback, useEffect, useRef, useState } from 'react'
import FaceLandmarkerOverlay from './FaceLandmarkerOverlay'

type FacingMode = 'user' | 'environment'
type Capture = { url: string; filename: string; kind: 'photo' | 'video' }

function CameraStudio({ onBack }: { onBack: () => void }) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [videoElement, setVideoElement] = useState<HTMLVideoElement | null>(null)
  const attachVideo = useCallback((node: HTMLVideoElement | null) => {
    videoRef.current = node
    setVideoElement(node)
  }, [])
  const streamRef = useRef<MediaStream | null>(null)
  const recorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const captureUrlRef = useRef<string | null>(null)
  const [facingMode, setFacingMode] = useState<FacingMode>('user')
  const [cameraState, setCameraState] = useState<'idle' | 'loading' | 'ready' | 'error'>('idle')
  const [error, setError] = useState('')
  const [recording, setRecording] = useState(false)
  const [capture, setCapture] = useState<Capture | null>(null)
  const [flash, setFlash] = useState(false)

  const stopStream = useCallback(() => {
    streamRef.current?.getTracks().forEach((track) => track.stop())
    streamRef.current = null
    if (videoRef.current) videoRef.current.srcObject = null
  }, [])

  const startCamera = useCallback(async (mode: FacingMode) => {
    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraState('error')
      setError('Camera access is unavailable. Use a modern browser over HTTPS or localhost.')
      return
    }

    setCameraState('loading')
    setError('')
    stopStream()

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: false,
        video: { facingMode: { ideal: mode }, width: { ideal: 1280 }, height: { ideal: 720 } },
      })
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        await videoRef.current.play()
      }
      setFacingMode(mode)
      setCameraState('ready')
    } catch (cause) {
      stopStream()
      setCameraState('error')
      const name = cause instanceof DOMException ? cause.name : ''
      if (name === 'NotAllowedError' || name === 'PermissionDeniedError') {
        setError('Camera permission was denied. Allow camera access in your browser settings, then try again.')
      } else if (name === 'NotFoundError' || name === 'DevicesNotFoundError') {
        setError('No camera was found on this device.')
      } else if (name === 'NotReadableError' || name === 'TrackStartError') {
        setError('The camera is already being used by another application.')
      } else {
        setError('We could not start your camera. Check your browser permissions and try again.')
      }
    }
  }, [stopStream])

  useEffect(() => () => {
    if (recorderRef.current?.state === 'recording') recorderRef.current.stop()
    stopStream()
    if (captureUrlRef.current) URL.revokeObjectURL(captureUrlRef.current)
  }, [stopStream])

  const downloadCapture = (item: Capture) => {
    const anchor = document.createElement('a')
    anchor.href = item.url
    anchor.download = item.filename
    document.body.appendChild(anchor)
    anchor.click()
    anchor.remove()
  }

  const takePhoto = () => {
    const video = videoRef.current
    if (!video || !video.videoWidth || !video.videoHeight) return
    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const context = canvas.getContext('2d')
    if (!context) {
      setError('Photo capture is not available in this browser.')
      return
    }
    if (facingMode === 'user') {
      context.translate(canvas.width, 0)
      context.scale(-1, 1)
    }
    context.drawImage(video, 0, 0, canvas.width, canvas.height)
    canvas.toBlob((blob) => {
      if (!blob) {
        setError('We could not create this photo. Please try again.')
        return
      }
      if (capture?.url) URL.revokeObjectURL(capture.url)
      const url = URL.createObjectURL(blob)
      captureUrlRef.current = url
      const item = { url, filename: `iris-photo-${Date.now()}.jpg`, kind: 'photo' as const }
      setCapture(item)
      downloadCapture(item)
      setFlash(true)
      window.setTimeout(() => setFlash(false), 180)
    }, 'image/jpeg', 0.94)
  }

  const startRecording = () => {
    const stream = streamRef.current
    if (!stream || typeof MediaRecorder === 'undefined') {
      setError('Video recording is not supported by this browser.')
      return
    }
    const mimeType = ['video/webm;codecs=vp9', 'video/webm;codecs=vp8', 'video/webm'].find((type) => MediaRecorder.isTypeSupported(type))
    try {
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined)
      chunksRef.current = []
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunksRef.current.push(event.data)
      }
      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: recorder.mimeType || 'video/webm' })
        if (capture?.url) URL.revokeObjectURL(capture.url)
        const url = URL.createObjectURL(blob)
        captureUrlRef.current = url
        const item = { url, filename: `iris-video-${Date.now()}.webm`, kind: 'video' as const }
        setCapture(item)
        downloadCapture(item)
        setRecording(false)
      }
      recorderRef.current = recorder
      recorder.start(250)
      setRecording(true)
      setError('')
    } catch {
      setError('Recording could not start. Please try again.')
    }
  }

  const stopRecording = () => {
    if (recorderRef.current?.state === 'recording') recorderRef.current.stop()
  }

  const switchCamera = async () => {
    if (recording) return
    const next = facingMode === 'user' ? 'environment' : 'user'
    await startCamera(next)
  }

  return <main className="studio-screen">
    <header className="studio-header"><button className="studio-back" onClick={onBack}>← <span>Explore</span></button><a className="studio-wordmark" href="#" aria-label="IRIS Studio">iris<span>.</span> <small>STUDIO</small></a><span className="studio-live"><i /> {cameraState === 'ready' ? 'CAMERA READY' : 'PRIVATE SESSION'}</span></header>
    <div className="studio-layout">
      <section className="studio-stage">
        <div className="studio-stage-top"><div><span className="eyebrow">YOUR CREATIVE SPACE</span><h1>Camera <em>Studio.</em></h1></div><span className="studio-stage-index">IRIS / 002</span></div>
        <div className="camera-frame">
          <video ref={attachVideo} className={facingMode === 'user' ? 'camera-video mirrored' : 'camera-video'} autoPlay playsInline muted aria-label="Live camera preview" />
          <FaceLandmarkerOverlay video={videoElement} enabled={cameraState === 'ready'} mirrored={facingMode === 'user'} />
          {cameraState !== 'ready' && <div className="camera-overlay"><div className="camera-overlay-icon">{cameraState === 'loading' ? '◌' : '◎'}</div><b>{cameraState === 'loading' ? 'Waking up your camera…' : cameraState === 'error' ? 'Camera unavailable' : 'Ready when you are.'}</b><p>{cameraState === 'error' ? error : 'Your camera preview will appear here. Nothing is captured until you choose to.'}</p>{cameraState !== 'loading' && <button className="button button-primary" onClick={() => startCamera(facingMode)}>{cameraState === 'error' ? 'Try again' : 'Enable camera'} <span>→</span></button>}</div>}
          {flash && <div className="camera-flash" />}
          {cameraState === 'ready' && <><span className="camera-corner corner-tl" /><span className="camera-corner corner-tr" /><span className="camera-corner corner-bl" /><span className="camera-corner corner-br" /><div className="camera-frame-label"><i /> LIVE PREVIEW</div></>}
        </div>
        {error && cameraState === 'ready' && <p className="studio-inline-error" role="alert">{error}</p>}
        <div className="studio-controls"><button className="studio-tool" onClick={switchCamera} disabled={cameraState !== 'ready' || recording} aria-label="Switch camera"><span>⇄</span><small>FLIP</small></button><button className={recording ? 'shutter-button recording' : 'shutter-button'} onClick={recording ? stopRecording : takePhoto} disabled={cameraState !== 'ready'} aria-label={recording ? 'Stop recording' : 'Take photo'}><i /></button><button className="studio-tool" onClick={recording ? stopRecording : startRecording} disabled={cameraState !== 'ready'} aria-label={recording ? 'Stop video recording' : 'Start video recording'}><span>{recording ? '■' : '●'}</span><small>{recording ? 'STOP' : 'VIDEO'}</small></button></div>
        <p className="studio-hint">{recording ? 'Recording in progress · Select STOP to finish' : 'PHOTO · Tap the shutter to capture   /   VIDEO · Start and stop recording'}</p>
      </section>
      <aside className="studio-side">
        <div className="studio-side-heading"><span className="eyebrow">YOUR SESSION</span><h2>Make it yours.</h2><p>Your camera stays on this device. You decide what to capture and download.</p></div>
        <div className="studio-setting"><div><b>Mirror preview</b><small>Flip the selfie preview horizontally.</small></div><span className="setting-state">{facingMode === 'user' ? 'ON' : 'OFF'}</span></div>
        <div className="studio-setting"><div><b>Camera</b><small>{facingMode === 'user' ? 'Front-facing camera' : 'Back-facing camera'}</small></div><span className="setting-state"> {cameraState === 'ready' ? 'ACTIVE' : '—'} </span></div>
        <div className="studio-gallery"><div className="studio-gallery-title"><b>Latest capture</b><span>{capture ? '1 ITEM' : 'EMPTY'}</span></div>{capture ? <div className="capture-result"><div className="capture-thumb">{capture.kind === 'photo' ? '▧' : '▶'}</div><div className="capture-info"><b>{capture.kind === 'photo' ? 'Photo captured' : 'Video recorded'}</b><small>{capture.filename}</small><button onClick={() => downloadCapture(capture)}>Download again ↗</button></div></div> : <div className="capture-empty"><span>▧</span><p>Your photos and videos will show up here after capture.</p></div>}</div>
        <div className="studio-privacy"><span>✳</span><p><b>Private by design.</b><br />Camera access starts only when you allow it. Leaving Studio turns the camera off.</p></div>
      </aside>
    </div>
    <footer className="studio-footer"><span>IRIS © 2026</span><span>CAMERA STUDIO · 02 / 04</span></footer>
  </main>
}

export default CameraStudio
