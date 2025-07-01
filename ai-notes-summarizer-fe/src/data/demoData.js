// Demo data for testing the application

export const demoJobAd = `Senior Software Engineer - Full Stack Development

Company: TechCorp Solutions
Location: San Francisco, CA (Remote friendly)
Salary: $120,000 - $160,000

Job Description:
We are seeking a highly skilled Senior Software Engineer to join our growing team. The ideal candidate will have extensive experience in full-stack development and a passion for building scalable web applications.

Key Responsibilities:
• Design and develop robust, scalable web applications using modern technologies
• Collaborate with cross-functional teams to define and implement new features
• Write clean, maintainable, and well-documented code
• Participate in code reviews and provide constructive feedback
• Mentor junior developers and contribute to technical decisions
• Optimize application performance and ensure high availability
• Work with DevOps team to deploy and monitor applications

Required Skills:
• 5+ years of experience in software development
• Proficiency in JavaScript, TypeScript, Python, or Java
• Experience with React, Vue.js, or Angular
• Strong knowledge of Node.js and Express.js
• Database experience with PostgreSQL, MongoDB, or MySQL
• Familiarity with cloud platforms (AWS, GCP, or Azure)
• Experience with containerization (Docker, Kubernetes)
• Understanding of microservices architecture
• Proficiency with Git and version control workflows
• Strong problem-solving and debugging skills

Preferred Qualifications:
• Bachelor's degree in Computer Science or related field
• Experience with CI/CD pipelines
• Knowledge of testing frameworks (Jest, Cypress, PyTest)
• Familiarity with GraphQL and REST APIs
• Experience with message queues (Redis, RabbitMQ)
• Previous experience in agile development methodologies
• Excellent communication and teamwork skills

Benefits:
• Competitive salary and equity package
• Comprehensive health, dental, and vision insurance
• 401(k) with company matching
• Flexible PTO and work-from-home options
• Professional development budget
• Modern office with state-of-the-art equipment

Apply now to join our innovative team and help shape the future of technology!`

export const demoSummaryResult = {
  original_text: demoJobAd,
  summarized_text: "Senior Software Engineer position at TechCorp Solutions requiring 5+ years experience in full-stack development. The role involves building scalable web applications, mentoring junior developers, and working with modern technologies including JavaScript/TypeScript, React/Vue/Angular, Node.js, and cloud platforms. The position offers $120K-$160K salary with comprehensive benefits and remote work options.",
  keywords: "JavaScript, TypeScript, Python, Java, React, Vue.js, Angular, Node.js, Express.js, PostgreSQL, MongoDB, MySQL, AWS, GCP, Azure, Docker, Kubernetes, microservices, Git, CI/CD, GraphQL, REST APIs",
  requirements: "5+ years software development experience, proficiency in modern programming languages and frameworks, database knowledge, cloud platform experience, containerization skills, version control proficiency, strong problem-solving abilities, and excellent communication skills. Bachelor's degree preferred.",
  message: "Demo data - showing example job ad analysis",
  jobad_id: 3,
  company_name: "TechCorp Solutions"
}

export const demoResumes = [
  {
    id: 2,
    resume_name: "demo_resume.pdf.pdf",
    created_at: "2025-06-15T10:30:00Z",
    s3_key: "2/demo_resume.pdf.pdf"
  }
]

export const demoUser = {
  id: 999,
  email: "demo@example.com",
  resume_name: "demo_resume.pdf"
}
