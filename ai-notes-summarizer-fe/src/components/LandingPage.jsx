import { useState } from 'react'
import { ArrowRight, Upload, FileText, Zap, Check } from 'lucide-react'

const LandingPage = ({ onGetStarted }) => {
  const [isLoading, setIsLoading] = useState(false)

  const handleGetStarted = () => {
    setIsLoading(true)
    setTimeout(() => {
      onGetStarted()
    }, 500)
  }

  return (
    <div className="landing-page">
      <div className="landing-container">
        <header className="landing-header">
          <h1 className="landing-title">
            AI Resume Summarizer
          </h1>
          <p className="landing-subtitle">
            Optimize your resume with AI-powered job analysis and get personalized improvement suggestions
          </p>
        </header>

        <div className="features-grid">
          <div className="feature-card">
            <Upload className="feature-icon" size={32} />
            <h3>Upload Resume</h3>
            <p>Securely upload your PDF resume and manage multiple versions</p>
          </div>
          
          <div className="feature-card">
            <FileText className="feature-icon" size={32} />
            <h3>Analyze Job Ads</h3>
            <p>Get AI-powered summaries, keywords, and requirements from job postings</p>
          </div>
          
          <div className="feature-card">
            <Zap className="feature-icon" size={32} />
            <h3>Get Suggestions</h3>
            <p>Receive personalized recommendations to improve your resume</p>
          </div>
        </div>

        <div className="benefits-section">
          <h2>Why Choose AI Resume Summarizer?</h2>
          <div className="benefits-list">
            <div className="benefit-item">
              <Check size={20} />
              <span>Save time analyzing job requirements</span>
            </div>
            <div className="benefit-item">
              <Check size={20} />
              <span>Identify key skills and keywords</span>
            </div>
            <div className="benefit-item">
              <Check size={20} />
              <span>Improve your resume targeting</span>
            </div>
            <div className="benefit-item">
              <Check size={20} />
              <span>Increase interview opportunities</span>
            </div>
          </div>
        </div>

        <div className="cta-section">
          <button 
            className="cta-button" 
            onClick={handleGetStarted}
            disabled={isLoading}
          >
            {isLoading ? 'Loading...' : 'Get Started'}
            {!isLoading && <ArrowRight size={20} />}
          </button>
          <p className="cta-text">
            Start optimizing your resume in minutes. No credit card required.
          </p>
        </div>
      </div>
    </div>
  )
}

export default LandingPage
