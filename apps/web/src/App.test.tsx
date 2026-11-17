import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import App from './App'

describe('IRIS application shell', () => {
  it('renders the brand and its tagline', () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: 'IRIS' })).toBeInTheDocument()
    expect(screen.getByText('See beyond yourself.')).toBeInTheDocument()
  })

  it('shows the camera experience placeholder message', () => {
    render(<App />)

    expect(
      screen.getByText('The creative camera experience is being prepared.'),
    ).toBeInTheDocument()
  })
})
