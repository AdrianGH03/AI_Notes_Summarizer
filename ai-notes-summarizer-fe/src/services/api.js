import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

//Auth endpoints
export const authAPI = {
  login: async (email, resumeName = null) => {
    const response = await api.post('/auth/login', { 
      email, 
      resume_name: resumeName 
    })
    return response.data
  },

  signup: async (email, resumeName = null) => {
    const response = await api.post('/auth/signup', { 
      email, 
      resume_name: resumeName 
    })
    return response.data
  }
}

//Resume endpoints
export const resumeAPI = {
  uploadResume: async (userId, resumeName, file) => {
    const formData = new FormData()
    formData.append('user_id', userId)
    formData.append('resume_name', resumeName)
    formData.append('file', file)

    const response = await axios.post(`${API_BASE_URL}/resume/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  getUserResumes: async (userId) => {
    const response = await api.get(`/resume/resumes/${userId}`)
    return response.data
  },

  replaceResumeFile: async (userId, newResumeName, file) => {
    const formData = new FormData()
    formData.append('user_id', userId)
    formData.append('new_resume_name', newResumeName)
    formData.append('file', file)

    const response = await axios.put(`${API_BASE_URL}/resume/replace_resume_file`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  updateResumeKeywords: async (userId, resumeName, jobadId) => {
    const response = await api.post('/resume/update_resume_keywords', null, {
      params: {
        user_id: userId,
        resume_name: resumeName,
        jobad_id: jobadId
      }
    })
    return response.data
  },

  deleteResume: async (userId, resumeName) => {
    const response = await api.delete('/resume/delete_resume', {
      params: {
        user_id: userId,
        resume_name: resumeName
      }
    })
    return response.data
  }
}

//Notes endpoints
export const notesAPI = {
  summarizeJobAd: async (userId, text, company_name) => {
    const formData = new FormData()
    formData.append('user_id', userId)
    formData.append('text', text)
    formData.append('company_name', company_name)
    

    const response = await axios.post(`${API_BASE_URL}/notes/summarize`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  getAllJobAds: async (userId) => {
    const response = await api.get(`/notes/summaries-list/${userId}`)
    return response.data
  },

  deleteJobAd: async (userId, jobadId) => {
    const response = await api.delete(`/notes/delete/${jobadId}/${userId}`)
    return response.data
  }
}

export default api
