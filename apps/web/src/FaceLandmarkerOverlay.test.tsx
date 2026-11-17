import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import FaceLandmarkerOverlay from './FaceLandmarkerOverlay'

describe('IRIS Face Landmarker overlay', () => {
  it('does not initialize or render the overlay while face tracking is disabled', () => {
    const { container } = render(
      <FaceLandmarkerOverlay video={null} enabled={false} mirrored={false} />,
    )

    expect(container.querySelector('canvas')).not.toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })
})
