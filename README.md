# 🤖 AI Notes Summarizer

**AI Notes Summarizer** is a backend-powered AI tool that helps job seekers analyze job ads, summarize them, extract keywords, and intelligently compare them to uploaded resumes.

> _Summarize. Compare. Improve._

---

## ⚙️ Key Features

- 📝 **Job Ad Summarization**  
  Uses AI to extract keywords and requirements from job descriptions.

- 📄 **Resume Analysis**  
  Matches your resume to job ad keywords and requirements with intelligent, fuzzy comparison logic.

- ☁️ **AWS S3 Resume Storage**  
  Securely stores user resumes in the cloud.

- 🐘 **PostgreSQL Integration**  
  Job ads, summaries, and resume metadata are stored and queried from a PostgreSQL database.

- 🐳 **Dockerized App**  
  Fully containerized with Docker for easy local development.

---

## 🧰 Tech Stack

- **Backend:** Python, FastAPI  
- **Frontend:** React, Vite, JavaScript, CSS
- **AI Processing:** Hugging Face Transformers  
- **Database:** PostgreSQL  
- **Storage:** AWS S3 (via Boto3)  
- **Containerization:** Docker, Docker Compose  

---

## 🎥 Demo and Screenshots

![Screenshot 2025-06-29 002709](https://github.com/user-attachments/assets/c961b496-064f-4814-b852-a523a7423f9b)
![Screenshot 2025-06-29 002721](https://github.com/user-attachments/assets/fe38a4e5-bbfb-4b97-aeb0-b52af33408ec)

https://github.com/user-attachments/assets/90b96ff6-25cd-4784-b0b3-b461f32675d4

---

## 🚀 How to Run Locally (with Docker)

1. Clone the repository:
   ```bash
   git clone https://github.com/AdrianGH03/AI_Notes_Summarizer
   ```

2. Create a `.env` file in `ai-notes-summarizer/` with:

   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=yourpassword
   POSTGRES_DB=ai_notes_db
   DATABASE_URL=postgresql://postgres:yourpassword@db:5432/ai_notes_db
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_REGION=your_region
   S3_BUCKET=your_bucket_name
   ```

   Replace `your_key`, `your_secret`, `your_region`, and `your_bucket_name` with your actual AWS credentials and S3 bucket name.

3. Create a `.env` file in `ai-notes-summarizer-fe` with:

   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```

4. From the project root, run:

   ```bash
   docker-compose up --build
   ```

5. Access the app:

   * **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
   * **Frontend:** [http://localhost:3000](http://localhost:3000)

---

## License

```
Copyright [2025] [Miguel Gomez]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```


