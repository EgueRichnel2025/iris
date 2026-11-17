import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import App from './App'

// Keep UI tests isolated from the developer's local Supabase project.
vi.mock('./lib/supabase', () => ({ supabase: null }))

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

  it('explains that password recovery needs Supabase configuration', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /i already have an account/i }))
    fireEvent.click(screen.getByRole('button', { name: /forgot password/i }))
    fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'hello@example.com' } })
    fireEvent.click(screen.getByRole('button', { name: /send reset link/i }))
    expect(screen.getByRole('alert')).toHaveTextContent(/supabase is configured/i)
  })

  it('shows a clear setup message when a visitor submits sign up without auth credentials', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /create your account/i }))
    fireEvent.change(screen.getByLabelText(/your name/i), { target: { value: 'Test User' } })
    fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'test@example.com' } })
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } })
    fireEvent.click(screen.getByRole('checkbox', { name: /terms of service/i }))
    fireEvent.click(screen.getByRole('button', { name: /create account/i }))
    expect(screen.getByRole('status')).toHaveTextContent(/VITE_SUPABASE_URL/i)
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
    expect(screen.getByRole('heading', { name: /camera studio/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /enable camera/i })).toBeInTheDocument()
  })
})
