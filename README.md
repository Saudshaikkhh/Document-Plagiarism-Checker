# Document Plagiarism Checker

A comprehensive AI-powered plagiarism detection system that analyzes academic documents containing Assessment Criteria (A.C.) sections. The application provides detailed plagiarism assessment, generates professional tutor feedback, and creates formatted PDF reports suitable for academic institutions.

## Features

- **Multi-format Support**: Processes both DOCX and PDF documents
- **AI-Powered Analysis**: Uses OpenAI GPT-4.1 for intelligent plagiarism detection
- **Assessment Criteria Processing**: Automatically extracts and analyzes A.C. sections
- **Professional Reports**: Generates comprehensive PDF reports with tutor feedback
- **Real-time Processing**: Live progress tracking with detailed status updates
- **Missing Section Detection**: Identifies and fills gaps in A.C. section sequences
- **Topic Recognition**: Automatically detects document subject matter for contextual analysis

## Dependencies

Install the required libraries using pip:

```bash
pip install streamlit
pip install python-docx
pip install PyPDF2
pip install azure-ai-inference
pip install azure-core
pip install reportlab
```

Or install all dependencies at once:
```bash
pip install streamlit python-docx PyPDF2 azure-ai-inference azure-core reportlab
```

## API Setup

To use OpenAI GPT-4.1 from the GitHub Marketplace via Azure:

1. **Access GitHub Models Marketplace**:
   - Go to https://github.com/marketplace/models
   - Search for "OpenAI GPT-4.1"
   - Click the "Use this model" button
   - Ensure programming language is set to **Python**
   - Verify that the SDK used is **Azure AI Inference SDK** (not OpenAI's default SDK)

2. **Generate Personal Access Token**:
   - Click "Create personal access token"
   - Select "Generate new token"
   - Also generate a classical token
   - Add a note like "APIkey"
   - Copy the generated token (format: `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`)

3. **Set Environment Variable**:
   ```bash
   # For Windows PowerShell
   $env:AZURE_TOKEN = "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"
   
   # For Windows Command Prompt
   set AZURE_TOKEN=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
   
   # For Linux/Mac
   export AZURE_TOKEN=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
   ```

## How to Run

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd document-plagiarism-checker
   ```

2. **Install dependencies** (see Dependencies section above)

3. **Set up environment variable** (see API Setup section above)

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the web interface**:
   - Open your browser and go to `http://localhost:8501`
   - Upload a DOCX or PDF document containing A.C. sections
   - Click "Process Document" to analyze
   - Download the generated PDF report

## Code Architecture

The application follows a modular architecture with clear separation of concerns:

### Core Components

**Frontend (app.py)**:
- Streamlit-based web interface
- File upload and validation
- Progress tracking and status updates
- Results visualization and PDF download

**Backend (plagiarism_backend.py)**:
- Document processing and text extraction
- AI integration and plagiarism analysis
- Report generation and PDF creation
- Error handling and retry mechanisms

### Key Algorithms

**1. A.C. Section Extraction Algorithm**:
- **Pattern Matching**: Uses multiple regex patterns to identify A.C. sections
- **Content Aggregation**: Collects text from paragraphs and tables
- **Sequential Processing**: Maintains proper A.C. numbering order
- **Fallback Methods**: Implements multiple extraction strategies for reliability

**2. Missing Section Detection Algorithm**:
- **Series Analysis**: Groups A.C. sections by major numbers (1.x, 2.x, etc.)
- **Gap Detection**: Identifies missing sections within sequences
- **Auto-completion**: Adds placeholder entries for missing A.C. sections
- **Sequence Validation**: Ensures complete A.C. numbering chains

**3. AI Plagiarism Analysis Algorithm**:
- **Content Preprocessing**: Truncates large content while preserving context
- **Prompt Engineering**: Uses structured prompts for consistent AI responses
- **Response Parsing**: Extracts structured data from AI responses
- **Retry Mechanism**: Implements fallback strategies for failed API calls
- **Error Recovery**: Provides default responses when AI analysis fails

**4. Report Generation Algorithm**:
- **Data Aggregation**: Combines individual A.C. analyses into comprehensive reports
- **Tutor Feedback Generation**: Uses AI to create professional academic feedback
- **PDF Formatting**: Creates professionally formatted reports with tables and styling
- **Template System**: Maintains consistent report structure across documents

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB INTERFACE                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────┐ │
│  │File Upload  │  │Progress     │  │Results      │  │PDF     │ │
│  │Validation   │  │Tracking     │  │Display      │  │Download│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOCUMENT PROCESSING LAYER                   │
│  ┌─────────────────────┐              ┌─────────────────────┐   │
│  │   DOCX Processor    │              │    PDF Processor    │   │
│  │ ┌─────────────────┐ │              │ ┌─────────────────┐ │   │
│  │ │Text Extraction  │ │              │ │Text Extraction  │ │   │
│  │ │Table Processing │ │              │ │Page Processing  │ │   │
│  │ │Pattern Matching │ │              │ │Pattern Matching │ │   │
│  │ └─────────────────┘ │              │ └─────────────────┘ │   │
│  └─────────────────────┘              └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    A.C. SECTION ANALYSIS                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │Section      │  │Missing      │  │Content                  │ │
│  │Extraction   │  │Section      │  │Validation               │ │
│  │             │  │Detection    │  │& Cleanup                │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI ANALYSIS ENGINE                          │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              AZURE AI INFERENCE SDK                        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │ │
│  │  │Topic        │  │Plagiarism   │  │Tutor Feedback       │ │ │
│  │  │Detection    │  │Analysis     │  │Generation           │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                 OPENAI GPT-4.1 MODEL                       │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REPORT GENERATION SYSTEM                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │Data         │  │PDF          │  │Professional             │ │
│  │Aggregation  │  │Generation   │  │Formatting               │ │
│  │& Analysis   │  │(ReportLab)  │  │& Styling                │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         OUTPUT                                  │
│  ┌─────────────────────┐       ┌─────────────────────────────┐ │
│  │  Professional PDF   │       │    Assessment Results      │ │
│  │      Report         │       │       Dashboard           │ │
│  │ ┌─────────────────┐ │       │ ┌─────────────────────────┐ │ │
│  │ │Assessment Table │ │       │ │Pass/Redo Decisions     │ │ │
│  │ │Tutor Feedback   │ │       │ │Plagiarism Scores       │ │ │
│  │ │Recommendations  │ │       │ │Detailed Feedback       │ │ │
│  │ └─────────────────┘ │       │ └─────────────────────────┘ │ │
│  └─────────────────────┘       └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Document Upload**: User uploads DOCX/PDF through Streamlit interface
2. **Text Extraction**: Appropriate processor extracts text and identifies A.C. sections
3. **Content Analysis**: Each A.C. section is analyzed for completeness and quality
4. **AI Processing**: GPT-4.1 analyzes content for plagiarism and generates feedback
5. **Report Compilation**: Results are aggregated into a comprehensive assessment report
6. **PDF Generation**: Professional PDF report is created with proper formatting
7. **Download**: User receives the completed assessment report

## Processing Features

**Smart Content Detection**: The system uses advanced pattern matching to identify A.C. sections across different document formats and styles.

**Contextual Analysis**: AI analysis considers the document's subject matter for more accurate plagiarism detection and relevant feedback.

**Quality Assurance**: Multiple validation layers ensure reliable extraction and processing of academic content.

**Professional Output**: Generated reports meet academic standards with proper formatting, professional language, and comprehensive feedback.

## Error Handling

The application includes robust error handling mechanisms:
- **API Timeout Management**: Automatic retry logic for failed AI requests
- **Content Validation**: Verification of extracted text quality and completeness
- **Fallback Responses**: Default assessments when AI analysis fails
- **File Format Validation**: Comprehensive checks for supported document types
- **Memory Management**: Efficient processing of large documents
