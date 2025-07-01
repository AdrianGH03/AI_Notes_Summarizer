import { useState, useEffect, useCallback } from 'react'
import { LogOut, Upload, FileText, Zap, Info } from 'lucide-react'
import { resumeAPI, notesAPI } from '../services/api'
import { demoResumes, demoSummaryResult, demoJobAd } from '../data/demoData'

const Dashboard = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState('upload')
  const [resumes, setResumes] = useState([])
  const [jobAdText, setJobAdText] = useState('')
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  //Demo mode detection
  const isDemoMode = user.id === 999

  //Job Ad summarization states
  const [jobAds, setJobAds] = useState([])
  const [hoveredJobAdId, setHoveredJobAdId] = useState(null)
  const [companyName, setCompanyName] = useState('')

  //Resume upload states
  const [selectedFile, setSelectedFile] = useState(null)
  const [resumeName, setResumeName] = useState('')
  const [hoveredResumeId, setHoveredResumeId] = useState(null)

  //Resume improvement states
  const [selectedResumeForImprovement, setSelectedResumeForImprovement] = useState('')
  const [improvements, setImprovements] = useState(null)

  //Get all of user's resumes
  const fetchUserResumes = useCallback(async () => {
    if (isDemoMode) {
      setResumes(demoResumes)
      return
    }

    try {
      const userResumes = await resumeAPI.getUserResumes(user.id)
      setResumes(userResumes)

    } catch {
      console.log('No resumes found or error fetching resumes')
      setResumes([])
    }
  }, [user.id, isDemoMode])

  const fetchJobAds = useCallback(async () => {
    let jobAdsData = []
    try {
      if (isDemoMode){
        jobAdsData = await notesAPI.getAllJobAds(demoResumes[0].id) // <-- add await here
      } else {
        jobAdsData = await notesAPI.getAllJobAds(user.id)
      }
      setJobAds(jobAdsData)
    }
    catch (err) {
      console.error('Error fetching job ads:', err)
      setError('Error fetching job ads')
    }
  }, [user.id, isDemoMode])

  useEffect(() => {
    fetchUserResumes()
    fetchJobAds()
  }, [fetchUserResumes, fetchJobAds])

  //Upload file
  const handleFileUpload = async (e) => {
    e.preventDefault()
    
    if (isDemoMode) {
      setError('Demo mode: File upload is disabled. This feature requires backend connection.')
      return
    }
    
    if (!selectedFile || !resumeName) {
      setError('Please select a file and enter a resume name')
      return
    }

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      await resumeAPI.uploadResume(user.id, resumeName, selectedFile)
      setSuccess('Resume uploaded successfully!')
      setSelectedFile(null)
      setResumeName('')
      fetchUserResumes()
    } catch (err) {
      setError(err.response?.data?.detail || 'Error uploading resume')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteResume = async (resumeName) => {
    if (isDemoMode) {
      setError('Demo mode: Resume deletion is disabled. This feature requires backend connection.')
      return  
    }
    if (!resumeName) {
      setError('Please select a resume to delete')
      return
    }
    setLoading(true)
    setError('')
    setSuccess('')
    try {
      await resumeAPI.deleteResume(user.id, resumeName)
      setSuccess('Resume deleted successfully!')
      setSelectedResumeForImprovement('')
      setImprovements(null)
      fetchUserResumes()
    } catch (err) {
      setError(err.response?.data?.detail || 'Error deleting resume')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteJobAd = async (jobAdId) => {
    if (!jobAdId) {
      setError('Please select a job ad to delete')
      return
    }
    setLoading(true)
    setError('')
    setSuccess('')
    try {
      if (isDemoMode) {
        await notesAPI.deleteJobAd(demoResumes[0].id, jobAdId)
      } else {
        await notesAPI.deleteJobAd(user.id, jobAdId)
      }
      setSuccess('Job ad deleted successfully!')
      setSelectedResumeForImprovement('')
      setImprovements(null)
      setSummary(null)
      fetchJobAds()
    } catch (err) {
      setError(err.response?.data?.detail || 'Error deleting job ad')
    } finally {
      setLoading(false)
    }
  }

  //Summarize job ad
  const handleJobAdSummarize = async (e) => {
    e.preventDefault()
    
    if (!jobAdText.trim()) {
      setError('Please enter job ad text')
      return
    }
    if (!companyName.trim()) {
      setError('Please enter a company name')
      return
    }

    setSummary(null)
    setSelectedResumeForImprovement('')
    setImprovements(null)

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      let result
      if(isDemoMode){
        result = await notesAPI.summarizeJobAd(demoResumes[0].id, jobAdText, demoSummaryResult.company_name)
      } else {
        result = await notesAPI.summarizeJobAd(user.id, jobAdText, companyName)
      }
     
      setSummary(result)
      setSuccess('Job ad summarized successfully!')
    } catch (err) {
      setError(err.response?.data?.detail || 'Error summarizing job ad')
    } finally {
      setLoading(false)
    }
  }

  const handleLoadDemoJobAd = () => {
    setJobAdText(demoJobAd)
    clearMessages()
  }

  //Get resume improvement suggestions
  const handleResumeImprovement = async (e) => {
    e.preventDefault()
    if (!selectedResumeForImprovement || !summary) {
      setError('Please select a resume and summarize a job ad first')
      return
    }
    try {
        setLoading(true)
        setError('')
        
        let updatedResume;
        if(isDemoMode){
            updatedResume = await resumeAPI.updateResumeKeywords(demoResumes[0].id, selectedResumeForImprovement, demoSummaryResult.jobad_id)
        } else {
            if(!summary.jobad_id) {
                setError('Resume improvement feature requires a job ad ID from the database. Please contact support.')
                return
            }
            updatedResume = await resumeAPI.updateResumeKeywords(user.id, selectedResumeForImprovement, summary.jobad_id)
        }
        
        if (updatedResume) {
            setSuccess('Resume improvement suggestions retrieved successfully!')
            setImprovements({
              ...updatedResume.suggestions,
              original_resume: updatedResume.original_resume
            }) 
        } else {
            setError('Failed to retrieve resume improvement suggestions. Please try again.')
        }

    } catch (err) {
      setError(err.response?.data?.detail || 'Error getting resume improvements')
    } finally {
      setLoading(false)
    }
  }

  const clearMessages = () => {
    setError('')
    setSuccess('')
  }

  return (
    <div className="dashboard">

      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>AI Resume Summarizer</h1>
          <div className="user-info">
            <span>Welcome, {user.email}</span>
            {isDemoMode && <span className="demo-badge">Demo Mode</span>}
            <button onClick={onLogout} className="logout-button">
              <LogOut size={20} />
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Upload resume content */}
      <div className="dashboard-content">
        <nav className="dashboard-nav">
          <button 
            className={`nav-button ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => {setActiveTab('upload'); clearMessages()}}
          >
            <Upload size={20} />
            Upload Resume
          </button>
          <button 
            className={`nav-button ${activeTab === 'summarize' ? 'active' : ''}`}
            onClick={() => {setActiveTab('summarize'); clearMessages()}}
          >
            <FileText size={20} />
            Summarize Job Ad
          </button>
          <button 
            className={`nav-button ${activeTab === 'improve' ? 'active' : ''}`}
            onClick={() => {setActiveTab('improve'); clearMessages()}}
          >
            <Zap size={20} />
            Improve Resume
          </button>
        </nav>

        <main className="dashboard-main">
          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          {isDemoMode && (
            <div className="demo-info">
              <Info size={20} />
              <span>You're in demo mode. Some features are limited without backend connection.</span>
            </div>
          )}

          {activeTab === 'upload' && (
            <div className="tab-content">
              <h2>Upload Resume</h2>
              <form onSubmit={handleFileUpload} className="upload-form">
                <div className="input-group">
                  <label htmlFor="resumeName">Resume Name</label>
                  <input
                    type="text"
                    id="resumeName"
                    value={resumeName}
                    onChange={(e) => setResumeName(e.target.value)}
                    placeholder="Enter a name for your resume"
                    required
                    disabled={isDemoMode}
                  />
                </div>
                
                <div className="input-group">
                  <label htmlFor="fileInput">Select PDF File</label>
                  <input
                    type="file"
                    id="fileInput"
                    accept=".pdf"
                    onChange={(e) => setSelectedFile(e.target.files[0])}
                    required
                    disabled={isDemoMode}
                  />
                  {selectedFile && (
                    <p className="file-info">Selected: {selectedFile.name}</p>
                  )}
                </div>

                <button type="submit" disabled={loading || isDemoMode} className="submit-button">
                  {loading ? 'Uploading...' : 'Upload Resume'}
                </button>
              </form>

              <div className="resumes-list">
                <h3>Your Resumes</h3>
                {resumes.length > 0 ? (
                  <ul>
                    {resumes.map((resume) => (
                      <li
                        key={resume.id}
                        className="resume-item"
                        onMouseEnter={() => setHoveredResumeId(resume.id)}
                        onMouseLeave={() => setHoveredResumeId(null)}
                      >
                        <span>{resume.resume_name}</span>
                        <span className="upload-date">
                          {hoveredResumeId === resume.id ? (
                            <span
                              style={{ color: 'red', cursor: 'pointer' }}
                              onClick={() => handleDeleteResume(resume.resume_name)}
                            >
                              Delete
                            </span>
                          ) : (
                            'Uploaded'
                          )}
                        </span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No resumes uploaded yet.</p>
                )}
              </div>
            </div>
          )}

          {/* Summarize Job Ad Tab */}
          {activeTab === 'summarize' && (
            <div className="tab-content">
              <h2>Summarize Job Advertisement</h2>
              
              {isDemoMode && (
                <div className="demo-controls">
                  <button 
                    onClick={handleLoadDemoJobAd}
                    className="demo-load-button"
                    type="button"
                  >
                    <FileText size={16} />
                    Load Demo Job Ad
                  </button>
                </div>
              )}

              <div className="input-group">
                <label htmlFor="companyName">Company Name</label>
                <input
                  type="text"
                  id="companyName"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  placeholder="Enter a name for this company"
                  required
                />
              </div>

              <form onSubmit={handleJobAdSummarize} className="summarize-form">
                <div className="input-group">
                  <label htmlFor="jobAdText">Job Advertisement Text</label>
                  <textarea
                    id="jobAdText"
                    value={jobAdText}
                    onChange={(e) => setJobAdText(e.target.value)}
                    placeholder="Paste the job advertisement text here..."
                    rows="10"
                    required
                  />
                </div>

                <button type="submit" disabled={loading} className="submit-button">
                  {loading ? 'Summarizing...' : 'Summarize Job Ad'}
                </button>

              </form>

              {/* DO NOT CONFUSE WITH RESUMES LIST, SIMILAR BUT NEEDS SAME STYLING */}
              <div
                className="resumes-list"
                style={{
                  maxHeight: '300px',
                  overflowY: 'auto',
                  overflowX: 'hidden'
                }}
              >
                <h3>Your Job Ads</h3>
                {jobAds.length > 0 ? (
                  <ul>
                    {jobAds.map((jobad) => (
                      <li
                        key={jobad.id}
                        className="resume-item"
                        onMouseEnter={() => setHoveredJobAdId(jobad.id)}
                        onMouseLeave={() => setHoveredJobAdId(null)}
                      >
                        <span>{jobad ? (jobad.company_name ? jobad.company_name : `Company #${jobad.id}`) : ''}</span>
                        <span className="upload-date">
                          {hoveredJobAdId === jobad.id ? (
                            <span
                              style={{ color: 'red', cursor: 'pointer' }}
                              onClick={() => handleDeleteJobAd(jobad.id)}
                            >
                              Delete
                            </span>
                          ) : (
                            'Summarized'
                          )}
                        </span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No Job Ads summarized yet.</p>
                )}
              </div>
            
              


              {summary && (
                <div className="summary-results">
                  <h3>Summary Results</h3>
                  
                  <div className="summary-section">
                    <h4>Summary</h4>
                    <p>{summary.summarized_text}</p>
                  </div>

                  <div className="summary-section">
                    <h4>Keywords</h4>
                    <div className="keywords">
                      {summary.keywords.split(',').map((keyword, index) => (
                        <span key={index} className="keyword-tag">
                          {keyword.trim()}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="summary-section">
                    <h4>Requirements</h4>
                    <p>{summary.requirements}</p>
                  </div>

                  {summary.message && (
                    <div className="info-message">
                      <p>{summary.message}</p>
                    </div>
                  )}
                </div>
                
              )}
            </div>
          )}

          {/* Improve Resume Tab */}
          {activeTab === 'improve' && (
            <div className="tab-content">
              <h2>Get Resume Improvement Suggestions</h2>
              
              {!summary && (
                <div className="info-message">
                  <p>Please summarize a job ad first to get resume improvement suggestions.</p>
                </div>
              )}

              {summary && (
                <form onSubmit={handleResumeImprovement} className="improve-form">
                  <div className="input-group">
                    <label htmlFor="resumeSelect">Select Resume</label>
                    <select
                      id="resumeSelect"
                      value={selectedResumeForImprovement}
                      onChange={(e) => setSelectedResumeForImprovement(e.target.value)}
                      required
                    >
                      <option value="">Choose a resume...</option>
                      {resumes.map((resume) => (
                        <option key={resume.id} value={resume.resume_name}>
                          {resume.resume_name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="info-message">
                    <p>This will analyze your resume against the job requirements and suggest improvements.</p>
                  </div>

                  <button type="submit" disabled={loading || resumes.length === 0} className="submit-button">
                    {loading ? 'Analyzing...' : 'Get Suggestions'}
                  </button>
                </form>
              )}

              {improvements && (
                <div className="improvements-results">
                  <div className="improvements-header">
                    <h3>📊 Resume Analysis Results</h3>
                    <p className="analysis-subtitle">AI-powered analysis of your resume against the job requirements</p>
                  </div>
                  
                  <div className="improvements-grid">
                    {/* Missing Keywords Section */}
                    {improvements.missing_keywords && improvements.missing_keywords.length > 0 && (
                      <div className="improvement-card keywords-card">
                        <div className="card-header">
                          <h4>🔍 Missing Keywords</h4>
                          <span className="keyword-count">{improvements.missing_keywords.length} missing</span>
                        </div>
                        <p className="card-description">Consider adding these keywords to improve your resume's visibility:</p>
                        <div className="keywords-container">
                          {improvements.missing_keywords.map((keyword, index) => (
                            <span key={index} className="keyword-tag missing-keyword">
                              {keyword.trim()}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Unmet Requirements Section */}
                    {improvements.unmet_requirements && (
                      <div className="improvement-card requirements-card">
                        <div className="card-header">
                          <h4>⚠️ Improvement Areas</h4>
                        </div>
                        <p className="card-description">Areas where your resume could be strengthened:</p>
                        <div className="requirements-container">
                          {Array.isArray(improvements.unmet_requirements) ? (
                            <ul className="requirements-list">
                              {improvements.unmet_requirements.map((req, index) => (
                                <li key={index} className="requirement-item">
                                  <span className="requirement-bullet">•</span>
                                  {req}
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <div className="requirement-text">
                              <p>{improvements.unmet_requirements}</p>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Success Message */}
                    {(!improvements.missing_keywords || improvements.missing_keywords.length === 0) && 
                     !improvements.unmet_requirements && (
                      <div className="improvement-card success-card">
                        <div className="card-header">
                          <h4>✅ Excellent Match!</h4>
                        </div>
                        <p className="success-message">
                          Great! Your resume appears to be well-aligned with the job requirements. 
                          You've included most of the relevant keywords and meet the key requirements.
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Original Resume Text Section */}
                  <div className="original-resume-section">
                    <div className="resume-text-header">
                      <h4>📄 Your Resume Content</h4>
                      <p className="resume-text-subtitle">This is the text that was analyzed from your resume</p>
                    </div>
                    <div className="resume-text-container">
                      <div className="resume-text-content">
                        {improvements.original_resume ? (
                          <pre className="resume-text">{improvements.original_resume}</pre>
                        ) : (
                          <p className="no-resume-text">Resume text not available</p>
                        )}
                      </div>
                      <div className="resume-text-actions">
                        <button 
                          className="copy-button"
                          onClick={() => navigator.clipboard.writeText(improvements.original_resume || '')}
                        >
                          📋 Copy Text
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

export default Dashboard
