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
})
