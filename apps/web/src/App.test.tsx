import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import App from './App'

describe('IRIS onboarding experience', () => {
  it('opens on the splash screen with the IRIS brand promise', () => {
    render(<App />)
    expect(screen.getByRole('heading', { name: /see beyond yourself/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /create your account/i })).toBeInTheDocument()
  })

  it('navigates from splash to sign in and back to sign up', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /i already have an account/i }))
    expect(screen.getByRole('heading', { name: /good to see you again/i })).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /create an account/i }))
    expect(screen.getByRole('heading', { name: /let's make some magic/i })).toBeInTheDocument()
  })

  it('opens password recovery from the sign-in screen', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /i already have an account/i }))
    fireEvent.click(screen.getByRole('button', { name: /forgot password/i }))
    expect(screen.getByRole('heading', { name: /forgot your password/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /send reset link/i })).toBeInTheDocument()
  })

  it('shows a confirmation state after submitting password recovery', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /i already have an account/i }))
    fireEvent.click(screen.getByRole('button', { name: /forgot password/i }))
    fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'hello@example.com' } })
    fireEvent.click(screen.getByRole('button', { name: /send reset link/i }))
    expect(screen.getByRole('heading', { name: /check your inbox/i })).toBeInTheDocument()
  })

  it('lets visitors explore the dashboard without pretending they are authenticated', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /explore iris first/i }))
    expect(screen.getByRole('heading', { name: /make a little more you/i })).toBeInTheDocument()
    expect(screen.getByText(/preview mode/i)).toBeInTheDocument()
  })

  it('filters the effect gallery by category and search term', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /explore iris first/i }))
    fireEvent.click(screen.getByRole('button', { name: 'Distortion' }))
    expect(screen.getByRole('heading', { name: 'Bubble face' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Tiny mouth' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Soft glow' })).not.toBeInTheDocument()
    fireEvent.change(screen.getByRole('textbox', { name: /search effects/i }), { target: { value: 'tiny' } })
    expect(screen.getByRole('heading', { name: 'Tiny mouth' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Bubble face' })).not.toBeInTheDocument()
  })

  it('opens the camera studio preview from the dashboard', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /explore iris first/i }))
    fireEvent.click(screen.getByRole('button', { name: /open camera studio/i }))
    expect(screen.getByRole('heading', { name: /your camera\. your canvas\./i })).toBeInTheDocument()
  })
})
