# CLAUDE.md - AI Assistant Guide

## Project Overview

**Chat_Bot_Oracle_Cloud** is a chatbot application that integrates Oracle Cloud Infrastructure (OCI) Generative AI services with a Streamlit web interface. The application enables users to interact with Oracle's generative AI models through a conversational interface.

**Language**: Brazilian Portuguese (UI text and user interactions)
**Primary Technology Stack**: Python, Streamlit, OCI SDK
**Cloud Provider**: Oracle Cloud Infrastructure (OCI)
**Region**: sa-saopaulo-1 (São Paulo, Brazil)

---

## Repository Structure

```
Chat_Bot_Oracle_Cloud/
├── README.md              # Brief project description (Portuguese)
├── requirements.txt       # Python dependencies
├── app.py                 # Main application using OCI config file
├── streamlit_app.py       # Alternative app with hardcoded config
└── .git/                  # Git repository
```

### File Descriptions

- **app.py**: Streamlit chatbot application that loads OCI configuration from `~/.oci/config` file
- **streamlit_app.py**: Similar chatbot but uses hardcoded configuration dictionary with optional environment variable for key file path
- **requirements.txt**: Python package dependencies including `oci`, `streamlit`, and supporting libraries

---

## Architecture & Key Components

### 1. OCI Configuration

**Two Configuration Approaches:**

**A. app.py** - File-based configuration:
```python
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)
```

**B. streamlit_app.py** - Dictionary-based configuration:
```python
config = {
    "user": "ocid1.user.oc1...",
    "key_file": "C:\\Temp\\oci_api_key.pem",
    "fingerprint": "...",
    "tenancy": "ocid1.tenancy.oc1...",
    "region": "sa-saopaulo-1"
}
```

### 2. Core Components

- **Compartment ID**: `ocid1.tenancy.oc1..aaaaaaaahzmfodyyhz7vzcktsbkwazcu3ohadbwvwloi33v4gox5yty7kobq`
- **Model ID**: `ocid1.generativeaimodel.oc1.sa-saopaulo-1.amaaaaaask7dceyaz4nxgyqobjvphdho6cup7opj7niharfohm5luw3jbnka`
- **Endpoint**: `https://inference.generativeai.sa-saopaulo-1.oci.oraclecloud.com`

### 3. API Client Configuration

```python
generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(
    config=config,
    service_endpoint=endpoint,
    retry_strategy=oci.retry.NoneRetryStrategy(),  # No automatic retries
    timeout=(10, 240)  # 10s connect, 240s read timeout
)
```

### 4. Chat Request Parameters

Located in `get_chatbot_response()` function (both files):

- **max_tokens**: 600
- **temperature**: 1
- **frequency_penalty**: 0
- **top_p**: 0.75
- **top_k**: -1
- **API Format**: GenericChatRequest.API_FORMAT_GENERIC

### 5. Session State Management

Streamlit session state is used to maintain conversation history:

```python
st.session_state.messages = [
    {"role": "user", "content": "..."},
    {"role": "bot", "content": "..."}
]
```

---

## Development Workflows

### Initial Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure OCI credentials**:
   - **For app.py**: Create `~/.oci/config` file with OCI credentials
   - **For streamlit_app.py**: Update hardcoded config dictionary or set `OCI_CONFIG_FILE` env var

3. **Ensure OCI API key file exists** at the path specified in configuration

### Running the Application

**Run app.py (recommended for local development)**:
```bash
streamlit run app.py
```

**Run streamlit_app.py**:
```bash
streamlit run streamlit_app.py
```

The application will start on `http://localhost:8501` by default.

### Common Development Tasks

#### Modifying UI Text
- All UI text is in Portuguese
- Text is defined inline within Streamlit calls (e.g., `st.title()`, `st.write()`, `st.text_input()`)
- Key UI strings in both files:
  - Title: "Chatbot Generative AI - OCI"
  - Input placeholder: "Digite sua mensagem:"
  - User prefix: "**Você:**"
  - Bot prefix: "**Chatbot:**"

#### Adjusting Model Parameters
Edit the chat request configuration in `get_chatbot_response()`:
- `chat_request.max_tokens` - Response length limit
- `chat_request.temperature` - Creativity level (0-2)
- `chat_request.top_p` - Nucleus sampling
- `chat_request.top_k` - Top-k sampling

#### Changing the AI Model
Update the `model_id` variable to use a different OCI Generative AI model.

---

## Key Conventions & Patterns

### Code Style
- **Encoding**: UTF-8 (specified in file headers)
- **Indentation**: 4 spaces
- **Function naming**: snake_case
- **Comments**: Minimal; code is self-documenting

### Error Handling
- **Current state**: Minimal error handling
- **Fallback response**: "Desculpe, não consegui entender a sua pergunta." (Sorry, I couldn't understand your question)
- **API errors**: Not explicitly handled; will raise exceptions

### Security Considerations

**CRITICAL SECURITY NOTES**:

1. **Sensitive credentials are hardcoded** in `streamlit_app.py`:
   - User OCID
   - Fingerprint
   - Tenancy OCID
   - File path to private key

2. **Best practices for AI assistants**:
   - **NEVER commit credentials** or API keys to version control
   - **ALWAYS use environment variables** or secure config files for sensitive data
   - **DO NOT log or expose** OCI credentials in error messages
   - **Recommend .gitignore** for `.oci/`, `.env`, and `*.pem` files

3. **Recommended refactoring**:
   - Move all credentials to environment variables
   - Use `.env` file with `python-dotenv`
   - Add `.env` to `.gitignore`

---

## Testing Strategy

**Current State**: No automated tests exist in the repository.

**Recommended Testing Approach**:

1. **Manual Testing**:
   - Run the Streamlit app
   - Test various input prompts
   - Verify conversation history persistence
   - Check error handling with invalid inputs

2. **Future Test Coverage**:
   - Unit tests for `get_chatbot_response()`
   - Mock OCI API calls
   - Test session state management
   - Validate error handling paths

3. **Integration Testing**:
   - Test OCI API connectivity
   - Validate authentication
   - Test timeout scenarios
   - Verify model response parsing

---

## Dependencies

### Core Dependencies
- **streamlit** (1.38.0): Web UI framework
- **oci** (2.134.0): Oracle Cloud Infrastructure SDK
- **pandas** (2.2.2): Data manipulation (Streamlit dependency)
- **numpy** (2.1.1): Numerical computing (Streamlit dependency)

### Notable Dependencies
- **requests** (2.32.3): HTTP library
- **cryptography** (42.0.8): Security library for OCI
- **pyOpenSSL** (24.2.1): SSL/TLS support

### Full dependency list available in `requirements.txt`

---

## Git Workflow

**Current Branch**: `claude/claude-md-mi33qaqy9j5jatef-01GYSXTAWYpPj6aK5MdaowDG`

### Commit History Pattern
Recent commits show:
- Direct updates to `streamlit_app.py`
- File additions via GitHub web interface
- No conventional commit message format

### Recommended Commit Conventions
- Use descriptive commit messages
- Prefix with type: `feat:`, `fix:`, `docs:`, `refactor:`
- Keep commits atomic and focused

---

## Common Issues & Solutions

### Issue: "Configuration file not found"
**Solution**: Ensure `~/.oci/config` exists for `app.py` or update hardcoded config in `streamlit_app.py`

### Issue: "Authentication failed"
**Solution**:
- Verify OCI user OCID is correct
- Check API key fingerprint matches
- Ensure private key file exists and is readable

### Issue: "Model not found"
**Solution**: Verify the model_id is correct and accessible in your OCI tenancy and region

### Issue: "Connection timeout"
**Solution**:
- Check network connectivity to OCI endpoints
- Verify region and endpoint URL are correct
- Consider increasing timeout values in client configuration

---

## AI Assistant Guidelines

When working with this codebase, AI assistants should:

1. **Preserve Language**: Maintain Portuguese text in UI elements
2. **Respect Security**: Never commit or expose credentials
3. **Test Changes**: Recommend manual testing after code modifications
4. **Document Changes**: Update this CLAUDE.md if architecture changes
5. **Consider Both Files**: Changes may need to be applied to both `app.py` and `streamlit_app.py`
6. **Maintain Simplicity**: This is a demonstration project; keep solutions straightforward
7. **Validate OCI IDs**: Ensure OCIDs follow the proper format when modifying
8. **Check Dependencies**: Verify compatibility when updating `requirements.txt`

---

## Future Enhancement Opportunities

1. **Multi-turn Conversations**: Currently sends only the latest message; could send full conversation history
2. **Environment Configuration**: Move to `.env` file with environment variables
3. **Error Handling**: Add comprehensive try-catch blocks and user-friendly error messages
4. **Conversation Export**: Allow users to save/download chat history
5. **Model Selection**: Add UI to select different AI models
6. **Response Streaming**: Implement streaming responses for better UX
7. **Authentication**: Add user authentication for multi-user deployment
8. **Testing**: Add unit and integration tests
9. **Docker**: Create Dockerfile for containerized deployment
10. **CI/CD**: Set up automated testing and deployment pipeline

---

## Resources

- **OCI Python SDK Documentation**: https://docs.oracle.com/en-us/iaas/tools/python/latest/
- **OCI Generative AI**: https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm
- **Streamlit Documentation**: https://docs.streamlit.io/
- **OCI São Paulo Region**: sa-saopaulo-1

---

*Last Updated: 2025-11-17*
*Repository: sandovalmedeiros/Chat_Bot_Oracle_Cloud*
