import { useEffect, useRef, useState } from 'react'
import { FaceLandmarker, FilesetResolver } from '@mediapipe/tasks-vision'

type VisionStatus = 'loading' | 'ready' | 'no-face' | 'error'
type Props = { video: HTMLVideoElement | null; enabled: boolean; mirrored: boolean }

const WASM_URL = 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.2.3/wasm'
const MODEL_URL = 'https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task'

export default function FaceLandmarkerOverlay({ video, enabled, mirrored }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [status, setStatus] = useState<VisionStatus>('loading')
  const [mouthOpen, setMouthOpen] = useState(0)

  useEffect(() => {
    if (!enabled || !video) return
    let cancelled = false
    let frame = 0
    let landmarker: FaceLandmarker | null = null
    let lastVideoTime = -1

    const draw = () => {
      if (cancelled || !landmarker || video.readyState < HTMLMediaElement.HAVE_CURRENT_DATA) {
        if (!cancelled) frame = requestAnimationFrame(draw)
        return
      }
      if (video.currentTime !== lastVideoTime) {
        lastVideoTime = video.currentTime
        const canvas = canvasRef.current
        const context = canvas?.getContext('2d')
        if (canvas && context && video.videoWidth && video.videoHeight) {
          if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
            canvas.width = video.videoWidth
            canvas.height = video.videoHeight
          }
          context.clearRect(0, 0, canvas.width, canvas.height)
          try {
            const result = landmarker.detectForVideo(video, performance.now())
            const landmarks = result.faceLandmarks[0]
            if (landmarks) {
              context.fillStyle = '#C7E56B'
              for (let index = 0; index < landmarks.length; index += 2) {
                const point = landmarks[index]
                context.beginPath()
                context.arc(point.x * canvas.width, point.y * canvas.height, Math.max(1.5, canvas.width / 500), 0, Math.PI * 2)
                context.fill()
              }
              context.fillStyle = '#F27E70'
              for (const index of [0,13,14,17,37,39,40,61,78,81,82,84,87,88,91,95,146,178,181,185,267,269,270,291,308,311,312,314,317,318,321,324,375,402,405,409]) {
                const point = landmarks[index]
                if (!point) continue
                context.beginPath()
                context.arc(point.x * canvas.width, point.y * canvas.height, Math.max(2.5, canvas.width / 300), 0, Math.PI * 2)
                context.fill()
              }
              const openness = result.faceBlendshapes[0]?.categories.find((item) => item.categoryName === 'jawOpen')?.score ?? 0
              setMouthOpen(openness)
              setStatus('ready')
            } else {
              setStatus('no-face')
              setMouthOpen(0)
            }
          } catch {
            setStatus('error')
          }
        }
      }
      frame = requestAnimationFrame(draw)
    }

    const initialize = async () => {
      setStatus('loading')
      try {
        const fileset = await FilesetResolver.forVisionTasks(WASM_URL)
        try {
          landmarker = await FaceLandmarker.createFromOptions(fileset, {
            baseOptions: { modelAssetPath: MODEL_URL, delegate: 'GPU' },
            runningMode: 'VIDEO', numFaces: 1,
            outputFaceBlendshapes: true, outputFacialTransformationMatrixes: true,
          })
        } catch {
          landmarker = await FaceLandmarker.createFromOptions(fileset, {
            baseOptions: { modelAssetPath: MODEL_URL, delegate: 'CPU' },
            runningMode: 'VIDEO', numFaces: 1,
            outputFaceBlendshapes: true, outputFacialTransformationMatrixes: true,
          })
        }
        if (cancelled) { landmarker.close(); return }
        setStatus('no-face')
        frame = requestAnimationFrame(draw)
      } catch {
        setStatus('error')
      }
    }

    void initialize()
    return () => {
      cancelled = true
      cancelAnimationFrame(frame)
      landmarker?.close()
    }
  }, [enabled, video])

  if (!enabled) return null
  return <>
    <canvas ref={canvasRef} className={`face-landmarks-canvas${mirrored ? ' mirrored' : ''}`} aria-label="Facial landmarks overlay" />
    <div className="vision-status" role="status">
      <span className={`vision-status-dot vision-${status}`} />
      {status === 'loading' && 'Loading face model…'}
      {status === 'ready' && `Face tracked · Mouth ${Math.round(mouthOpen * 100)}%`}
      {status === 'no-face' && 'Looking for a face…'}
      {status === 'error' && 'Face tracking unavailable'}
    </div>
  </>
}
