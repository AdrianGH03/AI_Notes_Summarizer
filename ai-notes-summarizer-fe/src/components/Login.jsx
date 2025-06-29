import { useState } from 'react'
import { Play } from 'lucide-react'
import { authAPI } from '../services/api'
import { demoUser } from '../data/demoData'

const Login = ({ onLogin }) => {
  const [isSignup, setIsSignup] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    resumeName: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      let userData
      if (isSignup) {
        userData = await authAPI.signup(formData.email, formData.resumeName || null)
      } else {
        userData = await authAPI.login(formData.email, formData.resumeName || null)
      }
      onLogin(userData)
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleDemoMode = () => {
    setLoading(true)
    setTimeout(() => {
      onLogin(demoUser)
      setLoading(false)
    }, 1000)
  }

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>AI Resume Summarizer</h1>
          <p>{isSignup ? 'Create your account' : 'Welcome back'}</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="input-group">
            <input
              type="email"
              name="email"
              placeholder="Email address"
              value={formData.email}
              onChange={handleInputChange}
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? 'Processing...' : (isSignup ? 'Sign Up' : 'Login')}
          </button>
        </form>

        <div className="demo-section">
          <div className="divider">
            <span>or</span>
          </div>
          <button 
            type="button" 
            className="demo-button"
            onClick={handleDemoMode}
            disabled={loading}
          >
            <Play size={20} />
            Try Demo Mode
          </button>
          <p className="demo-text">
            Test the application with sample data (no backend required)
          </p>
        </div>

        <div className="login-footer">
          <p>
            {isSignup ? 'Already have an account?' : "Don't have an account?"}
            <button 
              type="button" 
              className="link-button"
              onClick={() => setIsSignup(!isSignup)}
            >
              {isSignup ? 'Login' : 'Sign Up'}
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login
