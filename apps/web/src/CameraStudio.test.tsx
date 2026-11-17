import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import CameraStudio from './CameraStudio'

const setupMedia = (getUserMedia: ReturnType<typeof vi.fn>) => {
  Object.defineProperty(navigator, 'mediaDevices', {
    configurable: true,
    value: { getUserMedia },
  })
}

describe('IRIS Camera Studio', () => {
  beforeEach(() => {
    vi.spyOn(HTMLMediaElement.prototype, 'play').mockResolvedValue()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('asks for camera permission only after the visitor chooses to enable it', async () => {
    const getUserMedia = vi.fn().mockResolvedValue({
      getTracks: () => [{ stop: vi.fn() }],
    })
    setupMedia(getUserMedia)

    render(<CameraStudio onBack={vi.fn()} />)

    expect(getUserMedia).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: /enable camera/i }))

    await waitFor(() => expect(getUserMedia).toHaveBeenCalledWith({
      audio: false,
      video: { facingMode: { ideal: 'user' }, width: { ideal: 1280 }, height: { ideal: 720 } },
    }))
    expect(await screen.findByText(/camera ready/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /take photo/i })).toBeEnabled()
  })

  it('explains when camera permission is denied', async () => {
    const getUserMedia = vi.fn().mockRejectedValue(new DOMException('Permission denied', 'NotAllowedError'))
    setupMedia(getUserMedia)

    render(<CameraStudio onBack={vi.fn()} />)
    fireEvent.click(screen.getByRole('button', { name: /enable camera/i }))

    expect(await screen.findByText(/camera permission was denied/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument()
  })

  it('switches from the front camera to the rear camera', async () => {
    const getUserMedia = vi.fn().mockResolvedValue({
      getTracks: () => [{ stop: vi.fn() }],
    })
    setupMedia(getUserMedia)

    render(<CameraStudio onBack={vi.fn()} />)
    fireEvent.click(screen.getByRole('button', { name: /enable camera/i }))
    await screen.findByText(/camera ready/i)
    fireEvent.click(screen.getByRole('button', { name: /switch camera/i }))

    await waitFor(() => expect(getUserMedia).toHaveBeenLastCalledWith({
      audio: false,
      video: { facingMode: { ideal: 'environment' }, width: { ideal: 1280 }, height: { ideal: 720 } },
    }))
    expect(screen.getByText(/back-facing camera/i)).toBeInTheDocument()
  })

  it('returns to Explore when the visitor clicks the back control', () => {
    const onBack = vi.fn()
    render(<CameraStudio onBack={onBack} />)
    fireEvent.click(screen.getByRole('button', { name: /explore/i }))
    expect(onBack).toHaveBeenCalledOnce()
  })
})
